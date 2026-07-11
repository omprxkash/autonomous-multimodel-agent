# Verification Log

Adversarial re-verification pass, run 2026-07-11. Method: re-fetch every evidence URL cited in candidates.md for the target candidate, classify each as VERIFIED-VERBATIM / VERIFIED-SUBSTANCE / UNVERIFIABLE / REFUTED, hunt 1-2 new corroborating/undercutting sources, and sanity-check market size against a citable anchor.

---

## C13: Involuntary churn / failed-payment recovery for small SaaS

### Per-URL verdicts

| # | URL | Claim in candidates.md | Verdict | Notes |
|---|---|---|---|---|
| 1 (load-bearing) | https://www.indiehackers.com/post/where-is-your-revenue-quietly-disappearing-e620ea7771 | heze comment: "Involuntary churn from failed Stripe payments...erase 5-15% of MRR silently" | **REFUTED** | Re-fetched full verbatim comment (posted Mon Mar 9 2026, 4:52pm). Actual text: *"Failed subscription payments are the clearest example — 5-9% of monthly Stripe charges fail at any given time, and most founders don't see it because it doesn't show up as a cost, just as missing revenue they never expected."* This says **5-9% of Stripe charges fail** (a decline rate), not "5-15% of MRR erased." The "5-15%" figure and the "% of MRR" framing do not appear anywhere in heze's comment — candidates.md's quote is a fabricated/inflated paraphrase presented as a direct quote. Thread-level engagement stats (6 likes, 1 bookmark, 95 comments) were accurate as cited. |
| 2 | https://www.indiehackers.com/post/i-went-looking-for-a-saas-opportunity-and-found-one-in-failed-payment-recovery-259e73871e | davidjamess: "most dunning tools fire their first recovery email 24 to 48 hours after a failure..." | VERIFIED-VERBATIM | Confirmed exact wording. |
| 3 | same URL | Greg Smethells (OP): tools "charge percentage fees (15–30%), fixed high minimums ($250+/month), or require manual implementation"; "2-5% of monthly MRR silently disappears" | VERIFIED-VERBATIM/SUBSTANCE | Re-fetch found: *"if you're a SaaS founder doing $2K–10K MRR, none of these fit. You either pay 15–30% of what you recover, pay $250/month before you've done anything"* and *"2–5% of MRR disappears to involuntary churn every month, and the tools to fix it are priced for businesses 10x larger."* Close paraphrase, substance matches. Post metrics (2 likes, 15 comments, 2026-04-29) confirmed. |
| 4 | https://www.indiehackers.com/post/is-there-a-service-for-recovering-stripe-failed-payments-6bde0e94c4 | Greg Kopyltsov: "a significant amount of failed payments on subscriptions"; ProfitWell Retain "priced out of reach" | VERIFIED-VERBATIM/SUBSTANCE | Confirmed: *"I've been running a small SaaS company for the last few months (KeywordSearch.com) and have seen a significant amount of failed payments on subscriptions."* On Retain: he says *"their Retain solution is out of our price range"* — candidates.md's "priced out of reach for an early-stage founder" is a fair paraphrase, correctly flagged as description not verbatim. Date confirmed 2021-09-26. |

**Load-bearing problem-statement check**: The C13 problem statement claims small SaaS lose "2–15% of MRR every month" — the 2% lower bound traces cleanly to Greg Smethells' verified "2-5% of MRR" figure, but the 15% upper bound traces to the REFUTED heze misquote. The range as stated overstates the upper end relative to what any single source in the file actually says.

### Independent corroboration hunt

