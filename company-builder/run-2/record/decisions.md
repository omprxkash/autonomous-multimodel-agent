# Build Log — Decisions & Judgment Calls (run-2)

No one was available to ask; every question below was answered by research + reasoning and
logged here, as instructed.

## D1. Resume-from-crash strategy (2026-07-12)
Run was terminated mid-phase-2 by an API error; coordinator ordered: no more sub-agents,
work solo and sequentially, conserve fetches. State at resume: directory skeleton existed,
zero files written, all phase-1 research + 2.5 pitch investigations held in conversation
context. **Call:** persist everything to disk first, then continue. Sub-agent findings are
kept (they were real fetches), with their confidence flags preserved rather than laundered
into certainty.

## D2. Q: Should sub-agent-fetched evidence count as "a real URL you actually fetched"?
**A: Yes, with flags.** The agents ran real WebSearch/WebFetch calls inside this run. But
anything that was only search-snippet-corroborated is marked [snippet] in pain-hunt.md and
listed in honesty.md. Where a claim is load-bearing for the thesis, I re-verified it myself
(CSLB, COI case, BLS numbers, competitor scan) — see research/verification.md.

## D3. Q: Which idea wins the tournament?
**A: Solo-trades compliance deadline guard.** Full scoring in research/tournament.md. The
deciding factors: consequence-backed pain with a government primary source; competitors
either generic or selling to the opposite side of the table (GCs policing subs); honest
local demoability without faking integrations. Runner-up (small-landlord tool) failed on
crowding; dental verification failed on crowding + un-demoable core tech.

## D4. Q: Is this independent enough from run-1?
**A: Yes.** Run-1 built Shopify inventory sync (per its folder name/README glanced only for
tooling reference). Different industry (trades vs e-commerce), buyer (contractor vs
merchant), product shape (deadline intelligence vs data sync). I did not read run-1's
research or business files; only `_tools/` scripts, as the brief allows.

## D5. Q: The bls.gov and biggerpockets.com pages 403 our fetcher; projul.com socket-fails.
Use their numbers?
**A: Use with attribution + disclosure.** BLS OEWS numbers were confirmed via a secondary
page that reprints them (fetched) AND matched search summaries of bls.gov pages. The NAHB
34%-stat is used only as "per projul.com citing NAHB" and flagged in honesty.md. The
BiggerPockets quotes belong to the losing landlord candidate anyway and are not used in any
outward-facing artifact.

## D6. Q: Product scope for the demo — how much is honest to show?
**A:** The demo shows the *product experience* on seeded fictional data: a compliance
dashboard for one fictional solo electrician business across two states. State CE/renewal
rules shown in the demo are drawn from real state rule *patterns* (e.g. CA 2-year renewal,
TX yearly CE hours) but the demo data itself is fictional and labeled as a demo. No claim of
live state-registry integration is made anywhere; the roadmap describes registry monitoring
as planned, not built. This is the same standard a real pre-launch founder demo would meet.

## D7. Q: Brand name + domain without buying anything?
**A:** Chose "TicketSafe"? No — see D8. Domain availability checked via RDAP (free,
no signup), not purchased. Availability recorded in brand/name-search.md with check dates.

## D8. Q: Naming. Requirements: says "keeps your license safe," works on a van decal, not
already a funded company in the space.
**A: "LapseGuard"** — the product guards against lapses (license, CE, COI, bond). Checked
RDAP for lapseguard.com availability; checked search for name collisions (see
brand/name-search.md). Rejected: TradeCurrent (vague), RenewalRadar (radar cliché),
TicketMinder ("ticket" is UK-slang for license but reads as event tickets in the US),
CardCurrent (obscure), Licentia (pretentious latin).

## D9. Q: Pricing model?
**A:** $12/mo solo (or $99/yr), $29/mo crew (up to 5 people's credentials), founding-member
lifetime $199 pre-launch offer capped at 200 seats. Reasoning: below the "expense-report
threshold" a solo tradesperson will pay without deliberation; anchored against the $47k
documented single-incident downside and the ~$150–350/yr cost of one delinquent renewal fee.
Labeled inference in business docs — no price testing was possible.

## D10. Q: Videos with no paid TTS/avatar services?
**A:** Same pattern as run-1's tooling (allowed as engineering reference): HTML title cards +
Playwright-recorded UI footage; Windows System.Speech TTS for the founder voiceover, clearly
labeled synthetic; music synthesized in Node as a WAV; assembly via ffmpeg-static. Launch
video ~60–75s benefit-led; founder video calm/precise/zero-hype per the stated standard
(no private voice doc exists — using the brief's standard, noted in honesty.md).

## D11. Q: Red team without sub-agents?
**A:** Ran an adversarial pass myself under a separate rubric (kill-the-company checklist:
crowding, WTP, churn, data moat, distribution, legal) writing objections *before* rebuttals,
and let objections stand un-rebutted where honest rebuttal was weak. Output in
record/red-team.md and surfaced in RECAP + investor teaser (not hidden in an appendix).

## D12. Q: What's the one unexpected deliverable?
**A:** A **printable "Lapse Math" one-pager** (extras/lapse-math.html): a fill-in worksheet a
tradesperson can print, tape inside the van door, and use to compute their own personal
cost-of-a-lapse number from real state fee schedules — designed as the top-of-funnel lead
magnet for the trade-forum launch channel. Chosen because it matches how this audience
actually shares things (print > SaaS landing pages), and doubles as an ad creative.
Also added: state-rules starter dataset (product/data/state-rules.json) as a genuine seed
asset a founder could ship with.

## D13. Q: Demo realism vs honesty on the "monitored registries" feature?
**A:** The demo's "Registry check" panel shows *what the feature will do* using fictional
checks with timestamps clearly in demo data; site copy says "state registry monitoring —
rolling out state by state" and the roadmap marks it as in development. Nothing anywhere
claims 50-state live coverage. Honesty.md discloses.

## D14. Q: RECAP scope?
**A:** Single self-contained HTML page, relative links to every artifact, five-minute-read
structure: what/why/proof/how-to-run/what-would-kill-it. Same bar as definition of done.

## D15. Q: Founder video pacing defect found during frame inspection.
**A:** First assembly left a ~70s frozen close card (VO 114s vs 46s of footage). Fixed by
regenerating VO at default TTS rate (104s), re-recording a slower 57s product tour, and
inserting the pricing card where the VO reaches the price. Residual 29s end-card hold
accepted (gap-analysis). This is why the definition of done requires *watching* the videos.

## D16. Q: RECAP scope check before close.
**A:** Link check run twice (28/28 resolve). Mobile overflow 0px on site and product.
Decode checks + frame extraction on both MP4s. Self-grading written to record/gap-analysis.md
with two PASS-WITH-NOTES grades rather than inflating to straight passes.
