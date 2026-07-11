# ReconStock — Launch video script

Fast-paced product demo, ~45 seconds, 1280×720. Music bed only (no narration —
the copy is carried on title cards and by the UI itself). Voice rules per
brand-guidelines.md: state numbers, name actions, never exclaim, never
manufacture fear (the disaster shown is the one the product *stopped*).
Red-team rules honored: no "never fails" claim; the promise is fails-safe +
reversible; the breaker and rollback lead, not the diff table.

| # | Beat | Visual | On-screen copy | ~Time |
|---|------|--------|----------------|-------|
| 1 | Hook | Title card, navy, mono type | "09:12 AM. An incoming sync just tried to zero **2,143 SKUs**." / "Here is what didn't happen next." | 0:00–0:04 |
| 2 | Breaker halts it | UI: flagged sync → circuit-breaker halt screen, hold on the headline and the 2,143 / EU Store / 97% stats | (UI carries it: "Halted: this sync would zero 2,143 SKUs across EU Store — review before applying.") | 0:04–0:14 |
| 3 | Diff preview | UI: normal pending sync → diff table, old qty → new qty, sources; dry-run report "0 writes made" | (UI: diff table + "Dry run complete — 0 writes made.") | 0:14–0:24 |
| 4 | Rollback | UI: audit log → one-click Rollback → status flips to "Rolled back", dashboard quantities restore | (UI: audit log + toast "Rolled back — quantities restored.") | 0:24–0:33 |
| 5 | Tagline | Title card, logo | "Every sync is previewed, dry-run, and reversible." | 0:33–0:37 |
| 6 | Pricing | Title card | "Free — dry-run, diff, audit log · Standard $29 · Pro $49 · Scale $99" | 0:37–0:42 |
| 7 | Close | Title card, dark, logo | "ReconStock. The sync that shows every change before it writes — and lets you undo it." | 0:42–0:46 |

Music: subtle ambient pad, gentle fade in/out, no percussion.
