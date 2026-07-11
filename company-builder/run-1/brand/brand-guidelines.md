# ReconStock Brand Guidelines

Version 1.0 — 2026-07-11

---

## 1. Brand Story

Every merchant running more than one Shopify store knows the specific dread of an inventory sync tool: it works silently, until the morning it doesn't — and 2,000 SKUs read zero, oversells stack up, and nobody can say what changed or when. The incumbent tools are trusted the way a tightrope is trusted: they hold, but you never stop watching. ReconStock exists to remove that watchfulness. The name says the method — *recon* before action, *reconcile* before trust — and the product enforces it: every sync shows a human-readable diff first, runs as a dry run, can be rolled back in one click, and a circuit breaker halts anything anomalous before it lands ("about to zero 2,000 SKUs — halted").

ReconStock's emotional job is relief and control, in that order. We are not the fastest sync, the cleverest sync, or the most automated sync — we are the sync that never surprises you. The brand therefore behaves like a good operations manager: it shows its work, states numbers precisely, warns early, and never celebrates doing its job. Everything we ship — copy, color, iconography, UI — should make an operator's shoulders drop half an inch. Nothing bad happens here, and when something *would* have, you'll see exactly what we stopped.

## 2. Voice

**Calm. Precise. Zero hype.** We are the brand of "nothing bad happens." The voice sounds like a competent colleague reading from real data — never a marketer, never an alarmist. Rules: state numbers, name the action, prefer verbs of verification (*previewed, reconciled, held, rolled back*), never exclaim, never blame the user, never use fear as a sales lever (we relieve fear; we don't manufacture it).

| # | Don't write | Do write |
|---|---|---|
| 1 | "🎉 Sync complete! Everything went perfectly!" | "Sync complete. 412 SKUs updated, 0 skipped. View the diff." |
| 2 | "WARNING!!! Your inventory may be corrupted!" | "Held: this sync would set 2,014 SKUs to zero. Nothing was changed. Review and approve, or dismiss." |
| 3 | "Blazing-fast, AI-powered, next-gen inventory magic." | "Every sync is previewed, dry-run, and reversible." |
| 4 | "Oops! Something went wrong 😅" | "Sync paused at step 3 of 5: the source store returned an error. Your inventory was not modified. Retry or roll back." |
| 5 | "Trust us — set it and forget it!" | "You approve the first sync. After that, the circuit breaker watches every one." |

## 3. Color Palette

Safety-green on deep-navy family. All "text use" pairings below meet **WCAG 2.1 AA** (≥ 4.5:1 for body text; ≥ 3:1 for large text/UI glyphs).

### Primary — Deep Navy
| Token | Hex | Use | Contrast |
|---|---|---|---|
| `navy-900` | `#0E2A47` | Brand color: logo, headings, primary buttons (white text) | 12.7:1 on white; white text on it 12.7:1 — AA/AAA |
| `navy-700` | `#1E4062` | Hover states, secondary emphasis | 9.0:1 on white — AA |

### Accent — Safety Green (the "verified" color)
| Token | Hex | Use | Contrast |
|---|---|---|---|
| `green-700` | `#166534` | Success text, "sync verified" labels on light backgrounds | 6.7:1 on white — AA body text |
| `green-500` | `#16A34A` | Success icons, badges, charts — **large text and glyphs only**, never body text on white | 3.3:1 on white — AA large-text/UI only |
| `green-300` | `#4ADE80` | Success text/icons **on navy backgrounds** | 7.7:1 on `navy-900` — AA |

### Neutrals
| Token | Hex | Use | Contrast |
|---|---|---|---|
| `ink-900` | `#0F172A` | Body text | 16.9:1 on white — AAA |
| `slate-600` | `#475569` | Secondary text, captions | 7.5:1 on white — AA/AAA |
| `slate-300` | `#CBD5E1` | Borders, dividers (non-text) | — |
| `mist-50` | `#F8FAFC` | App background | — |
| `white` | `#FFFFFF` | Cards, dark-variant logo | — |

### Danger & Warning (used sparingly — this brand rarely shouts)
| Token | Hex | Use | Contrast |
|---|---|---|---|
| `red-700` | `#B91C1C` | Destructive-action text, halted-state labels | 6.5:1 on white — AA |
| `amber-700` | `#B45309` | Caution text ("review before approving") | 4.6:1 on white — AA |

Rules: green means *verified*, never decoration. Red appears only when the product has **already protected you** (halted, held, rolled back) or when an action is destructive — never as ambient urgency. Most of the UI is navy + neutrals; a calm screen is the brand working.

## 4. Typography

Free Google Fonts only.

- **UI / marketing sans: [Inter](https://fonts.google.com/specimen/Inter)** — designed for screens at UI sizes, with a tall x-height and open apertures that stay legible in dense tables and 12px labels; its tabular-figures feature (`font-feature-settings: "tnum"`) keeps SKU counts and quantities column-aligned, which a numbers-heavy trust product needs. Weights: 400 (body), 500 (labels), 700 (headings, wordmark).
- **Mono / data & diffs: [JetBrains Mono](https://fonts.google.com/specimen/JetBrainsMono)** — used for SKU codes, quantities in diff views, log excerpts, and before→after values. Chosen over Roboto Mono for its clearly distinguished `0/O` and `1/l/I` (operators must never misread a SKU) and slightly wider counters that hold up at small sizes. Weights: 400, 700 (changed values in diffs).

Pairing rule: anything a human *reads* is Inter; anything a human *verifies* (IDs, counts, diffs) is JetBrains Mono. This split is itself a trust signal — data always looks like data.

## 5. Logo Usage

Files: `brand/logo.svg` (light backgrounds), `brand/logo-dark.svg` (navy/dark backgrounds), PNG exports in `brand/exports/` (32/180/512/1024 px).

1. **Clear space:** keep a margin equal to the height of the bracket mark's check stroke (≈ 25% of logo height) on all sides. Nothing enters it.
2. **Minimum sizes:** full lockup ≥ 96px wide. Below that, use the bracket-check mark alone (it is the favicon at 16–32px).
3. **Color:** one color only — `navy-900` on light, `#FFFFFF` on dark. Never gradient, never multicolor, never green (green is reserved for verified states in the UI, not identity).
4. **Backgrounds:** light logo on white/`mist-50`; dark variant on `navy-900` or photography darker than 50% luminance. Never place either on busy imagery without a solid backing panel.
5. **Don'ts:** don't rotate, skew, outline, shadow, or animate the mark; don't restyle the wordmark in another font; don't separate the check from its brackets (an unframed check is not our mark — the frame *is* the promise); don't add "app," "sync," or taglines to the lockup.

## 6. Iconography Style

Match the logo's construction so every icon feels like part of the mark:

- **Stroke icons, 2px at 24px grid** (scale stroke proportionally), round caps and round joins — identical to the logo's stroke grammar.
- **Geometry first:** orthogonals and simple arcs; no freehand curves, no filled blobs, no 3D, no swooshes.
- **One color per icon:** `navy-900`/`ink-900` default; `green-700` only for verified/success; `red-700` only for halted/destructive; `amber-700` for review-needed.
- **Motifs to reuse:** brackets (preview/review), checkmark (verified), pause bars (held/circuit breaker), counter-clockwise arc with square terminus (rollback — deliberately *not* a full loop), two aligned nodes (stores in sync).
- **Motifs to avoid:** circular refresh arrows (the category cliché), shields, padlocks, warning triangles with exclamation marks (use the pause/held motif instead — our warnings are calm holds, not alarms), lightning bolts, sparkles/AI glitter.
- **Corner radius:** 2px at 24px grid on rectangular shapes, matching the logo's rounded joins.
