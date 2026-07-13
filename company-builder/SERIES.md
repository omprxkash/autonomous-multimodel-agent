# SERIES — Autonomous Company-Builder Runs (start here)

Three complete companies were built autonomously from `MASTER_PROMPT.md`, each from fresh
open-internet research, each fully local (nothing published, nothing purchased, no paid
APIs). Every run contains a working product demo, landing page, two videos, verified
research, brand system, red team, honesty ledger, and a self-contained `RECAP.html`.

## The verdict

**Winner: run-3, WideTally.** Full head-to-head scoring, reasoning, and a skeptic pass on
the verdict itself: [VERDICT.md](VERDICT.md).

| Rank | Run | Company | What it is | Start here |
|---|---|---|---|---|
| 🥇 | run-3 | **WideTally** | Local-first royalty + ad-ROI ledger for wide self-published authors. Parses the KDP/D2D/Kobo/Amazon-Ads report files authors already download — entirely on their machine. $59 once vs $120–348/yr incumbents. The moat is architectural: Amazon confirmed in writing there is no KDP API, so every cloud rival scrapes and breaks; the market leader's own blog documents it. | `run-3\RECAP.html` |
| 🥈 | run-1 | **ReconStock** | Shopify inventory sync that shows every change before writing and can undo it (dry-run, diff preview, anomaly circuit breaker, one-click rollback). Best process and best single demo moment of the series; loses on crowded market + platform risk. | `run-1\RECAP.html` |
| 🥉 | run-2 | **DueCrew** | Compliance deadline guard for solo licensed trade contractors (license/CE/COI/bond alerts). Government-grade evidence anchor (CSLB), but its own red team left the moat and retention objections standing. | `run-2\RECAP.html` |

## Run any of them

Each run's README has exact commands. Pattern (Node.js required):

```powershell
cd d:\AI\Business\run-3
node serve.js                 # → product demo + landing page on localhost:8130
# run-1: cd run-1\_tools; node verify\server.js      (port 8123)
# run-2: cd run-2\_tools; node verify\server.js 8231 (port 8231)
```

Videos are plain MP4s in each run's `video\` folder.

## What was verified, and by whom

- Each builder self-graded against the definition of done (`record/gap-analysis.md`).
- The orchestrator then independently re-audited runs 2 and 3 (`record/orchestrator-audit.md`
  in each): drove the demos with Playwright (run-3's file-import flow parsed 652 rows across
  3 real dropped CSVs, zero errors), null-decoded and frame-inspected all four videos,
  link-checked every RECAP (0 broken), and re-fetched the load-bearing claims live —
  including the CSLB expired-license rule (run-2), the $47k COI anecdote (run-2), Amazon's
  official no-KDP-API statement (run-3), and the ScribeCount recommendation withdrawal
  (run-3). All verified verbatim.
- Post-verdict, the winner's two weakest evidence points were strengthened with fresh
  primary sources: `run-3\research\verification-addendum.md`.

## Honest residual weaknesses (unhidden, per run)

- **run-3 / WideTally:** indie-author market is small-wallet (44% earn ≤$100/mo — hence
  one-time pricing); demand for the privacy/local angle is unproven; parsers proven against
  officially-documented schemas but not yet against real account exports; tournament and
  red team were single-agent (spend cap), disclosed.
- **run-1 / ReconStock:** "no incumbent ships dry-run/diff/rollback" is listing-verified
  only; TAM multiplier is a labeled assumption; the real sync engine doesn't exist — the
  demo is seeded local data.
- **run-2 / DueCrew:** weekend-build moat, annual value event vs monthly subscription,
  willingness-to-pay asserted by analogy — all left standing by its own red team.

## Process notes

- Runs 2 and 3 were repeatedly killed mid-build by the account's monthly spend limit and
  resumed each time from disk state; both runs disclose this in their honesty files. The
  limit also forced single-agent judging in both runs (disclosed).
- The build environment had no generative-media API keys, so: all imagery is hand-authored
  SVG, all voiceover is Windows TTS (disclosed in-video and in honesty files), all footage
  is Playwright-recorded real product UI, assembled with ffmpeg-static.

*Written 2026-07-13 by the orchestrating session. Everything above traces to files in this
folder — nothing here is a claim without an artifact behind it.*
