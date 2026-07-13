# DueCrew — Competitive Landscape

Scan date: 2026-07-12 (WebSearch, one thorough pass; budget-constrained — see red team R6).
Every named product below surfaced in live search results; URLs listed.

## Bucket 1 — Generic expiry-reminder SaaS (closest in function, farthest in fit)

| Product | What it is | Why it doesn't own our user |
|---------|-----------|------------------------------|
| ExpiryEdge — expiryedge.com/solutions/license-management/ | Horizontal license/cert expiry tracker for teams; CE-hour tracking mentioned | Team/compliance-officer framing; no trade-specific state rules; no COI share; nothing about trades |
| RemindCal — remindcal.com/license-expiration-reminder | Email/SMS reminders at 90/60/30/14/7 days for licenses | Pure reminders; no rules knowledge, no CE ledger, no locker |
| ExpiryKeeper — expirykeeper.com/industries/construction | Expiry tracking with a construction industry page | Generic engine with an industry landing page; tracks what you type in, knows nothing itself |
| ExpiryGuard — expiryguard.app/contractor-license-renewal-tracker | Contractor license renewal tracker page | Same pattern; also note: this crowd of near-identical "expiry*" microtools suggests low barrier — see red team R1 |

**Read:** the existence of four interchangeable "expiry" tools proves demand for the
reminder primitive and proves the primitive alone is not a company. Differentiation must be
the trade-native layer: state rules, CE math, COI workflow, trade language.

## Bucket 2 — GC-side subcontractor compliance (same documents, opposite buyer)

| Product | Buyer | Note |
|---------|-------|------|
| SkillSignal — skillsignal.com/certification-management/ | GC / site safety | Tracks workers' certs, "block expired workers at the gate" — enforcement, from above |
| SimpleCerts — simplecerts.ai/contractor-license-verification | GC / PM | AI-extracts license data from subs' documents, alerts the GC |
| TrackMyVendor — trackmyvendor.com | GC / vendor mgmt | COI tracking of vendors |
| Jones — getjones.com | GC / property | Enterprise COI verification |

**Read:** this bucket is DueCrew's tailwind, not competition — the more GCs automate
enforcement, the more a sub needs his own side of the table. It's also the acquirer list.

## Bucket 3 — FSM suites (the incumbents our user already rejected)

- **ServiceTitan** — enterprise-priced; users report add-on stacking ($12–33.6k/yr) and
  implementation fees $5–50k (capterra.com/p/150053, snippet-corroborated); HeatingHelp
  forum users report stress and glitches at the point of sale (forum.heatinghelp.com/discussion/169798, fetched).
- **Jobber / Housecall Pro** — SMB-friendlier, but small contractors describe all
  scheduling-suite software as "way too involved… for a small company"
  (contractortalk.com/threads/scheduling-software.421853, snippet).
- None of the three markets license/CE/COI tracking as a capability for solo operators
  (checked their public feature pages via search results in this run; not exhaustively
  re-verified — noted in red team R2 as the "feature-shipped-by-Jobber" risk).

## Bucket 4 — Adjacent capital (validation, and a ceiling to respect)

- **PermitFlow** — $54M Series B, Dec 2025, permit submission for GCs/developers
  (businesswire.com, fetched by researcher E). Proves construction-compliance pain is
  fundable; also the most likely fast-follower into sub-side compliance if it works.
- **License-service consultancies** (contractor-state-license.com renewals-maintenance
  service) — human-powered renewal management exists as a paid service today, which is
  direct evidence of willingness to pay for exactly this job.

## Whitespace claim (bounded)

No product found in one thorough search pass that combines: contractor-side framing +
state/trade rules knowledge + CE ledger + COI locker/share + escalating alerts at a solo
price point. Bounded honestly: a niche tool with poor SEO could exist; scan was
budget-limited; see record/red-team.md R6.
