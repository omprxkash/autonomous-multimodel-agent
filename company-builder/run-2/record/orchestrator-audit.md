# Orchestrator Audit — run-2 (DueCrew)

Date: 2026-07-13. Independent verification by the orchestrating session, performed after the
builder agent's self-grading (`gap-analysis.md`). All checks re-executed fresh, not taken on
trust from the builder.

## Mechanical checks

| Check | Result |
|---|---|
| Product smoke test (`_tools/verify/smoke-product.js` against live server on :8231) | PASS — renew flow and CE flow drive real state changes ("1 needs action" → "You're good", "4 / 4 hours"), no JS errors |
| `launch.mp4` ffmpeg null-decode | PASS — exit 0, zero decode errors |
| `founder.mp4` ffmpeg null-decode | PASS — exit 0, zero decode errors |
| Video frame visual inspection | PASS — reviewed `frame-launch-20s.png` (stakes card: $47k / 11 days, CSLB attribution) and `frame-founder-100s.png` (close card with fictional-data disclosure) — on-brand, honest labeling visible in-frame |
| RECAP.html link check (all relative hrefs vs. disk) | PASS — 28/28 resolve, 0 broken |

## Load-bearing claim re-fetch (live, this session)

| Claim | Result |
|---|---|
| CSLB: "Any work performed while the license is expired is considered to be unlicensed and disciplinary action can be taken against you" + 90-day retroactive window + 5-year reapplication | VERIFIED verbatim at cslb.ca.gov (Failing_To_Renew_Your_License.aspx), fetched 2026-07-13 |
| $47,000 withheld / 11 days off the job COI anecdote + $18K–$75K annual figure | VERIFIED verbatim at theagentsoffice.com, fetched 2026-07-13 (insurance-agency marketing content, as the run itself disclosed) |

## Verdict

Definition of done met. The builder's self-grade (11 PASS / PASS-WITH-NOTES) is consistent
with independent re-verification. Known gaps the builder disclosed (self-run red team, 107s
founder video, single-pass competitor scan, projul.com re-fetch failure) were spot-confirmed
as disclosed rather than hidden. No placeholders found pretending to be finished work.
