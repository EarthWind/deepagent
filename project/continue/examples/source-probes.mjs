/** Isolated probes of pinned upstream functions, not a Continue integration test. */
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourceRoot = process.argv[2];
if (!sourceRoot) throw new Error("Usage: node source-probes.mjs /path/to/pinned/continue");
const manifest = JSON.parse(readFileSync(path.join(root, "research/sources.json"), "utf8"));
const loaded = [];

function readPinned(relativePath) {
  const raw = readFileSync(path.join(sourceRoot, relativePath), "utf8");
  const expected = manifest.sources.find((entry) => entry.path === relativePath);
  assert(expected, `Unlisted source ${relativePath}`);
  assert.equal(createHash("sha256").update(raw).digest("hex"), expected.sha256, `Source drift: ${relativePath}`);
  loaded.push(relativePath);
  return raw;
}

function load(relativePath, exports, dependencies = {}) {
  const raw = readPinned(relativePath);
  // Only import declarations and TS syntax are removed; function bodies are upstream.
  // Dependencies are explicit below. No model, shell, network or disk-writing tool runs.
  const importsRemoved = raw.replace(/^import\s[\s\S]*?;\s*$/gm, "");
  const javascript = stripTypeScriptTypes(importsRemoved, { mode: "transform", sourceUrl: relativePath })
    .replace(/^export\s+/gm, "");
  const evaluate = new Function(...Object.keys(dependencies), `${javascript}\nreturn {${exports.join(",")}};`);
  return evaluate(...Object.values(dependencies));
}

