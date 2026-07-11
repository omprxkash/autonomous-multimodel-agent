# ReconStock — Run the demo (Windows)

Two deliverables live in this folder, both fully local (no CDNs, no network assets):

- `product\` — the ReconStock app demo (Sync Console) with seeded data
- `site\` — the marketing landing page

Both are static HTML/CSS/JS. They need a local web server (opening `index.html` directly via `file://` blocks `localStorage` in some browsers). A tiny Node server is included — Node.js is the only requirement (already used by `_tools\`).

## 0. First-time setup (only if `_tools\node_modules` is missing)

If you cloned this from a repository, the toolchain isn't checked in. Install it once:

```powershell
cd <this-folder>\_tools
npm install
npx playwright install chromium
```

(Node.js 18+ required. The paths below assume `d:\AI\Business\run-1` — substitute your clone location.)

## 1. Start the server

Open PowerShell (or Command Prompt) and run:

```powershell
cd d:\AI\Business\run-1\_tools
node verify\server.js
```

You should see:

```
ReconStock demo server running at http://localhost:8123/
  Product demo: http://localhost:8123/product/
  Landing page: http://localhost:8123/site/
```

Leave it running. (Different port: `node verify\server.js 9000`.)

## 2. Open the deliverables

- **Product demo:** http://localhost:8123/product/
- **Landing page:** http://localhost:8123/site/

### Product demo — suggested walkthrough (the core flow)

1. **Dashboard** — 2 connected stores, ~30 SKUs of live inventory, sync status, recent activity.
2. **Diff preview** — under *Pending syncs*, click **Review diff** on "Daily inventory pull". Every proposed change is listed: SKU, store, old qty → new qty, source.
3. **Dry-run** — click **Run dry-run**: the sync runs against live data, writes nothing, and produces a report (exportable as CSV).
4. **Approve** — switch off the *Dry-run mode* toggle, then **Approve & apply live**. Watch the inventory table update (changed rows flash green).
5. **Circuit breaker** — back on the dashboard, click **Review sync** on the flagged "Bulk restock import". ReconStock halts it before any write: *"Halted: this sync would zero 2,143 SKUs across EU Store."* Dismiss it (force-apply is deliberately locked).
6. **Rollback** — open **Audit Log & Rollback**, click **Rollback** on the applied sync. Quantities visibly restore on the dashboard.

State persists in `localStorage`. Use **Reset demo data** (top right) to restore the original seed at any time.

## 3. Re-run the verification script

The Playwright script serves both deliverables, drives the full flow above (dashboard → diff → dry-run → approve → circuit breaker → rollback → landing page), asserts 34 checks, and saves screenshots.

```powershell
cd d:\AI\Business\run-1\_tools
node verify\verify.js
```

- Expected final line: `ALL CHECKS PASSED — screenshots in record/shots/` (exit code 0).
- Screenshots land in `d:\AI\Business\run-1\record\shots\`:
  `01-dashboard.png`, `02-diff-preview.png`, `03-circuit-breaker.png`, `04-rollback.png`, `05-landing-hero.png`, `06-landing-pricing.png`
- The script starts its own server on port 8123 — stop `server.js` first if it's already using that port.
- Playwright + Chromium are preinstalled in `_tools\node_modules`. If Chromium is ever missing: `cd d:\AI\Business\run-1\_tools; npx playwright install chromium`.
- Mobile/desktop screenshot verification: with `server.js` running, `node verify\mobile-shots.js` captures `08-landing-mobile.png` (390×844), `09-product-mobile.png`, `10-landing-desktop-full.png` and reports mobile horizontal overflow (expected: 0px).

## Videos

- `video\launch.mp4` — ~46s fast product demo (hook card → circuit-breaker halt → diff preview + dry-run → rollback → tagline/pricing/close cards), ambient music bed.
- `video\founder.mp4` — ~60s calm founder voiceover (Windows TTS, Microsoft Zira) over title cards + a slow product tour, music low under the voice.
- How they were made (fully local): scripts in `video\*-script.md`; footage recorded with Playwright `recordVideo` (`_tools\video\record.js`), voiceover via Windows System.Speech (PowerShell), music synthesized by `_tools\video\make-music.js`, assembled with ffmpeg-static by `_tools\video\assemble.js`.
- Rebuild: `cd d:\AI\Business\run-1\_tools` then `node video\record.js`, `node video\make-music.js`, `node video\assemble.js`.

## Extras (beyond the required deliverables)

- `extras\investor-teaser.html` — one-page investor teaser (brand-styled, honesty-labeled; open via the server: http://localhost:8123/extras/investor-teaser.html).
- `extras\onboarding-emails.md` — 5-email onboarding sequence mirroring the product's trust ramp (read-only → dry-run → supervised sync → convert).
- `extras\premortem.html` — "The review we must never earn": a self-authored future 1-star review, each sentence answered by an engineering commitment.

## Notes

- ReconStock is a concept demo: seeded data, no live Shopify connection, and the landing page's founder is fictional (disclosed on the page). The merchant quotes in the "problem" section are real public app-store reviews of *other* apps, linked to their sources.
- Brand palette/type follow `brand\brand-guidelines.md`; since the build is fully offline, Inter and JetBrains Mono are approximated with system font stacks (Segoe UI / Consolas-family).
