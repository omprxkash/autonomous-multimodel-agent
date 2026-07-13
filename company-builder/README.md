# Autonomous Company Builder — three companies, one prompt

An experiment: an AI agent was given a single goal prompt ([MASTER_PROMPT.md](MASTER_PROMPT.md)) —
*build a complete company from scratch, alone, asking nothing* — and executed it three times,
each run independently researched from live internet pain, each producing a finished
go-to-market package: verified market research, business plan, brand system, working product
demo, landing page, launch + founder videos, adversarial red team, and a self-graded honesty
ledger. Nothing was published, purchased, or deployed; every market claim traces to a real
fetched URL or is labeled as an assumption.

## Start here

- **[SERIES.md](SERIES.md)** — what was built, how each was verified, honest weaknesses.
- **[VERDICT.md](VERDICT.md)** — the three runs judged head-to-head, with a skeptic pass
  on the verdict itself.

## The three companies

| Rank | Run | Company | One-liner |
|---|---|---|---|
| 🥇 | [run-3](run-3/) | **WideTally** | Local-first royalty + ad-ROI ledger for wide self-published authors — parses the KDP/D2D/Kobo/Amazon-Ads report files authors already download, entirely on their machine. $59 once vs $120–348/yr incumbents. Moat: Amazon confirmed in writing there is no KDP API, so every cloud rival scrapes and breaks. |
| 🥈 | [run-1](run-1/) | **ReconStock** | Shopify inventory sync that shows every change before writing — dry-run, diff preview, anomaly circuit breaker, one-click rollback. |
| 🥉 | [run-2](run-2/) | **DueCrew** | Compliance deadline guard for solo licensed trade contractors — license/CE/COI/bond expirations with escalating alerts. |

Each run folder is self-contained: open its `RECAP.html` for the five-minute version, or its
`README.md` for run-locally instructions.

## Run the demos (Node.js 18+ required)

```powershell
# WideTally (winner)
cd run-3
node serve.js            # product + landing page → http://localhost:8130

# ReconStock
cd run-1\_tools
npm install              # first time only (toolchain is not checked in)
node verify\server.js    # → http://localhost:8123

# DueCrew
cd run-2\_tools
npm install              # first time only
node verify\server.js 8231   # → http://localhost:8231
```

Videos are plain MP4s in each run's `video\` folder. To re-run the Playwright verification
suites or rebuild the videos, see each run's README (`npm install` + `npx playwright install
chromium` inside that run's `_tools\` first — `node_modules` is intentionally not committed).

## What "verified" means here

- Builders self-graded against a definition of done (`run-*/record/gap-analysis.md`).
- An orchestrating session then independently re-audited runs 2 and 3
  (`record/orchestrator-audit.md`): drove the demos with Playwright (run-3's import flow
  parsed 652 rows across 3 real dropped CSVs, zero errors), null-decoded and frame-inspected
  all videos, link-checked every recap, and re-fetched the load-bearing claims live — all
  verified verbatim against their sources.
- Post-verdict, the winner's two weakest evidence points were strengthened with fresh
  primary sources: [run-3/research/verification-addendum.md](run-3/research/verification-addendum.md).

## Honest framing

These are complete **packages**, not live businesses. The demos run on seeded/synthetic data
(labeled in-product); founders are fictional (disclosed); voiceovers are Windows TTS
(disclosed in-video). Each run's `record/honesty.md` lists everything simulated, assumed, or
unverifiable. The constraint set — no paid APIs, no publishing, no spending — is part of the
experiment's design, and the runs were built through repeated spend-limit terminations by
resuming from disk state (also disclosed).

*Built 2026-07-11 → 2026-07-13, autonomously, from a single prompt per run.*
