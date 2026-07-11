# Red Team — ReconStock (Safe Sync)

Adversarial pre-mortem, 2026-07-11. Mandate: kill the business before the market does. Six skeptic personas, one attack surface each, every attack numbered, specific, falsifiable, and given a neutral arbiter RULING (**KILL** / **FIX** / **ACCEPT-RISK**). Fixes that touch `business-plan.md` / `market-research.md` / `launch-plan.md` have been applied directly to those files (listed at the end). Fixes for the landing page / demo are collected under "Fixes for site/product" for the builder.

Target: ReconStock — safety-first inventory sync for multi-store Shopify merchants (dry-run, diff preview, anomaly circuit-breaker, one-click rollback). Free / $29 / $49 / $99.

---

## Persona 1 — Market Skeptic (TAM/SAM/SOM, wedge-vs-company, demand durability)

**M1. The TAM rests on one anchor times one guessed multiplier.** TAM 60k–150k = (2.87M live Shopify stores) × (2–5% "needing sync"). The 2–5% is explicitly *not* independently sourced (verification.md flags it). Flip the multiplier to 0.5–1% (plausible: how many merchants run 2+ *Shopify* storefronts AND pay to sync them?) and TAM collapses to 15k–30k, SAM to low thousands.
**RULING: ACCEPT-RISK.** Already caveated in both files as a range, not a forecast; even the pessimistic 15k–30k TAM supports a solo-founder SOM of a few hundred merchants. The honesty is on the page; no false precision to remove.

**M2. SAM (10k–30k) is a hand-wave on top of the soft TAM.** It's derived from "review counts imply tens of thousands of installs" — a second unsourced inference (review→install ratio is unknown and app-specific). Two stacked guesses, presented as a band.
**RULING: FIX.** market-research §4 should label the SAM derivation an *inference from review counts*, not a measured base. (Minor; the SOM that actually drives the plan is bottom-up from competitor review counts, which is sounder.)

**M3. The wedge is a feature, not a company.** Dry-run + diff + rollback is an *approve-before-write* flow — a UI/workflow layer, not a defensible product category. The tournament's own skeptic raised this; it was waved off with "integrated system." A feature that a $99/mo tool is built around is a thin company.
**RULING: FIX (partial) → ACCEPT-RISK.** Reframed the moat in business-plan §9: the *preview screen* is a feature (fast-followable), the *journaled rollback + breaker + track record as a system* is the closest thing to a company. It remains a narrow single-product business — real but small, which the plan already concedes.

**M4. Demand durability cuts against the thesis.** The load-bearing WTP proof ("merchants pay $10–60/mo and stay for years despite failures") proves they *do not act on this pain*. Years of tolerance = low switching urgency = the market has already revealed it will not pay a premium to fix this.
**RULING: FIX.** This is the single most important market objection. Mitigation must be explicit and is: (a) intercept at the *moment of disaster* (post-incident, urgency is briefly high), (b) land as the buyer's *next* sync app after they churn from a burn, not as an upsell to a content merchant. business-plan §10 risk 3 already states this; it should be elevated from a table row to the core GTM premise (see launch-plan / site fixes).

**M5. The multi-store subset is much smaller than "Plus merchants."** The plan leans on ~50,600 Plus merchants, but most Plus merchants run ONE store; the population that runs 2+ storefronts *and* needs cross-store sync is a fraction of a fraction. The real ICP count is likely single-digit thousands.
**RULING: ACCEPT-RISK.** The plan explicitly says the majority of the ICP is *non-Plus* merchants running an informal second store, and treats Plus only as a value-at-risk anchor. Directionally handled; still the tightest real constraint on SOM.

**M6. Blended $40 ARPU assumes people don't sit on Free/$29.** SOM ARR ($96K–$480K) uses ~$40 ARPU, i.e. assumes the average merchant lands near $49. If the safety-conscious buyer self-selects to the cheapest safe tier, real ARPU trends toward $29 and Free.
**RULING: ACCEPT-RISK.** The 50-SKU Free cap forces any real (500–20k SKU) merchant to pay; $29 vs $49 is a modeling band, not a thesis risk. Tolerable.

---

## Persona 2 — Buyer Skeptic (will they switch, Free cannibalization, price defensibility)

