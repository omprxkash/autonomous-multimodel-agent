/* Smoke test: exercise every product view + interactions; capture desktop shots. */
const path = require("path");
const { chromium } = require("playwright");
const SHOTS = path.join(__dirname, "..", "..", "record", "shots");

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1366, height: 850 } });
  const errors = [];
  page.on("pageerror", e => errors.push("pageerror: " + e.message));
  page.on("console", m => { if (m.type() === "error") errors.push("console: " + m.text()); });

  await page.goto("http://localhost:8231/product/", { waitUntil: "networkidle" });
  await page.waitForSelector(".card.s-act");
  console.log("summary:", await page.textContent("#board-summary"));
  console.log("pill:", await page.textContent("#standing-pill"));
  await page.screenshot({ path: path.join(SHOTS, "01-product-board.png") });

  // detail of red card
  await page.click('.card[data-id="ok-jman"]');
  await page.waitForSelector("#view-detail:not([hidden])");
  await page.screenshot({ path: path.join(SHOTS, "02-product-detail-act.png") });

  // mark renewed -> board goes calm
  await page.click("#mark-renewed-btn");
  await page.waitForSelector("#view-board:not([hidden])");
  console.log("pill after renew:", await page.textContent("#standing-pill"));
  await page.screenshot({ path: path.join(SHOTS, "03-product-board-after-renew.png") });

  // CE ledger + log hours
  await page.click('.nav-tab[data-view="ce"]');
  await page.click("#log-ce-btn");
  await page.waitForTimeout(800);
  console.log("ce label:", await page.textContent("#ce-label"));
  await page.screenshot({ path: path.join(SHOTS, "04-product-ce-done.png") });

  // locker, alerts, rules
  await page.click('.nav-tab[data-view="locker"]');
  await page.screenshot({ path: path.join(SHOTS, "05-product-locker.png") });
  await page.click('.nav-tab[data-view="alerts"]');
  await page.screenshot({ path: path.join(SHOTS, "06-product-alerts.png") });
  await page.click('.nav-tab[data-view="rules"]');
  await page.screenshot({ path: path.join(SHOTS, "07-product-rules.png") });

  // pill should now be all good?
  await page.click('.nav-tab[data-view="board"]');
  console.log("final pill:", await page.textContent("#standing-pill"));
  console.log("final summary:", await page.textContent("#board-summary"));

  await browser.close();
  if (errors.length) { console.log("ERRORS:\n" + errors.join("\n")); process.exit(1); }
  console.log("smoke OK, no JS errors");
})().catch(e => { console.error(e); process.exit(1); });
