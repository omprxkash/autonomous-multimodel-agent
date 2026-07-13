/* DueCrew product demo — all data fictional (see footer). No backend; state lives in memory. */
"use strict";

/* Fixed "today" so the demo is stable and recordable */
const TODAY = new Date(2026, 6, 13); // Jul 13 2026

const fmt = d => d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
const fmtMY = d => d.toLocaleDateString("en-US", { month: "short", year: "numeric" });
const daysLeft = d => Math.ceil((d - TODAY) / 86400000);

const state = {
  ceLogged: 2,
  ceRequired: 4,
  creds: [
    {
      id: "ok-jman", kind: "License", name: "Oklahoma — Electrical Journeyman",
      num: "OKJ-4471", expires: new Date(2026, 6, 22),
      facts: { "Renewal fee": "$75", "Delinquent fee": "$150 after date", "Renew at": "CIB online portal" },
      consequence: "Past this date, any work under this card is unlicensed work. States can fine it, and permits pulled on it can be frozen. California's board puts it plainly: work performed while a license is expired “is considered to be unlicensed.”",
      timeline: [
        { when: "Apr 23", label: "90-day nudge", chan: "email", sent: true },
        { when: "May 23", label: "60-day nudge", chan: "email", sent: true },
        { when: "Jun 22", label: "30-day nudge", chan: "SMS + email", sent: true },
        { when: "Jul 8",  label: "14-day nudge", chan: "SMS + email", sent: true },
        { when: "Jul 15", label: "7-day nudge — includes renewal link + fee", chan: "SMS + email + missed-call ring", sent: false },
        { when: "Jul 21", label: "Day-before: we call you", chan: "phone", sent: false }
      ],
      renewable: true
    },
    {
      id: "tx-ce", kind: "Continuing education", name: "Texas CE — 4 hours before renewal",
      num: "TME-88214", expires: new Date(2027, 2, 14), ce: true,
      facts: { "Required": "4 hours (TDLR-approved)", "Logged": "2 of 4 hours", "Covers": "NEC · NFPA 70E · TX law" },
      consequence: null,
      timeline: [
        { when: "Jun 1", label: "CE check-in — you're 2 hours short", chan: "email", sent: true },
        { when: "Sep 1", label: "CE check-in", chan: "email", sent: false }
      ],
      renewable: false
    },
    {
      id: "gl-coi", kind: "Insurance — COI", name: "General liability — Ridgeline Mutual",
      num: "GL-2201-884", expires: new Date(2026, 7, 3),
      facts: { "Carrier": "Ridgeline Mutual (fictional)", "Limit": "$1M / $2M", "Agent lead time": "about a week" },
      consequence: "A lapsed COI gets you blocked at the gate and your progress payments held. Documented case: 11 days off the job, $47,000 withheld.",
      timeline: [
        { when: "May 5", label: "90-day nudge", chan: "email", sent: true },
        { when: "Jun 4", label: "60-day nudge", chan: "email", sent: true },
        { when: "Jul 4", label: "30-day nudge — cc'd your agent", chan: "SMS + email", sent: true },
        { when: "Jul 20", label: "14-day nudge", chan: "SMS + email", sent: false }
      ],
      renewable: false
    },
    {
      id: "tx-license", kind: "License", name: "Texas — Master Electrician",
      num: "TME-88214", expires: new Date(2027, 2, 14),
      facts: { "Renewal fee": "$45", "CE gate": "4 hours before renewal", "Renew at": "TDLR online" },
      consequence: null,
      timeline: [{ when: "Dec 14", label: "90-day nudge", chan: "email", sent: false }],
      renewable: false
    },
    {
      id: "bond", kind: "Bond", name: "Surety bond — City of Tulsa",
      num: "B-55-0912", expires: new Date(2026, 10, 30),
      facts: { "Amount": "$5,000", "Holder": "City of Tulsa", "Broker": "Anchor Surety (fictional)" },
      consequence: null,
      timeline: [{ when: "Sep 1", label: "90-day nudge", chan: "email", sent: false }],
      renewable: false
    },
    {
      id: "auto", kind: "Insurance — COI", name: "Commercial auto — Ridgeline Mutual",
      num: "CA-7731-002", expires: new Date(2027, 1, 9),
      facts: { "Carrier": "Ridgeline Mutual (fictional)", "Vehicles": "2 vans", "Limit": "$1M CSL" },
      consequence: null,
      timeline: [{ when: "Nov 11", label: "90-day nudge", chan: "email", sent: false }],
      renewable: false
    }
  ]
};

