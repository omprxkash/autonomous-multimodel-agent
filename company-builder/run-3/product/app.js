/* WideTally demo app — all parsing local, no network after page load (sample library is fetched
   from the same local static server, then parsed through the identical code path as dropped files). */
"use strict";

/* ---------------- format registry (header fingerprints) ---------------- */
const FORMATS = [
  { id: "kdp-royalty", label: "KDP Sales & Royalties", sig: ["Royalty Date", "ASIN/ISBN", "Net Units Sold"] },
  { id: "kdp-kenp", label: "KDP KENP Read", sig: ["KENP Read", "ASIN"] },
  { id: "d2d", label: "Draft2Digital sales", sig: ["Sale Date", "Store", "Author Earnings"] },
  { id: "kobo", label: "Kobo Writing Life", sig: ["Period", "Payable Amount"] },
  { id: "amazon-ads", label: "Amazon Ads campaigns", sig: ["Campaign Name", "ACOS"] }
];
/* KDP Select per-page rates (demo table; real app ships monthly updates). Months not listed use DEFAULT_RATE and are flagged est. */
const KENP_RATE = { "2025-07": .00459, "2025-08": .00452, "2025-09": .00448, "2025-10": .00446, "2025-11": .00450, "2025-12": .00441, "2026-01": .00455, "2026-02": .00447, "2026-03": .00444, "2026-04": .00449, "2026-05": .00443, "2026-06": .00447 };
const DEFAULT_RATE = 0.0045;

const PLATFORMS = [
  { id: "amazon", label: "Amazon", color: "#2E6EB5" },
  { id: "d2d", label: "Draft2Digital", color: "#B8862D" },
  { id: "ku", label: "Kindle Unlimited", color: "#6B5CA5" },
  { id: "kobo", label: "Kobo", color: "#0B9377" }
];
const PCOLOR = Object.fromEntries(PLATFORMS.map(p => [p.id, p.color]));
const PLABEL = Object.fromEntries(PLATFORMS.map(p => [p.id, p.label]));

/* ---------------- state ---------------- */
const S = { tx: [], ads: [], files: [], titleAsin: {} };

/* ---------------- CSV parsing ---------------- */
function parseCSV(text) {
  const rows = []; let row = [], cell = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += c; }
    else if (c === '"') q = true;
    else if (c === ",") { row.push(cell); cell = ""; }
    else if (c === "\n" || c === "\r") { if (cell !== "" || row.length) { row.push(cell); rows.push(row); row = []; cell = ""; } }
    else cell += c;
  }
  if (cell !== "" || row.length) { row.push(cell); rows.push(row); }
  return rows;
}
function detectFormat(header) {
  const h = header.join(",");
  return FORMATS.find(f => f.sig.every(s => h.includes(s))) || null;
}
const month = s => (s || "").slice(0, 7);
const num = s => parseFloat(String(s).replace(/[%$,]/g, "")) || 0;
const baseTitle = t => t.replace(/\s*\(Paperback\)\s*$/i, "");
function seriesOf(title) {
  const t = baseTitle(title);
  const m = t.match(/^(.+?):\s/); if (m) return m[1];
  const KNOWN = ["Low Tide at Halloran Bay", "The Lighthouse Ledger", "Squall Line Secrets", "The Driftwood Casket", "Harbor of Lost Things"];
  return KNOWN.includes(t) ? "Halloran Bay" : "Standalone";
}

