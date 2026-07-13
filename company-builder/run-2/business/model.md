# DueCrew — Business Model

All math in this file is **inference** built on the verified anchors cited in thesis.md.
No pricing was tested with real customers in this run.

## Pricing

| Plan | Price | Covers |
|------|-------|--------|
| **Solo** | $12/mo or $99/yr | 1 credential holder, unlimited credentials, SMS+email alerts, COI locker + share link, CE ledger |
| **Crew** | $29/mo or $249/yr | Up to 5 credential holders, owner board, per-tech alerts |
| **Founding member** (pre-launch only) | $199 lifetime, capped at 200 | Solo plan forever + name on the wall |

Rationale (inference):
- $12/mo sits below the deliberation threshold for a business expense in this segment, and
  prices against the downside: one delinquent renewal fee alone typically exceeds a year of
  DueCrew; the verified worst case (COI lapse) was $47,000 withheld + 11 days off the job.
- Annual-first pricing fits a product whose value events are annual. Target: >70% of solo
  subs on annual.
- The $199 lifetime cap (200 seats = $39,800) is a launch-financing and social-proof
  instrument, not a revenue strategy.

## Unit economics (inference, stated assumptions)

- **COGS:** SMS (~6 alerts/credential/yr × ~6 credentials ≈ 36 SMS/user/yr ≈ $0.40), email
  negligible, hosting negligible at this scale. Gross margin >90%.
- **State-rules maintenance:** the real cost. Assume 0.25 FTE researcher once at 50 states
  × 3 trades (~$20k/yr contract). This is the moat spend — treated as COGS-adjacent R&D.
- **CAC channels** are organic-first (see gtm.md); assume blended CAC $25–60. At $99/yr and
  >90% margin, payback < 8 months even at the pessimistic end.
- **Churn:** the honest unknown. Renewal events are annual, so perceived value is spiky.
  Mitigations: CE ledger creates monthly touch; COI share link creates weekly utility.
  Model assumes 4%/mo solo churn year one (pessimistic), improving with annual plans.

## Market math (inference, labeled)

- 1.76M workers in the three core licensed trades (BLS, verified) + adjacent licensed
  trades (GC licenses, fire/alarm, mechanical) beyond that.
- ~2.88M no-employee construction businesses (Census 2022 via jobstackcrm.com, directional).
- Assume conservatively **~1.0M** US solo/small-crew operators hold at least one renewable
  trade license with meaningful lapse consequences → **SAM ≈ $99M ARR** at Solo-annual
  pricing.
- Year-3 target: 0.5% of SAM = **5,000 paying subs ≈ $500k ARR** — a healthy solo-founder
  business; 2% = $2M ARR — a fundable seed story. Neither number is a promise; both are
  arithmetic on the anchors above.

## Expansion paths (roadmap, not promises)

1. **More credential verticals** on the same engine: DOT medical cards, EPA certs,
   cosmetology, real-estate CE — every licensed trade has the same date problem.
2. **CE marketplace referral revenue**: approved-provider links are natural affiliate
   inventory (the $9-course ecosystem already runs on affiliates).
3. **Registry monitoring** (in development): automated checks of public state license
   registries to confirm status independently — upgrades DueCrew from reminders to
   verification, and enables the "board is proof" use with GCs.
4. **GC hand-off**: a sub's share link is a wedge into the GC's own compliance workflow —
   long-term option to sell the *pair* a connection, not to switch sides.
