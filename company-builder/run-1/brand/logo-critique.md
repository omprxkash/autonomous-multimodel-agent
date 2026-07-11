# Logo Critique — ReconStock

Six candidates were designed (`brand/logo-candidates/candidate-1..6.svg`), then each was rendered at 16px (favicon), 64px, 256px, and full lockup at 1600px via sharp and inspected. Criteria: **(a)** legible at 16px favicon, **(b)** distinctive at billboard scale, **(c)** no clichés (no generic swoosh, no free-running sync loop), **(d)** works in one color.

## Candidate-by-candidate

### Candidate 1 — Shield Check (shield outline + checkmark)
- **16px:** Good. The shield silhouette survives; the check reads as a lighter notch.
- **Billboard:** Clean but anonymous — reads "security product," not "inventory sync."
- **Cliché risk:** **High.** Shield-with-check is the single most overused trust glyph (antivirus, VPNs, checkout badges, browser padlocks). Fails the distinctiveness bar.
- **One color:** Yes.
- **Verdict:** Rejected — generic; says "safe" without saying "sync" or "review."

### Candidate 2 — Mirrored Nodes (two nodes on a line + floating check)
- **16px:** Weak. The check floats detached from the node-line and at favicon size the composition collapses into "dumbbell plus smudge." The off-center vertical balance also wastes canvas.
- **Billboard:** The two-stores metaphor is nice and on-product, but the three loose elements never resolve into one shape.
- **Cliché risk:** Low.
- **One color:** Yes.
- **Verdict:** Rejected — poor cohesion, worst 16px performance of the six.

### Candidate 3 — Diff Brackets (facing brackets framing a checkmark)
- **16px:** **Best of the six.** Three strokes, all near-orthogonal, generous counters — the bracket-check silhouette is still readable at 16px in the actual render.
- **Billboard:** Distinctive and ownable. Brackets are the visual language of diffs and code review; a check *inside the review frame* is literally the product promise: nothing ships until it's been previewed and approved. No competitor in the space (Syncio, Stock Sync, Easify all use loops/arrows) uses this shape.
- **Cliché risk:** Low. It deliberately avoids the sync-loop cliché while still implying process.
- **One color:** Yes — pure stroke geometry, works in navy, white, or any single ink.
- **Verdict:** **Winner.**

### Candidate 4 — Loop Check (broken sync loop closing through a check)
- **16px:** Mediocre — the arrowheads turn to noise and it reads as a generic refresh icon.
- **Billboard:** Fine, but it is the category cliché: every sync app on the App Store is a circular-arrows mark. The check inside doesn't rescue it from looking like "refresh."
- **Cliché risk:** **Very high.**
- **One color:** Yes.
- **Verdict:** Rejected — the exact visual territory competitors already occupy.

### Candidate 5 — Scope Sync (recon crosshair/target with arrow)
- **16px:** Poor — five elements (ring, four ticks, center dot, arc, arrowhead) alias into mush.
- **Billboard:** The "recon scope" pun is clever, but crosshairs carry aiming/weapon connotations — wrong emotion for a brand whose job is RELIEF. Too busy overall.
- **Cliché risk:** Medium (location-pin/target territory).
- **One color:** Yes.
- **Verdict:** Rejected — emotionally off-brand and over-detailed.

### Candidate 6 — Chevron Interlock (facing chevrons meeting at a point)
- **16px:** **Fails.** In the actual 16px render it reads as a letter **X** — the exact opposite of "verified/safe." A brand about nothing going wrong cannot have an error glyph as its favicon.
- **Billboard:** Bold and minimal, but the X reading persists at every size.
- **Cliché risk:** Low.
- **One color:** Yes.
- **Verdict:** Rejected — catastrophic misreading.

## Winner and refinement

**Candidate 3 (Diff Brackets) wins.** It is the only mark that is simultaneously on-product (diff preview → approval), emotionally right (a calm "approved" inside a careful frame), category-distinctive (no loops/arrows/shields), and technically robust at 16px in one color.

Refinements applied in `brand/logo.svg` / `brand/logo-dark.svg`:
1. **Tightened bracket geometry:** bracket arms lengthened from 14→15 units and the frame extended to y=13–67, so the brackets claim the full cap-height of the wordmark and the internal whitespace is a balanced optical square.
2. **Re-balanced the check:** endpoints nudged (28,42 → 37,53 → 54,27) so the check's optical center sits at the center of the bracket frame instead of drifting low-left, and its terminal no longer crowds the right bracket.
3. **Consistent stroke system:** single 7-unit stroke, round caps/joins everywhere — one stroke weight means the mark scales as a system and can be re-cut at heavier weight for sub-24px favicon use if needed.
4. **Wordmark spec:** Inter Bold (with Arial fallback in the SVG), +0.3 letter-spacing, baseline aligned to the mark's optical midline. Two-word camel-case "ReconStock" kept as a single set word.
5. **Dark variant:** pure white (#FFFFFF) strokes/text for navy or dark UI backgrounds — no color remapping tricks, guaranteed AA on the brand navy.
