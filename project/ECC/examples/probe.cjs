#!/usr/bin/env node
'use strict';

// Original research probe. Imports ECC's real implementations from a pinned
// checkout. All generated state stays in one temporary directory.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync, execFileSync } = require('node:child_process');

const commit = '8321021c54d670126ce3b2969d5deb880b4b0c2a';
if (!process.argv[2]) throw new Error('Usage: node probe.cjs /path/to/ECC');
const source = path.resolve(process.argv[2]);
assert.equal(execFileSync('git', ['-C', source, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim(), commit);
const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'ecc-blog-probe-'));
const report = { commit, node: process.version, experiments: [] };

function child(script, args, input, extraEnv = {}) {
  const result = spawnSync(process.execPath, [path.join(source, script), ...args], {
    cwd: fixture,
    input: JSON.stringify(input),
    encoding: 'utf8',
    timeout: 15000,
    env: { PATH: process.env.PATH, TMPDIR: fixture, CLAUDE_PLUGIN_ROOT: source, ...extraEnv },
  });
  if (result.error) throw result.error;
  return result;
}

try {
  const { isHookEnabled, getHookProfile } = require(path.join(source, 'scripts/lib/hook-flags.js'));
  const id = 'pre:config-protection';
  const flags = { profiles: 'standard,strict' };
  const profile = {
    defaultProfile: getHookProfile({}),
    minimal: isHookEnabled(id, { ...flags, env: { ECC_HOOK_PROFILE: 'minimal' } }),
    strict: isHookEnabled(id, { ...flags, env: { ECC_HOOK_PROFILE: 'strict' } }),
    globallyDisabled: isHookEnabled(id, { ...flags, env: { ECC_HOOKS_ENABLED: 'false' } }),
  };
  assert.deepEqual(profile, { defaultProfile: 'standard', minimal: false, strict: true, globallyDisabled: false });
  report.experiments.push({ name: 'hook profiles', ...profile });

  const configPath = path.join(fixture, 'eslint.config.js');
  const event = { tool_name: 'Write', tool_input: { file_path: configPath, content: 'export default [];' } };
  const args = [id, 'scripts/hooks/config-protection.js', 'standard,strict'];
  const absent = child('scripts/hooks/run-with-flags.js', args, event);
  fs.writeFileSync(configPath, 'export default [];\n');
  const existing = child('scripts/hooks/run-with-flags.js', args, event);
  const disabled = child('scripts/hooks/run-with-flags.js', args, event, { ECC_HOOKS_ENABLED: 'false' });
  assert.equal(absent.status, 0);
  assert.equal(existing.status, 2);
  assert.equal(disabled.status, 0);
  report.experiments.push({ name: 'real hook runner', newConfig: absent.status, existingConfig: existing.status, disabledHook: disabled.status });

  const vault = require(path.join(source, 'scripts/lib/memory-vault.js'));
  const roots = vault.resolveVaultRoots({ cwd: fixture, homeDir: path.join(fixture, 'user-data'), env: {} });
  const options = { roots, now: () => '2026-09-15T00:00:00.000Z' };
  const saved = vault.saveMemory({ id: 'mem_probe_retry', title: 'Retry policy',
    body: 'Use retry after a transient error.', kind: 'decision', scope: 'project',
    sourceHarness: 'codex', targetHarnesses: ['claude'], tags: ['retry'] }, options);
  assert.equal(saved.memory.trust, 'unreviewed');
  assert.throws(() => vault.saveMemory({ id: 'mem_probe_retry', kind: 'decision', title: 'Overwrite', body: 'replacement' }, options), /create-only/);
  // Synthetic canary, never a real credential; its value is not printed.
  assert.throws(() => vault.saveMemory({ title: 'Secret fixture', body: 'sk-' + 'A'.repeat(24) }, options), /suspected secret/);
  const visible = vault.searchMemories('retry', { roots, targetHarness: 'claude' });
  const hidden = vault.searchMemories('retry', { roots, targetHarness: 'codex' });
  assert.equal(visible.results.length, 1);
  assert.equal(visible.results[0].score, 35);
  assert.equal(hidden.results.length, 0);
  report.experiments.push({ name: 'memory vault', trust: saved.memory.trust,
    matchingHarnessResults: visible.results.length, otherHarnessResults: hidden.results.length,
    lexicalScore: visible.results[0].score, overwriteRejected: true, secretCanaryRejected: true });

  const instinctCli = path.join(source, 'skills/continuous-learning-v2/scripts/instinct-cli.py');
  function evolve(label, triggers) {
    const data = path.join(fixture, label);
    const personal = path.join(data, 'instincts/personal');
    fs.mkdirSync(personal, { recursive: true });
    for (const [i, trigger] of triggers.entries()) {
      fs.writeFileSync(path.join(personal, `probe-${i}.yaml`),
        `---\nid: probe-${i}\ntrigger: ${trigger}\nconfidence: 0.85\ndomain: testing\nscope: global\n---\n\n## Action\n\nCheck the expected result.\n`);
    }
    const result = spawnSync('python3', [instinctCli, 'evolve'], { cwd: fixture, encoding: 'utf8', timeout: 15000,
      env: { PATH: process.env.PATH, TMPDIR: fixture, PYTHONDONTWRITEBYTECODE: '1', CLV2_HOMUNCULUS_DIR: data, CLAUDE_PROJECT_DIR: '' } });
    if (result.error) throw result.error;
    assert.equal(result.status, 0, result.stderr + result.stdout);
    const count = result.stdout.match(/Potential skill clusters found:\s*(\d+)/);
    assert.ok(count, result.stdout);
    return Number(count[1]);
  }
  const english = evolve('english', ['when writing database migration tests', 'when reviewing database migration tests', 'when rotating signing certificates']);
  const chinese = evolve('chinese', ['编写数据库迁移测试时', '审查数据库迁移测试时', '轮换签名证书时']);
  assert.equal(english, 1);
  assert.equal(chinese, 0);
  report.experiments.push({ name: 'instinct keyword clustering', englishClusters: english, chineseClusters: chinese,
    note: 'Pure Chinese triggers have no tokens under the current ASCII tokenizer.' });

  const gate = child('scripts/eval-harness.js', ['gate', 'run', path.join(fixture, 'does-not-exist.json')], {});
  assert.equal(gate.status, 1);
  assert.match(gate.stderr, /gate\.isolation_required/);
  report.experiments.push({ name: 'evaluation execution boundary', exitCode: gate.status, error: 'gate.isolation_required', configWasAbsent: true });
  console.log(JSON.stringify(report, null, 2));
} finally {
  fs.rmSync(fixture, { recursive: true, force: true });
}
