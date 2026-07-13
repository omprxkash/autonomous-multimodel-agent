# Honesty & Disclosures — run-2 (DueCrew)

Everything simulated, assumed, synthesized, or not independently verified in this package.

## Simulated / fictional
1. **DueCrew is not a real company.** No entity, domain, bank, or customer exists. The site,
   demo, teaser, emails, and posts are pre-launch artifacts a founder *could* ship.
2. **All product data is fictional**: "Delgado Electric LLC," Ray's credentials, "Ridgeline
   Mutual," "Anchor Surety," "Caprock Builders," "Meridian West GC," all dates, fees shown
   on demo cards ($75 renewal / $150 delinquent for OK), registry-check timestamps, and the
   share-link viewers. The demo and video end-card say so on screen.
3. **The waitlist form sends nothing** (labeled on the page).
4. **Founder voiceover is Windows built-in TTS** (Microsoft David) — disclosed here and in
   founder-script.md; no attempt to pass it as human. Music is synthesized in Node.
5. **Registry monitoring is a concept feature.** No state-registry integration exists. The
   demo labels it beta/in-development and marks timestamps as demo data.

## Assumed / inferred (labeled at point of use)
6. **All pricing** ($12/$29/$199) and every number in business/model.md (CAC, churn, margin,
   SAM ≈ $99M, ~1M solo licensees) are inference from the cited anchors; no price test or
   customer interview was possible under the guardrails (publish nothing, contact no one).
7. **Demo state-rules rows other than Texas** are drafted patterns, marked "Draft"/"Partly
   verified" in the UI and in product/data/state-rules.json. Only the TX 4-hour TDLR CE rule
   and the CSLB consequence/delinquency rules were verified this run.
8. The claim that FSM suites "don't market license/CE/COI tracking for solos" rests on
   search-level checks of public materials, not an exhaustive feature audit.

## Verified but with caveats
9. **CSLB quotes** — fetched from cslb.ca.gov (government primary source). HIGH confidence.
10. **$47,000 / 11-day COI case** — fetched verbatim from theagentsoffice.com, but it is an
    insurance agency's marketing anecdote about a client; not auditable via court/news
    records. Labeled as an "agency client account" in every artifact that uses it.
11. **BLS trade counts** — bls.gov itself returned 403 to our fetcher; numbers were taken
    from a fetched secondary reprint (skilledtradesiq.com) that matched search summaries of
    bls.gov pages.
12. **Census "~2.88M no-employee construction businesses"** — surfaced via a search-result
    reprint (jobstackcrm.com); used as a directional anchor only.
13. **NAHB "34% use permit-tracking tools"** — cited via projul.com; a sub-agent fetched the
    page during the pain hunt, but the orchestrator's re-fetch failed (socket errors).
    Always attributed as "per projul.com citing NAHB."
14. **Forum quotes** (ElectricianTalk "fold like a cheap suit," ContractorTalk "too
    involved," ServiceTitan add-on figures) — real thread URLs surfaced in live search;
    wording came from search snippets, not full-page fetches (403s). Flagged [snippet] in
    research files. The HeatingHelp ServiceTitan quotes and Capterra/Indie Hackers quotes
    WERE full-page fetches by researcher agents within this run.
15. **Reddit** was not directly fetchable at all this session; nothing in the final
    deliverables depends on a Reddit-only source.

## Process disclosures
16. Phase 1–2 research was done by parallel sub-agents whose WebSearch/WebFetch calls were
    real but whose budget died mid-phase; the orchestrator finished verification directly.
    One pitch agent (trades) was killed by the API before reporting; its verification was
    redone by the orchestrator (research/verification.md).
17. **The red team is a self-pass** (one adversary, same author) because sub-agent budget
    was exhausted — logged as red-team weakness R8.
18. **Name clearance is a knockout search only** (RDAP + web search on 2026-07-12), not a
    trademark clearance. duecrew.com was unregistered when checked; not purchased (guardrail).
19. **No private founder-voice rules doc exists**; the founder script follows the brief's
    stated standard (calm, precise, zero-hype), as the brief instructs to disclose.
20. **Run-1 independence:** run-1's business/research files were not read. Only
    `run-1/_tools/*` was used as engineering reference (allowed); run-2's video/server
    scripts are adapted from those patterns with a different composition, cards, flows,
    and music chords. All business/brand/product content is original to run-2.
21. The run was twice terminated by API errors and resumed; the coordinator's resume orders
    (work solo, conserve budget) are reflected in decisions.md D1 and the process notes.
22. **CE-provider ecosystem claim** ("$9–10 courses") — verified via live search results
    listing multiple sellers (expertce.com, hlonlinece.com, anytimecertification.com).
