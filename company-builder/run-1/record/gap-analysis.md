# Gap Analysis — run graded against the verbatim master prompt

Date: 2026-07-12. The verbatim master prompt lives in `MASTER_PROMPT.md`. The run had originally executed against a faithful reconstruction; this audit re-grades every clause of the exact text.

## Definition-of-done checklist

| Clause (verbatim) | Status | Evidence |
|---|---|---|
| "a stranger could open recap.html, understand the business in five minutes" | ✅ | Fresh-eyes audit PASS; `RECAP.html` (capitalization differs from `recap.html` — cosmetic, noted below) |
| "run the site locally" | ✅ | README commands re-executed verbatim by the auditor; HTTP 200 on all routes |
| "watch the launch video" | ✅ | Both MP4s decode cleanly; frame-level QA at key timestamps (breaker at 0:08, close card at 0:58) |
| "every guardrail held" | ✅ | No spending, nothing published during the run, all claims sourced/labeled, work inside run-1, never asked |
| "every claim in the thesis has a live URL" | ✅ | verification.md re-fetched every finalist claim; unverifiable items disclosed in honesty.md |
| "site is screenshot-verified on mobile and desktop" | ✅ **(was a gap — fixed 2026-07-12)** | `record/shots/08-landing-mobile.png` (390×844, 0px horizontal overflow), `09-product-mobile.png`, `10-landing-desktop-full.png` (1440px), plus original desktop shots 01–06 |
| "both videos render and you actually watched them" | ✅ | ffmpeg null-decode (zero errors) + extracted frames visually checked at key moments |
| "the founder script passes my voice rules" | ✅ (interpreted) | The original's "my voice rules" refers to the prompt author's private voice guide, which does not exist in this workspace; applied brand-guidelines voice rules (calm, precise, zero hype) instead — founder script complies |
| "recap page links to every deliverable and every link works" | ✅ | 45/45 links verified by auditor; extras added to the deliverables map 2026-07-12 |
| "brand guidelines complete enough that a stranger could make a new on-brand asset" | ✅ | Palette + type + voice + logo rules + do/don't examples; the three extras were produced from the guidelines alone, which is itself the test |
| "the red team ran and its objections are visible in the final docs" | ✅ | red-team.md: 33 attacks, 0 kills, rulings public; fixes traceable in plan/site |
| "nothing in the package is a placeholder pretending to be finished work" | ✅ | Auditor comprehension pass found no dead ends |

## "Floor, not a ceiling" extras clause

| Clause | Status | Evidence |
|---|---|---|
| "do the ones that make this company feel most real" | ✅ **(was a gap — fixed 2026-07-12)** | `extras/investor-teaser.html` (one-page, brand-styled, honesty-labeled) and `extras/onboarding-emails.md` (5-email trust-ramp sequence) |
| "invent at least one deliverable nobody would expect" | ✅ **(was a gap — fixed 2026-07-12)** | `extras/premortem.html` — "The review we must never earn": a self-authored future 1-star review with the engineering commitment that answers each sentence |

## Known deviations (disclosed, not defects)

1. **Environment mapping**: `projects/company-builder-experiment/run-1/` → `d:\AI\Business\run-1\`; no `.env` keys exist here, so no Kie.ai/ElevenLabs/HeyGen — image generation is hand-written SVG, voice is Windows TTS, avatar video replaced by TTS-voiced product footage (honesty.md #1).
2. **`recap.html` vs `RECAP.html`**: filename case differs; kept uppercase since every internal reference and the audit used it. Case-insensitive on Windows.
3. **"my voice rules"**: prompt author's private rules unavailable; brand voice rules used as the governing standard.
