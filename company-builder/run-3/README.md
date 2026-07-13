# WideTally — Run 3 of the autonomous company-building series

**WideTally** is a local-first royalty & ad-ROI ledger for self-published authors who sell beyond Amazon. It parses the report files authors already download (KDP, KENP, Draft2Digital, Kobo, Amazon Ads) entirely on their machine — no upload, no password, no subscription. $59 once. Built end-to-end in this run: verified research → business plan → brand → working demo → landing page → videos → red team.

> Start at **RECAP.html** — it links every deliverable with context.

## Run it locally
Requires Node.js (any recent version). No dependencies for the server.

```
cd run-3
node serve.js
```
Then open:
- **http://localhost:8130/site/** — marketing landing page
- **http://localhost:8130/product/** — the working demo (click "Load sample library", or drag the CSVs from `product/sample-data/` onto the Imports tab)
- **http://localhost:8130/** — RECAP (project overview)

Videos: `video/launch.mp4` (54s) and `video/founder.mp4` (64s, TTS-voiced — disclosed).

## What's where
| Path | Contents |
|---|---|
| `RECAP.html` | Five-minute overview linking everything |
| `research/` | Four lane hunts, idea tournament, skeptic verification (every load-bearing claim re-fetched) |
| `business/` | Business plan, pricing rationale, 30-day launch plan, **Report Format Registry** (the unexpected deliverable) |
| `brand/` | Logo SVGs, full brand guidelines |
| `product/` | The demo app (static HTML/CSS/JS) + synthetic sample data |
| `site/` | Landing page |
| `video/` | Both videos, assets, founder script |
| `record/` | decisions.md, honesty.md, red-team.md, gap-analysis.md, screenshots, extracted video frames |
| `_tools/` | Data generator, reddit research fetcher, screenshot/record/assemble scripts (Playwright + ffmpeg-static) |

To rebuild media: `cd _tools && npm install`, then `node video/make-music.js`, `powershell -File video/make-vo.ps1`, `node video/record.js`, `node video/assemble.js`. Screenshots: `node screenshot.js`.

## Honesty
This is a research artifact: the company is fictional, sample data is synthetic (labeled), voiceover is Windows TTS (disclosed on-screen), and every external claim traces to a URL fetched during the run. Full disclosures: `record/honesty.md`. Objections a skeptic should read first: `record/red-team.md`.