function statusOf(c) {
  if (c.ce) return state.ceLogged >= state.ceRequired ? "good" : "watch";
  const d = daysLeft(c.expires);
  if (d <= 14) return "act";
  if (d <= 30) return "watch";
  return "good";
}
const S_LABEL = { good: "Good", watch: "Watch", act: "Act now" };

/* ---------- board ---------- */
function chipFor(c) {
  const st = statusOf(c);
  if (c.ce) {
    const left = state.ceRequired - state.ceLogged;
    return `<span class="chip s-${st}">${st === "good" ? "4 of 4 hours" : left + " hours short"}</span>`;
  }
  const d = daysLeft(c.expires);
  return `<span class="chip s-${st}">${st === "good" ? "Good through " + fmtMY(c.expires) : d + " days"}</span>`;
}

function renderBoard() {
  const wrap = document.getElementById("board-cards");
  wrap.innerHTML = state.creds.map(c => {
    const st = statusOf(c);
    return `<div class="card s-${st}" data-id="${c.id}" role="button" tabindex="0">
      <span class="eyebrow">${c.kind}</span>
      <h3>${c.name}</h3>
      <div class="card-date-row">
        <span class="card-date">${c.ce ? state.ceLogged + " / " + state.ceRequired + " hrs" : fmt(c.expires)}</span>
        ${chipFor(c)}
      </div>
      ${noteFor(c, st)}
    </div>`;
  }).join("");
  wrap.querySelectorAll(".card").forEach(el => {
    el.addEventListener("click", () => openDetail(el.dataset.id));
    el.addEventListener("keydown", e => { if (e.key === "Enter") openDetail(el.dataset.id); });
  });

  const counts = { act: 0, watch: 0, good: 0 };
  state.creds.forEach(c => counts[statusOf(c)]++);
  const pill = document.getElementById("standing-pill");
  if (counts.act > 0) {
    pill.className = "standing-pill has-act";
    pill.textContent = counts.act + " needs action";
  } else {
    pill.className = "standing-pill all-good";
    pill.textContent = "You're good";
  }
  document.getElementById("board-summary").textContent =
    `${counts.act} needs action · ${counts.watch} to watch · ${counts.good} good — ${fmt(TODAY)}`;
}

function noteFor(c, st) {
  if (c.id === "ok-jman" && st !== "good") return `<p class="card-note">Renewal takes ~10 minutes online. Delinquent fee doubles it.</p>`;
  if (c.id === "gl-coi" && st !== "good") return `<p class="card-note">Your agent needs about a week. 30-day nudge already cc'd them.</p>`;
  if (c.id === "tx-ce" && st !== "good") return `<p class="card-note">2 approved hours online tonight closes this.</p>`;
  return "";
}

/* ---------- registry strip ---------- */
function renderRegistry() {
  document.getElementById("registry-items").innerHTML = `
    <div><strong>TDLR (Texas)</strong> — checked today 6:02 AM · status: <strong style="color:#6FCB96">Active</strong></div>
    <div><strong>Oklahoma CIB</strong> — connector in development</div>`;
}