- **Baremetrics blog, "How to Stop Involuntary Churn Before It Drains Your MRR"** (baremetrics.com/blog/recover-failed-payments-save-lost-revenue, 2026): states "subscription businesses lose around 9% of monthly recurring revenue to failed payments" and separately "failure rates hovering between 5% and 15% across the industry" — no external citation given for either figure, but this is an independent vendor source and it happens to land on the same 5-15% band candidates.md misattributed to heze. This substantively **rescues** the 15%-upper-bound claim (as an industry range, not as heze's words) — it just needed a different citation than the one given.
- **Competitor pricing check**: Confirmed current 2026 pricing for the incumbents named as "too expensive": Churnkey $250/mo→$700+/mo (also noted by reviewers as a voluntary-churn/cancel-flow tool with limited dunning depth), Stunning.co ~$120/mo for Stripe-only, Baremetrics Recover +$129/mo add-on, Churn Buster from $249/mo. This corroborates the candidates.md claim that $250+/mo tools exist and that a sub-$100/mo Stripe-only niche (RecoveryMRR $99/mo, Stunning $120/mo) is where new entrants cluster — consistent with, not contradicting, the candidate's incumbent-gap thesis.

### Market-size sanity check

- No authoritative, single-source count of "Stripe-billing SaaS businesses in the $2K-10K MRR range" exists publicly (Stripe does not publish this breakdown).
- Order-of-magnitude anchor: independent market-research aggregations put global SaaS company counts at roughly **30,000–42,000** (range across sources: demandsage/ascendixtech-style aggregator stats, 2026), of which a large fraction are small/bootstrapped and a large fraction of *those* bill via Stripe (Stripe is the de facto default for indie SaaS). If even 20-30% of ~35,000 global SaaS companies are Stripe-billed and in the sub-$10K MRR band, that's roughly **5,000-10,000** target businesses — a real but modest TAM for a single-purpose dunning tool, consistent with existing competitors (RecoveryMRR, RecoverKit, Stunning) already splitting a niche market rather than one player dominating. This is a soft, aggregator-sourced estimate, not a verified count — flagged as low-confidence.

### Verdict

**SURVIVES-WITH-CAVEATS** — the core pain (involuntary churn, dunning tools priced for larger businesses) is independently corroborated by Baremetrics' own published stats and current competitor pricing, but the file's headline "2-15% of MRR" figure rests partly on a misquoted source (heze never said 5-15% of MRR) and should be re-cited to the Baremetrics industry figure instead.

---

## C09: Shopify multi-store/multi-location inventory sync apps corrupt data instead of failing safely

### Per-URL verdicts

| # | URL | Claim in candidates.md | Verdict | Notes |
|---|---|---|---|---|
| 1 (load-bearing) | https://apps.shopify.com/multi-store-inventory-sync/reviews (Italy Station by GD, 2020-07-17) | "Don't install the app!!! Almost 2000 variants turned to negative qty...I need to fix up the whole inventory which will take me a while" | VERIFIED-VERBATIM | Confirmed via 1-star-filtered URL (default reviews page only shows recent reviews, so the unfiltered fetch initially missed it — this itself is a minor reproducibility gotcha worth flagging). Exact match on the quoted portion: *"Don't install the app!!! Almost 2000 variants turned to negative qty and still not sure it messed up other items as well."* |
| 2 | same URL (Babies Mart Australia, 2025-11-19) | "This was a catastrophic failure. It took me over 3 hours of manual effort...cost my business thousands of dollars." | VERIFIED-SUBSTANCE | Confirmed present: app "instantly and inexplicably set my entire inventory quantity to zero (0) across all products," required "3+ hours of manual restoration work," resulting in lost sales costing "thousands of dollars." Matches candidates.md substance closely; exact "catastrophic failure" phrase not independently re-quoted by the fetch tool but the described incident matches in full. |
| 3 | https://apps.shopify.com/stock-sync/reviews (Media Alliance CT, 2024-12-02) | "I am extremely disappointed with the service I received from Stock Sync...frequent synchronization errors causing overselling and stockouts" | VERIFIED-VERBATIM | Confirmed, dated Dec 2, 2024, South Africa, ~4 years using app: *"Frequent synchronization errors have caused disruptions in my inventory management, leading to overselling and stockouts."* Also: "I do not recommend making use of Stock Sync!" |
| 4 | https://apps.shopify.com/easify-inventory-sync/reviews (Kurti Connection USA, 2026-06-21) | "all inventory level for connected products in both stores is either zero or even negative" (2,000+ products needing manual adjustment) | VERIFIED-VERBATIM | Exact match: *"all inventory level for connected products in both stores is either zero or even negative, now i have to adjust and check inventoty [sic] update all my 2000+ products."* 1-star, dated 2026-06-21 confirmed. Caveat: the developer's public reply disputes root cause, attributing it to the merchant's repeated install/uninstall/reconfigure rather than a pure app bug — worth noting as a live dispute, not a settled cause, though the customer-visible damage (2,000+ products corrupted) is undisputed. |

All four load-bearing/evidence citations for C09 check out as accurate — no refutations.

### Independent corroboration hunt

- **Shopify Community thread**, "How do multi-store merchants handle inventory syncing? (researching the real pain)" — https://community.shopify.com/t/how-do-multi-store-merchants-handle-inventory-syncing-researching-the-real-pain/629499 (visible activity late May 2026). Independent merchants (PieLab, Lumine) describe the same failure class in their own words: *"The 'zeroing out' nightmare you mentioned is usually caused by SKU mapping errors or circular sync loops, where Store A updates Store B, which accidentally triggers Store B to update Store A with empty data,"* and *"Having to email a customer to apologize and cancel their order because the stock didn't actually exist completely ruins brand trust."* This is a new, previously-uncited source that independently corroborates the "sync tools zero out inventory / cause overselling" pattern outside the three apps named in candidates.md, strengthening the "category-wide architecture gap" claim.
- **Reddit** (surfaced via search, not yet independently re-fetched verbatim): a merchant reported selling "the same last 12 units on both Shopify and TikTok Shop over a weekend," waking up to "24 orders and zero inventory," leading to refunds and a compliance warning — same failure mode (multi-channel inventory desync causing overselling), different channel (TikTok Shop vs. a second Shopify store), reinforcing that this is a structural multi-channel sync problem, not specific to the three named Shopify apps.

### Market-size sanity check

- Anchor: Store Leads / storeleads.app (2026) counts **~2.87 million live Shopify storefronts** worldwide, and separately **~50,600 distinct Shopify Plus merchants operating ~76,000 Plus domains** — i.e., tens of thousands of merchants are confirmed running multiple storefronts on Plus alone, before counting non-Plus merchants who run a second store informally (common pattern: separate stores per brand/region/wholesale channel) or sync to non-Shopify channels (TikTok Shop, Amazon, etc., as the Reddit example shows).
- Order-of-magnitude estimate: if even 2-5% of live Shopify stores are part of a multi-store/multi-channel operation needing sync (a conservative slice given Plus alone is ~1.8% of live stores, and non-Plus multi-store/multi-channel setups are undercounted by that figure), that implies roughly **60,000-150,000** merchants in the addressable population — consistent with, and probably larger than, the combined installed base of the three named competitor apps (Multi-Store Sync Power 139 reviews, Stock Sync 860 reviews, Easify 68 reviews — reviews are a small fraction of installs). This is a rough estimate built from a real, citable anchor (Store Leads live-store and Plus-merchant counts) but the "% needing sync" figure itself is not independently sourced — flagged as an estimate, not a verified count.

### Verdict

**SURVIVES** — all four evidence URLs check out verbatim/substance-accurate on re-fetch, a new independent Shopify Community thread and a Reddit anecdote corroborate the same zero-out/overselling failure mode beyond the three named apps, and the market anchor (Store Leads live-store/Plus-merchant counts) supports a real, multi-tens-of-thousands-of-merchants addressable population.

---

## C04: SOC 2 / security-compliance readiness burden on early-stage startups

### Per-URL verdicts

| # | URL | Claim in candidates.md | Verdict | Notes |
|---|---|---|---|---|
| 1 (load-bearing) | https://news.ycombinator.com/item?id=46495507 | andy89: "Paid consultants $15k just to tell us what controls we were missing." — 3 points, 2026-01-05 | **VERIFIED-VERBATIM** | Re-fetched via HN Algolia API. Title "Show HN: Free SoC 2 readiness checker – built after spending $15k on consultant," author andy89, 3 points confirmed. Comment substance ("paid consultants $15k just to tell us what controls we were missing," "80% of the assessment was a standardized checklist") confirmed. |
| 2 | https://news.ycombinator.com/item?id=46706083 | asdxrfx: "it's extremely unclear how to start" — 12 pts/5 comments, 2026-01-21 | **VERIFIED-VERBATIM** | Re-fetched via HN Algolia API. Title, author, 12 points, 5 comments all match. Phrase confirmed present in post body. |
| 3 | https://www.indiehackers.com/post/founders-selling-to-enterprise-how-are-you-handling-the-security-questionnaire-subprocessor-asks-bcff95f018 | Salah Eddine Boussettah: "the moment you start selling to bigger customers, the security review shows up"; "two weeks to two days" — 5 likes/21 comments, 2026-05-26 | **VERIFIED-SUBSTANCE** | Re-fetched directly. Author, date, 5 likes/21 comments confirmed. "Response time drops from two weeks to two days" confirmed in substance (fetch rendered it as close paraphrase rather than exact string, but the claim checks out). |
| 4 | https://www.indiehackers.com/post/soc2-as-a-solo-founder-868b173ed4 | Andrew G: "$10k/y + 1-3 months is...challenging for small bootstrapped SaaS" — 2022-02-08 | **VERIFIED-VERBATIM** | Re-fetched directly. Exact quote "$10k/y + 1-3 months is the cost of getting certified. That's may be challenging for small bootstrapped SaaS businesses" confirmed, dated Feb 8 2022 — used correctly in candidates.md as an older corroborating data point, not as current evidence. |

All four cited URLs check out — no refutations, no fabricated quotes, no misattributed dates.

### Special scrutiny: incumbent saturation (Vanta / Drata / Secureframe)

Fetched current 2026 pricing intelligence (vendors don't publish list pricing, so this draws on multiple pricing-benchmark sites):

- **Vanta**: Startup plan ~$10,000–$20,000/year for a single framework, scaling to $80,000+/year at Scale/Enterprise. Audit fees separate: +$10,000–$50,000.
- **Drata**: Foundation plan starts ~$7,500/year for <50-employee companies (single framework); extra frameworks +$1,500–$7,500/year each. Onboarding adds $10,000–$25,000 → realistic **year-1 all-in cost $25,000–$50,000**.
- **Secureframe**: Starts ~$7,500/year, runs past $80,000/year at the high end.

**Conclusion**: A software-only entry tier now exists below the "$15K/year" figure candidates.md cites (Drata/Secureframe both advertise ~$7,500/year floors) — the pure evidence-automation gap has narrowed since the 2022 corroborating post. But this does **not** fill the gap C04 actually claims. C04's thesis is that the unmet need is *readiness* (knowing what controls are missing, in what order, before committing to a platform or auditor), not evidence-collection tooling. Vanta/Drata/Secureframe assume the company already knows its gaps; none functions as a cheap "tell me what's missing before I commit" diagnostic. Total realistic year-1 cost remains $25k-$50k+, and the $15k consultant fee in the load-bearing post was paid *in addition to*, not instead of, platform costs. Independent evidence the wedge is real but contested: **Lumoar** (lumoar.com), a startup found via search unrelated to this research, explicitly markets itself as saving "$45,000 in average consultant fees" on SOC 2 readiness — confirms the pain is large enough to already be monetized by at least one other builder.

### Independent corroboration (new sources)

1. **Lumoar** (https://www.lumoar.com/) — independent compliance-readiness product targeting the exact "readiness not tooling" wedge, claiming ~$45k average consultant-fee savings. Validates the pain's size; also shows the space isn't unclaimed.
2. WebSearch for fresh 2026 SOC 2 readiness complaints beyond the cited HN/IndieHackers threads turned up no new independent complaint threads on Reddit or review sites — corroboration is real but concentrated specifically in founder-community forums (HN, IndieHackers), not broadly documented elsewhere.

### Verdict

**C04: SURVIVES-WITH-CAVEATS** — all four cited quotes verify verbatim/substance with correct dates and engagement numbers; the pain (unclear starting point, $15k+ consultant spend, recurring subprocessor drift) is real, dated 2022→2026. Caveat: the "readiness, not tooling" wedge is not unclaimed — Lumoar already sells directly into it, and Drata/Secureframe now offer ~$7,500/year entry tiers — so this is validated-but-contested, not validated-and-open.

---

## C14: Scope creep & unlimited revisions — freelancers do free extra work

### Per-URL verdicts

| # | URL | Claim in candidates.md | Verdict | Notes |
|---|---|---|---|---|
| 1 (load-bearing anecdote) | https://www.reddit.com/r/freelance/comments/1ozc3zq/lost_2300_to_scope_creep_on_one_project_how_do/ | "$2,000 for 20 hours... 43 hours worked, $2,000 paid... $2,300 in unpaid work" — 2025-11-17, score 63, 109 comments | **VERIFIED-SUBSTANCE, engagement-count discrepancy** | Direct reddit.com/old.reddit.com fetch blocked by tooling; re-fetched via Arctic Shift API by post ID. Title "Lost $2,300 to scope creep on one project. How do you prevent this?"; the 43-hour / $2,000-paid / $2,300-unpaid substance is confirmed. Timestamp decodes to Nov 17, 2025, matching exactly. However Arctic Shift returned **score 27 / 33 comments**, not the 63/109 claimed in candidates.md — an unexplained ~2-3x overstatement of engagement in the source lane file. Does not affect the substance of the pain claim, but is a real data-quality flag. |
| 2 | https://www.reddit.com/r/advertising/comments/1nuir9m/how_do_you_deal_with_endless_chaotic_feedback/ | "5-6 versions of the same video... never a real 'final'" — 2025-09-30, score 35, 52 comments | **VERIFIED-SUBSTANCE, minor engagement discrepancy** | Same blocking issue; re-fetched via Arctic Shift by post ID. Title "How do you deal with endless, chaotic feedback?" confirmed; timestamp decodes to Sep 30, 2025, matching. Substance (contradictory feedback, multiple iterations, no real "final," poster is a motion designer) confirmed. Arctic Shift returned score 30 / 45 comments vs. claimed 35/52 — closer than item 1 but still not exact. |
| 3 (load-bearing WTP) | https://www.microgaps.com/gaps/2026-02-18-ai-scope-creep-detector-freelancers | "Freelancers lose $7,800–$15,600/year... 57% of agencies lose $1K–$5K monthly... 99% fail to bill... $19-79/month tested well" | **REFUTED as market validation / one sub-stat partially verified** | See special scrutiny below. This is a paid AI-assisted idea-listing product, not independent research. The headline WTP claim ("$19-79/month tested well") has no methodology, citation, or data behind "tested" anywhere on the page. |
| 4 | r/GraphicDesigning / r/graphic_design threads, 2025-08-18 and 2025-09-21 ("$50/hr for extra rounds" etc.) | No URLs provided in candidates.md | **UNVERIFIABLE** | candidates.md gives no URL for this item — only subreddit names and two dates. Cannot re-fetch or verify a claim with no locator; this is a citation gap in the underlying research. |

### Special scrutiny: what is microgaps.com, and does the WTP figure trace to anything real?

Fetched microgaps.com's homepage and the specific scope-creep gap page directly.

- **What it is**: A **paid subscription directory of "validated" micro-SaaS ideas** (30-day refund guarantee), marketing itself as evidence-based ("every gap built from 9 real sources: Reddit, HN, G2, Capterra, Product Hunt, Trustpilot, IndieHackers, pricing pages, Google Trends"). It is not a research firm or market-research vendor with independent standing — it's a content/lead-gen product whose business model depends on ideas *looking* well-validated, a direct conflict of interest with rigorous validation.
- **The "$7,800–$15,600/year" freelancer-loss figure is NOT a cited statistic — it's arithmetic the page states inline**: "$75-$150/hour, 2 hours/week of scope creep" × 52 weeks. Assumption stacked on assumption (assumed rate range, assumed 2 hrs/week drift), not a survey finding, not sourced to any freelancer poll. **This is synthetic, not empirical.**
- **The "57% of agencies lose $1,000-$5,000/month" figure IS real and traceable**: it's from Ignition's "2025 Agency Pricing & Cash Flow Report," a genuine survey of 273 agency managers/executives, independently corroborated by The Drum and Demand Gen Report trade-press coverage. **But this stat measures agencies, not solo freelancers** — MicroGaps imports an agency statistic to build a freelancer market-sizing argument, a population mismatch dressed up as freelancer evidence.
- **The "$19-79/month tested well" pricing claim has zero supporting methodology on the page** — no Van Westendorp study, no landing-page conversion data, no survey N. Reads as a positioning assertion despite the word "tested."
- **Circularity check on "ScopeShield" as corroboration**: the MicroGaps page cites ScopeShield (launched Feb 2026, $20/mo) as validation that "someone else independently identified this exact opportunity." Further search found near-identical competitors launched in the same window — ScopeGuard AI, ScopeGuard.pro, ScopeLock — plus the same idea independently listed on IdeaBrowser.com (a competing AI-idea-mill site). This is consistent with several builders reading the same trending "AI micro-SaaS idea" content and cloning it simultaneously, not with organically-arising freelancer demand. Weak corroboration at best — arguably anti-corroboration (a crowded field of unproven MVPs, not a proven market).
- **Reddit-seeding check**: A live Arctic Shift search of r/freelance for "scope creep" turned up a cluster of very-low-engagement (score 0-1, zero comments, several `[removed]`) self-promotional posts pitching scope-creep frameworks/tools/prompts from generic throwaway-style accounts — consistent with tool builders seeding Reddit with guerrilla marketing rather than organic distress signal, further weakening the "grassroots demand" reading.

**Bottom line, stated bluntly**: the willingness-to-pay evidence for C14 is **substantially synthetic and circular**. The one real third-party number (Ignition's 57%/$1K-5K) measures the wrong population, and the headline freelancer dollar figure ($7,800-$15,600) is an unsourced arithmetic guess presented as a finding. The "$19-79/month tested well" claim is unsupported assertion. This is a market-sizing narrative built by an AI-idea content site to sell its own subscription/catalog — not evidence that real freelancers were surveyed, interviewed, or observed paying anything.

### Independent corroboration (new sources)

1. **Ignition's "2025 Agency Pricing & Cash Flow Report"** (ignitionapp.com, corroborated by The Drum, Demand Gen Report) — a real, methodologically-described survey (n=273) confirming 57% of agencies lose $1K-$5K/month to unbilled scope creep, 78% rarely/only-sometimes bill for out-of-scope work. Genuine third-party evidence of the underlying *behavior* (chronic under-billing for scope creep) — agency-level, not solo-freelancer-level, but real.
2. **Arctic Shift live search of r/freelance** for "scope creep" — confirms the underlying pain is still actively discussed, but skews toward low-engagement self-promotion rather than organic high-engagement distress, a mildly undercutting signal about how saturated/marketing-heavy this exact niche has become.

### Verdict

**C14: SURVIVES-WITH-CAVEATS** — the underlying pain (unbilled scope creep, chaotic revision cycles) is real and verbatim-confirmed in substance in both cited Reddit posts, though their reported score/comment counts are inflated 2-3x versus a live refetch (unexplained data-quality issue in the source lane file), and is independently corroborated at the agency level by a genuine third-party survey. But the specific $19-79/month willingness-to-pay case rests on microgaps.com, which is **synthetic/circular and should not be trusted as pricing evidence** — it's an AI-idea-marketplace product's self-serving arithmetic, not freelancer research, and its "independent validation" (ScopeShield) is one of several likely-clone products chasing the same trending content, not proof of organic market pull.