const { BUILT_IN_GROUP_NAME } = load("core/tools/builtIn.ts", ["BUILT_IN_GROUP_NAME"]);
const defaultSettingRaw = readPinned("gui/src/redux/slices/uiSlice.ts");
assert.match(defaultSettingRaw, /DEFAULT_TOOL_SETTING: ToolPolicy = "allowedWithPermission"/);
const { selectActiveTools } = load("gui/src/redux/selectors/selectActiveTools.ts", ["selectActiveTools"], {
  BUILT_IN_GROUP_NAME,
  DEFAULT_TOOL_SETTING: "allowedWithPermission",
  // Redux's memoization is irrelevant to the selection predicate being probed.
  createSelector: (selectors, project) => (state) => project(...selectors.map((select) => select(state))),
});
const { evaluateFileAccessPolicy } = load("core/tools/policies/fileAccess.ts", ["evaluateFileAccessPolicy"]);
const matching = load("core/edit/searchAndReplace/findSearchMatch.ts", ["findSearchMatch", "findSearchMatches"]);
const errors = load("core/util/errors.ts", ["ContinueError", "ContinueErrorReason"]);
const replacement = load("core/edit/searchAndReplace/performReplace.ts", ["executeFindAndReplace", "executeMultiFindAndReplace"], { ...matching, ...errors });
const defaults = load("extensions/cli/src/permissions/defaultPolicies.ts", ["getDefaultToolPolicies", "PLAN_MODE_POLICIES", "AUTO_MODE_POLICIES"]);
const dynamicTools = [];
const permission = load("extensions/cli/src/permissions/permissionChecker.ts", ["checkToolPermission", "matchesToolPattern"], { ALL_BUILT_IN_TOOLS: dynamicTools });
// Token counters are fixtures. The threshold arithmetic and pruning are real source.
const compaction = load("extensions/cli/src/compaction.ts", ["shouldAutoCompact", "pruneLastMessage", "getHistoryForLLM"], {
  countTotalInputTokens: ({ model }) => model.fixtureInputTokens,
  getModelContextLimit: (model) => model.fixtureContext,
  getModelMaxTokens: (model) => model.fixtureOutput,
  countToolDefinitionTokens: () => 0,
  countChatHistoryTokens: () => 0,
  encode: () => [],
  logger: { debug() {} },
});
const naming = load("core/tools/mcpToolName.ts", ["getToolNameFromMCPServer"]);
const results = [];
function probe(name, fn) {
  const observation = fn();
  results.push({ name, passed: true, observation });
}
const tools = [
  { function: { name: "read" }, group: BUILT_IN_GROUP_NAME, readonly: true },
  { function: { name: "write" }, group: BUILT_IN_GROUP_NAME, readonly: false },
  { function: { name: "mcp_write" }, group: "external", readonly: false },
];
function select(mode, toolSettings = {}, toolGroupSettings = {}) {
  return selectActiveTools({ session: { mode }, config: { config: { tools } }, ui: { toolSettings, toolGroupSettings } }).map((t) => t.function.name);
}
function check(name, policies, arguments_ = {}) {
  return permission.checkToolPermission({ name, arguments: arguments_ }, { policies }).permission;
}
probe("IDE Plan only filters built-in write tools", () => {
  assert.deepEqual(select("chat"), []);
  assert.deepEqual(select("plan"), ["read", "mcp_write"]);
  assert.deepEqual(select("agent"), ["read", "write", "mcp_write"]);
  return "Plan exposes an enabled external tool even with readonly=false.";
});
probe("IDE explicit tool/group exclusions", () => {
  assert.deepEqual(select("agent", { read: "disabled" }, { external: "exclude" }), ["write"]);
  return "Explicit disabled and group exclude remove tools before invocation.";
});
probe("Workspace boundary tightens file access", () => {
  assert.equal(evaluateFileAccessPolicy("allowedWithoutPermission", false), "allowedWithPermission");
  assert.equal(evaluateFileAccessPolicy("allowedWithoutPermission", true), "allowedWithoutPermission");
  assert.equal(evaluateFileAccessPolicy("disabled", false), "disabled");
  return "Outside-workspace changes allow to ask, while disabled remains disabled.";
});
probe("Search replacement includes relaxed match strategies", () => {
  assert.equal(matching.findSearchMatch("const foo = 1;", "const foo = 1;").strategyName, "exactMatch");
  assert.equal(matching.findSearchMatch("Hello", "hello").strategyName, "caseInsensitiveMatch");
  assert.equal(matching.findSearchMatch("a = 1;", "a=1;").strategyName, "whitespaceIgnoredMatch");
  return "Exact, trimmed, case-insensitive and whitespace-ignored strategies are active; Jaro is disabled.";
});
probe("Ambiguous replacement is rejected unless replace_all", () => {
  assert.throws(() => replacement.executeFindAndReplace("foo foo", "foo", "bar", false), (e) => e.reason === errors.ContinueErrorReason.FindAndReplaceMultipleOccurrences);
  assert.equal(replacement.executeFindAndReplace("foo foo", "foo", "bar", true), "bar bar");
  return "Duplicate matches fail single replacement; replace_all changes both occurrences.";
});
probe("MultiEdit applies operations to successive string states", () => {
  assert.equal(replacement.executeMultiFindAndReplace("a=1", [{ old_string: "1", new_string: "2" }, { old_string: "2", new_string: "3" }]), "a=3");
  const original = "a=1";
  assert.throws(() => replacement.executeMultiFindAndReplace(original, [{ old_string: "1", new_string: "2" }, { old_string: "absent", new_string: "3" }]));
  assert.equal(original, "a=1");
  return "Later edits see earlier results; string computation failure returns no new content (no disk atomicity claim).";
});
probe("CLI headless permissions retain earlier write ask rules", () => {
  const policies = defaults.getDefaultToolPolicies(true);
  assert.equal(check("Edit", policies), "ask");
  assert.equal(check("Bash", policies), "allow");
  assert.equal(check("external_write", policies), "allow");
  assert.equal(check("Bash", [{ tool: "*", permission: "exclude" }, { tool: "Bash", permission: "allow" }]), "exclude");
  return "First match wins: headless Edit=ask, Bash=allow, external fallback=allow.";
});
probe("CLI Plan permits Bash and unmatched MCP tools", () => {
  assert.equal(check("Write", defaults.PLAN_MODE_POLICIES), "exclude");
  assert.equal(check("Bash", defaults.PLAN_MODE_POLICIES), "allow");
  assert.equal(check("external_write", defaults.PLAN_MODE_POLICIES), "allow");
  return "Plan is a tool policy preset, not an OS-level read-only environment.";
});
probe("CLI dynamic ask does not override static allow", () => {
  dynamicTools.push({ name: "Fixture", evaluateToolCallPolicy: () => "allowedWithPermission" });
  assert.equal(check("Fixture", defaults.AUTO_MODE_POLICIES), "allow");
  dynamicTools[0].evaluateToolCallPolicy = () => "disabled";
  assert.equal(check("Fixture", defaults.AUTO_MODE_POLICIES), "exclude");
  return "With an injected dynamic evaluator, only disabled overrides the configured allow.";
});
probe("CLI auto-compaction uses capped buffer arithmetic", () => {
  const cases = [[128000, 4096, 108904], [32000, 4096, 22323], [16000, 4000, 8000]];
  for (const [fixtureContext, fixtureOutput, threshold] of cases) {
    const args = { chatHistory: [], model: { fixtureContext, fixtureOutput, fixtureInputTokens: threshold - 1 } };
    assert.equal(compaction.shouldAutoCompact(args), false);
    args.model.fixtureInputTokens = threshold;
    assert.equal(compaction.shouldAutoCompact(args), true);
  }
  return cases.map(([context, output, threshold]) => ({ context, output, threshold }));
});
probe("CLI emergency pruning removes from the tail", () => {
  const message = (role, content, extra = {}) => ({ message: { role, content, ...extra }, contextItems: [] });
  const old = [message("user", "old"), message("assistant", "answer")];
  assert.deepEqual(compaction.pruneLastMessage([...old, message("user", "new"), message("assistant", "new answer")]), old);
  assert.deepEqual(compaction.pruneLastMessage([...old, message("assistant", "", { toolCalls: [{ id: "t" }] }), message("tool", "result")]), old);
  assert.deepEqual(compaction.pruneLastMessage([message("user", "only")]), []);
  return "Tail user/assistant or adjacent assistant-tool pairs can be removed; this differs from IDE head pruning.";
});
probe("Compaction view preserves leading system message", () => {
  const history = [{ message: { role: "system", content: "rules" } }, { message: { role: "user", content: "old" } }, { message: { role: "assistant", content: "summary" }, conversationSummary: "summary" }, { message: { role: "user", content: "next" } }];
  assert.deepEqual(compaction.getHistoryForLLM(history, 2), [history[0], history[2], history[3]]);
  return "The LLM view starts from the compaction marker plus a retained leading system message.";
});
probe("MCP normalization is not collision-free", () => {
  assert.equal(naming.getToolNameFromMCPServer("My API", "read"), "my_api_read");
  assert.equal(naming.getToolNameFromMCPServer("My-API", "read"), "my_api_read");
  return "Different server display names can normalize to the same prefix; use distinct configuration names.";
});

console.log(JSON.stringify({ commit: manifest.commit, runtime: process.version, method: "Pinned source functions with explicit dependency injection; no full-product execution", loaded, passed: results.length, failed: 0, results }, null, 2));