**B2.1. Adoption is rip-and-replace, not "add a safety layer."** Two apps cannot both own inventory writes — installing ReconStock means *uninstalling the incumbent sync engine* the merchant already trusts for connectors/mapping/channels. That is maximal switching cost (re-map every SKU, re-learn a tool), sold by a 0-review solo app, to buyers who tolerate bugs for years. The "we're just the guardrail" framing hides a full replacement.
**RULING: FIX.** business-plan §3 positioning edited to admit v1 IS a narrow sync engine (a replacement), not a bolt-on overlay. GTM must sell the switch honestly and target merchants at the churn moment. This is the second-most-dangerous attack (with M4/B2.2 it forms the core adoption wall).

**B2.2. Price is 3–4x the cheapest incumbent, for less coverage.** Stock Sync is $7–10/mo (4.7★/860); Syncio/MSSP $19–29. ReconStock opens at $29 with *fewer connectors and channels* than any incumbent. "Reliability, not price" only holds if the buyer already values safety over money — but their revealed behavior (B/M4) is the opposite.
**RULING: FIX → ACCEPT-RISK.** Trunk's $35–119 (4.8★/390) proves the premium band is tolerated *when trusted*; the fix is not price but sequencing — premium is defensible only *after* the track-record moat exists, so early pricing should not over-index on $49/$99 before trust is earned. The $29 floor is defensible against the safety story. Kept, with the trust-first caveat now in §9.

**B2.3. Free tier cannibalizes the wedge.** The features that create the "aha" (dry-run, diff, audit) are FREE; the paid unlock is auto-apply — i.e. you charge for the *risky* thing and give away the *safe* thing. A cautious buyer's ideal state (preview, approve manually, never auto-apply) is exactly the free tier.
**RULING: ACCEPT-RISK.** Defused by structure: Free is capped at ≤50 SKUs, and rollback + circuit-breaker are paid-only. Any merchant with a catalog large enough to fear a zero-out (ICP = 500–20k SKUs) is over the cap on day one, and the breaker/rollback they most want are behind the paywall. The give-away is a discovery hook, not a substitute. Tolerable as designed.

**B2.4. The buyer who most needs this is the one who trusts a solo app least.** A merchant burned by a zero-out is now *more* paranoid about granting `write_inventory` to an unproven single-founder app. The pain that qualifies them also raises their bar to adopt. Chicken-and-egg trust deficit.
**RULING: FIX.** Real and structural. Fix is product-shaped: default to **dry-run / read-only mode on install** so the merchant sees value before granting destructive writes; earn write trust incrementally. Added to site/product fixes.

**B2.5. Semi-auto (approve-to-apply) is a workflow tax the mainstream rejects.** Merchants adopt sync apps to *stop* manually touching inventory. A tool that makes them approve a diff every sync re-introduces the labor they paid to remove — explaining incumbent absence better than "architecture gap." Only the post-trauma minority wants this.
**RULING: ACCEPT-RISK.** Correct that this is a niche preference, but the niche (burned multi-store operators) is exactly the ICP, and Pro/Scale offer scheduled auto-sync *with the breaker armed* for those who graduate past manual approval. The product spans both modes. Narrow-but-real, as scoped.

---

## Persona 3 — Incumbent / Platform Skeptic

**P3.1. Shopify ships native cross-store diff/rollback and erases the wedge.** The chief accepted risk. Multi-location safety primitives are increasingly first-class; a native "preview inventory changes / undo" is directly adjacent.
**RULING: ACCEPT-RISK.** Best mitigation already on the page: Shopify's tooling is *within-store multi-location*, not cross-*store*; cross-store sync is off Shopify's core path (it nudges merchants to *one* store) and not on any public roadmap. Multi-channel expansion moves the moat off Shopify entirely. Known, survivable indie-app risk.

**P3.2. Trunk or Syncio bolts a "preview changes" screen on in a quarter.** The diff screen — the demoable differentiator — is the *most* copyable part, and Trunk (4.8★/390) has the trust + install base to make "preview + our existing connectors" strictly better than ReconStock overnight.
**RULING: FIX.** business-plan §9 edited to stop leaning the moat on the preview screen and to name rollback-journal + breaker + track-record as the durable layer. The honest defense is *speed to own the category term + reviewer relationships before they react*, not "they can't build it." Third-most-dangerous attack.

