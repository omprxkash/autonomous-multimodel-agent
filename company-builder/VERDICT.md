# VERDICT — Cross-Run Judgment (run-1 vs run-2 vs run-3)

Date: 2026-07-13. Judged by the orchestrating session after independently auditing each run
(see each run's `record/orchestrator-audit.md`; run-1 was audited by its own builder's
fresh-eyes pass plus the earlier gap re-grade). Judged from the deliverables, as a stranger
would encounter them. A skeptic pass on this verdict is included at the end.

## The three companies

| Run | Company | One-liner | Price |
|---|---|---|---|
| 1 | **ReconStock** | Shopify inventory sync that shows every change before it writes, and can undo it (dry-run, diff, circuit breaker, rollback) | $29–99/mo |
| 2 | **DueCrew** | Compliance deadline guard for solo licensed trade contractors (license/CE/COI/bond, escalating alerts) | $12/mo, $199 lifetime founding seats |
| 3 | **WideTally** | Local-first royalty + ad-ROI ledger for wide (multi-platform) self-published authors; parses the report files authors already download | $59 once |

## Scores (1–10, higher is better)

| Dimension | run-1 ReconStock | run-2 DueCrew | run-3 WideTally |
|---|---|---|---|
| Evidence quality | 9 | 7 | 9 |
| Believability of the wedge | 7 | 5 | 9 |
| Product demo persuasiveness | 9 | 7 | 9 |
| Brand craft | 8 | 7 | 8 |
| Video quality | 8 | 7 | 8 |
| Honesty / rigor | 9 | 9 | 9 |
| **Total** | **50** | **42** | **52** |

## Ranking and reasoning

### 1st — run-3, WideTally
The only run where the **architecture is the moat and the demo is honest about being the
product**. The chain of verified facts is unusually tight: Amazon states in writing there is
no KDP API (official GitHub answer, re-fetched verbatim) → every cloud incumbent must scrape
dashboards or ride browser cookies → the market leader's own maintenance blog documents
years of exactly that fragility (B&N cookie breakage unresolved, Google Play report-format
breakage, Apple data misread) → the authoritative reviewer in the space publicly withdrew
his recommendation ("I currently can't support the program with the status it's at today")
→ a local parser of the author's own downloaded report files is the same data path minus
the fragile part. The demo genuinely parses real dropped CSVs in-browser (proven in audit:
3 formats auto-detected, 652 rows parsed, zero errors) — so the demo-to-product gap is the
smallest of the three runs. Pricing ($59 once vs $120–348/yr subscriptions) is calibrated
to a market where 44% of surveyed authors earn ≤$100/mo. The abandoned-in-2019 TrackerBox
proves people paid one-time for exactly this model and that the modern slot is empty.

### 2nd — run-1, ReconStock
The strongest *process* of the three (8-lane hunt, five-judge tournament, adversarial
verification that caught two of its own research errors, 33-attack red team) and a genuinely
persuasive demo (34/34 automated checks; the circuit-breaker halt is the best single product
moment in the series). Loses to WideTally on wedge believability: it enters a **crowded,
platform-dependent market** (five incumbents, Shopify controls the API and the app store),
its "no incumbent ships dry-run/diff/rollback" claim is listing-verified only, and the
distance from local demo to real product is large — a production sync engine against live
Shopify APIs is most of the company and none of it exists yet.

### 3rd — run-2, DueCrew
The best single piece of evidence in the series (CSLB, a government primary source: expired-
license work "is considered to be unlicensed") and the most creative extra (the printable
"Lapse Math" van-door worksheet). But its own red team left the fatal objections standing,
and they are fatal-shaped: the alert primitive is a weekend build, four generic expiry
trackers already exist, Jobber could ship it as a feature, the value event is annual (brutal
for retention), and willingness-to-pay is asserted by analogy. Ranked third because the run
itself, honestly, gives you the reasons to doubt it.

## Skeptic pass on this verdict

- **"WideTally's market is poor."** True and priced in: most indie authors earn little —
  which is why the run priced at $59 once instead of a subscription. But it caps the upside;
  this is a healthy lifestyle business thesis, not a venture one. The verdict stands because
  the master prompt asked for a company a founder could take to market this month, not a
  unicorn.
- **"ReconStock's market has proven spend; WideTally's doesn't."** Shopify merchants
  demonstrably pay $10–60/mo for sync. But proven spend in a crowded category cuts both
  ways: acquisition runs through an app store owned by the platform, against five funded
  incumbents. WideTally's demand evidence is thinner but its competition is an abandoned
  2019 desktop app and a publicly failing scraper. Wedge quality > market size for a
  this-month launch.
- **"The judge audited runs 2 and 3 more deeply than run 1."** Correct — run-1's audit
  relied more on its builder's own (thorough) verification pass. Bias acknowledged; the
  gap between 1st and 2nd (2 points) is within this margin, so treat the top two as close.
  The tiebreaker remains the demo-to-product honesty gap, which is structural, not a
  scoring artifact.
- **"Single judge, not a panel."** Correct, forced by the account spend limit that killed
  sub-agents repeatedly during runs 2 and 3. Mitigation: every score dimension above is
  traceable to audited artifacts, and this skeptic section was written adversarially against
  the ranking before it was finalized.

## Improvement list for the winner (run-3)

1. **DONE (2026-07-13):** Broaden the "failing incumbent" evidence beyond the single
   Kindlepreneur reviewer — ScribeCount's own maintenance blog now corroborates the
   fragility mechanism first-party. See `run-3/research/verification-addendum.md`.
2. **DONE (2026-07-13):** Anchor parser schema fidelity to Amazon's official documentation
   of the Historical Report columns (Title, ASIN, Units Sold, Units Refunded, Net Units
   Sold, KENP Read, Free Units) rather than synthetic schemas alone. Same addendum.
3. Remaining (for a human founder, pre-launch): obtain 3–5 real export files from real
   accounts and run them through the parser; publish the Format Registry publicly; get one
   wide author with >10 books to use it for a week.
