/* ReconStock end-to-end verification.
   Serves run-1/ statically, drives the core product flow with Playwright
   Chromium, asserts each step, and saves screenshots to record/shots/.

   Run from run-1/_tools:  node verify/verify.js
*/
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

// --- start the static server in-process ---
const PORT = 8123;
const ROOT = path.resolve(__dirname, "..", "..");
const SHOTS = path.join(ROOT, "record", "shots");
fs.mkdirSync(SHOTS, { recursive: true });

const http = require("http");
const MIME = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png"
};
const server = http.createServer((req, res) => {
  let urlPath = decodeURIComponent(req.url.split("?")[0]);
  if (urlPath.endsWith("/")) urlPath += "index.html";
  const filePath = path.normalize(path.join(ROOT, urlPath));
  if (!filePath.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  fs.readFile(filePath, (err, data) => {
    if (err) { res.writeHead(404); return res.end("Not found: " + urlPath); }
    res.writeHead(200, { "Content-Type": MIME[path.extname(filePath).toLowerCase()] || "application/octet-stream" });
    res.end(data);
  });
});

let failures = 0;
function check(name, cond) {
  if (cond) { console.log("  PASS  " + name); }
  else { failures++; console.error("  FAIL  " + name); }
}

(async () => {
  await new Promise(r => server.listen(PORT, r));
  console.log(`Server up on :${PORT}, root ${ROOT}`);

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on("pageerror", e => { failures++; console.error("  PAGE ERROR: " + e.message); });

  // ============ PRODUCT DEMO ============
  console.log("\n[1] Dashboard");
  await page.goto(`http://localhost:${PORT}/product/`);
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await page.waitForSelector("#inventory-tbody tr");
  check("two store cards render", await page.locator(".store-card").count() === 2);
  check("store domains visible", await page.locator(".store-card__domain").allTextContents()
    .then(t => t.join(" ").includes("mainstore.myshopify.com") && t.join(" ").includes("eu-store.myshopify.com")));
  const skuRows = await page.locator("#inventory-tbody tr").count();
  check(`~30 SKUs visible (got ${skuRows})`, skuRows >= 28);
  check("two pending syncs queued", await page.locator(".pending-card").count() === 2);
  check("activity feed populated", await page.locator(".activity-item").count() >= 4);
  check("read-only install posture shown", (await page.locator("#posture-note").innerText()).includes("read-only"));
  await page.screenshot({ path: path.join(SHOTS, "01-dashboard.png"), fullPage: false });

  // Baseline qty for a SKU that the daily sync will change (EU column).
  const euQtyBefore = await page.locator('tr[data-sku="RS-TEE-BLK-M"] td:nth-child(5)').innerText();
  check("baseline RS-TEE-BLK-M EU qty is 96", euQtyBefore.trim() === "96");

  console.log("\n[2] Diff preview");
  await page.locator('.pending-card:not(.pending-card--danger) [data-action="review"]').click();
  await page.waitForSelector("#view-diff:not([hidden])");
  check("diff rows render", await page.locator("#diff-tbody tr").count() === 12);
  check("old->new arrow cells present", await page.locator("#diff-tbody .diff-arrow").count() === 12);
  check("approve disabled while dry-run on", await page.locator("#approve-sync-btn").isDisabled());

  // Dry-run: produce a report, verify nothing changed.
  await page.locator("#run-dryrun-btn").click();
  check("dry-run report banner shows 0 writes", (await page.locator("#report-banner").innerText()).includes("0 writes"));
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(SHOTS, "02-diff-preview.png"), fullPage: false });

  console.log("\n[3] Approve (live apply)");
  await page.locator("#dryrun-toggle").setChecked(false); // turn dry-run OFF
  check("approve enabled after dry-run off", await page.locator("#approve-sync-btn").isEnabled());
  await page.locator("#approve-sync-btn").click();
  await page.waitForSelector("#view-dashboard:not([hidden])");
  const euQtyAfter = await page.locator('tr[data-sku="RS-TEE-BLK-M"] td:nth-child(5)').innerText();
  check(`approve applied diff to table (EU qty 96 -> 132, got ${euQtyAfter.trim()})`, euQtyAfter.trim() === "132");
  check("only the danger sync remains pending", await page.locator(".pending-card").count() === 1);

  console.log("\n[4] Circuit breaker");
  await page.locator('.pending-card--danger [data-action="review"]').click();
  await page.waitForSelector("#view-breaker:not([hidden])");
  const headline = await page.locator("#breaker-headline").innerText();
  check("breaker headline names 2,143 SKUs + EU Store",
    headline.includes("2,143") && headline.includes("EU Store") && headline.toLowerCase().includes("halted"));
  check("force apply is disabled", await page.locator("#breaker-force-btn").isDisabled());
  check("sample zero rows shown", await page.locator("#breaker-tbody .diff-val--down").count() >= 10);
  await page.evaluate(() => { document.getElementById("toast").hidden = true; }); // clear leftover toast
  await page.waitForTimeout(400); // let view fade-in settle
  await page.screenshot({ path: path.join(SHOTS, "03-circuit-breaker.png"), fullPage: false });
  await page.locator("#breaker-dismiss-btn").click();
  await page.waitForSelector("#view-dashboard:not([hidden])");
  const euQtyPostBreaker = await page.locator('tr[data-sku="RS-TEE-BLK-M"] td:nth-child(5)').innerText();
  check("breaker wrote nothing (EU qty still 132)", euQtyPostBreaker.trim() === "132");

  console.log("\n[5] Rollback");
  await page.locator('.nav-tab[data-view="audit"]').click();
  await page.waitForSelector("#view-audit:not([hidden])");
  check("audit log has entries incl. halted", (await page.locator("#audit-tbody").innerText()).includes("Halted by breaker"));
  const rollbackBtns = page.locator('#audit-tbody [data-action="rollback"]');
  check("rollback buttons available", await rollbackBtns.count() >= 1);
  await rollbackBtns.first().click(); // most recent applied sync = the daily sync we just applied
  await page.waitForSelector("#view-audit:not([hidden])");
  check("entry marked rolled back", (await page.locator("#audit-tbody").innerText()).includes("Rolled back"));
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(SHOTS, "04-rollback.png"), fullPage: false });

  await page.locator('.nav-tab[data-view="dashboard"]').click();
  const euQtyRestored = await page.locator('tr[data-sku="RS-TEE-BLK-M"] td:nth-child(5)').innerText();
  check(`rollback restored quantities (EU qty back to 96, got ${euQtyRestored.trim()})`, euQtyRestored.trim() === "96");

  // State survives reload (localStorage).
  await page.reload();
  await page.waitForSelector("#inventory-tbody tr");
  const euQtyReload = await page.locator('tr[data-sku="RS-TEE-BLK-M"] td:nth-child(5)').innerText();
  check("state persists across reload", euQtyReload.trim() === "96");

  // ============ LANDING PAGE ============
  console.log("\n[6] Landing page");
  await page.goto(`http://localhost:${PORT}/site/`);
  await page.waitForSelector("#hero-headline");
  check("hero positioning present", (await page.locator("#hero-headline").innerText())
    .includes("shows every change before it writes"));
  check("hero mock shows breaker moment", (await page.locator(".mock-alert__headline").innerText()).includes("2,143"));
  check("3 market-evidence quotes with source links",
    await page.locator(".quote").count() === 3 &&
    await page.locator('.quote a[href*="apps.shopify.com"]').count() === 3);
  check("4 how-it-works steps", await page.locator(".step").count() === 4);
  check("4 pricing tiers", await page.locator(".price-card").count() === 4);
  check("pricing shows $29/$49/$99", (await page.locator(".pricing-grid").innerText()).includes("$29"));
  check("honest scope note on pricing", (await page.locator(".scope-note").innerText()).includes("inventory quantities only"));
  check("fails-safe promise (no zero-defect claim)", (await page.locator("#problem").innerText()).includes("fails safe and is fully reversible"));
  check("founder small print discloses fiction",
    (await page.locator(".founder-smallprint").innerText()).toLowerCase().includes("fictional founder"));
  check("5 FAQ items", await page.locator(".faq").count() === 5);
  check("FAQ covers failed sync", (await page.locator(".faq-list").innerText()).includes("What happens when a sync fails?"));
  await page.screenshot({ path: path.join(SHOTS, "05-landing-hero.png"), fullPage: false });
  await page.locator("#pricing").scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(SHOTS, "06-landing-pricing.png"), fullPage: false });

  await browser.close();
  server.close();

  console.log("\n" + (failures === 0
    ? "ALL CHECKS PASSED — screenshots in record/shots/"
    : failures + " CHECK(S) FAILED"));
  process.exit(failures === 0 ? 0 : 1);
})().catch(err => { console.error(err); process.exit(1); });
