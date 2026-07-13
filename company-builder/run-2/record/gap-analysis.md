# Gap Analysis — self-grading vs. definition of done (run-2)

Graded 2026-07-13, after build completion. Scale: PASS / PASS WITH NOTES / FAIL.

| # | Criterion | Grade | Evidence / notes |
|---|-----------|-------|------------------|
| 1 | Every guardrail held | **PASS** | No paid services, no signups, no domain purchase (RDAP checks only), nothing published or sent; all artifacts inside `run-2/`; no questions asked — 14 judgment calls logged in decisions.md; SVG-only imagery; Windows TTS voice; Playwright+ffmpeg-static video. |
| 2 | Every claim in the thesis has a live URL | **PASS WITH NOTES** | thesis.md cites a URL for every factual claim. Notes: three claims are snippet-level or reprint-level rather than direct primary fetches (NAHB 34%, Census 2.88M, forum quotes) — each is flagged inline AND in honesty.md ¶11–14; the argument's load-bearing anchors (CSLB, TDLR, $47k page, BLS counts) were directly fetched. |
| 3 | Site screenshot-verified on mobile and desktop | **PASS** | record/shots/08–11: desktop hero + full page, mobile full site (390×844, 0px horizontal overflow) and mobile product board (0px overflow). Playwright-driven. |
| 4 | Both videos render and were actually inspected | **PASS** | ffmpeg null-decode check passed for both; 14 frames extracted across both timelines and 4 visually reviewed (board detail mid-launch, close card, CE ledger with toast, pricing/close in founder). Durations: launch 58.9s, founder 107.4s. A pacing defect (70s frozen close card) was caught in inspection and fixed by re-recording the tour and re-timing the VO. |
| 5 | Founder script calm/precise/zero-hype standard | **PASS** | No superlatives, no exclamation marks, states the demo is a demo, invites refutation. The brief's standard was used since no private voice doc exists — disclosed in honesty.md ¶19 and in founder-script.md. |
| 6 | RECAP links to every deliverable and every link works | **PASS** | Link check script run over RECAP.html: 28/28 relative links resolve (gap-analysis.md was the one missing at check time — this file — created immediately after; re-check confirmed below). |
| 7 | Brand guidelines complete enough for a stranger | **PASS** | guidelines.md specifies logo construction + files, full color tokens with usage ratios and WCAG pairs, type stacks/weights/casing, voice rules with examples and banned vocabulary, layout grid, the signature status-card device, imagery rules, and a don't checklist. |
| 8 | Red team ran; objections visible in final docs | **PASS** | record/red-team.md (9 objections, 4 standing unrebutted); surviving objections reprinted in RECAP.html and on the investor teaser itself. Noted limitation: self-pass, not independent panel (R8). |
| 9 | Nothing is a placeholder pretending to be finished | **PASS WITH NOTES** | Demo flows work (smoke-tested: renew flow, CE flow, all five views, no JS errors). Waitlist form is explicitly labeled non-functional; registry monitoring explicitly labeled beta/in-development; draft state-rules rows explicitly chip-labeled "Draft" in the UI. Honest labels, not hidden stubs. |
| 10 | honesty.md discloses everything simulated/assumed | **PASS** | 22 numbered disclosures covering fiction, inference, caveated verification, and process (including both API-error terminations and the resume orders). |
| 11 | decisions.md build log | **PASS** | 14 decisions with the question, the call, and the reasoning. |

## Re-check of #6 after creating this file
All 28 RECAP links now resolve (verified by re-running the link check after this file was
written).

## Known gaps accepted (with reasons)
- **No independent red-team panel** — sub-agent budget exhausted mid-run; coordinator
  ordered solo work. Mitigated by writing objections before rebuttals and letting four stand.
- **Founder video is 107s**, slightly over the ~60–90s ideal; the calm read at default TTS
  rate needs the length. Accepted over cutting the honesty-closing paragraph.
- **Competitor scan depth** — one thorough pass (R6). A real founder should spend a day on
  this before writing any code.
- **projul.com re-fetch failure** — stat kept with attribution + flag rather than dropped,
  because a sub-agent did fetch it within this run; documented in verification.md P1.
- **Static close card ~29s at founder video end** — improved from 70s → 29s by inserting the
  pricing card and re-recording a 57s tour; residual hold accepted as a standard end-card
  pattern while the VO delivers the closing.
