/* Record title cards + UI clips for the DueCrew videos.
   Each clip = fresh context, recordVideo 1280x720. Requires server on :8231.
   Run: node video/record.js */
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..", "..");
const CLIPS = path.join(ROOT, "video", "assets", "clips");
fs.mkdirSync(CLIPS, { recursive: true });
const SIZE = { width: 1280, height: 720 };
const base = "http://localhost:8231";
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
  const browser = await chromium.launch();

  // ---- title cards (generous length; trimmed at assembly) ----
  for (const card of ["hook", "stakes", "logo", "pricing", "close", "onething"]) {
    await record(browser, "card-" + card, async page => {
      await page.goto(`${base}/video/assets/cards/card-${card}.html`);
      await wait(card === "close" ? 12000 : 9000);
    });
  }

  // ---- ui-board: board hero with red card ----
  await record(browser, "ui-board", async page => {
    await page.goto(`${base}/product/`);
    await page.waitForSelector(".card.s-act");
    await wait(2500);
    await page.hover('.card[data-id="ok-jman"]');
    await wait(2200);
    await page.hover('.card[data-id="gl-coi"]');
    await wait(2200);
    await page.hover('.card[data-id="tx-license"]');
    await wait(2000);
  });

  // ---- ui-renew: red card detail -> schedule -> mark renewed -> calm board ----
  await record(browser, "ui-renew", async page => {
    await page.goto(`${base}/product/`);
    await page.waitForSelector(".card.s-act");
    await wait(1500);
    await page.click('.card[data-id="ok-jman"]');
    await page.waitForSelector("#view-detail:not([hidden])");
    await wait(4200); // read facts + consequence
    await page.mouse.wheel(0, 260); // reveal alert schedule
    await wait(3200);
    await page.hover("#mark-renewed-btn");
    await wait(900);
    await page.click("#mark-renewed-btn");
    await wait(4200); // toast "You're good", green pill
  });

  // ---- ui-ce: ledger 2/4 -> log -> 4/4 green ----
  await record(browser, "ui-ce", async page => {
    await page.goto(`${base}/product/`);
    await page.waitForSelector(".card.s-act");
    await page.click('.nav-tab[data-view="ce"]');
    await wait(3000); // read requirement + meter at 2/4
    await page.hover("#log-ce-btn");
    await wait(900);
    await page.click("#log-ce-btn");
    await wait(4000); // meter fills, toast
  });

  // ---- ui-founder: slow full tour (~40s) ----
  await record(browser, "ui-founder", async page => {
    await page.goto(`${base}/product/`);
    await page.waitForSelector(".card.s-act");
    await wait(5000); // board reads
    await page.click('.card[data-id="ok-jman"]');
    await page.waitForSelector("#view-detail:not([hidden])");
    await wait(3500);
    await page.mouse.wheel(0, 260);
    await wait(3200); // alert schedule
    await page.click("#mark-renewed-btn");
    await wait(3200); // calm board
    await page.click('.nav-tab[data-view="ce"]');
    await wait(3000);
    await page.click("#log-ce-btn");
    await wait(3200); // 4/4
    await page.click('.nav-tab[data-view="locker"]');
    await wait(3400); // share link panel
    await page.click('.nav-tab[data-view="rules"]');
    await wait(3600); // rules table with verified chips
    await page.click('.nav-tab[data-view="board"]');
    await wait(4500); // all-good board hold
  });

  await browser.close();
  console.log("All clips recorded to", CLIPS);
})().catch(e => { console.error(e); process.exit(1); });
