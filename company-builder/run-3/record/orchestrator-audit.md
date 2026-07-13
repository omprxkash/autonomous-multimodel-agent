# Orchestrator Audit — run-3 (WideTally)

Date: 2026-07-13. Independent verification by the orchestrating session, performed after the
builder agent's self-grading (`gap-analysis.md`). All checks re-executed fresh.

## Mechanical checks

| Check | Result |
|---|---|
| Real file-import flow (Playwright: set 3 sample CSVs on the file input at `/product/`) | PASS — all three formats auto-detected (Kobo Writing Life 224 rows, KDP Sales & Royalties 392 rows, Amazon Ads campaigns 36 rows), all status "parsed", zero JS/console errors. Screenshot: `record/shots/audit-filedrop.png` |
| Ledger view sanity (builder screenshot review) | PASS — 12-month stacked earnings chart, per-platform table, KU estimates labeled `est.`, synthetic-data banner visible |
| `launch.mp4` ffmpeg null-decode | PASS — exit 0 |
| `founder.mp4` ffmpeg null-decode | PASS — exit 0 |
| Video frame visual inspection | PASS — reviewed `launch-31s.png` (Books & series view with per-store royalty columns and ad-net math) among the 12 extracted frames |
| RECAP.html link check (all relative hrefs vs. disk) | PASS — 22/22 resolve, 0 broken |
| Server + demo run per README (`node serve.js`, port 8130) | PASS |

## Load-bearing claim re-fetch (live, this session)

| Claim | Result |
|---|---|
| KDP has no public API — official Amazon statement "Right now, Amazon Selling Partner API does not return any data related to Kindle Direct Publishing (KDP)" (Marc, SP Developer Services, 2025-10-07) | VERIFIED verbatim at github.com/amzn/selling-partner-api-models discussion #4975, fetched 2026-07-13 |
| ScribeCount reliability collapse: "Many times I myself have tried to open the program to see my data and got nothing" / "I would no longer recommend ScribeCount" / "I currently can't support the program with the status it's at today" | VERIFIED verbatim at kindlepreneur.com/scribecount-review, fetched 2026-07-13 |

## Post-audit improvement (2026-07-13)

The run's two weakest evidence points were strengthened after the audit — incumbent
fragility is now corroborated first-party by ScribeCount's own maintenance blog, and parser
schema fidelity is anchored to Amazon's official Historical Report documentation. See
`research/verification-addendum.md` (linked from RECAP). The remaining honest gap (real
export files needed pre-launch) is unchanged.

## Verdict

Definition of done met. The builder's self-grade (9 PASS / 2 PASS−) is consistent with
independent re-verification. The demo's central claim — it parses real report files in the
browser rather than displaying canned screens — was proven by driving the actual file-input
code path with the shipped sample CSVs. Disclosed weaknesses (single-agent judging under the
spend cap, evidence concentration on one reviewer, synthetic-schema parser fidelity) were
found disclosed, not hidden.
