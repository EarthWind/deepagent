/**
 * Run with a local Chrome already listening for CDP:
 * google-chrome --headless=new --no-sandbox --disable-gpu \
 *   --user-data-dir=/tmp/continue-blog-browser --remote-debugging-port=9225 about:blank
 * node project/continue/research/browser_checks.mjs http://127.0.0.1:9225
 * To close that dedicated browser after inspection, add --close-browser-only.
 * Only local file URLs are opened; generated screenshots go to /tmp.
 */
import { mkdirSync, readdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const endpoint = process.argv[2] ?? "http://127.0.0.1:9225";
if (process.argv.includes("--close-browser-only")) {
  const version = await (await fetch(`${endpoint}/json/version`)).json();
  const browserSocket = new WebSocket(version.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => { browserSocket.onopen = resolve; browserSocket.onerror = reject; });
  browserSocket.send(JSON.stringify({ id: 1, method: "Browser.close" }));
  await new Promise((resolve) => { browserSocket.onclose = resolve; });
  console.log("Closed dedicated research browser");
  process.exit(0);
}
const output = "/tmp/continue-blog-checks";
mkdirSync(output, { recursive: true });
const target = await (await fetch(`${endpoint}/json/new?about:blank`, { method: "PUT" })).json();
const socket = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => { socket.onopen = resolve; socket.onerror = reject; });
let nextId = 0;
const pending = new Map();
const events = new Map();
socket.onmessage = ({ data }) => {
  const message = JSON.parse(data);
  if (message.id) {
    const pair = pending.get(message.id);
    if (!pair) return;
    pending.delete(message.id);
    message.error ? pair.reject(new Error(JSON.stringify(message.error))) : pair.resolve(message.result);
  } else if (events.has(message.method)) {
    const callback = events.get(message.method);
    events.delete(message.method);
    callback(message.params);
  }
};
function cdp(method, params = {}) {
  const id = ++nextId;
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject });
    socket.send(JSON.stringify({ id, method, params }));
  });
}
async function evaluate(expression) {
  const result = await cdp("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
  if (result.exceptionDetails) throw new Error(JSON.stringify(result.exceptionDetails));
  return result.result.value;
}
async function navigate(file) {
  const loaded = new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error(`Load timeout: ${file}`)), 15000);
    events.set("Page.loadEventFired", () => { clearTimeout(timeout); resolve(); });
  });
  await cdp("Page.navigate", { url: pathToFileURL(file).href });
  await loaded;
  await evaluate("document.fonts.ready.then(() => true)");
}
async function screenshot(name) {
  const { data } = await cdp("Page.captureScreenshot", { format: "png", captureBeyondViewport: false });
  writeFileSync(path.join(output, name), Buffer.from(data, "base64"));
}

await cdp("Page.enable");
await cdp("Runtime.enable");
const pages = [];
for (const [name, width, height] of [["desktop", 1440, 1100], ["mobile", 390, 844]]) {
  await cdp("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: false });
  await navigate(path.join(root, "index.html"));
  const result = await evaluate(`(() => ({
    title: document.title,
    viewport: innerWidth,
    scrollWidth: document.documentElement.scrollWidth,
    chapters: document.querySelectorAll('a[id^="sec-"]').length,
    images: [...document.images].map(img => ({src: img.getAttribute('src'), loaded: img.complete && img.naturalWidth > 0})),
    badAnchors: [...document.querySelectorAll('a[href^="#"]')].filter(a => !document.getElementById(a.hash.slice(1))).map(a => a.hash),
    responsiveToc: getComputedStyle(document.querySelector('.mobile-toc')).display,
    remoteResources: performance.getEntriesByType('resource').filter(x => /^https?:/.test(x.name)).map(x => x.name)
  }))()`);
  pages.push({ name, ...result });
  await screenshot(`${name}.png`);
  await evaluate("document.getElementById('sec-13').scrollIntoView({behavior:'instant'})");
  await screenshot(`${name}-editing.png`);
}

const diagrams = [];
for (const file of readdirSync(path.join(root, "assets")).filter((f) => f.endsWith(".svg")).sort()) {
  await cdp("Emulation.setDeviceMetricsOverride", { width: 1280, height: 900, deviceScaleFactor: 1, mobile: false });
  await navigate(path.join(root, "assets", file));
  const result = await evaluate(`(() => {
    const svg = document.documentElement;
    const view = svg.viewBox.baseVal;
    const cards = [...svg.querySelectorAll('rect[fill="white"]')].map(r => r.getBBox());
    const issues = [];
    for (const text of svg.querySelectorAll('text')) {
      const b = text.getBBox();
      if (b.x < 0 || b.y < 0 || b.x+b.width > view.width+1 || b.y+b.height > view.height+1)
        issues.push({kind:'canvas-overflow', text:text.textContent, x:b.x, right:b.x+b.width});
      const card = cards.find(r => b.x >= r.x && b.x < r.x+r.width && b.y >= r.y && b.y < r.y+r.height);
      if (card && (b.x+b.width > card.x+card.width-8 || b.y+b.height > card.y+card.height-5))
        issues.push({kind:'card-overflow', text:text.textContent, right:b.x+b.width, limit:card.x+card.width-8});
    }
    return {title:svg.querySelector('title').textContent, textCount:svg.querySelectorAll('text').length, issues};
  })()`);
  diagrams.push({ file, ...result });
  await screenshot(file.replace(".svg", ".png"));
}

const failures = [];
for (const p of pages) {
  if (p.scrollWidth > p.viewport || p.badAnchors.length || p.remoteResources.length || p.images.some((x) => !x.loaded)) failures.push(p.name);
}
for (const d of diagrams) if (d.issues.length) failures.push(d.file);
const report = { browser: (await cdp("Browser.getVersion")).product, pages, diagrams, screenshots: output, failures };
writeFileSync(path.join(root, "research/browser-checks.json"), JSON.stringify(report, null, 2) + "\n");
console.log(JSON.stringify(report, null, 2));
socket.close();
await fetch(`${endpoint}/json/close/${target.id}`);
process.exitCode = failures.length ? 1 : 0;