function ingest(name, text) {
  const rows = parseCSV(text).filter(r => r.length > 1);
  if (!rows.length) return { name, format: "empty file", rows: 0, ok: false };
  const fmt = detectFormat(rows[0]);
  if (!fmt) return { name, format: "unrecognized header", rows: rows.length - 1, ok: false };
  const H = rows[0], idx = k => H.findIndex(h => h.trim() === k);
  let n = 0;
  if (fmt.id === "kdp-royalty") {
    const [d, t, a, mk, u, r] = [idx("Royalty Date"), idx("Title"), idx("ASIN/ISBN"), idx("Marketplace"), idx("Net Units Sold"), idx("Royalty")];
    for (const row of rows.slice(1)) {
      const title = baseTitle(row[t]);
      S.tx.push({ month: month(row[d]), platform: "amazon", store: row[mk], title, units: num(row[u]), usd: num(row[r]) });
      if (row[a] && row[a].startsWith("B0")) S.titleAsin[row[a]] = title;
      n++;
    }
  } else if (fmt.id === "kdp-kenp") {
    const [d, t, a, mk, p] = [idx("Date"), idx("Title"), idx("ASIN"), idx("Marketplace"), idx("KENP Read")];
    for (const row of rows.slice(1)) {
      const m = month(row[d]); const rate = KENP_RATE[m] || DEFAULT_RATE;
      S.tx.push({ month: m, platform: "ku", store: row[mk], title: baseTitle(row[t]), units: 0, pages: num(row[p]), usd: num(row[p]) * rate, est: true, rateKnown: m in KENP_RATE });
      if (row[a]) S.titleAsin[row[a]] = baseTitle(row[t]);
      n++;
    }
  } else if (fmt.id === "d2d") {
    const [d, st, t, u, e] = [idx("Sale Date"), idx("Store"), idx("Title"), idx("Units Sold"), idx("Author Earnings")];
    for (const row of rows.slice(1)) { S.tx.push({ month: month(row[d]), platform: "d2d", store: row[st], title: baseTitle(row[t]), units: num(row[u]), usd: num(row[e]) }); n++; }
  } else if (fmt.id === "kobo") {
    const [d, t, u, p] = [idx("Period"), idx("Title"), idx("Units"), idx("Payable Amount")];
    for (const row of rows.slice(1)) { S.tx.push({ month: month(row[d]), platform: "kobo", store: "Kobo " + (row[idx("Country")] || ""), title: baseTitle(row[t]), units: num(row[u]), usd: num(row[p]) }); n++; }
  } else if (fmt.id === "amazon-ads") {
    const [d, c, a, im, cl, sp, sa] = [idx("Start Date"), idx("Campaign Name"), idx("ASIN"), idx("Impressions"), idx("Clicks"), idx("Spend"), idx("14 Day Total Sales")];
    for (const row of rows.slice(1)) { S.ads.push({ month: month(row[d]), name: row[c], asin: row[a], imps: num(row[im]), clicks: num(row[cl]), spend: num(row[sp]), sales: num(row[sa]) }); n++; }
  }
  return { name, format: fmt.label, rows: n, ok: true };
}

/* ---------------- helpers ---------------- */
const fmtUSD = (v, dp = 0) => (v < 0 ? "−$" : "$") + Math.abs(v).toLocaleString("en-US", { minimumFractionDigits: dp, maximumFractionDigits: dp });
const monthsOf = () => [...new Set(S.tx.map(t => t.month))].sort();
const last12 = () => monthsOf().slice(-12);
const MSHORT = m => ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][+m.slice(5)] + (m.slice(5) === "01" || m === monthsOf()[0] ? " ’" + m.slice(2, 4) : "");
const sum = a => a.reduce((s, x) => s + x, 0);

/* ---------------- views ---------------- */
function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;"); }
const $ = s => document.querySelector(s);

function renderAll() {
  const has = S.tx.length > 0, hasAds = S.ads.length > 0;
  for (const v of ["ledger", "books"]) {
    $(`#view-${v} [data-empty]`).hidden = has; const f = $(`#view-${v} [data-full]`); if (f) f.hidden = !has;
  }
  $("#view-ads [data-empty]").hidden = hasAds; $("#view-ads [data-full]").hidden = !hasAds;
  $("#import-count").hidden = !S.files.length;
  $("#import-count").textContent = S.files.length;
  $("#reset-btn").hidden = !S.files.length;
  $("#imports-card").hidden = !S.files.length;
  renderImports();
  if (has) { renderStats(); renderChart(); renderPlatformTable(); renderBooks(); }
  if (hasAds) renderAds();
}

