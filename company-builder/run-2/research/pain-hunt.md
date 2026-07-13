# Phase 1 — Pain Hunt (5 parallel researchers, consolidated)

Date: 2026-07-12. Method: five parallel research agents ran WebSearch/WebFetch across
Reddit/Indie Hackers, SaaS review sites (G2/Capterra/Trustpilot), Hacker News, trade &
healthcare forums, and market/funding news. Every quote below traces to a URL an agent
actually fetched or that appeared in live search results. Confidence flags are preserved:
**[fetched]** = page body retrieved directly; **[snippet]** = wording came via search-engine
snippet of the cited page (real page, wording not read verbatim from source).

---

## Researcher A — freelancers / solopreneurs (Indie Hackers primary-source)

1. **Cross-tool "leakage" of billable time.** OP lost ~$13,000/yr while all four tools "worked
   perfectly"; commenters replicated 18–22% unaccounted-time findings. [fetched]
   https://www.indiehackers.com/post/i-was-losing-13-000-year-and-all-4-of-my-apps-were-working-perfectly-Oqnoj4nLfDCyNhC1ElDd
2. **Forgotten timers** — "I've probably lost $10k this year just from forgotten timers"
   (r/freelance via aggregator). [snippet] https://painonsocial.com/blog/freelance-time-tracking-reddit
3. **Payment-chasing fatigue** — "that steady drumbeat of 'is it time to follow up again?' is
   genuinely exhausting" (Foundryih). [fetched]
   https://www.indiehackers.com/post/how-to-invoice-and-not-get-stiffed-as-a-freelancer-159ac95174
4. **Scope creep with no shared record of approvals** (ynnhlr, same thread). [fetched]
5. **Post-sale client onboarding chaos** — "we've definitely felt that post-sale chaos doing
   client work" (chaosandcoffee). [fetched]
   https://www.indiehackers.com/post/building-a-tool-to-fix-client-onboarding-chaos-early-feedback-welcome-b601f6f53f

## Researcher B — SaaS review mining (G2/Capterra/Trustpilot)

1. **AppFolio support cliff** — "customer support was often lacking… overly-focused on rolling
   out new features" (Kyle S., 2★); "Zero support, horrible interface… about a week [to reach
   a human]" (Ari W., 1★). [fetched]
   https://www.capterra.com/p/92228/AppFolio-Property-Manager/reviews/
2. **Square for Restaurants crashes mid-service** — "Glitches crashed our restaurant multiple
   nights in a row" (Leah C., 1★). [fetched]
   https://www.capterra.com/p/175628/Square-Point-of-Sale/reviews/
3. **Gusto/Rippling billing errors + impossible cancellation.** [snippet]
   https://www.trustpilot.com/review/gusto.com
4. **Open Dental Cloud freezes "20x a day"** (Heather C., 1★, Mar 2025). [fetched]
   https://www.capterra.com/p/122350/Open-Dental/reviews/
5. **ServiceTitan add-on stacking** — add-ons reportedly $12,000–33,600/yr on top of base;
   implementation $5,000–$50,000+. [snippet]
   https://www.capterra.com/p/150053/ServiceTitan/reviews/

Cross-cutting themes: post-sale support cliff; pricing opacity/add-on stacking; reliability
failures during customer-facing moments; cancellation friction.

## Researcher C — Hacker News / Indie Hackers

1. **Modern MS Access successor** — Ask HN, 115 pts / 111 comments.
   https://news.ycombinator.com/item?id=15246061
2. **"Contact Us" pricing opacity** — reaperducer "I don't have time for games" ($120k budget
   walked). https://news.ycombinator.com/item?id=33425443
3. **PE analysts rebuilding financials from CIM PDFs** (marcelk123 on a Show HN).
4. **Expensive per-seat software resentment** — Ask HN id=41518797 (Bloomberg $27,660/yr,
   Cadence $150k/seat).
5. **Teams priced out of Teleport** — https://news.ycombinator.com/item?id=41873439

## Researcher D — trades / healthcare / property forums

1. **Prior authorization: 12–16 staff-hrs/week per physician** (AMA + AAPC forum).
   https://www.ama-assn.org/practice-management/prior-authorization/fixing-prior-auth-nearly-40-prior-authorizations-week-way
   https://www.aapc.com/discuss/threads/prior-authorization.121704/
2. **Dental insurance verification: 12–13 min/patient, 5+ hrs/day in payer portals; denials
   cost $25–50k/yr.** [partially verified — headline corroborated via snippet; article body
   did not render on direct fetch]
   https://dentalofficemanagers.com/post/insurance-verification-front-desk-cost/
