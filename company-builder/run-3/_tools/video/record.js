/* Record UI clips + title cards for WideTally videos (1280x720 webm).
   Run from run-3/_tools:  node video/record.js  */
const path = require("path"), fs = require("fs"), http = require("http");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..", "..");
const CLIPS = path.join(ROOT, "video", "assets", "clips");
fs.mkdirSync(CLIPS, { recursive: true });
const PORT = 8132;
const MIME = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".csv": "text/csv" };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
  const f = path.normalize(path.join(ROOT, p));
  if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "Content-Type": MIME[path.extname(f)] || "text/plain" }); res.end(d); });
});
const SIZE = { width: 1280, height: 720 };
const wait = ms => new Promise(r => setTimeout(r, ms));

async function record(browser, name, fn) {
  const ctx = await browser.newContext({ viewport: SIZE, recordVideo: { dir: CLIPS, size: SIZE } });
  const page = await ctx.newPage();
  await fn(page);
  const video = page.video();
  await ctx.close();
  const src = await video.path();
  const dst = path.join(CLIPS, name + ".webm");
  if (fs.existsSync(dst)) fs.unlinkSync(dst);
  fs.renameSync(src, dst);
  console.log("recorded", name + ".webm");
}
const loadSamples = async page => {
  await page.goto(`http://localhost:${PORT}/product/index.html`);
  await page.locator('[data-action="load-samples"]').first().click();
  await page.waitForSelector("#stat-row .stat");
};

(async () => {
  await new Promise(r => server.listen(PORT, r));
  const browser = await chromium.launch();
  const base = `http://localhost:${PORT}`;

  for (const [card, dur] of [["hook", 7000], ["noapi", 8000], ["logo", 7000], ["pricing", 8000], ["privacy", 9000], ["close", 16000]]) {
    await record(browser, "card-" + card, async page => {
      await page.goto(`${base}/video/assets/cards/card-${card}.html`);
      await wait(dur);
    });
  }

  // imports: dropzone view, then samples parsed
  await record(browser, "ui-imports", async page => {
    await page.goto(`${base}/product/index.html`);
    await page.locator('.tab[data-view="imports"]').click();
    await wait(2500);
    await page.locator('#dropzone [data-action="load-samples"]').click();
    await page.waitForSelector("#imports-table tr");
    await wait(4500);
  });

  // ledger: stats + chart, hover across bars
  await record(browser, "ui-ledger", async page => {
    await loadSamples(page);
    await wait(2500);
    const box = await page.locator("#chart-monthly").boundingBox();
    for (let i = 0; i <= 8; i++) {
      await page.mouse.move(box.x + 80 + (box.width - 140) * i / 8, box.y + box.height * 0.55, { steps: 6 });
      await wait(420);
    }
    await wait(1200);
    await page.mouse.wheel(0, 300);
    await wait(2500);
  });

  await record(browser, "ui-books", async page => {
    await loadSamples(page);
    await page.locator('.tab[data-view="books"]').click();
    await wait(3200);
    await page.mouse.wheel(0, 220);
    await wait(3800);
  });

  await record(browser, "ui-ads", async page => {
    await loadSamples(page);
    await page.locator('.tab[data-view="ads"]').click();
    await wait(4200);
    await page.mouse.wheel(0, 260);
    await wait(3800);
  });

  // founder slow tour ~36s
  await record(browser, "ui-founder", async page => {
    await page.goto(`${base}/product/index.html`);
    await wait(2500); // empty state
    await page.locator('[data-action="load-samples"]').first().click();
    await page.waitForSelector("#stat-row .stat");
    await wait(7000); // ledger read
    const box = await page.locator("#chart-monthly").boundingBox();
    for (let i = 0; i <= 5; i++) { await page.mouse.move(box.x + 100 + (box.width - 160) * i / 5, box.y + box.height * .5, { steps: 5 }); await wait(380); }
    await page.locator('.tab[data-view="books"]').click();
    await wait(7500); // books read
    await page.locator('.tab[data-view="ads"]').click();
    await wait(9000); // ads read
    await page.locator('.tab[data-view="imports"]').click();
    await wait(5000); // imports
  });

  await browser.close(); server.close();
  console.log("All clips recorded.");
})().catch(e => { console.error(e); process.exit(1); });
