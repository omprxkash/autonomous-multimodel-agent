# Phase 2 — Idea Tournament & Decision

Six candidates advanced from the pain hunt. Three got full pitch investigations by
independent agents (one was terminated by an API budget error before reporting; its
verification was completed by the orchestrator directly — see verification.md). Scoring
below is the orchestrator's judge pass over all evidence. Scale 1–10.

| # | Candidate | Evidence | Market | Underserved | Buildable demo | WTP* | Total |
|---|-----------|----------|--------|-------------|----------------|------|-------|
| 1 | **Solo-trades license/CE/COI compliance tracker** | 8 | 7 | 8 | 9 | 7 | **39** |
| 2 | Small-landlord (1–9 unit) admin tool | 7 | 8 | 3 | 8 | 6 | 32 |
| 3 | Dental insurance verification automation | 7 | 7 | 3 | 4 | 8 | 29 |
| 4 | Vet front-desk phone/no-show automation | 6 | 6 | 4 | 6 | 7 | 29 |
| 5 | Freelancer cross-tool billable "leakage" audit | 7 | 6 | 6 | 6 | 4 | 29 |
| 6 | Gig-worker cross-platform schedule conflicts | 5 | 6 | 8 | 7 | 2 | 28 |

*WTP = willingness-to-pay signal.

## Why each loser lost

- **#2 Small landlord:** the 1–9 unit segment is *directly* targeted by TurboTenant, Avail
  (owned by Realtor.com), Innago, Baselane, RentRedi, Stessa, Landlord Studio — several
  free or freemium. The pitch agent could not complete its competitor scan (budget), but the
  prior from the funding landscape is strong enough: underserved-ness fails. Scored 3.
- **#3 Dental verification:** own pitch agent returned 3/10 conviction — nine live
  competitors found (Zuub, Vyne, DentalXChange, Curve Eligibility+, SuperDial…), incumbents
  embedding into PMS vendors, and the core build (cross-payer integration) is genuinely hard
  and not demoable honestly. Killed on crowding + buildability.
- **#4 Vet front desk:** pain is real but the fix is an AI phone agent — a hot, crowded 2025
  category, and the strongest stats came from vendor blogs (Puppilot) marketing exactly that
  product. Somebody funded is already doing it; evidence sources are conflicted.
- **#5 Freelancer leakage:** best primary-source thread of the whole hunt, but the product
  is fuzzy (an audit/reconciliation layer over tools people already resent paying for),
  time-tracking is a brutally crowded category, and freelancer WTP is historically weak.
- **#6 Gig calendar:** true white space but the buyer is a gig worker optimizing already-thin
  margins; researcher E flagged monetization as unclear. WTP 2 kills it.

## Why #1 won

1. **Consequence-backed pain, not annoyance-backed.** CSLB (government source, fetched):
   work on an expired license "is considered to be unlicensed and disciplinary action can be
   taken" — in CA that's a misdemeanor with up to $15,000 in administrative fines. A
   documented COI lapse case: 11 days off the job, $47,000 withheld (verification.md V1/V2/V5).
   This is not "paperwork is annoying" — it's "a missed date stops your income."
2. **The people most exposed are the least tooled.** Solo operators reject FSM suites as
   overbuilt (ContractorTalk), hate paperwork enough to stay employees (ElectricianTalk),
   and per projul/NAHB ~66% of residential contractors have no dedicated tracking tool.
3. **Competition is generic or aims at the wrong buyer.** Generic expiry-reminder SaaS
   (ExpiryEdge, RemindCal) knows nothing about trades; compliance platforms (SkillSignal,
   SimpleCerts, TrackMyVendor) sell to GCs to police their subs. Nobody found is building
   for the tradesperson's side of the table. PermitFlow's $54M raise proves investors see
   contractor-compliance-adjacent pain as fundable — while leaving this wedge open.
4. **Market is big and reachable.** 1.76M workers across just the three core licensed trades
   (BLS, verified); ~2.88M no-employee construction businesses (Census via search, labeled).
   Licensing is near-universal for electricians/plumbers/HVAC and renewals recur forever —
   built-in retention.
5. **Honestly demoable.** A deadline-intelligence dashboard is fully buildable as a local
   product demo without faking any integration. The dental idea would have required a
   pretend payer network; this requires a calendar, state-rule data, and good design.

## Decision

**Build: a compliance deadline guard for solo and 2–5 person licensed trade contractors** —
tracks license renewals, CE-credit progress, COI/insurance expirations, and bond/permit
dates per state, with escalating alerts long before anything lapses. Working name decided in
brand phase. Independent of run-1's idea (inventory sync for Shopify) — different industry,
different buyer, different product shape; convergence check done and passed.
