/* Record UI footage clips + title cards for the ReconStock videos.
   Each clip = fresh browser context (fresh seed state) with recordVideo 1280x720.
   Output: run-1/video/assets/clips/*.webm  */
const path = require("path");
const fs = require("fs");
const http = require("http");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..", "..");
const CLIPS = path.join(ROOT, "video", "assets", "clips");
fs.mkdirSync(CLIPS, { recursive: true });
const PORT = 8125;
const MIME = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml" };
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

(async () => {
  await new Promise(r => server.listen(PORT, r));
  const browser = await chromium.launch();
  const base = `http://localhost:${PORT}`;

  // ---- title cards (generous length; trimmed at assembly) ----
  for (const card of ["hook", "logo", "failsafe", "pricing", "close"]) {
    await record(browser, "card-" + card, async page => {
      await page.goto(`${base}/video/assets/cards/card-${card}.html`);
      await wait(card === "close" ? 16000 : 7000);
    });
  }

  // ---- clip: breaker hero moment (dashboard -> flagged sync -> halt screen, long hold) ----
  await record(browser, "ui-breaker", async page => {
    await page.goto(`${base}/product/`);
    await page.waitForSelector(".pending-card--danger");
    await wait(2000);
    await page.locator('.pending-card--danger [data-action="review"]').hover();
    await wait(900);
    await page.locator('.pending-card--danger [data-action="review"]').click();
    await page.waitForSelector("#view-breaker:not([hidden])");
    await wait(4500); // hero hold
    await page.mouse.wheel(0, 380); // reveal sample table of zeroed SKUs
    await wait(3000);
  });

  // ---- clip: diff preview + dry-run report ----
  await record(browser, "ui-diff", async page => {
    await page.goto(`${base}/product/`);
    await page.waitForSelector(".pending-card");
    await wait(1500);
    await page.locator('.pending-card:not(.pending-card--danger) [data-action="review"]').click();
    await page.waitForSelector("#view-diff:not([hidden])");
    await wait(3000); // read the diff table
    await page.locator("#run-dryrun-btn").hover();
    await wait(800);
    await page.locator("#run-dryrun-btn").click();
    await wait(3200); // read "0 writes made" report
  });

  // ---- clip: rollback (audit log -> rollback -> dashboard restored) ----
  await record(browser, "ui-rollback", async page => {
    await page.goto(`${base}/product/`);
    await page.waitForSelector(".pending-card");
    await wait(1200);
    await page.locator('.nav-tab[data-view="audit"]').click();
    await page.waitForSelector("#view-audit:not([hidden])");
    await wait(2200); // read the audit log
    await page.locator('#audit-tbody [data-action="rollback"]').first().click({ force: true });
    await wait(2600); // "Rolled back" badge + toast
    await page.locator('.nav-tab[data-view="dashboard"]').click();
    await wait(2400); // restored quantities flash green
  });

  // ---- clip: slow full tour for the founder video (~34s) ----
  await record(browser, "ui-founder", async page => {
    await page.goto(`${base}/product/`);
    await page.waitForSelector(".pending-card");
    await wait(3500); // dashboard reads
    await page.locator('.pending-card:not(.pending-card--danger) [data-action="review"]').click();
    await page.waitForSelector("#view-diff:not([hidden])");
    await wait(3500); // diff table
    await page.locator("#run-dryrun-btn").click();
    await wait(3500); // dry-run report
    await page.locator('[data-back="dashboard"]').click();
    await wait(1500);
    await page.locator('.pending-card--danger [data-action="review"]').click();
    await page.waitForSelector("#view-breaker:not([hidden])");
    await wait(6000); // long hold on the halt screen
    await page.locator("#breaker-dismiss-btn").click();
    await wait(1500);
    await page.locator('.nav-tab[data-view="audit"]').click();
    await wait(2500);
    await page.locator('#audit-tbody [data-action="rollback"]').first().click({ force: true });
    await wait(2500);
    await page.locator('.nav-tab[data-view="dashboard"]').click();
    await wait(3000); // quantities restored
  });

  await browser.close();
  server.close();
  console.log("All clips recorded to", CLIPS);
})().catch(e => { console.error(e); process.exit(1); });
