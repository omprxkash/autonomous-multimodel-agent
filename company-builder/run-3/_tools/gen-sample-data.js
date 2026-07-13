/* Generate WideTally synthetic sample library (clearly labeled synthetic).
   Files modeled on Amazon's published KDP report schema (see business/format-registry.md)
   and generic store CSV exports. Deterministic seeded PRNG so the demo numbers are stable.
   Output: product/sample-data/*.csv  */
const fs = require("fs");
const path = require("path");
const OUT = path.resolve(__dirname, "..", "product", "sample-data");
fs.mkdirSync(OUT, { recursive: true });

let seed = 20260713;
const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;

const BOOKS = [
  { asin: "B0C1HB101", isbn: "9781736209011", title: "Low Tide at Halloran Bay", series: "Halloran Bay", n: 1, price: 4.99, launch: "2023-05", pop: 1.00 },
  { asin: "B0C1HB102", isbn: "9781736209028", title: "The Lighthouse Ledger", series: "Halloran Bay", n: 2, price: 4.99, launch: "2023-11", pop: 0.85 },
  { asin: "B0C1HB103", isbn: "9781736209035", title: "Squall Line Secrets", series: "Halloran Bay", n: 3, price: 4.99, launch: "2024-06", pop: 0.78 },
  { asin: "B0C1HB104", isbn: "9781736209042", title: "The Driftwood Casket", series: "Halloran Bay", n: 4, price: 5.99, launch: "2025-02", pop: 0.90 },
  { asin: "B0C1HB105", isbn: "9781736209059", title: "Harbor of Lost Things", series: "Halloran Bay", n: 5, price: 5.99, launch: "2025-11", pop: 1.25 },
  { asin: "B0C1IV201", isbn: "9781736209066", title: "Ironvale: The Salt Crown", series: "Ironvale", n: 1, price: 3.99, launch: "2024-09", pop: 0.55 },
  { asin: "B0C1IV202", isbn: "9781736209073", title: "Ironvale: The Ember Court", series: "Ironvale", n: 2, price: 4.99, launch: "2025-05", pop: 0.48 },
  { asin: "B0C1IV203", isbn: "9781736209080", title: "Ironvale: The Hollow King", series: "Ironvale", n: 3, price: 4.99, launch: "2026-03", pop: 0.70 }
];
const MONTHS = [];
for (let y = 2025, m = 7; !(y === 2026 && m === 7); m === 12 ? (m = 1, y++) : m++) MONTHS.push(`${y}-${String(m).padStart(2, "0")}`);

const monthIdx = m => MONTHS.indexOf(m);
const launched = (b, m) => b.launch <= m;
// seasonality: Dec bump, Jan slump, summer flat
const SEASON = { "2025-07": .95, "2025-08": .92, "2025-09": 1.0, "2025-10": 1.05, "2025-11": 1.1, "2025-12": 1.3, "2026-01": .8, "2026-02": .9, "2026-03": 1.0, "2026-04": 1.02, "2026-05": 1.05, "2026-06": 1.0 };
// release spike: big in launch month & next
function spike(b, m) {
  const i = monthIdx(m), li = MONTHS.indexOf(b.launch);
  if (li < 0) return 1;
  if (i === li) return 3.2; if (i === li + 1) return 1.9; if (i === li + 2) return 1.3;
  return 1;
}
const KENP_RATE = { "2025-07": .00459, "2025-08": .00452, "2025-09": .00448, "2025-10": .00446, "2025-11": .00450, "2025-12": .00441, "2026-01": .00455, "2026-02": .00447, "2026-03": .00444, "2026-04": .00449, "2026-05": .00443, "2026-06": .00447 };

// ---------- KDP: modeled on Amazon's published term definitions (fetched; format-registry.md) ----------
// One consolidated CSV (like a Prior Months' Royalties export flattened), monthly rows.
let kdp = "Royalty Date,Title,Author Name,ASIN/ISBN,Marketplace,Royalty Type,Transaction Type,Units Sold,Units Refunded,Net Units Sold,Avg. List Price without tax,Royalty,Currency\n";
let kenp = "Date,Title,Author Name,ASIN,Marketplace,KENP Read\n";
const MARKETS = [["Amazon.com", .72], ["Amazon.co.uk", .13], ["Amazon.com.au", .08], ["Amazon.ca", .07]];
for (const m of MONTHS) for (const b of BOOKS) {
  if (!launched(b, m)) continue;
  const base = 46 * b.pop * SEASON[m] * spike(b, m);
  for (const [mk, share] of MARKETS) {
    const units = Math.max(0, Math.round(base * share * (0.85 + rnd() * .3)));
    if (units === 0 && rnd() < .5) continue;
    const refunds = rnd() < .3 ? Math.min(units, Math.round(units * .015 + rnd())) : 0;
    const net = units - refunds;
    const roy = net * b.price * .7;
    kdp += `${m}-15,"${b.title}",R. E. Halloran,${b.asin},${mk},70%,Standard,${units},${refunds},${net},${b.price.toFixed(2)},${roy.toFixed(2)},USD\n`;
    // KENP: cozy series is in KU (wide for others) — Halloran Bay ebooks are NOT in KU (wide); Ironvale IS in KU
    if (b.series === "Ironvale") {
      const pages = Math.round(base * share * 320 * (0.8 + rnd() * .5));
      if (pages > 0) kenp += `${m}-15,"${b.title}",R. E. Halloran,${b.asin},${mk},${pages}\n`;
    }
  }
  // paperback (Amazon.com only, Halloran Bay only)
  if (b.series === "Halloran Bay") {
    const u = Math.round(base * .12 * (0.7 + rnd() * .6));
    if (u > 0) kdp += `${m}-15,"${b.title} (Paperback)",R. E. Halloran,${b.isbn},Amazon.com,60%,Standard,${u},0,${u},12.99,${(u * 3.61).toFixed(2)},USD\n`;
  }
}
fs.writeFileSync(path.join(OUT, "kdp-royalties-jul2025-jun2026.csv"), kdp);
fs.writeFileSync(path.join(OUT, "kdp-kenp-read-jul2025-jun2026.csv"), kenp);