function renderStats() {
  const L12 = last12(), cur = L12[L12.length - 1], prev = L12[L12.length - 2];
  const inMonth = m => sum(S.tx.filter(t => t.month === m).map(t => t.usd));
  const t12 = sum(S.tx.filter(t => L12.includes(t.month)).map(t => t.usd));
  const adSpend = sum(S.ads.filter(a => L12.includes(a.month)).map(a => a.spend));
  const curV = inMonth(cur), prevV = inMonth(prev || cur);
  const d = prevV ? (curV - prevV) / prevV * 100 : 0;
  $("#stat-row").innerHTML = `
    <div class="stat"><div class="label">Trailing 12 mo royalties</div><div class="value">${fmtUSD(t12)}</div><div class="delta">across ${PLATFORMS.filter(p => S.tx.some(t => t.platform === p.id)).length} platforms</div></div>
    <div class="stat"><div class="label">${MSHORT(cur)} royalties</div><div class="value">${fmtUSD(curV)}</div><div class="delta ${d >= 0 ? "up" : "down"}">${d >= 0 ? "▲" : "▼"} ${Math.abs(d).toFixed(0)}% vs ${MSHORT(prev || cur)}</div></div>
    <div class="stat"><div class="label">Ad spend, 12 mo</div><div class="value">${fmtUSD(adSpend)}</div><div class="delta">${S.ads.length ? S.ads.filter(a => L12.includes(a.month)).length + " campaign-months" : "no ads file imported"}</div></div>
    <div class="stat"><div class="label">Net after ads, 12 mo</div><div class="value">${fmtUSD(t12 - adSpend)}</div><div class="delta ${t12 - adSpend >= 0 ? "up" : "down"}">royalties − ad spend</div></div>`;
}

/* stacked monthly bar chart, hand-rolled SVG per dataviz spec */
function renderChart() {
  const L12 = last12();
  const byMP = {}; let maxTotal = 0;
  for (const m of L12) {
    byMP[m] = {};
    for (const p of PLATFORMS) byMP[m][p.id] = sum(S.tx.filter(t => t.month === m && t.platform === p.id).map(t => t.usd));
    maxTotal = Math.max(maxTotal, sum(Object.values(byMP[m])));
  }
  const W = 1000, H = 300, padL = 56, padB = 34, padT = 18, padR = 8;
  const iw = W - padL - padR, ih = H - padT - padB;
  const step = iw / L12.length, bw = Math.min(54, step * .62);
  const yMax = Math.ceil(maxTotal / 500) * 500 || 500;
  const y = v => padT + ih - v / yMax * ih;
  let g = "";
  const ticks = 4;
  for (let i = 0; i <= ticks; i++) {
    const v = yMax / ticks * i;
    g += `<line x1="${padL}" x2="${W - padR}" y1="${y(v)}" y2="${y(v)}" stroke="#E5DCC9" stroke-width="1"/>
          <text x="${padL - 8}" y="${y(v) + 4}" text-anchor="end" font-size="11" fill="#5B6B7C" style="font-variant-numeric:tabular-nums">${v >= 1000 ? (v / 1000) + "k" : v}</text>`;
  }
  const bars = [];
  L12.forEach((m, i) => {
    const x = padL + step * i + (step - bw) / 2;
    let acc = 0; const total = sum(Object.values(byMP[m]));
    for (const p of PLATFORMS) {
      const v = byMP[m][p.id]; if (v <= 0) continue;
      const y1 = y(acc + v), h = y(acc) - y(acc + v);
      bars.push(`<rect data-m="${m}" x="${x}" y="${y1}" width="${bw}" height="${Math.max(h, 0)}" fill="${p.color}" stroke="#FAF6EF" stroke-width="1" ${acc === 0 ? `rx="0"` : ""} ${acc + v >= total - .01 ? `rx="3"` : ""}/>`);
      acc += v;
    }
    // selective direct labels: last month and the max month only
    const isMax = total === Math.max(...L12.map(mm => sum(Object.values(byMP[mm]))));
    if (i === L12.length - 1 || isMax) bars.push(`<text x="${x + bw / 2}" y="${y(total) - 6}" text-anchor="middle" font-size="11.5" fill="#16324F" style="font-variant-numeric:tabular-nums">${fmtUSD(total)}</text>`);
    g += `<text x="${x + bw / 2}" y="${H - 12}" text-anchor="middle" font-size="11" fill="#5B6B7C">${MSHORT(m)}</text>`;
    // invisible hover target column
    bars.push(`<rect class="hover-col" data-m="${m}" x="${padL + step * i}" y="${padT}" width="${step}" height="${ih}" fill="transparent"/>`);
  });
  const svg = $("#chart-monthly");
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.innerHTML = g + bars.join("");
  $("#chart-legend").innerHTML = PLATFORMS.filter(p => S.tx.some(t => t.platform === p.id))
    .map(p => `<span class="key"><span class="swatch" style="background:${p.color}"></span>${p.label}</span>`).join("");
  // tooltip
  const tip = $("#tooltip");
  svg.onmousemove = e => {
    const el = e.target.closest("[data-m]"); if (!el) { tip.hidden = true; return; }
    const m = el.dataset.m;
    const rows = PLATFORMS.filter(p => byMP[m][p.id] > 0)
      .map(p => `<div class="t-row"><span><span class="sw" style="background:${p.color}"></span>${p.label}</span><b>${fmtUSD(byMP[m][p.id])}</b></div>`).join("");
    tip.innerHTML = `<div class="t-title">${MSHORT(m)} — ${fmtUSD(sum(Object.values(byMP[m])))}</div>${rows}`;
    tip.hidden = false;
    tip.style.left = Math.min(e.clientX + 14, innerWidth - 280) + "px";
    tip.style.top = (e.clientY + 14) + "px";
  };
  svg.onmouseleave = () => tip.hidden = true;
}