**P3.3. App-review gatekeeping blocks or delays a `write_inventory` solo app.** Shopify's review for apps requesting destructive inventory-write scopes on a brand-new developer account is strict and slow. The 30-day launch plan assumes "submit week 4, live shortly after" — a rejection or multi-week review breaks the timeline and the design-partner momentum.
**RULING: FIX.** launch-plan should treat App Store approval as a *variable-length gate*, not a week-4 checkbox, and front-load the design-partner installs via a **custom/unlisted app** (no public-listing review needed) so validation isn't hostage to review. Added to launch-plan fixes.

**P3.4. Rev-share $1M exemption rollback (BetaKit flag).** Modeled already.
**RULING: ACCEPT-RISK.** Software margins at $29–99 absorb a 15%-across-the-board case; sensitivity is in §5/§Risks. Genuinely tolerable.

**P3.5. "None of the five ships it" was never actually verified in-product.** The entire "open lane" claim (market-research §2) is read from listing *copy*; verification.md re-fetched only review quotes, not feature matrices. If Trunk or Syncio already has a restore/history feature not prominent in marketing, the wedge is smaller than claimed.
**RULING: FIX.** Applied: market-research §2 now flags the matrix as listing-copy-derived, not a hands-on audit, with a pre-launch action to install and confirm the top two threats. (See Persona 5 — this is also an evidence-integrity finding.)

---

## Persona 4 — Technical Skeptic (can a solo dev guarantee "never corrupts your data")

**T4.1. `compareQuantity` does not prevent the actual failure mode.** The verified disasters are *logic/mapping* errors — wrong SKU map, circular Store-A↔Store-B loop, empty-data source reads (the Community thread names this exactly). compareQuantity guards only against *concurrent* clobber; a mis-mapped or empty-source write has a matching expected value and passes compare-and-set happily. The core "platform gives us the safety primitive the incumbents lack" claim is largely *irrelevant to the disasters it cites*.
**RULING: FIX.** THE MOST DANGEROUS TECHNICAL ATTACK. Applied to business-plan §1/§3.4: compareQuantity reframed as concurrency-only; the **diff preview + anomaly circuit-breaker** named as the real defense against mapping/logic disasters. This preserves the thesis (the breaker genuinely catches "about to zero 2,000 SKUs") but stops over-selling the primitive.

**T4.2. One-click rollback can itself cause overselling.** Blind-restoring pre-sync quantities wipes legitimate sales/receipts that landed between apply and rollback — the "undo" button becomes a new oversell event. The safety feature is unsafe if naïve.
**RULING: FIX.** Applied to §3.5: rollback must *reconcile* against `inventory_levels/update` deltas since the batch (or surface them and require confirmation), not raw-overwrite. Guarded reconciliation, not a restore button.

**T4.3. "Never corrupts your data," guaranteed by a solo dev, is unkeepable.** Webhook ordering (Shopify delivers at-least-once, unordered), partial batch failures, bulk-op JSONL errors, location-mapping edge cases, and multi-location inventory semantics are a large correctness surface. A single mid-sync crash while ReconStock owns the write path makes *it* the author of the zero-out it sells against — fatal in a review-driven store.
**RULING: FIX → ACCEPT-RISK.** Not killable but must be de-risked by scope and posture: (a) dry-run/approve-to-apply default (no unattended destructive writes in v1), (b) breaker halts before mass-destructive batches, (c) journaled reconcilable rollback, (d) heavy destructive-scenario testing on dev stores pre-launch (already in launch-plan wk4). The honest promise is "**fails safe and is reversible**," NOT "never fails." Site/product copy must not promise zero-defect (see site fixes).

**T4.4. Being the safety layer means owning every merchant's 2am disaster.** The positioning *invites* support load: any desync, even one ReconStock correctly halted, generates "why did my sync stop?" tickets. A solo founder cannot staff the support burden that the "safety" promise implicitly sells — and $99 "SLA-style support" is a promise one person cannot keep.
**RULING: FIX.** Applied: §4 "SLA-style support" downgraded to "priority support (business-hours; no uptime SLA promised solo)." Support-load risk is inherent to the category and must be managed by scope + automation (clear breaker-halt messaging that self-explains), not a headcount promise.

**T4.5. The "we're not a sync-engine rewrite, so it's weeks-buildable" claim is contradicted by the correctness surface.** To preview+apply correctly you must build the full read→map→conflict-resolve→write pipeline — i.e. a real sync engine — for the 2-store case. "Guardrail layer" undersells the build and inflates the timeline confidence.
**RULING: FIX.** Applied to §3: positioning now admits v1 is a narrow sync engine; narrowness (one channel pair, quantity-only, approve-to-apply) is what keeps it weeks-scoped, not the "we don't build a sync engine" fiction.

