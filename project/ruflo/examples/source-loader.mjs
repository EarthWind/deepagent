// Research-only loader: execute the pinned TypeScript sources without a build.
// No business logic is replaced. Resolve emitted .js imports to their .ts source.
import { registerHooks, stripTypeScriptTypes } from 'node:module';
import { existsSync, readFileSync } from 'node:fs';
import { resolve as resolvePath } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = process.env.RUFLO_SOURCE;
if (!root) throw new Error('Set RUFLO_SOURCE to the pinned Ruflo checkout');

registerHooks({
  resolve(specifier, context, nextResolve) {
    if (specifier.startsWith('@claude-flow/cli-core/')) {
      const relative = specifier.slice('@claude-flow/cli-core/'.length);
      const path = resolvePath(root, 'v3/@claude-flow/cli-core/src', relative + '.ts');
      return { url: pathToFileURL(path).href, shortCircuit: true };
    }
    if (specifier.startsWith('.') && specifier.endsWith('.js') && context.parentURL?.startsWith('file:')) {
      const tsURL = new URL(specifier.slice(0, -3) + '.ts', context.parentURL);
      if (existsSync(fileURLToPath(tsURL))) return { url: tsURL.href, shortCircuit: true };
    }
    return nextResolve(specifier, context);
  },
  load(url, context, nextLoad) {
    if (url.startsWith('file:') && url.endsWith('.ts')) {
      const source = stripTypeScriptTypes(readFileSync(fileURLToPath(url), 'utf8'), {
        mode: 'transform', sourceUrl: url,
      });
      return { format: 'module', source, shortCircuit: true };
    }
    return nextLoad(url, context);
  },
});
