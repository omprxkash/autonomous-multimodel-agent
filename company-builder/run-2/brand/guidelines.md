# DueCrew — Brand Guidelines v1.0

Complete enough to build a new on-brand asset from this file alone.

---

## 1. The idea

DueCrew is the tradesperson's side of the table. GCs have compliance departments; our user
has a glovebox. The brand behaves like a **good foreman**: calm, specific, watching the
clock so you don't have to. Never panicked, never cute about consequences, never corporate.

Brand line: **"We watch the dates so you can work."**
Product question the brand always answers: **"Am I good to work?"**

## 2. Logo

**Mark:** a high-vis **hex nut** (flat-top hexagon outline, rounded corners) containing a
bold **checkmark**. Hex = trades hardware; check = good standing. Files:
- `logo-mark.svg` — hex+check, amber on navy tile (app icon / favicon / avatar)
- `logo-lockup.svg` — mark + wordmark, horizontal (site header, documents)
- `logo-wordmark.svg` — wordmark only (tight spaces)

**Wordmark:** "DueCrew" set in the heading stack at weight 800, tight tracking (-0.02em).
"Due" in Amber 500, "Crew" in Ink 900 on light / Paper 50 on dark. No space, both capitals.

**Rules:** clear space = height of the hex's flat side on all sides. Minimum mark size
16px. Never rotate the hex to point-top (point-top = warning sign, wrong message). Never
put the amber mark on white without the navy tile (contrast fails). Never add a shadow,
gradient, or outline to the wordmark.

## 3. Color

| Token | Hex | Use |
|-------|-----|-----|
| Navy 900 `--ink` | `#101B2C` | Primary dark surface, wordmark on light |
| Navy 700 | `#1B2B45` | Cards on dark, secondary surfaces |
| Paper 50 | `#F7F5F0` | Light background (warm off-white — paper, not clinic) |
| Paper 100 | `#EDEAE2` | Light secondary surface / dividers |
| Amber 500 (High-Vis) | `#F5A623` | THE brand accent: CTAs, "Due" in wordmark, mark fill |
| Amber 600 | `#D98E0B` | Hover/pressed amber, amber text on light backgrounds |
| Green 500 (Good) | `#2E9E5B` | "Good" status only |
| Amber 500 doubles as "Watch" status | | |
| Red 500 (Lapse) | `#D64545` | "Act now"/lapsed status only |
| Slate 400 | `#8A94A6` | Secondary text on dark |
| Slate 600 | `#55617A` | Secondary text on light |

Ratios: dark surfaces dominate product; light (Paper) dominates marketing/print. Amber is
≤10% of any layout — it must stay rare enough to mean something. Status colors are
reserved for status; never use green/red decoratively.

Accessibility: body text pairs must clear WCAG AA — Paper 50 on Navy 900 (13.9:1), Ink on
Paper 50 (13.4:1), Amber 500 on Navy 900 (7.8:1 — fine for text ≥14px bold), Amber 600 on
Paper 50 for amber text on light. Never amber-on-paper at 500 weight/small size.

## 4. Type

- **Headings:** `"Segoe UI", -apple-system, Roboto, "Helvetica Neue", Arial, sans-serif`
  at weight 800, tracking -0.02em. Sentence case ("Am I good to work?"), never Title Case,
  ALL-CAPS only for tiny eyebrow labels (11px, +0.08em tracking, Slate).
- **Body:** same stack, weight 400, 1.55 line-height, 16–18px.
- **Numbers/dates (status cards, countdowns):** `"Consolas", "SF Mono", monospace` weight
  700 — dates are the product; they get the "machined" treatment.
- No external font loads anywhere (assets must be self-contained).

## 5. Voice

Write like a good foreman. Rules:
1. Short sentences. One clause where one clause will do.
2. Concrete over abstract: "9 days" not "soon"; "$47,000 withheld" not "significant impact."
3. Never scare-sell. State the consequence once, in plain words, cite it, move on.
4. Trade-respectful: the reader runs a business with their hands. No "we make compliance
   delightful!", no emoji, no exclamation marks in product copy.
5. Say "you're good" when they're good. The brand celebrates green quietly.
6. Product tone in one line each — Good: "Good through Mar 2028." Watch: "COI expires in
   21 days. Your agent needs about a week." Act: "9 days. Renew today — here's the link."

Vocabulary: "card," "ticket" (sparingly), "good standing," "board," "crew," "lapse."
Banned: "seamless," "supercharge," "peace of mind" (show it, don't say it), "revolutionary,"
"all-in-one" (we are pointedly one-thing).

## 6. Layout & imagery

- Grid: 12-col, max 1080px content width, 8px spacing scale.
- Corners: 10px radius on cards, 8px on buttons; never pill-shaped buttons.
- The signature graphic device is the **status card**: left status bar (4px), credential
  name, monospace date, days-left chip. When in doubt, the asset is a status card.
- A subtle "blueprint" background texture (1px Navy 700 grid lines at low opacity on navy)
  is permitted on dark hero surfaces only.
- Imagery: hand-drawn/flat SVG only in this run (no stock, no fake photos). Depict tools,
  vans, cards, calendars — never cartoon people, never hard-hat clip-art clichés.
- Print assets (Lapse Math sheet): Paper 50 background, Ink text, single amber accent,
  designed to photocopy legibly in pure black-and-white.

## 7. Naming & product terms

Product = "DueCrew" (never "Due Crew" or "Duecrew"). The main screen = "the board."
Statuses = Good / Watch / Act (exactly these three words). Plans = Solo, Crew, Founding
member. Alerts are "nudges" internally, "alerts" in public copy.

## 8. Don'ts (fast checklist)

✗ Point-top hexagon ✗ Amber >10% of layout ✗ Status colors as decoration ✗ Title Case
headings ✗ External fonts/CDNs ✗ Exclamation marks ✗ "Peace of mind" ✗ Fear-mongering
imagery (no red sirens) ✗ Shadow/gradient on wordmark ✗ Cartoon tradespeople