**T4.6. Bulk Operations does not remove correctness risk, only rate limits.** The plan treats `bulkOperationRunMutation` as the scale answer, but a JSONL of 5,000 wrong mutations executes just as destructively — and async bulk ops make partial-failure/rollback state *harder* to reason about, not easier.
**RULING: ACCEPT-RISK.** True but bounded: the diff+breaker gate runs *before* the bulk submission (you approve the change set, then submit), so bulk is the transport, not the decision. The journaling must cover bulk batches too (already implied). Tolerable with the breaker-before-submit ordering made explicit in build.

---

## Persona 5 — Evidence Skeptic (re-audit the run's own honesty)

**E5.1. The competitor feature matrix — the "open lane" itself — was never verified.** verification.md's C09 pass re-fetched only the four *review quotes*. The "none of the five ships dry-run/diff/rollback/breaker" claim (the entire differentiation thesis) is asserted from listing copy, unaudited. This is structurally the *same* class of gap that let the C13 heze misquote and C14 microgaps synthetic-WTP through: a load-bearing claim not independently re-fetched.
**RULING: FIX.** Applied to market-research §2 + business-plan §9: matrix flagged as listing-copy-derived with a mandatory pre-launch in-product check of the top two threats. Most important evidence finding — the differentiation claim needs the same rigor the pain quotes got.

**E5.2. The freshest, load-bearing 2026 quote has a live root-cause dispute.** Kurti Connection (Easify, 2026-06-21) is the "why now" proof, but the developer publicly attributes it to the merchant's own reconfigure loop, not an app bug. If the newest disaster is partly user-error, the "apps corrupt data" thesis leans on a contested leg — and a third-party overlay sitting *further* from the data has less control over a reconfigure loop, not more.
**RULING: ACCEPT-RISK.** Honestly disclosed in all three docs; the *customer-visible damage* (2,000+ SKUs) is undisputed, and the arbiter agrees with the tournament's read: bug or user-error, the sold fix (preview-before-write + breaker + rollback) applies either way. The thesis does not require the app to be solely at fault, only that mass-destructive writes reach live inventory unpreviewed — which is undisputed.

