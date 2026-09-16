// Tiny static file server for fixtures. Library + CLI.
//   import { startStaticServer } from './static-server.mjs'
//   const s = await startStaticServer({ root, port: 0 }); s.port; s.hits; await s.close();
//   node static-server.mjs --port 47831 [--root <dir>]   (runs until killed; prints one JSON line)
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { appendFileSync } from 'node:fs';
import { join, extname, resolve, normalize } from 'node:path';

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.txt': 'text/plain; charset=utf-8',
};

export async function startStaticServer({ root, port = 0, host = '127.0.0.1', hitsFile = null }) {
  const rootAbs = resolve(root);
  const hits = [];
  const server = createServer(async (req, res) => {
    const url = new URL(req.url, `http://${host}`);
    let pathname = decodeURIComponent(url.pathname);
    if (pathname.endsWith('/')) pathname += 'index.html';
    const hit = { ts: new Date().toISOString(), method: req.method, path: pathname };
    hits.push(hit);
    if (hitsFile) { try { appendFileSync(hitsFile, JSON.stringify(hit) + '\n'); } catch { /* ignore */ } }
    const file = normalize(join(rootAbs, pathname));
    if (!file.startsWith(rootAbs)) { res.writeHead(403); res.end('forbidden'); return; }
    try {
      const st = await stat(file);
      if (!st.isFile()) throw new Error('not a file');
      const body = await readFile(file);
      res.writeHead(200, { 'content-type': TYPES[extname(file).toLowerCase()] ?? 'application/octet-stream', 'cache-control': 'no-store' });
      res.end(body);
    } catch {
      res.writeHead(404, { 'content-type': 'text/plain' });
      res.end('not found');
    }
  });
  await new Promise((res, rej) => { server.once('error', rej); server.listen(port, host, res); });
  const actualPort = server.address().port;
  return {
    port: actualPort,
    url: `http://${host}:${actualPort}/`,
    hits,
    close: () => new Promise((res) => server.close(() => res())),
  };
}

if (import.meta.url === `file:///${process.argv[1].replace(/\\/g, '/')}` || process.argv[1]?.endsWith('static-server.mjs')) {
  const args = process.argv.slice(2);
  const get = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
  const root = get('--root', join(import.meta.dirname, '..', 'fixtures', 'static'));
  const port = Number(get('--port', '0'));
  const hitsFile = get('--hits-file', null);
  const s = await startStaticServer({ root, port, hitsFile });
  process.stdout.write(JSON.stringify({ ok: true, port: s.port, url: s.url, root }) + '\n');
  process.on('SIGINT', () => s.close().then(() => process.exit(0)));
  process.on('SIGTERM', () => s.close().then(() => process.exit(0)));
}
