# company-builder

One goal prompt → a complete company, built autonomously with no human input mid-run.

An orchestrator agent read [MASTER_PROMPT.md](MASTER_PROMPT.md) and executed the full arc — hunt for pain on the open internet, run an idea tournament with adversarial fact-checking, design the business, build the brand, build the product, make the videos, red-team it, package it. The result is **ReconStock**: a safety-first inventory-sync concept for multi-store Shopify merchants (dry-run by default, diff preview before every write, anomaly circuit-breaker, one-click rollback), priced Free/$29/$49/$99 against a verified $10–60/mo incumbent band.

## The run in numbers

- **8 parallel research lanes** → 20 verified candidate problems → 4 finalists → unanimous 3–0 final vote
- **Adversarial verification caught real errors**: a misattributed stat and a candidate whose "willingness to pay" traced to synthetic AI-generated evidence — both documented, not hidden
- **Red team**: 33 attacks, 0 kills, 19 fixes applied, verdict VIABLE-WITH-FIXES
- **34 automated end-to-end checks** (Playwright) pass against the working product demo and landing page, verified on desktop and mobile
- **2 videos** produced fully locally (Playwright screen recording + TTS + ffmpeg)

## See it

`RECAP.html` doesn't render on github.com — clone and open it locally:

```powershell
git clone https://github.com/omprxkash/autonomous-multimodel-agent
cd autonomous-multimodel-agent\company-builder\run-1\_tools
npm install
npx playwright install chromium
node verify\server.js
```

Then open:
- **Recap (start here):** http://localhost:8123/RECAP.html
- **Product demo:** http://localhost:8123/product/
- **Landing page:** http://localhost:8123/site/

Full walkthrough and video/verification rebuild instructions: [run-1/README.md](run-1/README.md).

## Map

| Path | What's inside |
|---|---|
| [MASTER_PROMPT.md](MASTER_PROMPT.md) | The single prompt that produced everything below |
| [run-1/RECAP.html](run-1/RECAP.html) | Self-contained recap linking every artifact |
| [run-1/research/](run-1/research/) | Raw lane findings, candidates, verification, tournament, red team |
| [run-1/business/](run-1/business/) | Business plan, market research, 30-day launch plan |
| [run-1/brand/](run-1/brand/) | Name rationale, logo (+ candidates & critique), guidelines, exports |
| [run-1/product/](run-1/product/) | Working demo app (seeded data, full core workflow) |
| [run-1/site/](run-1/site/) | Landing page |
| [run-1/video/](run-1/video/) | launch.mp4, founder.mp4, scripts |
| [run-1/extras/](run-1/extras/) | Investor teaser, onboarding emails, premortem ("the review we must never earn") |
| [run-1/record/](run-1/record/) | Decision log, honesty file, gap analysis, verification screenshots |

## Honesty

This is a concept package, not a live business: the product demo runs on seeded data (no Shopify connection), the founder is fictional and labeled, the voiceover is TTS, and domains were checked but never bought. Every market claim traces to a fetched URL or is disclosed as an assumption — see [run-1/record/honesty.md](run-1/record/honesty.md).
