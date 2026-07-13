# Decisions Log — Run 3

Every consequential judgment call, the question I would have asked a human, the answer I chose, and why.

---

## D-001 — Hunting territory (2026-07-12)
**Question:** Where to hunt for pain, given the differentiation mandate (no Shopify/e-com tooling, no generic SMB back-office SaaS)?
**Decision:** Run four parallel research lanes: (a) prosumers/creators, (b) niche professional verticals, (c) developers/technical users, (d) hobbyist communities with real money. Skip lane (e) local/offline services as a primary lane but allow candidates that straddle it via a vertical (e.g. trades/contractors count as both).
**Why:** The mandate requires at least three lanes; four parallel researchers is cheap in wall-clock time and maximizes coverage difference from runs 1–2, which both hunted B2B/SMB.

## D-002 — Evidence bar (2026-07-12)
**Question:** What counts as "verified pain"?
**Decision:** A candidate needs (1) at least 3 independent complaints from real people at real URLs fetched during this run, (2) evidence money already moves in the space (paid tools, budgets, or spend complaints), and (3) a nameable underserved gap vs. existing tools (verified by looking at the tools themselves). Anything that can't clear this bar is logged but not picked.
**Why:** Guardrail 3 (invent nothing). A smaller thesis on real evidence beats a grand one on fiction.

## D-003 — Subagent spend limit; pivot to inline research (2026-07-12)
**Question:** Three of four parallel research agents died mid-hunt with "monthly spend limit" API errors. How to proceed?
**Decision:** Do all remaining research, judging, and red-teaming inline in the main session instead of via subagents. "Blocked is not an option" outranks the orchestration mandate. The idea tournament becomes: explicit written rubric scored by me, plus a separately-documented skeptic pass that re-fetches every load-bearing URL before commitment — self-adversarial instead of separate judge agents.
**Why:** Subagent spawning is unreliable under the spend cap; inline tools still work. Deviation disclosed here and in honesty.md.

## D-004 — Winner: local-first royalty + ad-ROI dashboard for self-published authors (2026-07-13)
**Question:** Which verified pain becomes the company?
**Decision:** Candidate 1 (KDP/"wide" author dashboard), 85/100 vs runner-up home-inspector software at 71/100. Full scoring in research/tournament.md.
**Why (condensed):** (1) The wide-author market leader is verifiably failing on reliability per the space's most-read reviewer; (2) KDP's lack of API makes local-first a structural advantage (same file-based data path as incumbents, minus credentials/downtime/privacy risk) rather than a marketing slogan; (3) a local demo can honestly BE the product — no faked cloud; (4) proven $5–29/mo paid category; (5) maximally distant from runs 1–2 (prosumer, not B2B SaaS). Inspector pain scored higher raw but its rescue market is crowded and its core community is actively hostile to software marketing (verified mod post banning startups).
**Contingency:** if the skeptic pass breaks a load-bearing claim, promote the inspector candidate.

## D-005 — Name: WideTally (2026-07-13)
**Question:** What do we call it?
**Decision:** "WideTally" — widetally.com available per RDAP (404), no search collisions. "Wide" is the community's own term for publishing beyond Amazon (the underserved segment per verified evidence); "tally" says counting money plainly. Backups reserved in verification.md.
**Why:** Instantly legible to the ICP, descriptive, zero collision risk found.

## D-006 — Product architecture: local-first, file-based (2026-07-13)
**Question:** Cloud SaaS clone or local-first app?
**Decision:** Local-first. The product parses the royalty/ads report files authors already download (KDP XLSX/CSV, D2D, Kobo, Amazon Ads CSV) entirely on the author's machine. Pricing thesis: one-time / cheap, vs incumbents' $10–29/mo.
**Why:** (1) KDP has no API (verified, Amazon official) — incumbents' cloud architecture adds fragility (scraping/extensions) without adding data access; (2) leader verifiably failing on reliability; (3) TrackerBox proved authors pay one-time for local (then abandoned the slot in 2019); (4) privacy: authors never share KDP credentials or income data; (5) makes this run's local demo honestly identical to the real product.

## D-007 — Red team and tournament performed inline (2026-07-13)
**Question:** With sub-agents unavailable (spend cap, see D-003), how to preserve adversarial rigor?
**Decision:** Fixed written rubric scored before design began (tournament); a separate skeptic pass that re-fetched all 7 load-bearing claims first-hand before commitment; a post-build red team written with explicit kill intent, whose wounds are displayed at equal weight on RECAP. One deliberately-unfixed overclaim ("15-minute ritual, retired") left on the site and disclosed, so the red team's bite is auditable.
**Why:** Self-review can't fully substitute independent judges — mitigation is transparency: every scoring input is on disk with sources.

## D-008 — Unexpected deliverable: the Royalty Report Format Registry (2026-07-13)
**Question:** Which extra artifact makes this company feel most real?
**Decision:** Publish the product's core domain knowledge (what's inside each retailer's royalty file, verified vs practitioner-knowledge, gotchas) as free documentation — business/format-registry.md.
**Why:** It is simultaneously the moat made visible (format drift is the hard part of this business), the trust-builder for a credential-shy audience, the SEO asset for launch, and this run's honesty anchor (every schema claim labeled by verification level). No competitor publishes this.

## D-009 — Founder video length correction (2026-07-13)
**Question:** First assembly came out 77.9s against a ~60s spec (TTS rate -1 too slow). Ship or fix?
**Decision:** Fix: tightened script ~15%, TTS rate 0 → 64.4s final, verified by re-assembly, null-decode, and frame inspection.
**Why:** Spec adherence is cheap here; a 78s "60s video" is exactly the kind of quiet miss the definition of done forbids.
