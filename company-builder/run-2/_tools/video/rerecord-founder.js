/* Re-record only the founder UI tour, slower (~65s), to match VO length. */
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..", "..");
const CLIPS = path.join(ROOT, "video", "assets", "clips");
const SIZE = { width: 1280, height: 720 };
const base = "http://localhost:8231";
const wait = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: SIZE, recordVideo: { dir: CLIPS, size: SIZE } });
  const page = await ctx.newPage();

  await page.goto(`${base}/product/`);
  await page.waitForSelector(".card.s-act");
  await wait(8000);                                   // board reads (VO: expiration dates...)
  await page.hover('.card[data-id="ok-jman"]');
  await wait(3000);
  await page.click('.card[data-id="ok-jman"]');
  await page.waitForSelector("#view-detail:not([hidden])");
  await wait(5000);                                   // facts + consequence
  await page.mouse.wheel(0, 260);
  await wait(4500);                                   // alert schedule
  await page.hover("#mark-renewed-btn");
  await wait(1200);
  await page.click("#mark-renewed-btn");
  await wait(5000);                                   // calm board + toast
  await page.click('.nav-tab[data-view="ce"]');
  await wait(4500);                                   // CE 2/4
  await page.click("#log-ce-btn");
  await wait(5000);                                   // 4/4 green
  await page.click('.nav-tab[data-view="locker"]');
  await wait(6000);                                   // share link panel
  await page.click('.nav-tab[data-view="rules"]');
  await wait(6500);                                   // rules with verified chips
  await page.click('.nav-tab[data-view="board"]');
  await wait(8000);                                   // all-good hold

  const video = page.video();
  await ctx.close();
  const src = await video.path();
  const dst = path.join(CLIPS, "ui-founder.webm");
  if (fs.existsSync(dst)) fs.unlinkSync(dst);
  fs.renameSync(src, dst);
  await browser.close();
  console.log("re-recorded ui-founder.webm");
})().catch(e => { console.error(e); process.exit(1); });