// ---------- Draft2Digital (distributes to Apple, B&N, etc.) ----------
let d2d = "Sale Date,Store,Title,Author,ISBN,Units Sold,List Price,Author Earnings,Currency\n";
const D2DSTORES = [["Apple Books", .48], ["Barnes & Noble", .3], ["OverDrive (Libraries)", .14], ["Scribd", .08]];
for (const m of MONTHS) for (const b of BOOKS) {
  if (!launched(b, m) || b.series !== "Halloran Bay") continue; // wide series only
  const base = 17 * b.pop * SEASON[m] * spike(b, m);
  for (const [st, share] of D2DSTORES) {
    const units = Math.max(0, Math.round(base * share * (0.8 + rnd() * .4)));
    if (!units) continue;
    const earn = units * b.price * .60; // ~60% after store + D2D's ~10% commission (verified ~10%, faq fetched)
    d2d += `${m}-28,${st},"${b.title}",R. E. Halloran,${b.isbn},${units},${b.price.toFixed(2)},${earn.toFixed(2)},USD\n`;
  }
}
fs.writeFileSync(path.join(OUT, "d2d-sales-jul2025-jun2026.csv"), d2d);

// ---------- Kobo Writing Life ----------
let kobo = "Period,Title,ISBN,Country,Units,List Price,Payable Amount,Currency\n";
const KCOUNTRIES = [["US", .35], ["CA", .3], ["AU", .2], ["NZ", .15]];
for (const m of MONTHS) for (const b of BOOKS) {
  if (!launched(b, m) || b.series !== "Halloran Bay") continue;
  const base = 11 * b.pop * SEASON[m] * spike(b, m);
  for (const [c, share] of KCOUNTRIES) {
    const units = Math.max(0, Math.round(base * share * (0.75 + rnd() * .5)));
    if (!units) continue;
    kobo += `${m},"${b.title}",${b.isbn},${c},${units},${b.price.toFixed(2)},${(units * b.price * .7).toFixed(2)},USD\n`;
  }
}
fs.writeFileSync(path.join(OUT, "kobo-sales-jul2025-jun2026.csv"), kobo);

// ---------- Amazon Ads (Sponsored Products campaign report) ----------
let ads = "Start Date,End Date,Campaign Name,ASIN,Impressions,Clicks,Spend,14 Day Total Sales,ACOS,Currency\n";
const CAMPS = [
  { asin: "B0C1HB101", name: "HB1 Auto - US", cpc: .42, ctr: .0042, cvr: .13 },    // wide starter: roughly break-even on direct royalty
  { asin: "B0C1HB105", name: "HB5 Launch - US", cpc: .55, ctr: .0051, cvr: .23 },  // strong launch: clearly earning
  { asin: "B0C1IV201", name: "Ironvale 1 Auto - US", cpc: .48, ctr: .0031, cvr: .055 }, // looks bad on ACOS; KU read-through caveat
  { asin: "B0C1IV203", name: "IV3 Launch - US", cpc: .61, ctr: .0038, cvr: .06 }
];
for (const m of MONTHS) for (const c of CAMPS) {
  const b = BOOKS.find(x => x.asin === c.asin);
  if (!launched(b, m)) continue;
  const budget = (c.name.includes("Launch") ? (spike(b, m) > 1.2 ? 260 : 90) : 120) * SEASON[m];
  const spend = budget * (0.82 + rnd() * .3);
  const clicks = Math.round(spend / c.cpc);
  const imps = Math.round(clicks / c.ctr);
  const orders = Math.round(clicks * c.cvr * (0.85 + rnd() * .3));
  const sales = orders * b.price;
  const acos = sales > 0 ? (spend / sales * 100) : 0;
  ads += `${m}-01,${m}-28,"${c.name}",${c.asin},${imps},${clicks},${spend.toFixed(2)},${sales.toFixed(2)},${acos.toFixed(1)}%,USD\n`;
}
fs.writeFileSync(path.join(OUT, "amazon-ads-campaigns-jul2025-jun2026.csv"), ads);

// ---------- README for the folder ----------
fs.writeFileSync(path.join(OUT, "README.txt"),
`WideTally sample library — SYNTHETIC DATA
These files describe a fictional author ("R. E. Halloran") and were generated
by _tools/gen-sample-data.js for demo purposes. Column layouts are modeled on
each platform's published/exported report structure (see business/format-registry.md
for what was verified against primary sources vs. practitioner knowledge).
No real sales data is included. Drag these files into the WideTally demo.
`);
console.log("Wrote sample data:", fs.readdirSync(OUT).join(", "));