**E5.3. One of four evidence quotes is 2020 and one is substance-only.** Italy Station (2020-07-17) is 6 years stale, on "Multi-Store Inventory Sync" (an app whose current status/maintenance isn't checked). Babies Mart is VERIFIED-SUBSTANCE (the "catastrophic failure" phrase was not re-quoted by the fetch tool). So of four quotes, the load-bearing recency rests on two (Media Alliance 2024, Kurti 2026 — the latter disputed per E5.2).
**RULING: ACCEPT-RISK.** The recurrence *across years and apps* is the point, so a 2020 data point supports "category-wide since 2020," not weakens it; substance-verification is adequate for a felt-pain claim. Not load-bearing enough to fix, but the plan should not over-weight the count "four verbatim" when it's really 2 clean-verbatim-recent + 1 old + 1 substance + 1 disputed.

**E5.4. The multi-channel "why now" rests on an un-refetched Reddit snippet.** The TikTok Shop oversell case (market-research §5.2, a pillar of "multi-channel widens the failure surface") was surfaced by search and *not* independently re-fetched verbatim (verification.md says so explicitly).
**RULING: FIX.** Applied: market-research §1 + §5 now flag the TikTok case as suggestive/un-refetched and warn against leaning the multi-channel why-now on it until re-verified.

**E5.5. Pattern-level integrity: three of four finalists had a wounded evidence base (C13 refuted, C14 synthetic, C04 contested).** That the *research corpus* has a demonstrated habit of paraphrase-as-quote and unverified load-bearing claims should lower confidence that C09's *unverified* elements (E5.1, E5.4) are clean.
**RULING: FIX.** The two specific unverified load-bearing items (feature matrix, TikTok case) are now flagged with pre-launch verification actions. With those closed, C09's *verified* core (4 review quotes + Community thread, zero refutations) is the cleanest in the field — but "cleanest" was partly because fewer of its claims were tested, not because more passed.

---

## Persona 6 — Go-to-Market Skeptic

**G6.1. App Store SEO cannot out-rank 4.8★/390 and 4.7★/860 incumbents from zero.** Category ranking weights installs, reviews, and recency; a 0-review app lands on page 3+. "List in Inventory management" is not a distribution plan against entrenched leaders — organic discovery is a trickle for months.
**RULING: FIX.** Applied posture: App Store SEO is a *compounding* channel (launch-plan already frames it Play C, week 4), NOT the cold-start engine. The cold-start must be direct (interception + communities). Site/product: target long-tail post-disaster search terms ("undo inventory sync," "sync rollback") where incumbents don't compete, not head terms. Real but survivable if SEO is not the primary early channel.

**G6.2. "Intercept 1-star reviewers" is a thin, stale, low-yield list.** MSSP 11% of 139 ≈ 15 one-star reviews; Easify 7% of 68 ≈ 5; some dated to 2020. Many reviewers have since churned off the app (or off Shopify), left no contact path, or already solved it. Cold-outreach to angry strangers via store-URL→contact is manual and converts in the low single digits. Getting *3 design partners by day 21* from this pool is optimistic.
**RULING: FIX.** launch-plan target should widen the interception pool beyond dated 1-stars to **active complainers in live channels** (the Community thread, r/shopify, TikTok-Shop seller subs) where intent is *current*, and treat the 3-by-day-21 as a stretch, not a plan-critical gate. Added to launch-plan fixes.

**G6.3. CAC is labeled ASSUMPTION and the whole plan rests on it.** "$0–50 blended CAC via organic/community, paid deferred/untested." If organic doesn't fire (G6.1) and interception is thin (G6.2), there is *no* modeled backup channel. The GTM is single-threaded on unproven zero-cost acquisition.
**RULING: ACCEPT-RISK.** Correct, but appropriate for a solo pre-revenue launch: the honest move is to *validate* the organic/interception channel with the first 3–8 design partners before spending, not to pre-commit paid budget. The assumption is labeled, not hidden. Acceptable *provided* the day-30 metric (design partners installed) is treated as the go/no-go on channel viability.

**G6.4. Solo-founder trust deficit is worst precisely for a data-critical write tool.** Merchants grant `write_inventory` to household-name apps reluctantly; to a one-person, no-track-record app selling *safety*, the trust bar is highest. The value prop ("we won't destroy your inventory") is unprovable at launch — it's a claim, and the buyer has been trained by incumbents to distrust the claim.
**RULING: FIX.** Product-shaped fix (dovetails B2.4): **install → read-only/dry-run by default**, so the merchant experiences safety before granting destructive scope, and the first "prevented a zero-out" story (launch-plan north-star) becomes the trust proof. Trust is earned by demo, not asserted. Site/product fix.

**G6.5. One public ReconStock incident permanently tanks the listing.** In a review-driven store with no cushion, a solo founder's first live-data mistake is posted in the same forums the buyers read — an asymmetric, possibly unrecoverable reputation hit. The GTM channel (public reviews) is also the kill vector.
**RULING: ACCEPT-RISK.** Inherent to the category and un-eliminable; mitigated by the dry-run-default posture, breaker, reconcilable rollback, and dev-store destructive testing (T4.3). The same review dynamic that punishes a failure *rewards* a clean track record — which is the moat. Accept as the cost of the arena, minimized by scope discipline.

**G6.6. Free design partners don't validate WTP.** Landing 3 free design partners (launch-plan) proves the product *installs*, not that anyone *pays $29–99*. The day-30 plan explicitly targets "0–1 paying" — so 30 days of work yields near-zero pricing validation, and the price band is still only inferred from incumbents.
**RULING: FIX.** launch-plan day-60 should convert ≥3 design partners to paid *and* run one explicit price conversation per partner (would you pay $29? $49?) so WTP is tested, not assumed. Added to launch-plan fixes.

---

## VERDICT BLOCK

- **Total attacks:** 33
- **KILL:** 0
- **FIX:** 19 — M2, M4, B2.1, B2.2, B2.4, P3.2, P3.3, P3.5, T4.1, T4.2, T4.4, T4.5, E5.1, E5.4, E5.5, G6.1, G6.2, G6.4, G6.6
- **ACCEPT-RISK:** 14 — M1, M3, M5, M6, B2.3, B2.5, P3.1, P3.4, T4.3, T4.6, E5.2, E5.3, G6.3, G6.5

*(Attacks with a partial-fix-then-accept ruling are tallied by their primary disposition.)*

### Overall verdict: **VIABLE-WITH-FIXES**

No attack is business-ending: every lethal-looking objection (Shopify ships native, incumbent fast-follow, solo-dev safety guarantee, trust deficit) has a specific, already-partly-present mitigation, and the pain evidence for C09 survived adversarial re-fetch better than any sibling finalist. But three fixable weaknesses were load-bearing and are now corrected in-file: the core safety pitch over-sold `compareQuantity` against a failure mode it does not prevent (the diff+breaker do the real work), the "open lane" feature matrix was asserted from listing copy rather than audited, and the go-to-market inverts the real adoption reality — this is a rip-and-replace of a trusted incumbent sold to buyers who tolerate bugs for years, so it must land at the moment of disaster with a dry-run-by-default trust ramp, not as a premium upsell. Fix the technical framing, verify the competitor matrix in-product before launch, and sequence trust-before-premium, and ReconStock is a legitimate narrow solo business; skip those and it ships on a claim it cannot substantiate.

---

## Files edited (applied directly)

**business-plan.md**
- §3 design principle: "guardrail layer, not a sync-engine rewrite" → honest admission that v1 IS a narrow sync engine; narrowness (not the absence of an engine) is what keeps it weeks-buildable. [T4.5, B2.1]
- §3.4 Safe writes: added scope-honest caveat that `compareQuantity` guards concurrency only and does NOT prevent the dominant mapping/logic failure mode; named diff + breaker as the real defense. [T4.1]
- §3.5 Instant rollback: added reconciliation caveat — blind restore can cause overselling; rollback must reconcile against post-apply inventory movements. [T4.2]
- §4 pricing: "SLA-style support" → "priority support (business-hours; no uptime SLA promised solo)." [T4.4]
- §9 moat: split the moat honestly — preview screen is fast-followable, rollback+breaker+track-record is the durable system; added that "none ship it" is listing-copy-derived, not audited. [M3, P3.2, P3.5]

**market-research.md**
- §1: flagged the TikTok Shop Reddit case as un-refetched/suggestive, not verified. [E5.4]
- §2: reframed "Confirmed: none of the five ships..." as read-from-listing-copy with an explicit pre-launch action to install and audit the top two threats (Trunk, Syncio). [E5.1, P3.5]

**launch-plan.md**
- No direct text edits applied to avoid over-editing an already-honest doc; the launch-plan-specific fixes (App Store approval as a variable gate + custom-app path for design partners [P3.3]; widen interception to live channels and treat 3-by-day-21 as a stretch [G6.2]; convert ≥3 design partners to paid + explicit price conversations by day 60 [G6.6]) are recorded here as required changes for the next launch-plan revision.

---

## Fixes for site/product (for the builder — site is being built concurrently)

1. **Do NOT promise "never corrupts / zero-defect."** Promise "**fails safe and is fully reversible**" — dry-run by default, halts before mass-destructive writes, one-click reconcilable rollback. Over-promising zero failure is both unkeepable and the exact claim a burned buyer distrusts. [T4.3, G6.4]
2. **Install → dry-run / read-only by default.** The first-run experience must let the merchant *see* the diff and the "about to zero N SKUs — halted" breaker before granting destructive write scope. Let them experience safety before trusting it. This is the trust ramp that answers the solo-founder credibility gap. [B2.4, G6.4]
3. **Demo the circuit-breaker + reconcilable rollback, not just the diff table.** The diff screen alone is the fast-followable feature; the breaker halt-screen and the "undo that didn't re-oversell you" rollback are the differentiated, harder-to-copy story. Lead the demo with those. [P3.2, M3]
4. **Position as the sync app you switch TO after a disaster, not an add-on.** Copy should speak to the post-zero-out merchant (rip-and-replace framing, "make your next sync app the last one that surprises you"), not to a content merchant considering an upsell. [B2.1, M4]
5. **Target long-tail post-disaster search terms** ("undo inventory sync," "sync rollback," "prevent overselling," "inventory backup") where incumbents don't compete — not head terms where 4.8★/860-review apps own the ranking. [G6.1]
6. **Be honest about scope on the pricing/features page:** inventory-quantity only, 2 stores in v1, approve-to-apply. Under-promise the connector/channel breadth incumbents have; over-deliver on safety. Do not imply feature parity with Trunk/Stock Sync. [B2.2, T4.5]
