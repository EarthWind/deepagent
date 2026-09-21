/** Real pinned AgentRuntime, scripted model, zero external requests. Node 24+. */
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, readFile, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { loadSources, COMMIT } from './source-loader.mjs';

if (!process.argv[2]) throw new Error('Usage: node runtime-lab.mjs /path/to/cline [results.json]');
const { Agent, policies, guard, editor, loaded } = await loadSources(process.argv[2]);
const results = [];
const trace = [];
const tool = (name, execute, extra = {}) => ({ name, description: name, inputSchema: { type: 'object' }, execute, ...extra });
const call = (name, input = {}, id = name) => ({ type: 'tool-call-delta', toolName: name, toolCallId: id, input });
const finish = { type: 'finish', reason: 'tool-calls' };
const answer = text => [{ type: 'text-delta', text }, { type: 'finish', reason: 'stop' }];
function scripted(turns) {
  return { requests: [], async *stream(request) {
    this.requests.push(structuredClone({ messages: request.messages, tools: request.tools }));
    const events = turns[this.requests.length - 1];
    assert.ok(events, 'Unexpected additional model request');
    yield* events;
  } };
}
async function check(name, test) {
  try { await test(); }
  catch (error) { console.error(`FAIL ${name}: ${error.message}`); process.exit(1); }
  results.push({ name, passed: true }); console.log(`PASS ${name}`);
}

await check('streamed JSON → approval → execution → tool result → final answer', async () => {
  const model = scripted([
    [{ type: 'tool-call-delta', toolCallId: 'c1', toolName: 'inspect', inputText: '{"path":' },
      { type: 'tool-call-delta', toolCallId: 'c1', inputText: '"main.ts"}' }, finish], answer('已检查 main.ts'),
  ]);
  const agent = new Agent({ model, tools: [tool('inspect', async input => { assert.equal(input.path, 'main.ts'); return 'OK'; })],
    toolPolicies: { '*': { autoApprove: false } }, requestToolApproval: async request => {
      trace.push({ type: 'approval', tool: request.toolName, approved: true }); return { approved: true };
    }, maxIterations: 4 });
  agent.subscribe(event => trace.push({ type: event.type, iteration: event.iteration }));
  const result = await agent.run('检查 main.ts');
  assert.equal(result.status, 'completed'); assert.equal(result.iterations, 2);
  assert.equal(result.outputText, '已检查 main.ts');
  assert.equal(model.requests[1].messages.at(-1).content[0].output, 'OK');
});

await check('unlisted tool executes without an approval callback', async () => {
  let calls = 0;
  const agent = new Agent({ model: scripted([[call('write'), finish], answer('done')]),
    tools: [tool('write', async () => ++calls)] });
  assert.equal((await agent.run('go')).status, 'completed'); assert.equal(calls, 1);
});

await check('approval absent or denied → no side effect, error fed back to model', async () => {
  for (const requestToolApproval of [undefined, async () => ({ approved: false, reason: '拒绝写入' })]) {
    let calls = 0;
    const model = scripted([[call('write'), finish], answer('已取消')]);
    const result = await new Agent({ model, tools: [tool('write', async () => ++calls)],
      toolPolicies: { '*': { autoApprove: false } }, requestToolApproval }).run('go');
    assert.equal(calls, 0); assert.equal(result.status, 'completed');
    assert.equal(model.requests[1].messages.at(-1).content[0].isError, true);
  }
});

await check('beforeTool block happens before approval; disabled tool cannot execute', async () => {
  for (const hookBlock of [true, false]) {
    let approvals = 0, calls = 0;
    const result = await new Agent({ model: scripted([[call('write'), finish], answer('stop')]),
      tools: [tool('write', async () => ++calls)],
      toolPolicies: { write: { enabled: hookBlock, autoApprove: false } },
      hooks: hookBlock ? { beforeTool: () => ({ skip: true, reason: 'Plan guard' }) } : undefined,
      requestToolApproval: async () => { approvals++; return { approved: true }; },
    }).run('go');
    assert.equal(result.status, 'completed'); assert.equal(calls, 0); assert.equal(approvals, 0);
  }
});

await check('adjacent parallel tools overlap, sequential tool is a barrier', async () => {
  const order = [];
  let started = 0, release;
  const gate = new Promise(resolve => { release = resolve; });
  const parallel = name => tool(name, async () => {
    order.push(`${name}:start`);
    if (++started === 2) release();
    await gate; order.push(`${name}:end`); return name;
  }, { executionMode: 'parallel' });
  const tools = [parallel('readA'), parallel('readB'), tool('write', async () => {
    assert.ok(order.includes('readA:end') && order.includes('readB:end'));
    order.push('write'); return 'written';
  }, { executionMode: 'sequential' }), tool('after', async () => {
    assert.ok(order.includes('write')); order.push('after'); return 'after';
  }, { executionMode: 'parallel' })];
  const model = scripted([[...tools.map(t => call(t.name)), finish], answer('done')]);
  const result = await new Agent({ model, tools }).run('go');
  assert.equal(result.status, 'completed');
  assert.deepEqual(order.slice(0, 2), ['readA:start', 'readB:start']);
  assert.deepEqual(model.requests[1].messages.filter(m => m.role === 'tool').map(m => m.content[0].toolName), tools.map(t => t.name));
  trace.push({ type: 'parallel_order', order });
});

