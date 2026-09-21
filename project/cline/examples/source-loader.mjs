/** Load pinned upstream modules without installing Cline's monorepo.
 * This is an isolated source experiment, NOT a replacement for Cline's build.
 * AgentRuntime's executable body is unchanged. Explicit boundary doubles:
 * - no telemetry/network; gateway and unclassified errors throw;
 * - IDs use randomUUID, not nanoid;
 * - nested JSON-like string normalization is identity (tests use parsed values).
 * Pure utility modules, VS Code policies, plan guard, and editor are real source.
 */
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { stripTypeScriptTypes } from 'node:module';
import { createHash } from 'node:crypto';

export const COMMIT = '4a56a43f39c2c75f941220989d4c65db006ee531';
export const dataUrl = code => `data:text/javascript;base64,${Buffer.from(code).toString('base64')}`;

export async function loadSources(sourceRoot) {
  const root = resolve(sourceRoot);
  const head = execFileSync('git', ['-C', root, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
  if (head !== COMMIT) throw new Error(`Expected ${COMMIT}, got ${head}`);
  const loaded = [];
  async function source(path) {
    const buffer = await readFile(resolve(root, path));
    const committed = execFileSync('git', ['-C', root, 'show', `${COMMIT}:${path}`], { maxBuffer: 4 * 1024 * 1024 });
    if (!buffer.equals(committed)) throw new Error(`Modified upstream file: ${path}`);
    loaded.push({ path, sha256: createHash('sha256').update(buffer).digest('hex') });
    return stripTypeScriptTypes(buffer.toString(), { mode: 'transform' });
  }
  const shared = 'sdk/packages/shared/src/';
  const utilityUrls = await Promise.all(['llms/tokens.ts', 'llms/model-options.ts', 'parse/object.ts', 'parse/string.ts']
    .map(async path => dataUrl(await source(shared + path))));
  const doublesUrl = dataUrl(`
    import { randomUUID } from 'node:crypto';
    ${utilityUrls.map(url => `export * from ${JSON.stringify(url)};`).join('\n')}
    const forbidden = () => { throw new Error('Untested dependency called: live gateway / error classifier'); };
    export const createGateway = forbidden, classifyProviderError = forbidden, isRetryableProviderError = forbidden;
    export const captureAgentUnexpectedReasoningTokens = () => {};
    export const captureSdkError = () => {}, captureTaskLifecycleEvent = () => {};
    export const normalizeJsonLikeStringsForSchema = input => input;
    export const nanoid = () => randomUUID();
    export const TOOL_REJECTION_SUFFIX = 'REJECTED_IN_OFFLINE_EXPERIMENT';
    export const TASK_CANCELLED_EVENT = 'cancelled', TASK_FIRST_CHUNK_RECEIVED_EVENT = 'first_chunk';
    export const TASK_PROVIDER_REQUEST_STARTED_EVENT = 'request', TASK_PROVIDER_STREAM_FAILED_EVENT = 'stream_failed';
    export const TASK_PROVIDER_STREAM_STARTED_EVENT = 'stream_started';
  `);
  let runtime = await source('sdk/packages/agents/src/agent-runtime.ts');
  runtime = runtime.replace(/from ["'](?:@cline\/llms|@cline\/shared|nanoid)["']/g, `from ${JSON.stringify(doublesUrl)}`);
  const { Agent } = await import(dataUrl(runtime));
  const policies = await import(dataUrl(await source('apps/vscode/src/sdk/sdk-tool-policies.ts')));
  const guard = await import(dataUrl(await source('sdk/packages/core/src/extensions/tools/command-guard.ts')));
  const executors = 'sdk/packages/core/src/extensions/tools/executors/';
  const eol = dataUrl(await source(executors + 'line-endings.ts'));
  const editorCode = (await source(executors + 'editor.ts')).replace(/from ["']\.\/line-endings["']/, `from ${JSON.stringify(eol)}`);
  const editor = await import(dataUrl(editorCode));
  return { Agent, policies, guard, editor, loaded };
}