function spark(vals, w = 110, h = 26, color = "#16324F") {
  const mx = Math.max(...vals, 1), mn = Math.min(...vals, 0);
  const pts = vals.map((v, i) => `${(i / (vals.length - 1) * (w - 6) + 3).toFixed(1)},${(h - 3 - (v - mn) / (mx - mn || 1) * (h - 8)).toFixed(1)}`);
  const last = pts[pts.length - 1].split(",");
  return `<svg width="${w}" height="${h}" aria-hidden="true"><polyline points="${pts.join(" ")}" fill="none" stroke="${color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/><circle cx="${last[0]}" cy="${last[1]}" r="3" fill="#B8862D"/></svg>`;
}

function renderPlatformTable() {
  const L12 = last12();
  const rows = PLATFORMS.map(p => {
    const monthly = L12.map(m => sum(S.tx.filter(t => t.month === m && t.platform === p.id).map(t => t.usd)));
    const total = sum(monthly);
    if (!total) return "";
    const units = sum(S.tx.filter(t => L12.includes(t.month) && t.platform === p.id).map(t => t.units));
    return `<tr><td><span class="swatch" style="background:${p.color};display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:8px"></span>${p.label}${p.id === "ku" ? ' <span class="est">est.</span>' : ""}</td>
      <td class="num">${p.id === "ku" ? Math.round(sum(S.tx.filter(t => L12.includes(t.month) && t.platform === "ku").map(t => t.pages || 0))).toLocaleString() + " pages" : units.toLocaleString() + " units"}</td>
      <td class="num">${fmtUSD(total, 2)}</td>
      <td class="num">${(total / sum(L12.map(m => sum(S.tx.filter(t => t.month === m).map(t => t.usd)))) * 100).toFixed(0)}%</td>
      <td class="num hide-mobile">${spark(monthly)}</td></tr>`;
  }).join("");
  $("#platform-table").innerHTML = `<thead><tr><th>Platform</th><th class="num">Volume</th><th class="num">Royalties</th><th class="num">Share</th><th class="num hide-mobile">12-mo trend</th></tr></thead><tbody>${rows}</tbody>`;
}