await check('maxIterations limits turns, successful terminal tool ends without another request', async () => {
  const neverFinish = new Agent({ model: scripted([[call('read'), finish]]), tools: [tool('read', async () => 'x')], maxIterations: 1 });
  assert.equal((await neverFinish.run('go')).status, 'failed');
  const model = scripted([[call('done'), finish]]);
  const result = await new Agent({ model, tools: [tool('done', async () => 'finished', { lifecycle: { completesRun: true } })] }).run('go');
  assert.equal(result.status, 'completed'); assert.equal(result.outputText, 'finished'); assert.equal(model.requests.length, 1);
});

await check('malformed tool JSON does not execute; tool exception becomes error result', async () => {
  let count = 0;
  for (const malformed of [true, false]) {
    const model = scripted([[malformed ? { type: 'tool-call-delta', toolName: 'write', toolCallId: 'x', inputText: '{"x":' } : call('write'), finish], answer('recovered')]);
    const result = await new Agent({ model, tools: [tool('write', async () => { count++; throw new Error('disk fixture error'); })] }).run('go');
    assert.equal(result.status, 'completed'); assert.equal(model.requests[1].messages.at(-1).content[0].isError, true);
  }
  assert.equal(count, 1);
});

await check('prepareTurn projects model context without rewriting runtime transcript', async () => {
  const model = scripted([answer('ok')]);
  const result = await new Agent({ model, prepareTurn: ctx => ({ messages: [{ ...ctx.messages[0], content: [{ type: 'text', text: 'compact' }] }] }) }).run('original long message');
  assert.equal(model.requests[0].messages[0].content[0].text, 'compact');
  assert.equal(result.messages[0].content[0].text, 'original long message');
});

await check('classified overflow retries once with a smaller context', async () => {
  const model = scripted([[{ type: 'finish', reason: 'error', error: 'context fixture', errorClass: 'context_window_exceeded', errorRetryable: false }], answer('recovered')]);
  const result = await new Agent({ model, prepareTurn: ctx => ctx.overflowRecovery
    ? { messages: [{ ...ctx.messages[0], content: [{ type: 'text', text: 'small' }] }] } : undefined }).run('x'.repeat(2000));
  assert.equal(result.status, 'completed'); assert.equal(result.iterations, 1); assert.equal(model.requests.length, 2);
});

await check('restore resets status and retains listeners and tool registrations', async () => {
  let events = 0, calls = 0;
  const agent = new Agent({ model: scripted([answer('first'), [call('read'), finish], answer('second')]), tools: [tool('read', async () => ++calls)] });
  agent.subscribe(() => events++);
  await agent.run('first'); const before = events;
  agent.restore([]); assert.equal(agent.snapshot().status, 'idle');
  const result = await agent.run('second');
  assert.equal(result.status, 'completed'); assert.ok(events > before); assert.equal(calls, 1);
  assert.equal(result.messages[0].content[0].text, 'second');
});

await check('VS Code forces callback for UI-governed tools; live toggles decide', async () => {
  const settings = { actions: { readFiles: true, editFiles: false, useMcp: false } };
  const built = policies.buildToolPolicies(settings, { getServers: () => [{ name: 'docs', tools: [{ name: 'lookup' }] }] });
  assert.equal(built.read_files.autoApprove, false); assert.equal(built.docs__lookup.autoApprove, false);
  assert.equal(policies.isToolAutoApproved('read_files', settings), true);
  assert.equal(policies.isToolAutoApproved('editor', settings), false);
  settings.actions.editFiles = true; assert.equal(policies.isToolAutoApproved('editor', settings), true);
});

await check('Plan command guard blocks common mutations but is not shell isolation', async () => {
  assert.ok(guard.findFileEditingCommand('rm example.txt'));
  assert.ok(guard.findFileEditingCommand('echo hi > example.txt'));
  assert.equal(guard.findFileEditingCommand('git status'), undefined);
  // Only parsing, never execute this string. This limitation is documented upstream.
  assert.equal(guard.findFileEditingCommand('python -c "print(42)"'), undefined);
});

await check('real editor preserves CRLF, rejects ambiguous match, accepts absolute paths', async () => {
  const root = await mkdtemp(join(tmpdir(), 'cline-editor-lab-'));
  try {
    const cwd = join(root, 'workspace'); await mkdir(cwd);
    const file = join(cwd, 'sample.txt'); await writeFile(file, 'hello\r\nworld\r\n');
    const execute = editor.createEditorExecutor();
    const context = { agentId: 'lab', runId: 'lab', iteration: 1, toolCallId: 'editor' };
    await execute({ path: 'sample.txt', old_text: 'hello\nworld', new_text: 'hello\ncline' }, cwd, context);
    assert.equal(await readFile(file, 'utf8'), 'hello\r\ncline\r\n');
    await writeFile(file, 'same\nsame\n');
    await assert.rejects(execute({ path: 'sample.txt', old_text: 'same', new_text: 'different' }, cwd, context), /multiple occurrences/);
    await assert.rejects(execute({ path: '../relative.txt', new_text: 'x' }, cwd, context), /within cwd/);
    const absolute = join(root, 'absolute.txt');
    await execute({ path: absolute, new_text: 'inside disposable fixture only' }, cwd, context);
    assert.equal(await readFile(absolute, 'utf8'), 'inside disposable fixture only');
  } finally { await rm(root, { recursive: true, force: true }); }
});

const report = { upstreamCommit: COMMIT, node: process.version, model: 'scripted; no provider requests',
  scope: 'Unmodified upstream executable bodies after TS erasure/import rewiring; explicit dependency doubles in source-loader.mjs',
  tests: results, trace, loadedSources: loaded };
if (process.argv[3]) {
  await mkdir(dirname(process.argv[3]), { recursive: true });
  await writeFile(process.argv[3], JSON.stringify(report, null, 2) + '\n');
}
console.log(`${results.length}/${results.length} checks passed`);
