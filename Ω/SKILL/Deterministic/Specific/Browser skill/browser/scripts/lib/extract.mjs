// Compiled-in extractors. bw.mjs passes these strings to `playwright-cli eval`.
// The agent never writes JavaScript; it only picks a --mode.
// Each extractor is a function body evaluated in the page. Optional target
// element `el` is bound when a ref/css is given; otherwise `document.body`.

const TEXT = `(el) => {
  const root = el || document.body;
  const t = (root.innerText || root.textContent || '').replace(/\\u00a0/g, ' ');
  return t.split('\\n').map(s => s.replace(/[ \\t]+/g, ' ').trim()).filter(Boolean).join('\\n');
}`;

// Markdown-ish: headings, paragraphs, list items, links, code, tables (pipe rows).
const MD = `(el) => {
  const root = el || document.body;
  const skip = new Set(['SCRIPT','STYLE','NOSCRIPT','TEMPLATE','SVG','CANVAS','IFRAME']);
  const out = [];
  const clean = (s) => (s || '').replace(/\\s+/g, ' ').trim();
  const walk = (n, depth) => {
    if (n.nodeType === 3) { const t = clean(n.nodeValue); if (t) out.push(t); return; }
    if (n.nodeType !== 1 || skip.has(n.tagName)) return;
    const cs = getComputedStyle(n);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const tag = n.tagName;
    if (/^H[1-6]$/.test(tag)) { out.push('\\n' + '#'.repeat(+tag[1]) + ' ' + clean(n.innerText) + '\\n'); return; }
    if (tag === 'A' && n.href) { out.push('[' + clean(n.innerText) + '](' + n.href + ')'); return; }
    if (tag === 'LI') { out.push('\\n' + '  '.repeat(depth) + '- ' + clean(n.innerText)); return; }
    if (tag === 'PRE') { out.push('\\n\`\`\`\\n' + n.innerText + '\\n\`\`\`\\n'); return; }
    if (tag === 'CODE') { out.push('\`' + clean(n.innerText) + '\`'); return; }
    if (tag === 'TABLE') {
      const rows = [...n.querySelectorAll('tr')].map(r => [...r.children].map(c => clean(c.innerText)));
      if (rows.length) {
        out.push('\\n| ' + rows[0].join(' | ') + ' |');
        out.push('\\n| ' + rows[0].map(() => '---').join(' | ') + ' |');
        for (const r of rows.slice(1)) out.push('\\n| ' + r.join(' | ') + ' |');
        out.push('\\n');
      }
      return;
    }
    if (tag === 'P' || tag === 'BLOCKQUOTE' || tag === 'DIV' || tag === 'SECTION' || tag === 'ARTICLE') out.push('\\n');
    for (const c of n.childNodes) walk(c, tag === 'UL' || tag === 'OL' ? depth + 1 : depth);
    if (tag === 'P' || tag === 'BR' || tag === 'TR') out.push('\\n');
  };
  walk(root, 0);
  return out.join(' ').replace(/[ \\t]+\\n/g, '\\n').replace(/\\n[ \\t]+/g, '\\n').replace(/\\n{3,}/g, '\\n\\n').trim();
}`;

const LINKS = `(el) => {
  const root = el || document;
  const seen = new Set();
  const res = [];
  for (const a of root.querySelectorAll('a[href]')) {
    const href = a.href; if (!href || seen.has(href)) continue; seen.add(href);
    res.push({ text: (a.innerText || a.getAttribute('aria-label') || '').replace(/\\s+/g, ' ').trim().slice(0, 120), href });
  }
  return JSON.stringify(res);
}`;

const TABLE = `(el) => {
  const root = el || document;
  const tables = root.tagName === 'TABLE' ? [root] : [...root.querySelectorAll('table')];
  const res = tables.map(t => {
    const rows = [...t.querySelectorAll('tr')].map(r => [...r.children].map(c => (c.innerText || '').replace(/\\s+/g, ' ').trim()));
    const header = rows.length && t.querySelector('th') ? rows[0] : null;
    const body = header ? rows.slice(1) : rows;
    return { caption: (t.caption && t.caption.innerText || '').trim(), header, rows: body };
  });
  return JSON.stringify(res);
}`;

export const EXTRACTORS = Object.freeze({ text: TEXT, md: MD, links: LINKS, table: TABLE });
export const EXTRACT_MODES = Object.freeze(Object.keys(EXTRACTORS));

/** Wait helpers evaluated via `run-code` (page-level). Template only; args are JSON-encoded by bw.mjs. */
export const WAIT_CODE = {
  text: (text, ms) => `async page => { await page.getByText(${JSON.stringify(text)}).first().waitFor({ state: 'visible', timeout: ${ms} }); return 'ok'; }`,
  url: (glob, ms) => `async page => { await page.waitForURL(${JSON.stringify(glob)}, { timeout: ${ms} }); return page.url(); }`,
  idle: (ms) => `async page => { await page.waitForLoadState('networkidle', { timeout: ${ms} }); return 'ok'; }`,
  ms: (ms) => `async page => { await page.waitForTimeout(${ms}); return 'ok'; }`,
  css: (css, ms) => `async page => { await page.locator(${JSON.stringify(css)}).first().waitFor({ state: 'visible', timeout: ${ms} }); return 'ok'; }`,
};