function renderBooks() {
  const L12 = last12();
  const books = {};
  for (const t of S.tx.filter(t => L12.includes(t.month))) {
    const b = books[t.title] || (books[t.title] = { title: t.title, series: seriesOf(t.title), plat: {}, monthly: Array(L12.length).fill(0) });
    b.plat[t.platform] = (b.plat[t.platform] || 0) + t.usd;
    b.monthly[L12.indexOf(t.month)] += t.usd;
  }
  // ad spend per title via ASIN map
  const adByTitle = {};
  for (const a of S.ads.filter(a => L12.includes(a.month))) {
    const title = S.titleAsin[a.asin]; if (!title) continue;
    adByTitle[title] = (adByTitle[title] || 0) + a.spend;
  }
  const bySeries = {};
  for (const b of Object.values(books)) (bySeries[b.series] = bySeries[b.series] || []).push(b);
  let html = `<thead><tr><th>Book</th>${PLATFORMS.map(p => `<th class="num hide-mobile">${p.label.replace("Kindle Unlimited", "KU")}</th>`).join("")}<th class="num">Total</th><th class="num">Ads</th><th class="num">Net</th><th class="num hide-mobile">Trend</th></tr></thead><tbody>`;
  for (const [series, list] of Object.entries(bySeries).sort((a, b) => sum(b[1].map(x => sum(Object.values(x.plat)))) - sum(a[1].map(x => sum(Object.values(x.plat)))))) {
    list.sort((a, b) => sum(Object.values(b.plat)) - sum(Object.values(a.plat)));
    const sTotal = sum(list.map(b => sum(Object.values(b.plat))));
    const sAds = sum(list.map(b => adByTitle[b.title] || 0));
    html += `<tr class="series-row"><td>${esc(series)} <span class="sub">(${list.length} book${list.length > 1 ? "s" : ""})</span></td>${PLATFORMS.map(p => `<td class="num hide-mobile">${fmtUSD(sum(list.map(b => b.plat[p.id] || 0)))}</td>`).join("")}<td class="num">${fmtUSD(sTotal)}</td><td class="num">${sAds ? fmtUSD(-sAds) : "—"}</td><td class="num ${sTotal - sAds >= 0 ? "money-pos" : "money-neg"}">${fmtUSD(sTotal - sAds)}</td><td class="hide-mobile"></td></tr>`;
    for (const b of list) {
      const total = sum(Object.values(b.plat)), ads = adByTitle[b.title] || 0;
      html += `<tr><td class="book-title" style="padding-left:26px">${esc(b.title)}</td>
        ${PLATFORMS.map(p => `<td class="num hide-mobile">${b.plat[p.id] ? fmtUSD(b.plat[p.id]) : '<span class="sub">—</span>'}</td>`).join("")}
        <td class="num">${fmtUSD(total)}</td><td class="num">${ads ? fmtUSD(-ads) : '<span class="sub">—</span>'}</td>
        <td class="num ${total - ads >= 0 ? "money-pos" : "money-neg"}">${fmtUSD(total - ads)}</td>
        <td class="num hide-mobile">${spark(b.monthly, 90, 22)}</td></tr>`;
    }
  }
  $("#books-table").innerHTML = html + "</tbody>";
}

