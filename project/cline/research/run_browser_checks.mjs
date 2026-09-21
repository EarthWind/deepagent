/** Exact viewport checks with local Chrome CDP. Node 24+, no npm dependencies.
 * Usage: node project/cline/research/run_browser_checks.mjs /tmp/cline-visual-check
 * First generate the review pages with prepare_visual_checks.py.
 */
import { spawn } from 'node:child_process';
import { readFile, writeFile, mkdtemp } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';

const dir = resolve(process.argv[2]);
const profile = await mkdtemp(join(dir, 'chrome-profile-'));
const child = spawn('google-chrome', ['--headless=new', '--no-sandbox', '--disable-gpu',
  '--disable-dev-shm-usage', '--no-first-run', '--no-default-browser-check', '--remote-debugging-port=0',
  `--user-data-dir=${profile}`, 'about:blank'], { stdio: ['ignore', 'ignore', 'ignore'] });
let childError;
child.on('error', error => { childError = error; });
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
let ws;
try {
  let socketPath, port;
  for (let i = 0; i < 100; i++) {
    if (childError) throw childError;
    try { [port, socketPath] = (await readFile(join(profile, 'DevToolsActivePort'), 'utf8')).trim().split('\n'); break; }
    catch { await pause(100); }
  }
  if (!socketPath) throw new Error('Chrome did not expose a debugging socket');
  ws = new WebSocket(`ws://127.0.0.1:${port}${socketPath}`);
  await new Promise((resolve, reject) => { ws.addEventListener('open', resolve, { once: true }); ws.addEventListener('error', reject, { once: true }); });
  let nextId = 0;
  const pending = new Map();
  ws.addEventListener('message', event => {
    const message = JSON.parse(event.data);
    const p = pending.get(message.id);
    if (!p) return;
    pending.delete(message.id); clearTimeout(p.timer);
    message.error ? p.reject(new Error(JSON.stringify(message.error))) : p.resolve(message.result);
  });
  function call(method, params = {}, sessionId) {
    return new Promise((resolve, reject) => {
      const id = ++nextId;
      const timer = setTimeout(() => { pending.delete(id); reject(new Error(`CDP timeout: ${method}`)); }, 20000);
      pending.set(id, { resolve, reject, timer }); ws.send(JSON.stringify({ id, method, params, sessionId }));
    });
  }
  const version = await call('Browser.getVersion');
  for (const [name, file, width, height, mobile] of [
    ['diagrams', 'diagrams.html', 1400, 1800, false],
    ['desktop', 'page.html', 1440, 1080, false],
    ['mobile', 'page.html', 390, 844, true],
  ]) {
    const { targetId } = await call('Target.createTarget', { url: 'about:blank' });
    const { sessionId } = await call('Target.attachToTarget', { targetId, flatten: true });
    await call('Page.enable', {}, sessionId);
    await call('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile }, sessionId);
    await call('Page.navigate', { url: pathToFileURL(join(dir, file)).href }, sessionId);
    let measured;
    for (let i = 0; i < 100; i++) {
      const value = await call('Runtime.evaluate', { expression: 'document.querySelector("#check-result")?.textContent', returnByValue: true }, sessionId);
      if (value.result.value && value.result.value !== 'pending') { measured = JSON.parse(value.result.value); break; }
      await pause(100);
    }
    if (!measured) throw new Error(`No measurement: ${name}`);
    if (name !== 'diagrams' && measured.viewportWidth !== width) throw new Error(`Unexpected viewport for ${name}: ${measured.viewportWidth}`);
    const html = await call('Runtime.evaluate', { expression: 'document.documentElement.outerHTML', returnByValue: true }, sessionId);
    await writeFile(join(dir, `${name}.dom.html`), html.result.value);
    const shot = await call('Page.captureScreenshot', { format: 'png' }, sessionId);
    await writeFile(join(dir, `${name}.png`), Buffer.from(shot.data, 'base64'));
    console.log(JSON.stringify({ name, browser: version.product, ...measured }));
    await call('Target.closeTarget', { targetId });
    if (!measured.passed) throw new Error(`Layout failed: ${name}`);
  }
  await call('Browser.close');
} finally {
  ws?.close();
  child.kill();
}
