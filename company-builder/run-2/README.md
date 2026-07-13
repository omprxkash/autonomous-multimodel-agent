# run-2 — DueCrew

Autonomous company-building experiment, run 2 (2026-07-12/13). The business built:
**DueCrew** — a compliance deadline guard for solo licensed trade contractors (license
renewals, CE hours, COI/bond expirations, escalating alerts).

**Start here: [RECAP.html](RECAP.html)** — the business in five minutes, links to every
deliverable, how to run everything, and why a skeptic might pass.

Quick run:
```
cd _tools
npm install            # playwright + ffmpeg-static (only for re-verification/re-render)
node verify/server.js 8231
# site:    http://localhost:8231/site/
# product: http://localhost:8231/product/
```
Both pages also open directly from disk (`site/index.html`, `product/index.html`).

Videos: `video/launch.mp4` (59s) and `video/founder.mp4` (107s, TTS-voiced, disclosed).

Honesty ledger: `record/honesty.md`. Red team: `record/red-team.md`. Build log:
`record/decisions.md`. Self-grading: `record/gap-analysis.md`.
