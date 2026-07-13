/* Screenshot verification: landing + product app (desktop & mobile), with sample data loaded.
   Run from run-3/_tools:  node screenshot.js   → writes ../record/shots/*.png and logs console errors. */
const path = require("path"), fs = require("fs");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "record", "shots");
fs.mkdirSync(OUT, { recursive: true });

const server = require("http").createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
  const f = path.normalize(path.join(ROOT, p));
  if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); return res.end(); }
    const M = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".csv": "text/csv" };
    res.writeHead(200, { "Content-Type": M[path.extname(f)] || "text/plain" }); res.end(d); });
});

(async () => {
  await new Promise(r => server.listen(8131, r));
  const browser = await chromium.launch();
  const errors = [];
  async function shoot(name, vp, url, actions) {
    const ctx = await browser.newContext({ viewport: vp });
    const page = await ctx.newPage();
    page.on("console", m => { if (m.type() === "error") errors.push(`[${name}] ${m.text()}`); });
    page.on("pageerror", e => errors.push(`[${name}] PAGEERROR ${e.message}`));
    await page.goto(`http://localhost:8131${url}`);
    if (actions) await actions(page);
    await page.screenshot({ path: path.join(OUT, name + ".png"), fullPage: true });
    await ctx.close();
    console.log("shot", name + ".png");
  }
  const D = { width: 1280, height: 800 }, M = { width: 390, height: 844 };
  const load = async page => {
    await page.locator('[data-action="load-samples"]').first().click();
    await page.waitForSelector("#stat-row .stat");
    await page.waitForTimeout(400);
  };
  await shoot("site-desktop", D, "/site/index.html");
  await shoot("site-mobile", M, "/site/index.html");
  await shoot("app-empty-desktop", D, "/product/index.html");
  await shoot("app-ledger-desktop", D, "/product/index.html", load);
  await shoot("app-ledger-mobile", M, "/product/index.html", load);
  await shoot("app-books-desktop", D, "/product/index.html", async p => { await load(p); await p.locator('.tab[data-view="books"]').click(); await p.waitForTimeout(300); });
  await shoot("app-ads-desktop", D, "/product/index.html", async p => { await load(p); await p.locator('.tab[data-view="ads"]').click(); await p.waitForTimeout(300); });
  await shoot("app-imports-desktop", D, "/product/index.html", async p => { await load(p); await p.locator('.tab[data-view="imports"]').click(); await p.waitForTimeout(300); });
  await browser.close(); server.close();
  if (errors.length) { console.log("CONSOLE ERRORS:\n" + errors.join("\n")); process.exit(2); }
  console.log("No console errors.");
})().catch(e => { console.error(e); process.exit(1); });
