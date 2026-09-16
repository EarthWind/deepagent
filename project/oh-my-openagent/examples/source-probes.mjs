// Research probes: execute upstream source without installing the agent or calling a model.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { existsSync, realpathSync, statSync } from 'node:fs';
import { registerHooks } from 'node:module';
import { resolve, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const PIN = 'bee849b228d1cb076a8f2ac839335f43399febe1';
if (!process.argv[2]) throw new Error('Usage: node --experimental-transform-types source-probes.mjs /path/to/oh-my-openagent');
const root = realpathSync(resolve(process.argv[2]));
const commit = execFileSync('git', ['-C', root, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
assert.equal(commit, PIN, 'Use the pinned source commit');
const testedTrees = ['packages/omo-opencode/src/features/background-agent', 'packages/senpi-task/src/dag', 'packages/hashline-core/src', 'packages/memory-core/src/search', 'packages/memory-core/src/recall'];
assert.equal(execFileSync('git', ['-C', root, 'status', '--porcelain', '--untracked-files=no', '--', ...testedTrees], { encoding: 'utf8' }).trim(), '', 'Tested upstream source trees must be clean');

// Node 24 can transform TypeScript. Upstream uses extensionless relative imports;
// this research-only resolver adds .ts or /index.ts inside the pinned checkout.
registerHooks({
  resolve(specifier, context, nextResolve) {
    if (specifier.startsWith('.') && context.parentURL?.startsWith('file:')) {
      const parent = fileURLToPath(context.parentURL);
      if (parent.startsWith(root + sep)) {
        const base = fileURLToPath(new URL(specifier, context.parentURL));
        for (const candidate of [base + '.ts', resolve(base, 'index.ts')]) {
          if (candidate.startsWith(root + sep) && existsSync(candidate) && statSync(candidate).isFile()) {
            return nextResolve(pathToFileURL(candidate).href, context);
          }
        }
      }
    }
    return nextResolve(specifier, context);
  },
});

const upstream = (path) => import(pathToFileURL(resolve(root, path)).href);
const results = [];
async function probe(name, fn) {
  const evidence = await fn();
  results.push({ name, status: 'passed', evidence });
}
const { ConcurrencyManager } = await upstream('packages/omo-opencode/src/features/background-agent/concurrency.ts');
const attempts = await upstream('packages/omo-opencode/src/features/background-agent/attempt-lifecycle.ts');
const { compileDag } = await upstream('packages/senpi-task/src/dag/graph.ts');
const hashes = await upstream('packages/hashline-core/src/hash-computation.ts');
const { applyHashlineEdits } = await upstream('packages/hashline-core/src/edit-operations.ts');
const { searchTranscripts } = await upstream('packages/memory-core/src/search/engine.ts');
const { planRecallQueries } = await upstream('packages/memory-core/src/recall/planner.ts');

await probe('provider queue handoff', async () => {
  const manager = new ConcurrencyManager({ providerConcurrency: { demo: 1 } });
  await manager.acquire('demo/a', 'first');
  let admitted = false;
  const pending = manager.acquire('demo/b', 'second').then(() => { admitted = true; });
  await Promise.resolve();
  assert.equal(admitted, false);
  assert.equal(manager.getQueueLength('demo'), 1);
  manager.release('demo/a');
  await pending;
  assert.equal(admitted, true);
  assert.equal(manager.getCount('demo'), 1);
  manager.release('demo/b');
  assert.equal(manager.getCount('demo'), 0);
  return 'Two models share one provider slot; release transfers that slot to the waiter.';
});

await probe('model override is a separate quota key', async () => {
  const manager = new ConcurrencyManager({ providerConcurrency: { demo: 1 }, modelConcurrency: { 'demo/special': 2 } });
  await manager.acquire('demo/a');
  await manager.acquire('demo/special');
  await manager.acquire('demo/special');
  assert.equal(manager.getCount('demo'), 1);
  assert.equal(manager.getCount('demo/special'), 2);
  assert.equal(manager.getConcurrencyLimit('other/a'), 5);
  assert.equal(new ConcurrencyManager({ defaultConcurrency: 0 }).getConcurrencyLimit('other/a'), Infinity);
  manager.clear();
  return 'Provider=1 and model override=2 can admit three tasks across two keys; quotas are not hierarchical.';
});

await probe('cancelled waiter does not consume the next slot', async () => {
  const manager = new ConcurrencyManager({ defaultConcurrency: 1 });
  await manager.acquire('demo/a', 'first');
  const cancelled = manager.acquire('demo/a', 'cancel-me').then(() => false, () => true);
  const next = manager.acquire('demo/a', 'third');
  assert.equal(manager.cancelWaiter('demo/a', 'cancel-me'), true);
  assert.equal(await cancelled, true);
  manager.release('demo/a');
  await next;
  assert.equal(manager.getCount('demo/a'), 1);
  manager.release('demo/a');
  return 'Cancellation rejects the selected waiter; the next waiter still receives the slot.';
});

await probe('old attempt cannot overwrite current task projection', () => {
  const task = { id: 'bg_probe', status: 'pending' };
  const first = attempts.startAttempt(task, { providerID: 'demo', modelID: 'a' });
  attempts.bindAttemptSession(task, first.attemptId, 'ses_old', task.model);
  const second = attempts.scheduleRetryAttempt(task, first.attemptId, { providerID: 'demo', modelID: 'b' }, 'retry');
  assert.ok(second);
  attempts.bindAttemptSession(task, second.attemptId, 'ses_new', task.model);
  attempts.finalizeAttempt(task, first.attemptId, 'completed');
  assert.equal(task.currentAttemptID, second.attemptId);
  assert.equal(task.sessionId, 'ses_new');
  assert.equal(task.status, 'running');
  return { attempts: task.attempts.length, currentSession: task.sessionId, currentStatus: task.status };
});

const node = (id, dependsOn = []) => ({ id, prompt: `Task ${id}; write results to an explicit artifact.`, category: 'quick', dependsOn });
await probe('DAG compile: fork and join', () => {
  const graph = compileDag({ key: 'probe', name: 'fork-join', nodes: [node('A'), node('B'), node('C', ['A']), node('D', ['B', 'C'])] });
  assert.equal(graph.ok, true);
  assert.deepEqual(graph.waves.map((wave) => wave.nodeIds), [['A', 'B'], ['C'], ['D']]);
  assert.deepEqual(graph.criticalPath, ['A', 'C', 'D']);
  return { waves: graph.waves, criticalPath: graph.criticalPath };
});

await probe('DAG compile: reject cycle, unknown dependency and duplicate id', () => {
  const cases = [
    ['cycle', [node('A', ['B']), node('B', ['A'])]],
    ['unknown_dependency', [node('A', ['missing'])]],
    ['duplicate_node_id', [node('A'), node('A')]],
  ];
  for (const [code, nodes] of cases) {
    const graph = compileDag({ key: 'invalid', name: 'invalid', nodes });
    assert.equal(graph.ok, false);
    assert.ok(graph.errors.some((error) => error.code === code));
    assert.equal(graph.nodes.length, 0);
  }
  return cases.map(([code]) => code);
});

await probe('hashline applies a fresh anchor and rejects a stale anchor', () => {
  const original = 'const count = 1;\nreturn count;';
  const anchor = `1#${hashes.computeLineHash(1, original.split('\n')[0])}`;
  const edit = [{ op: 'replace', pos: anchor, lines: ['const count = 2;'] }];
  assert.equal(applyHashlineEdits(original, edit), 'const count = 2;\nreturn count;');
  const changed = 'const count = 100;\nreturn count;';
  assert.throws(() => applyHashlineEdits(changed, edit), /changed since last read/);
  return { readOutput: hashes.formatHashLines(original), anchor };
});

await probe('short hash collision exists; it is not an integrity proof', () => {
  const seen = new Map();
  for (let i = 0; i <= 256; i++) {
    const line = `const value = ${i};`;
    const hash = hashes.computeLineHash(1, line);
    if (seen.has(hash)) return { hash, first: seen.get(hash), second: line };
    seen.set(hash, line);
  }
  assert.fail('257 inputs cannot fit into 256 hash buckets without collision');
});

await probe('lexical memory search: AND, phrase and hidden filtering', () => {
  const doc = (id, content, conversationId = 'visible') => ({ id, content, conversationId, date: '2026-09-16T00:00:00Z' });
  const provider = { listConversations: () => [
    { id: 'visible', messages: [doc('a', 'retry queue worker'), doc('b', 'retry worker queue'), doc('c', 'retry only')] },
    { id: 'hidden', hidden: true, messages: [doc('d', 'retry queue', 'hidden')] },
  ] };
  assert.deepEqual(searchTranscripts(provider, 'retry queue').map((x) => x.messageId).sort(), ['a', 'b']);
  assert.deepEqual(searchTranscripts(provider, '"retry queue"').map((x) => x.messageId), ['a']);
  assert.equal(searchTranscripts(provider, 'retry queue', { includeHidden: true }).length, 3);
  return 'AND terms and exact phrase adjacency; hidden conversations excluded unless explicitly included.';
});

await probe('recall planner is deterministic and handles non-ASCII text', () => {
  const input = ['排队失败 重试机制', 'retry queue worker'];
  const queries = planRecallQueries(input);
  assert.deepEqual(queries, planRecallQueries(input));
  assert.ok(queries.some((query) => /排队失败|重试机制/.test(query)));
  assert.ok(queries.length <= 4);
  const withTools = planRecallQueries(input, { toolTexts: ['cat src/scheduler/admission.ts'] });
  assert.ok(withTools.length <= 6);
  return { queries, withTools };
});

console.log(JSON.stringify({ commit, node: process.version, passed: results.length, results }, null, 2));