/* ---------- detail ---------- */
function openDetail(id) {
  const c = state.creds.find(x => x.id === id);
  const st = statusOf(c);
  const body = document.getElementById("detail-body");
  body.innerHTML = `<div class="detail-card">
    <span class="eyebrow">${c.kind} · ${c.num}</span>
    <h1>${c.name}</h1>
    <div class="detail-status-row">
      <span class="chip s-${st}">${S_LABEL[st]}</span>
      <span class="card-date">${c.ce ? state.ceLogged + " / " + state.ceRequired + " hours" : fmt(c.expires) + " · " + daysLeft(c.expires) + " days"}</span>
    </div>
    <div class="detail-facts">${Object.entries(c.facts).map(([k, v]) =>
      `<div class="fact"><span class="eyebrow">${k}</span><span class="fact-val">${v}</span></div>`).join("")}
    </div>
    ${c.consequence ? `<div class="consequence">${c.consequence}</div>` : ""}
    <div class="timeline">
      <h2>Alert schedule</h2>
      ${c.timeline.map(t => `<div class="tl-item">
        <span class="tl-when">${t.when}</span>
        <span class="${t.sent ? "tl-sent" : "tl-next"}">${t.sent ? "Sent" : "Scheduled"}</span>
        <span>${t.label} <span class="alert-chan">${t.chan}</span></span>
      </div>`).join("")}
    </div>
    <div class="detail-actions">
      ${c.renewable ? `<button class="btn btn-primary" id="mark-renewed-btn">Mark renewed — I did it</button>` : ""}
      ${c.ce ? `<button class="btn btn-primary" id="detail-ce-btn">Log 2-hour course</button>` : ""}
      <button class="btn btn-ghost" data-back="board">Back to board</button>
    </div>
  </div>`;
  document.querySelectorAll("[data-back]").forEach(b => b.addEventListener("click", () => showView("board")));
  const rn = document.getElementById("mark-renewed-btn");
  if (rn) rn.addEventListener("click", () => {
    c.expires = new Date(c.expires.getFullYear() + 1, c.expires.getMonth(), c.expires.getDate());
    renderBoard();
    showView("board");
    toast(`You're good — ${c.name.split("—")[1] ? c.name.split("—")[1].trim() : c.name} good through ${fmtMY(c.expires)}.`);
  });
  const ceb = document.getElementById("detail-ce-btn");
  if (ceb) ceb.addEventListener("click", () => { logCE(); showView("ce"); });
  showView("detail");
}

/* ---------- CE ---------- */
function renderCE() {
  const fill = document.getElementById("ce-fill");
  const pct = Math.min(100, state.ceLogged / state.ceRequired * 100);
  fill.style.width = pct + "%";
  fill.classList.toggle("done", state.ceLogged >= state.ceRequired);
  document.getElementById("ce-label").textContent = `${state.ceLogged} / ${state.ceRequired} hours`;
  const tb = document.querySelector("#ce-table tbody");
  tb.innerHTML = state.ceRows.map(r =>
    `<tr><td class="mono">${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td><td class="mono">${r[3]}</td></tr>`).join("");
  const btn = document.getElementById("log-ce-btn");
  btn.disabled = state.ceLogged >= state.ceRequired;
  btn.textContent = btn.disabled ? "Requirement met — 4 of 4 hours" : "Log 2-hour course — “2026 NEC significant changes”";
  if (btn.disabled) { btn.classList.remove("btn-primary"); btn.classList.add("btn-ghost"); }
}
state.ceRows = [["Feb 3, 2026", "NFPA 70E refresher (online)", "TDLR-registered provider", "2.0"]];

function logCE() {
  if (state.ceLogged >= state.ceRequired) return;
  state.ceLogged += 2;
  state.ceRows.push(["Jul 13, 2026", "2026 NEC significant changes (online)", "TDLR-registered provider", "2.0"]);
  renderCE(); renderBoard();
  toast("Logged. Texas CE requirement met — 4 of 4 hours.");
}

/* ---------- locker ---------- */
function renderLocker() {
  const docs = state.creds.filter(c => c.kind.startsWith("Insurance") || c.kind === "Bond");
  document.getElementById("locker-grid").innerHTML = docs.map(c => {
    const st = statusOf(c);
    return `<div class="card s-${st}" data-id="${c.id}" role="button" tabindex="0">
      <span class="eyebrow">${c.kind}</span>
      <h3>${c.name}</h3>
      <div class="card-date-row">
        <span class="card-date">${fmt(c.expires)}</span>
        ${chipFor(c)}
      </div>
      <p class="card-note">In the share link ✓</p>
    </div>`;
  }).join("");
  document.querySelectorAll("#locker-grid .card").forEach(el =>
    el.addEventListener("click", () => openDetail(el.dataset.id)));
}

