/** Source-level experiments; all provider responses are deterministic fixtures.
 * Requires Node >=24. Does not call a real model or execute shell tool payloads.
 */
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';

const source = process.env.RUFLO_SOURCE;
const pin = '6f0ed7112873eedc7cfe17281a2585188190b790';
assert.equal(execFileSync('git', ['-C', source, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim(), pin);
const scratch = mkdtempSync(join(tmpdir(), 'ruflo-probe-'));
process.chdir(scratch);
// Keep all upstream state project-local and turn off optional routing branches.
process.env.CLAUDE_FLOW_CWD = scratch;
delete process.env.CLAUDE_FLOW_CONFIG;
delete process.env.OPENROUTER_API_KEY;
delete process.env.OLLAMA_API_KEY;
delete process.env.RUFLO_PROVIDER;
process.env.ANTHROPIC_API_KEY = 'fixture-only-not-a-real-key';
process.env.CLAUDE_FLOW_ROUTER_NEURAL = '0';
process.env.CLAUDE_FLOW_ROUTER_TRAJECTORY = '0';
process.env.CLAUDE_FLOW_RUN_TRANSCRIPTS = '0';
process.env.RUFLO_FUNNEL = '0';

const results = [];
const importSource = (path) => import(pathToFileURL(join(source, path)).href);
const requests = [];
globalThis.fetch = async (url, options) => {
  // Replaces the network boundary, not Ruflo's execution code.
  const body = JSON.parse(options.body);
  requests.push({ url: String(url), body });
  return new Response(JSON.stringify({
    id: `fixture-${requests.length}`, model: body.model,
    content: [{ type: 'text', text: `fixture-output-${requests.length}` }],
    stop_reason: 'end_turn', usage: { input_tokens: 12, output_tokens: 8 },
  }), { status: 200, headers: { 'content-type': 'application/json' } });
};

const { agentTools } = await importSource('v3/@claude-flow/cli/src/mcp-tools/agent-tools.ts');
const { swarmTools } = await importSource('v3/@claude-flow/cli/src/mcp-tools/swarm-tools.ts');
const { workflowTools } = await importSource('v3/@claude-flow/cli/src/mcp-tools/workflow-tools.ts');
const registry = [...agentTools, ...swarmTools, ...workflowTools];
const call = (name, input = {}) => registry.find(t => t.name === name).handler(input);

const swarm = await call('swarm_init', { topology: 'hierarchical', maxAgents: 3 });
assert.equal(swarm.success, true);
const agent = await call('agent_spawn', { agentType: 'researcher', model: 'haiku', swarmId: swarm.swarmId });
assert.equal(agent.success, true);
assert.equal(agent.status, 'registered');
assert.equal(requests.length, 0);
const agentsFile = join(scratch, '.claude-flow/agents/store.json');
const initialRecord = JSON.parse(readFileSync(agentsFile)).agents[agent.agentId];
assert.equal(initialRecord.status, 'idle');
assert.equal(initialRecord.taskCount, 0);
results.push({ experiment: 'spawn-is-registration', status: 'passed', returned: agent.status, stored: initialRecord.status, providerCalls: 0 });

const executed = await call('agent_execute', { agentId: agent.agentId, prompt: 'Explain test fixtures.' });
assert.equal(executed.success, true);
assert.equal(requests.length, 1);
assert.equal('tools' in requests[0].body, false);
assert.equal(requests[0].body.messages.length, 1);
const finalRecord = JSON.parse(readFileSync(agentsFile)).agents[agent.agentId];
assert.equal(finalRecord.status, 'idle');
assert.equal(finalRecord.taskCount, 1);
results.push({ experiment: 'execute-single-provider-request', status: 'passed', providerCalls: 1, requestHasTools: false, taskCount: finalRecord.taskCount, usage: executed.usage });

const workflow = await call('workflow_create', {
  name: 'Research fixture', variables: { defaultAgentId: agent.agentId },
  steps: [
    { name: 'First', type: 'task', config: { prompt: 'First step' } },
    { name: 'Second', type: 'task', config: { prompt: 'Seen={{lastStepOutput}}; direct={{step-1.output}}' } },
    { name: 'Parallel', type: 'parallel', config: {} },
    { name: 'Loop', type: 'loop', config: {} },
    { name: 'Wait', type: 'wait', config: { ms: 1 } },
  ],
});
const run = await call('workflow_execute', { workflowId: workflow.workflowId });
assert.equal(run.status, 'completed');
assert.equal(run.stepsCompleted, 3);
assert.equal(run.stepsSkipped, 2);
const boundPrompt = requests[2].body.messages[0].content;
assert.equal(boundPrompt, 'Seen=fixture-output-2; direct={{step-1.output}}');
results.push({ experiment: 'workflow-supported-step-types-and-binding', status: 'passed', completed: run.stepsCompleted, skipped: run.stepsSkipped, observedPrompt: boundPrompt, caveat: 'Generated step IDs contain hyphens, which the interpolation regex does not match. lastStepOutput works.' });

const pausedWorkflow = await call('workflow_create', { name: 'Paused fixture', steps: [{ type: 'wait', config: { ms: 1 } }] });
const workflowFile = join(scratch, '.claude-flow/workflows/store.json');
const workflows = JSON.parse(readFileSync(workflowFile));
workflows.workflows[pausedWorkflow.workflowId].status = 'paused';
writeFileSync(workflowFile, JSON.stringify(workflows));
const resumed = await call('workflow_resume', { workflowId: pausedWorkflow.workflowId });
assert.equal(resumed.resumed, true);
const retry = await call('workflow_execute', { workflowId: pausedWorkflow.workflowId });
assert.equal(retry.error, 'Workflow already running');
results.push({ experiment: 'resume-state-without-runner', status: 'passed', stateAfterResume: resumed.status, subsequentExecuteError: retry.error, caveat: 'Seeded paused state; isolated handlers, not a live concurrently running worker.' });

const retrieval = await importSource('v3/@claude-flow/cli/src/memory/hybrid-retrieval.ts');
const docs = ['jwt authentication token rotation', 'database connection pooling', 'jwt authentication tests'];
const tokenized = docs.map(retrieval.tokenize);
const stats = retrieval.buildCorpusStats(tokenized);
const scores = tokenized.map(tokens => retrieval.bm25Score(retrieval.tokenize('jwt authentication'), tokens, stats));
assert.ok(scores[0] > scores[1]);
assert.equal(scores[1], 0);
assert.deepEqual(retrieval.tokenize('修复登录认证错误'), []);
results.push({ experiment: 'bm25-and-tokenizer', status: 'passed', scores, chineseTokens: [], caveat: 'This pure helper uses ASCII tokenization; other search paths use different tokenizers.' });

const transport = await importSource('v3/@claude-flow/swarm/src/consensus/transport.ts');
const keys = transport.generateNodeKeyPair();
const msg = { type: 'request-vote', from: 'a', to: 'b', payload: { term: 1 }, seq: 1 };
const signed = { ...msg, signature: transport.signMessage(msg, keys.privateKeyPem) };
assert.equal(transport.verifyMessage(signed, keys.publicKeyPem), true);
assert.equal(transport.verifyMessage({ ...signed, payload: { term: 2 } }, keys.publicKeyPem), false);
results.push({ experiment: 'consensus-message-signature', status: 'passed', validMessage: true, tamperedMessage: false, caveat: 'Cryptographic helper only; no distributed cluster was started.' });

const { generateAgentRouter } = await importSource('v3/@claude-flow/cli/src/init/helpers-generator.ts');
const routerPath = join(scratch, 'generated-router.cjs');
writeFileSync(routerPath, generateAgentRouter());
const require = createRequire(import.meta.url);
const router = require(routerPath);
const route = router.routeTask('write a unit test');
assert.equal(route.agent, 'tester');
assert.equal(route.confidence, 0.6);
results.push({ experiment: 'generated-hook-router', status: 'passed', agent: route.agent, confidence: route.confidence, caveat: 'A fixed heuristic prior, not a calibrated probability.' });

const output = { commit: pin, node: process.version, sourceLevelOnly: true, realProviderCalls: 0, fixtureProviderCalls: requests.length, experiments: results };
const outputPath = process.argv[2];
if (outputPath) writeFileSync(outputPath, JSON.stringify(output, null, 2) + '\n');
console.log(JSON.stringify(output, null, 2));
