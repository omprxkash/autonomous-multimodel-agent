/* ReconStock demo — application logic.
   No framework, no build step. State lives in memory + localStorage.
   Every mutation is explicit and reversible, mirroring the product's
   own "preview -> apply -> journal -> rollback" promise.
*/

(function () {
  "use strict";

  const STORAGE_KEY = "reconstock_state_v1";
  const STORE_LABEL = { main: "US Main Store", eu: "EU Store" };

  // ---------- state ----------
  let state = null;
  let activeDiffSyncId = null;

  function cloneSeed() {
    const seed = JSON.parse(JSON.stringify(SEED));
    return {
      stores: seed.stores,
      inventory: seed.skus,
      pendingSyncs: seed.pendingSyncs,
      auditLog: seed.auditLog.map(a => Object.assign({ rolledBack: false, rolledBackAt: null }, a)),
      activity: seed.activity
    };
  }

  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed && Array.isArray(parsed.inventory) && Array.isArray(parsed.pendingSyncs)) {
          return parsed;
        }
      }
    } catch (e) { /* fall through to fresh seed */ }
    return cloneSeed();
  }

  function saveState() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  // ---------- helpers ----------
  function findSku(sku) {
    return state.inventory.find(r => r.sku === sku);
  }
  function findPending(id) {
    return state.pendingSyncs.find(s => s.id === id);
  }
  function fmtNum(n) {
    return Number(n).toLocaleString("en-US");
  }
  function fmtDate(iso) {
    const d = new Date(iso);
    return new Intl.DateTimeFormat("en-US", {
      month: "short", day: "numeric", hour: "numeric", minute: "2-digit"
    }).format(d);
  }
  function nowIso() {
    return new Date().toISOString();
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }
  function toast(msg, kind) {
    const el = document.getElementById("toast");
    el.textContent = msg;
    el.className = "toast toast--show" + (kind ? " toast--" + kind : "");
    el.hidden = false;
    clearTimeout(toast._t);
    toast._t = setTimeout(() => { el.hidden = true; }, 3600);
  }
  function csvDownload(filename, rows) {
    const csv = rows.map(r => r.map(c => {
      const v = String(c == null ? "" : c);
      return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
    }).join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  let flashSkus = new Set();
  function flash(skus) {
    flashSkus = new Set(skus);
    setTimeout(() => { flashSkus.clear(); renderInventory(); }, 2200);
  }

  // ---------- view switching ----------
  function switchView(name) {
    document.querySelectorAll(".view").forEach(v => v.hidden = true);
    document.getElementById("view-" + name).hidden = false;
    document.querySelectorAll(".nav-tab").forEach(t => {
      t.classList.toggle("is-active", t.dataset.view === name);
    });
    window.scrollTo({ top: 0, behavior: "instant" in window ? "instant" : "auto" });
  }

  // ---------- render: stores ----------
  function renderStores() {
    const wrap = document.querySelector(".stores-row");
    wrap.innerHTML = state.stores.map(s => `
      <div class="store-card">
        <div class="store-card__top">
          <span class="dot dot--${s.connected ? "on" : "off"}"></span>
          <span class="store-card__domain mono">${esc(s.domain)}</span>
        </div>
        <div class="store-card__label">${esc(s.label)} &middot; ${esc(s.region)}</div>
        <div class="store-card__meta">
          <span>${esc(s.plan)}</span>
          <span>Last sync ${fmtDate(s.lastSync)}</span>
        </div>
      </div>
    `).join("");
  }

  // ---------- render: pending syncs ----------
  function renderPending() {
    const wrap = document.getElementById("pending-list");
    if (state.pendingSyncs.length === 0) {
      wrap.innerHTML = `<p class="empty-state">No syncs waiting on review. New syncs will queue here before anything is written.</p>`;
      return;
    }
    wrap.innerHTML = state.pendingSyncs.map(s => {
      if (s.kind === "danger") {
        return `
        <div class="pending-card pending-card--danger" data-sync="${esc(s.id)}">
          <div class="pending-card__badge badge badge--amber">Flagged &middot; pre-write check required</div>
          <div class="pending-card__title">${esc(s.title)}</div>
          <div class="pending-card__sub">${esc(s.subtitle)}</div>
          <div class="pending-card__meta">${esc(s.source)} &middot; queued ${fmtDate(s.queuedAt)}</div>
          <button class="btn btn--primary btn--sm" data-action="review" data-id="${esc(s.id)}" type="button">Review sync</button>
        </div>`;
      }
      return `
        <div class="pending-card" data-sync="${esc(s.id)}">
          <div class="pending-card__badge badge badge--navy">Awaiting review</div>
          <div class="pending-card__title">${esc(s.title)}</div>
          <div class="pending-card__sub">${esc(s.subtitle)}</div>
          <div class="pending-card__meta">${s.diffs.length} proposed changes &middot; queued ${fmtDate(s.queuedAt)}</div>
          <button class="btn btn--secondary btn--sm" data-action="review" data-id="${esc(s.id)}" type="button">Review diff</button>
        </div>`;
    }).join("");

    wrap.querySelectorAll('[data-action="review"]').forEach(btn => {
      btn.addEventListener("click", () => openReview(btn.dataset.id));
    });
  }

  // ---------- render: inventory table ----------
  function renderInventory() {
    const tbody = document.getElementById("inventory-tbody");
    const q = (document.getElementById("inventory-search").value || "").trim().toLowerCase();
    const rows = state.inventory.filter(r =>
      !q || r.sku.toLowerCase().includes(q) || r.product.toLowerCase().includes(q) || r.category.toLowerCase().includes(q)
    );
    tbody.innerHTML = rows.map(r => {
      const changed = flashSkus.has(r.sku);
      return `
      <tr class="${changed ? "row-flash" : ""}" data-sku="${esc(r.sku)}">
        <td class="mono">${esc(r.sku)}</td>
        <td>${esc(r.product)} <span class="muted">— ${esc(r.variant)}</span></td>
        <td>${esc(r.category)}</td>
        <td class="num mono">${fmtNum(r.main)}</td>
        <td class="num mono">${fmtNum(r.eu)}</td>
        <td class="num mono">${fmtNum(r.main + r.eu)}</td>
      </tr>`;
    }).join("") || `<tr><td colspan="6" class="empty-state">No SKUs match "${esc(q)}".</td></tr>`;
  }

  // ---------- render: activity ----------
  function renderActivity() {
    const list = document.getElementById("activity-list");
    const items = [...state.activity].sort((a, b) => new Date(b.at) - new Date(a.at));
    list.innerHTML = items.map(a => `
      <li class="activity-item activity-item--${a.type}">
        <span class="activity-item__dot"></span>
        <div>
          <p class="activity-item__text">${esc(a.text)}</p>
          <p class="activity-item__time">${fmtDate(a.at)}</p>
        </div>
      </li>
    `).join("");
  }

  function addActivity(text, type) {
    state.activity.unshift({ id: "act-" + Date.now(), at: nowIso(), type: type || "info", text });
  }

  // ---------- diff row rendering (shared by diff + breaker views) ----------
  function diffRowHtml(d) {
    const row = findSku(d.sku);
    const product = row ? row.product + " — " + row.variant : d.sku;
    const dir = d.newQty === d.oldQty ? "flat" : (d.newQty > d.oldQty ? "up" : "down");
    return `
      <tr>
        <td class="mono">${esc(d.sku)}</td>
        <td>${esc(product)}</td>
        <td>${esc(STORE_LABEL[d.store] || d.store)}</td>
        <td class="num mono">${fmtNum(d.oldQty)}</td>
        <td class="num diff-arrow diff-arrow--${dir}">&rarr;</td>
        <td class="num mono diff-val diff-val--${dir}">${fmtNum(d.newQty)}</td>
        <td class="muted">${esc(d.source)}</td>
      </tr>`;
  }

  // ---------- diff preview view ----------
  function openReview(id) {
    const sync = findPending(id);
    if (!sync) return;

    if (sync.kind === "danger") {
      openBreaker(sync);
      return;
    }

    activeDiffSyncId = id;
    document.getElementById("diff-title").textContent = sync.title;
    document.getElementById("diff-subtitle").textContent = sync.subtitle + " · " + sync.source;
    document.getElementById("diff-count-sub").textContent =
      sync.diffs.length + " SKUs proposed to change on " + (STORE_LABEL[sync.diffs[0].store] || "target store") + ".";
    document.getElementById("diff-tbody").innerHTML = sync.diffs.map(diffRowHtml).join("");

    const targetStore = STORE_LABEL[sync.diffs[0].store] || "the target store";
    document.getElementById("dryrun-target-store").textContent = targetStore;

    const toggle = document.getElementById("dryrun-toggle");
    toggle.checked = true;
    document.getElementById("report-banner").hidden = true;
    updateApproveState();

    switchView("diff");
  }

  function updateApproveState() {
    const dryRun = document.getElementById("dryrun-toggle").checked;
    const approveBtn = document.getElementById("approve-sync-btn");
    const hint = document.getElementById("approve-hint");
    approveBtn.disabled = dryRun;
    hint.textContent = dryRun
      ? "Turn off dry-run mode to enable live apply."
      : "Live apply is enabled — approving will write to " + document.getElementById("dryrun-target-store").textContent + ".";
  }

  function runDryRun() {
    const sync = findPending(activeDiffSyncId);
    if (!sync) return;
    const increases = sync.diffs.filter(d => d.newQty > d.oldQty).length;
    const decreases = sync.diffs.filter(d => d.newQty < d.oldQty).length;
    const banner = document.getElementById("report-banner");
    banner.hidden = false;
    banner.className = "report-banner report-banner--info";
    banner.innerHTML = `<strong>Dry run complete — 0 writes made.</strong> ` +
      `Simulated against live data: ${sync.diffs.length} SKUs would change ` +
      `(${increases} increase${increases === 1 ? "" : "s"}, ${decreases} decrease${decreases === 1 ? "" : "s"}). ` +
      `Ran ${fmtDate(nowIso())}.`;
  }

  function exportSyncReport() {
    const sync = findPending(activeDiffSyncId);
    if (!sync) return;
    const rows = [["sku", "product", "store", "old_qty", "new_qty", "source"]]
      .concat(sync.diffs.map(d => {
        const row = findSku(d.sku);
        return [d.sku, row ? row.product + " — " + row.variant : "", STORE_LABEL[d.store] || d.store, d.oldQty, d.newQty, d.source];
      }));
    csvDownload(sync.id + "-dry-run-report.csv", rows);
  }

  function approveSync() {
    const sync = findPending(activeDiffSyncId);
    if (!sync) return;
    const changedSkus = [];
    sync.diffs.forEach(d => {
      const row = findSku(d.sku);
      if (row) { row[d.store] = d.newQty; changedSkus.push(d.sku); }
    });
    state.auditLog.unshift({
      id: "audit-" + Date.now(),
      title: sync.title,
      subtitle: sync.subtitle,
      appliedAt: nowIso(),
      status: "applied",
      skuCount: sync.diffs.length,
      rolledBack: false,
      rolledBackAt: null,
      changes: sync.diffs.map(d => ({ sku: d.sku, store: d.store, oldQty: d.oldQty, newQty: d.newQty }))
    });
    addActivity(`${sync.title} applied — ${sync.diffs.length} SKUs updated on ${STORE_LABEL[sync.diffs[0].store]}.`, "success");
    state.pendingSyncs = state.pendingSyncs.filter(s => s.id !== sync.id);
    saveState();
    toast(`Applied — ${sync.diffs.length} SKUs updated on ${STORE_LABEL[sync.diffs[0].store]}.`, "success");
    renderAll();
    flash(changedSkus);
    switchView("dashboard");
  }

  function rejectSync() {
    const sync = findPending(activeDiffSyncId);
    if (!sync) return;
    state.auditLog.unshift({
      id: "audit-" + Date.now(),
      title: sync.title,
      subtitle: sync.subtitle,
      appliedAt: nowIso(),
      status: "rejected",
      skuCount: sync.diffs.length,
      rolledBack: false,
      rolledBackAt: null,
      changes: []
    });
    addActivity(`${sync.title} rejected — no changes written.`, "info");
    state.pendingSyncs = state.pendingSyncs.filter(s => s.id !== sync.id);
    saveState();
    toast("Sync rejected — no changes were written.", "info");
    renderAll();
    switchView("dashboard");
  }

  // ---------- circuit breaker view ----------
  function openBreaker(sync) {
    activeDiffSyncId = sync.id;
    const b = sync.breaker;
    document.getElementById("breaker-headline").textContent =
      `Halted: this sync would zero ${fmtNum(b.affectedSkuCount)} SKUs across ${b.storeLabel} — review before applying.`;
    document.getElementById("breaker-reason").textContent = b.reason;
    document.getElementById("breaker-count").textContent = fmtNum(b.affectedSkuCount);
    document.getElementById("breaker-store").textContent = b.storeLabel;
    document.getElementById("breaker-pct").textContent = b.catalogValueDropPct + "%";
    document.getElementById("breaker-rule").textContent = b.rule;
    document.getElementById("breaker-sample-sub").textContent =
      `Showing ${b.sampleDiffs.length} of ${fmtNum(b.affectedSkuCount)} SKUs that would be set to 0. No values have been written.`;
    document.getElementById("breaker-tbody").innerHTML =
      b.sampleDiffs.map(diffRowHtml).join("") +
      `<tr class="row-more"><td colspan="7">+ ${fmtNum(b.affectedSkuCount - b.sampleDiffs.length)} more SKUs not shown</td></tr>`;
    switchView("breaker");
  }

  function exportBreakerReport() {
    const sync = findPending(activeDiffSyncId);
    if (!sync || !sync.breaker) return;
    const b = sync.breaker;
    const rows = [["sku", "product", "store", "old_qty", "new_qty", "source"]]
      .concat(b.sampleDiffs.map(d => {
        const row = findSku(d.sku);
        return [d.sku, row ? row.product + " — " + row.variant : "", STORE_LABEL[d.store] || d.store, d.oldQty, d.newQty, d.source];
      }));
    rows.push([`(+${b.affectedSkuCount - b.sampleDiffs.length} more SKUs affected, not listed)`]);
    csvDownload(sync.id + "-halt-report.csv", rows);
  }

  function dismissBreaker() {
    const sync = findPending(activeDiffSyncId);
    if (!sync) return;
    const b = sync.breaker;
    state.auditLog.unshift({
      id: "audit-" + Date.now(),
      title: sync.title,
      subtitle: sync.subtitle,
      appliedAt: nowIso(),
      status: "halted",
      skuCount: b.affectedSkuCount,
      rolledBack: false,
      rolledBackAt: null,
      changes: []
    });
    addActivity(
      `Circuit breaker halted "${sync.title}" before any write — ${fmtNum(b.affectedSkuCount)} SKUs would have been zeroed on ${b.storeLabel}. Nothing was changed.`,
      "danger"
    );
    state.pendingSyncs = state.pendingSyncs.filter(s => s.id !== sync.id);
    saveState();
    toast(`Halted — ${fmtNum(b.affectedSkuCount)} SKUs were not written.`, "danger");
    renderAll();
    switchView("dashboard");
  }

  // ---------- audit log / rollback ----------
  function statusBadge(entry) {
    if (entry.rolledBack) return `<span class="badge badge--slate">Rolled back</span>`;
    if (entry.status === "applied") return `<span class="badge badge--green">Applied</span>`;
    if (entry.status === "halted") return `<span class="badge badge--red">Halted by breaker</span>`;
    if (entry.status === "rejected") return `<span class="badge badge--slate">Rejected</span>`;
    return `<span class="badge badge--slate">${esc(entry.status)}</span>`;
  }

  function renderAudit() {
    const tbody = document.getElementById("audit-tbody");
    const items = [...state.auditLog].sort((a, b) => new Date(b.appliedAt) - new Date(a.appliedAt));
    tbody.innerHTML = items.map(entry => {
      const storeIds = [...new Set(entry.changes.map(c => c.store))];
      const storeLabel = storeIds.length ? storeIds.map(id => STORE_LABEL[id] || id).join(", ") : (entry.subtitle || "—");
      let action = `<span class="muted">—</span>`;
      if (entry.status === "applied" && !entry.rolledBack && entry.changes.length) {
        action = `<button class="btn btn--secondary btn--sm" data-action="rollback" data-id="${esc(entry.id)}" type="button">Rollback</button>`;
      } else if (entry.rolledBack) {
        action = `<span class="muted small">Rolled back ${fmtDate(entry.rolledBackAt)}</span>`;
      }
      return `
        <tr data-audit="${esc(entry.id)}">
          <td class="mono">${fmtDate(entry.appliedAt)}</td>
          <td>${esc(entry.title)}<div class="muted small">${esc(entry.subtitle || "")}</div></td>
          <td>${esc(storeLabel)}</td>
          <td class="num mono">${fmtNum(entry.skuCount)}</td>
          <td>${statusBadge(entry)}</td>
          <td>${action}</td>
        </tr>`;
    }).join("");

    tbody.querySelectorAll('[data-action="rollback"]').forEach(btn => {
      btn.addEventListener("click", () => rollbackEntry(btn.dataset.id));
    });
  }

  function rollbackEntry(id) {
    const entry = state.auditLog.find(a => a.id === id);
    if (!entry || entry.rolledBack) return;
    const changedSkus = [];
    entry.changes.forEach(c => {
      const row = findSku(c.sku);
      if (row) { row[c.store] = c.oldQty; changedSkus.push(c.sku); }
    });
    entry.rolledBack = true;
    entry.rolledBackAt = nowIso();
    addActivity(`Rolled back "${entry.title}" — ${entry.changes.length} SKUs restored on ${[...new Set(entry.changes.map(c => STORE_LABEL[c.store] || c.store))].join(", ")}.`, "info");
    saveState();
    toast(`Rolled back — quantities restored for ${entry.changes.length} SKUs.`, "info");
    renderAll();
    flash(changedSkus);
    switchView("audit");
  }

  // ---------- global ----------
  function renderAll() {
    renderStores();
    renderPending();
    renderInventory();
    renderActivity();
    renderAudit();
  }

  function wireEvents() {
    document.querySelectorAll(".nav-tab").forEach(tab => {
      tab.addEventListener("click", () => switchView(tab.dataset.view));
    });
    document.querySelectorAll("[data-back]").forEach(btn => {
      btn.addEventListener("click", () => switchView(btn.dataset.back));
    });

    document.getElementById("inventory-search").addEventListener("input", renderInventory);

    document.getElementById("dryrun-toggle").addEventListener("change", updateApproveState);
    document.getElementById("run-dryrun-btn").addEventListener("click", runDryRun);
    document.getElementById("export-report-btn").addEventListener("click", exportSyncReport);
    document.getElementById("approve-sync-btn").addEventListener("click", approveSync);
    document.getElementById("reject-sync-btn").addEventListener("click", rejectSync);

    document.getElementById("breaker-dismiss-btn").addEventListener("click", dismissBreaker);
    document.getElementById("breaker-export-btn").addEventListener("click", exportBreakerReport);

    document.getElementById("reset-demo").addEventListener("click", () => {
      localStorage.removeItem(STORAGE_KEY);
      window.location.reload();
    });
  }

  function init() {
    state = loadState();
    saveState();
    wireEvents();
    renderAll();
    switchView("dashboard");
  }

  document.addEventListener("DOMContentLoaded", init);
})();
