/* Mobile + desktop screenshot verification for the ReconStock site and product.
   Requires the demo server running on :8123 (node _tools/verify/server.js). */
const { chromium } = require(require("path").join(__dirname, "..", "node_modules", "playwright"));
const path = require("path");

const SHOTS = path.join(__dirname, "..", "..", "record", "shots");
const BASE = "http://localhost:8123";

(async () => {
  const browser = await chromium.launch();

  // Mobile: iPhone-class viewport
  const mobile = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
  });
  let page = await mobile.newPage();
  await page.goto(BASE + "/site/", { waitUntil: "networkidle" });
  // sanity: no horizontal overflow on mobile
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  await page.screenshot({ path: path.join(SHOTS, "08-landing-mobile.png"), fullPage: true });
  await page.goto(BASE + "/product/", { waitUntil: "networkidle" });
  await page.screenshot({ path: path.join(SHOTS, "09-product-mobile.png"), fullPage: false });
  await mobile.close();

  // Desktop full-page landing (existing shots are section crops)
  const desktop = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  page = await desktop.newPage();
  await page.goto(BASE + "/site/", { waitUntil: "networkidle" });
  await page.screenshot({ path: path.join(SHOTS, "10-landing-desktop-full.png"), fullPage: true });
  await desktop.close();

  await browser.close();
  console.log("mobile horizontal overflow px:", overflow);
  console.log("saved: 08-landing-mobile.png, 09-product-mobile.png, 10-landing-desktop-full.png");
})();
