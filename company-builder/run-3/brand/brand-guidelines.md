# WideTally — Brand Guidelines v1.0
2026-07-13. Complete enough for a stranger to produce a new on-brand asset without asking anyone anything.

## 1. What WideTally is (positioning)
A local-first royalty and ad-ROI ledger for self-published authors. **"Every store. One ledger. Your machine."**
The brand's job: feel like a well-kept paper ledger operated by someone you'd trust with your bank statement — because the whole pitch is that we *never see it*.

## 2. Brand personality — four words
**Calm. Precise. Bookish. Private.**
- Calm: no urgency mechanics, no countdown timers, no exclamation marks.
- Precise: numbers are the hero; always tabular, always reconciled, estimates always labeled "est."
- Bookish: serif headlines, generous margins, paper-warm backgrounds. We sell to people who love books.
- Private: never ask for data we don't need; say "your machine," "your files," "nothing uploads" plainly and often.

## 3. Logo
- **Primary lockup** (`logo.svg`): four upright tally strokes + one diagonal brass stroke (the classic "count of five" — one stroke per major store) beside the serif wordmark. The diagonal ends in a pen-nib flick: counting done by hand, by a writer.
- **Mark only** (`logo-mark.svg`): navy rounded square, cream strokes, brass diagonal. Use at ≤64px, as favicon/app icon.
- Clear space: one stroke-width (9 units) on all sides. Don't rotate, outline, gradient, or recolor the mark outside the palette. On dark backgrounds use the mark or set the wordmark in Paper (#FAF6EF) with brass "Tally" unchanged.

## 4. Color
| Token | Hex | Use |
|---|---|---|
| **Ink** | `#16324F` | Primary text, headers, the four tally strokes, dark surfaces |
| **Paper** | `#FAF6EF` | Page background (light), text on Ink |
| **Brass** | `#B8862D` | THE accent: CTAs, links, the diagonal stroke, key numbers. Use `#D9A93F` for brass on dark surfaces |
| **Ledger Green** | `#1E7A46` | Positive money deltas only |
| **Ledger Red** | `#A63A2B` | Negative money deltas only |
| **Slate** | `#5B6B7C` | Secondary text, captions, table rules |
| **Line** | `#E5DCC9` | Hairlines, card borders on Paper |

Rules: Brass is never body text. Green/Red are *semantic only* (money direction), never decorative. Charts: Ink for primary series, Brass for comparison, Slate for context; one hue per meaning. Backgrounds are Paper or Ink — never pure white or pure black.
Accessibility: Ink on Paper = 10.9:1; Slate on Paper = 4.9:1; Paper on Ink = 10.9:1. Brass `#B8862D` on Paper is 3.4:1 — large text (≥19px bold / 24px) and graphics only; body-size brass links must be underlined. On Ink, use `#D9A93F` (5.0:1).

## 5. Typography (system stacks only — no webfont dependency, matches local-first ethos)
- **Headlines / wordmark:** `Georgia, 'Iowan Old Style', 'Times New Roman', serif`. Weight normal; sizes 28–56px; tight-ish leading (1.15); never all-caps.
- **UI & body:** `'Segoe UI', system-ui, -apple-system, sans-serif`. Body 16–17px/1.6.
- **Numbers & data:** same sans with `font-variant-numeric: tabular-nums` mandatory in any table/stat; money always 2 decimals with currency code or symbol; negative money in Ledger Red with a true minus (−), not a hyphen.
- **Eyebrow/label style:** 12–13px, letter-spacing 0.18em, uppercase, Slate.

## 6. Voice
- Sentences short. Verbs active. Zero hype adjectives ("revolutionary," "game-changing" banned).
- Numbers do the persuading: "ScribeCount is $185 a year. WideTally is $59 once."
- Say the quiet parts: estimates labeled, limitations stated ("KU pages are estimates until Amazon posts the fund rate — every tool works this way; we just say so").
- Privacy phrasing is concrete, never mystical: "Your reports are parsed on your machine. Open devtools — there's no network tab activity to find."
- We respect the reader's time the way the product does: headings scannable, one idea per paragraph.

### Sample copy (calibration)
✅ "Drop in last month's KDP file. Fifteen seconds later you know which series paid rent."
❌ "Unlock powerful AI-driven insights to supercharge your author business! 🚀"

## 7. Imagery & illustration
- No stock photos, no fake screenshots, no photorealistic AI images.
- Illustration language: flat SVG in the palette; ledger lines, tally strokes, book spines, folder/file glyphs. 1.5–2px stroke weight, rounded caps, minimal detail.
- Product screenshots always show the real UI with the synthetic sample library ("Halloran Bay" series etc.) — never mock numbers into a screenshot.

## 8. Layout
- Paper background, max content width 1080px, generous whitespace (48–96px section gaps).
- Cards: Paper surface, 1px Line border, 10px radius, no drop shadows heavier than `0 1px 2px rgba(22,50,79,.06)`.
- Data tables: hairline rules only (Line), row hover in `#F3ECDD`, right-aligned numerals.
- CTAs: Brass fill, Paper text, 8px radius; secondary = Ink outline.

## 9. Naming & product terms
- "WideTally" one word, capital W and T. The app tiers: **WideTally Lite** (free, 2 books) and **WideTally License** ($59). "Format Updates Pass" ($19/yr).
- Views inside the app: **Ledger** (dashboard), **Books**, **Ads**, **Imports**. Call reports "your files," never "uploads."
- Never say: "sync," "cloud," "account," "login" (we have none of these); "users" in customer-facing copy (say "authors").