3. **Vet front desk: ~1 in 4 peak calls unanswered; 85% won't call back; 22% no-show rate ≈
   $3,045/day idle capacity for 4-doctor clinic.** [vendor blogs — directional]
   https://www.puppilot.co/blog/breaking-the-phone-bottleneck-in-veterinary-clinics
4. **Small landlords: spreadsheets fail silently** — "lasted about three months before they
   missed a lease renewal" [snippet, corroborated across two search passes; direct fetch 403]
   https://www.biggerpockets.com/forums/899/topics/1279170-i-stopped-paying-my-property-manager-7-200-year-heres-how-i-self-manage-5-units
5. **Electricians hate/avoid paperwork** — "when it comes time to get all this paperwork done,
   I fold like a cheap suit"; one member stays an *employee* rather than going solo because of
   paperwork. [snippet] https://www.electriciantalk.com/threads/anybody-else-hate-paperwork.68465/
6. **Plumbers rekey field data into QuickBooks manually** — multi-page "I hate quickbooks!!!"
   thread. https://www.plumbingzone.com/threads/i-hate-quickbooks.19570/
7. **ServiceTitan stress at invoice-in-front-of-customer moment** — "Service Titan causes me
   stress" (GW); "glitches… invariably happen when doing the invoicing in front of the
   customer" (Paul Pollets). [fetched]
   https://forum.heatinghelp.com/discussion/169798/hvac-dispatch-software
8. **Small contractors reject scheduling software as overbuilt** — schedules still "in their
   head, pen and paper, spreadsheet, or Google calendar." [snippet]
   https://www.contractortalk.com/threads/scheduling-software.421853/

## Researcher E — market size / funding signals

1. **Contractor license/permit tracking**: NAHB 2025 Technology Adoption Survey (via
   projul.com): only 34% of residential contractors use dedicated permit tracking tools (11%
   in 2022) → ~66% have none. PermitFlow raised **$54M Series B (Dec 2025)** for permit
   *submission* for larger GCs — adjacent heat, but license/CE/COI *renewal tracking* for solo
   trades served only by small tools.
   https://projul.com/blog/best-construction-permit-tracking-software/
   https://www.businesswire.com/news/home/20251202551013/en/PermitFlow-Raises-$54-Million-to-Solve-Constructions-Biggest-Bottlenecks-With-AI
2. **Claim denials worsening**: Experian Health State of Claims 2025 — 41% of providers report
   >10% denial rates; only 14% use AI. https://www.experian.com/blogs/healthcare/state-of-claims-2025/
3. **Gig worker cross-platform scheduling** — documented pain, no funded dedicated product
   found; monetization unclear. https://www.myshyft.com/blog/multi-app-working/
4. **No-shows**: 10–30% by vertical; $250k/yr business loses ~$26k/yr; SMS reminders cut
   no-shows 38–50%. Beauty vertical saturated (GlossGenius ~$115M raised).
   https://www.etisia.com/no-show-statistics
5. **Freelancer tax**: crowded — Found ($50M C), Filed ($17M), Numeral ($35M), Sphere ($21M).
   https://techcrunch.com/2025/05/21/filed-raises-17m-to-automate-the-drudgery-of-tax-prep/
6. **Macro**: admin ≈36% of a small-business owner's workweek; Sage 2025: SMBs lose 24
   days/yr to financial admin. https://www.sage.com/en-gb/company/digital-newsroom/2025/05/09/the-hidden-admin-burden-on-small-businesses/
7. **Underinsurance**: Hiscox 2025 — 77% of US small businesses underinsured.
   https://www.hiscox.com/underinsurance

Researcher E bottom line: most genuinely underserved with real pain and weak funded
competition = **(1) contractor multi-state license/CE/COI renewal tracking for solo trades**,
(2) gig-worker cross-platform scheduling. Freelancer tax, no-shows-in-beauty, chargebacks,
SMB insurance = crowded with 2025-funded entrants.

## Known research limitations (disclosed)
- reddit.com was not directly fetchable this session; Reddit-sourced quotes came via
  aggregators or search snippets and are flagged lower-confidence.
- G2/Trustpilot/BiggerPockets blocked direct fetches (403) — those quotes are search-snippet
  corroborated.
- Mid-phase, web tools hit a monthly spend limit for sub-agents; remaining verification was
  done by the orchestrator directly with a conserved fetch budget (see verification.md).
