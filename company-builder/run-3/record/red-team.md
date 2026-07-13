# Red Team — Trying to Kill WideTally
2026-07-13. Adversarial pass written against the finished business (inline — the planned skeptic sub-agents were unavailable under the API spend cap, so this was done as a separate documented pass with the explicit goal of breaking the thesis). Attacks ordered by lethality. Each has a verdict: **KILL / WOUND / SCRATCH**, and what the founder must do about it.

---

## 1. The product doesn't actually serve the verified "daily refresh" pain — WOUND (the sharpest attack)
The pain evidence includes authors compulsively refreshing dashboards ("a dozen times a day" — verified). WideTally ingests **files an author manually downloads**; it cannot serve the compulsive real-time checking moment. Extensions and scrapers, whatever their fragility, show *today's* numbers. WideTally is a **reconciliation and decision** tool (monthly truth, series P&L, ad ROI, taxes), not a live ticker.
**Response required:** never market "retire the refresh ritual" as real-time; the honest claim is "one glance replaces the *monthly accounting* tour, and your ad decisions stop being guesses." The current site copy ("The 15-minute ritual, retired") leans slightly hot; flagged for revision in v1.1 copy. Roadmap answer: optional local auto-fetch of the KDP dashboard **by the author's own browser session on their machine** is possible later, but reintroduces fragility — decide only with real user data.

## 2. The reliability claim leans on one reviewer — WOUND
"The market leader is failing" is anchored to Kindlepreneur (Dave Chesson), a single — if authoritative — source who runs affiliate links and now crowns a competing subscription tool. If ScribeCount stabilizes (his own review says "as of early 2026 there seem to be some improvements"), the open flank narrows.
**Response:** the durable wedge is architecture (no credentials, offline, pay-once), not the incumbent's outage record. Business plan §5 already frames it this way; keep it that way. Do not build marketing on "ScribeCount is broken" — that claim has a shelf life.

## 3. TrackerBox is a warning, not just a validation — WOUND
The only precedent for local-file-based tracking was abandoned in 2019. Likeliest causes: parser-maintenance treadmill on one-time-purchase economics, and a Windows-only .NET stack. We priced the treadmill (Updates Pass) — but at 1,000 licenses and 50% attach, that's ~$9.5k/yr for what is realistically 4–6 founder-weeks of parser chasing plus support. Thin.
**Response:** the Format Registry doubles as community-sourced change detection (users report breakage with samples); parsers are data-driven (header fingerprints), so most changes are config-level. Still: this business only works founder-lean. Anyone modeling a team on it should stop.

## 4. Download friction is real — SCRATCH-to-WOUND
Authors must export files from each dashboard monthly. That's 10 minutes/month of chores WideTally cannot remove; cloud tools with stored credentials can. Counter-evidence: the leading wide tracker itself advertises "no passwords required" ingestion, meaning the market has already accepted file/no-credential flows; and monthly-files beat daily-logins for the accounting job. Accepted as a known cost of the privacy stance.

## 5. Is "privacy of royalty data" a real purchase driver? — WOUND (unproven demand hypothesis)
No fetched evidence shows authors *refusing* cloud trackers over privacy. The verified complaints are reliability and money — privacy is our inference of a resonant angle, not a demonstrated demand. It might be a nice-to-have that doesn't move wallets.
**Response:** privacy is positioned as the *trust guarantee* wrapped around verified pains (reliability, cost), never the headline pain. Launch plan's kill-signal metric (<2% Lite→license after 500 installs) is the test.

## 6. Amazon risk — SCRATCH
Amazon could improve native reporting (it stays Amazon-only by definition; wide authors' problem is cross-store) or theoretically restrict report exports (near-zero: authors need them for accounting/tax). Nominative use of "KDP/Kobo" names in comparison content is standard. Low.

## 7. Cloud incumbents copy the pitch — SCRATCH
"Local mode" is architecturally expensive for subscription businesses (it deletes their recurring-revenue justification and their data asset). A *marketing* copy of the privacy language is likely; the $59-once price is the part a $185/yr business can't match without self-harm.

## 8. Demo-to-product gap — SCRATCH (disclosed)
The demo is a browser app served locally; the shipped product needs installers, code-signing (~$100/yr), an XLSX parser (KDP's native workbook — demo parses CSV), and packaging (PWA/Tauri). None of this is research-risk, but it's ~2–4 weeks of unglamorous work not represented in the demo. Disclosed in honesty.md.

## 9. Sample-data realism — SCRATCH (disclosed)
Parsers are proven against *synthetic files modeled on published schemas*, not against real exports (no real author accounts exist in this environment). First real-file contact will find deviations — this is exactly what the registry/updates machinery is for, but day-one parser confidence is overstated by the demo's smoothness. Disclosed prominently.

---

## What survives
The thesis survives, narrowed: **WideTally is the pay-once accounting-and-ad-truth layer for working wide authors** — not a real-time dashboard, not a mass-market app for the 44% earning under $100/mo (they get Lite free), and not a venture-scale business. The three load-bearing facts — no KDP API (Amazon, in writing), a paid category at $5–29/mo, an abandoned-but-once-viable local precedent — are all primary-source verified and none was dented by this pass.

## Changes made because of this red team
1. This file's objections are linked from RECAP.html at equal visual weight to the pitch.
2. honesty.md discloses items 5, 8, 9 explicitly.
3. Marketing claim inventory: "retire the ritual" flagged for softening (item 1); "$59 once" and comparison table left as-is (verified); no real-time language anywhere.