/* ---------- alerts ---------- */
function renderAlerts() {
  const items = [
    ["Jul 8", "SMS + email", "Oklahoma journeyman card — 14 days. Renewal link + $75 fee inside."],
    ["Jul 4", "SMS + email", "General liability COI — 30 days. Copied your agent at Ridgeline Mutual."],
    ["Jun 22", "SMS", "Oklahoma journeyman card — 30 days."],
    ["Jun 4", "email", "General liability COI — 60 days."],
    ["Jun 1", "email", "Texas CE check-in — 2 of 4 hours logged. Two approved hours online closes it."],
    ["May 23", "email", "Oklahoma journeyman card — 60 days."],
    ["May 5", "email", "General liability COI — 90 days."],
    ["Apr 23", "email", "Oklahoma journeyman card — 90 days."]
  ];
  document.getElementById("alert-feed").innerHTML = items.map(i =>
    `<li><span class="alert-when">${i[0]}</span><span class="alert-chan">${i[1]}</span><span>${i[2]}</span></li>`).join("");
}

/* ---------- rules ---------- */
function renderRules() {
  const rows = [
    ["Texas", "Electrician", "Annual", "4 hrs (NEC, NFPA 70E, TX law)", "Delinquent fee; expired = unlicensed work", "verified"],
    ["California", "C-10 Electrical (CSLB)", "Drafted — 2-yr pattern", "Drafted", "Verified: delinquent fee; work while expired = unlicensed (CSLB)", "partial"],
    ["Oklahoma", "Electrician (CIB)", "Annual", "Drafted — verifying with CIB", "Drafted", "draft"],
    ["Florida", "Electrician (DBPR)", "2 years", "Drafted — 14 hrs pattern", "Drafted", "draft"],
    ["Arizona", "Contractor (ROC)", "2 years", "Drafted", "Drafted", "draft"],
    ["Colorado", "Electrician (DORA)", "3 years", "Drafted — 24 hrs pattern", "Drafted", "draft"],
    ["Washington", "Electrician (L&I)", "3 years", "Drafted — 24 hrs pattern", "Drafted", "draft"],
    ["Oregon", "Electrician (BCD)", "3 years", "Drafted — 24 hrs pattern", "Drafted", "draft"],
    ["North Carolina", "Electrical (Board of Examiners)", "Annual", "Drafted", "Drafted", "draft"],
    ["Georgia", "Electrical (Div. II)", "2 years", "Drafted", "Drafted", "draft"]
  ];
  document.querySelector("#rules-table tbody").innerHTML = rows.map(r =>
    `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td><td>${r[4]}</td>
     <td><span class="v-chip ${r[5]}">${r[5] === "verified" ? "Verified" : r[5] === "partial" ? "Partly verified" : "Draft"}</span></td></tr>`).join("");
}

/* ---------- shell ---------- */
function showView(name) {
  document.querySelectorAll(".view").forEach(v => v.hidden = true);
  document.getElementById("view-" + name).hidden = false;
  document.querySelectorAll(".nav-tab").forEach(t =>
    t.classList.toggle("active", t.dataset.view === name));
  window.scrollTo(0, 0);
}
document.querySelectorAll(".nav-tab").forEach(t =>
  t.addEventListener("click", () => showView(t.dataset.view)));

let toastTimer;
function toast(msg, warn) {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.className = "toast" + (warn ? " warn" : "");
  el.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.hidden = true; }, 3400);
}

document.getElementById("log-ce-btn").addEventListener("click", logCE);
document.getElementById("copy-link-btn").addEventListener("click", () => {
  toast("Link copied — duecrew.com/s/delgado-electric", true);
});
document.querySelector('#view-detail .back-link').addEventListener("click", () => showView("board"));

renderBoard(); renderRegistry(); renderCE(); renderLocker(); renderAlerts(); renderRules();