function renderAds() {
  const L12 = last12().length ? last12() : [...new Set(S.ads.map(a => a.month))].sort().slice(-12);
  const camps = {};
  for (const a of S.ads.filter(a => L12.includes(a.month))) {
    const c = camps[a.name] || (camps[a.name] = { name: a.name, asin: a.asin, spend: 0, sales: 0, clicks: 0 });
    c.spend += a.spend; c.sales += a.sales; c.clicks += a.clicks;
  }
  const kuTitles = new Set(S.tx.filter(t => t.platform === "ku").map(t => t.title));
  let anyKU = false;
  const rows = Object.values(camps).sort((a, b) => b.spend - a.spend).map(c => {
    const title = S.titleAsin[c.asin] || c.asin;
    const acos = c.sales ? c.spend / c.sales * 100 : 0;
    const royalty = c.sales * .7;               // ebook 70% royalty on attributed sales (est.)
    const net = royalty - c.spend;
    const inKU = kuTitles.has(title); if (inKU) anyKU = true;
    const verdict = net > 15 ? `<span class="badge good">earning</span>` : net > -15 ? `<span class="badge warn">break-even</span>` : `<span class="badge bad">losing</span>`;
    return `<tr><td><div class="book-title">${esc(c.name)}</div><div class="sub">${esc(title)}${inKU ? " · in KU†" : ""}</div></td>
      <td class="num">${fmtUSD(c.spend, 2)}</td>
      <td class="num hide-mobile">${fmtUSD(c.sales, 2)}</td>
      <td class="num hide-mobile">${acos.toFixed(0)}%</td>
      <td class="num">${fmtUSD(royalty, 2)}<span class="est">est.</span></td>
      <td class="num ${net >= 0 ? "money-pos" : "money-neg"}">${fmtUSD(net, 2)}</td>
      <td>${verdict}</td></tr>`;
  }).join("");
  $("#ads-table").innerHTML = `<thead><tr><th>Campaign</th><th class="num">Spend</th><th class="num hide-mobile">Amazon “sales”</th><th class="num hide-mobile">ACOS</th><th class="num">Your royalty</th><th class="num">True net</th><th>Verdict</th></tr></thead><tbody>${rows}</tbody>`;
  $("#ads-footnote").textContent = "Royalty estimated at 70% of attributed sales (ebook rate, before delivery fees)." + (anyKU ? " † Books in Kindle Unlimited also earn unattributed page reads — Amazon's report can't see them, so a 'losing' verdict on a KU series starter may still be profitable via read-through. WideTally shows both numbers instead of hiding the gap." : "");
}

function renderImports() {
  if (!S.files.length) { $("#imports-table").innerHTML = ""; return; }
  $("#imports-table").innerHTML = `<thead><tr><th>File</th><th>Detected format</th><th class="num">Rows</th><th>Status</th></tr></thead><tbody>` +
    S.files.map(f => `<tr><td>${esc(f.name)}</td><td>${esc(f.format)}</td><td class="num">${f.rows.toLocaleString()}</td><td>${f.ok ? '<span class="badge good">parsed</span>' : '<span class="badge bad">skipped</span>'}</td></tr>`).join("") + "</tbody>";
}

/* ---------------- wiring ---------------- */
document.querySelectorAll(".tab").forEach(b => b.onclick = () => {
  document.querySelectorAll(".tab").forEach(x => x.classList.toggle("active", x === b));
  document.querySelectorAll(".view").forEach(v => v.hidden = v.id !== "view-" + b.dataset.view);
});
function addFiles(fileList) {
  const arr = [...fileList];
  let pending = arr.length;
  for (const f of arr) {
    const r = new FileReader();
    r.onload = () => { S.files.push(ingest(f.name, r.result)); if (--pending === 0) renderAll(); };
    r.readAsText(f);
  }
}
$("#file-input").onchange = e => addFiles(e.target.files);
const dz = $("#dropzone");
["dragenter", "dragover"].forEach(ev => dz.addEventListener(ev, e => { e.preventDefault(); dz.classList.add("drag"); }));
["dragleave", "drop"].forEach(ev => dz.addEventListener(ev, e => { e.preventDefault(); dz.classList.remove("drag"); }));
dz.addEventListener("drop", e => addFiles(e.dataTransfer.files));

const SAMPLES = ["kdp-royalties-jul2025-jun2026.csv", "kdp-kenp-read-jul2025-jun2026.csv", "d2d-sales-jul2025-jun2026.csv", "kobo-sales-jul2025-jun2026.csv", "amazon-ads-campaigns-jul2025-jun2026.csv"];
async function loadSamples() {
  for (const s of SAMPLES) {
    try { const t = await (await fetch("sample-data/" + s)).text(); S.files.push(ingest(s + " (sample)", t)); }
    catch (e) { S.files.push({ name: s, format: "fetch failed (open via local server)", rows: 0, ok: false }); }
  }
  renderAll();
}
document.querySelectorAll('[data-action="load-samples"]').forEach(b => b.onclick = loadSamples);
document.querySelectorAll('[data-action="reset"]').forEach(b => b.onclick = () => { S.tx = []; S.ads = []; S.files = []; S.titleAsin = {}; renderAll(); });
renderAll();
