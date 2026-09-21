/** Public SDK counterpart. No API key, shell, disk tool or network request. */
import assert from 'node:assert/strict';
import { Agent, createTool } from '@cline/sdk';

let turn = 0;
const model = {
  async *stream(request) {
    if (turn++ === 0) {
      yield { type: 'tool-call-delta', toolCallId: 'count-1', toolName: 'count_chars', input: { text: 'Cline' } };
      yield { type: 'finish', reason: 'tool-calls' };
    } else {
      const result = request.messages.at(-1).content[0];
      assert.equal(result.output, 5);
      yield { type: 'text-delta', text: 'Cline 有 5 个字符。' };
      yield { type: 'finish', reason: 'stop' };
    }
  },
};

const count = createTool({
  name: 'count_chars', description: 'Count Unicode code points in a string.',
  inputSchema: { type: 'object', properties: { text: { type: 'string' } }, required: ['text'], additionalProperties: false },
  execute: async input => {
    if (!input || typeof input.text !== 'string') throw new TypeError('text must be a string');
    return [...input.text].length;
  },
});
const agent = new Agent({
  model, tools: [count], maxIterations: 3,
  toolPolicies: { '*': { autoApprove: false } },
  // This deterministic allowlist approves only the pure tool in this example.
  requestToolApproval: async request => ({ approved: request.toolName === 'count_chars' }),
});
agent.subscribe(event => console.log(event.type));
const result = await agent.run('请统计 Cline 的字符数。');
assert.equal(result.status, 'completed');
console.log(result.outputText);
