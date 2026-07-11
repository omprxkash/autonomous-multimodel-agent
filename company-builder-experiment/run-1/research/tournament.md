# Tournament — Five-Judge Scoring of C01–C20

Date: 2026-07-11. Input: `d:\AI\Business\run-1\research\candidates.md` (20 candidates).

## 1. Method

**Five judge personas, scored independently (no cross-talk, deliberate disagreement kept):**

1. **Boot** — bootstrapper who has shipped 3 micro-SaaS. Rewards narrow, solo-shaped, quickly-shippable products with proven price bands; punishes platform-scale builds and fuzzy monetization.
2. **Growth** — growth/distribution operator. Rewards clear buyer channels, "why now" momentum, SEO/marketplace discovery; punishes hard-to-reach buyers.
3. **VC** — skeptical VC analyst. Rewards incumbent weakness + defensibility + hard WTP evidence; downgrades low-confidence, cheap/churny buyers, and platform-dependency risk.
4. **Eng** — veteran product engineer. Rewards genuinely buildable local demos and clean API access; punishes candidates where the core is unbuildable in weeks or blocked by data access.
5. **SMB** — SMB owner who buys software. Scores from the gut on felt pain and "would I pay for this"; largely indifferent to buildability difficulty.

**Six criteria, each 1–10, with weights:**

| Criterion | Weight |
|---|---|
| Pain intensity | ×1.5 |
| Urgency (why now) | ×1.0 |
| Reachability of buyers | ×1.0 |
| Willingness to pay | ×1.5 |
| Buildability (tiny team, weeks, software-only, no money-movement/medical/legal-liability core) | ×1.25 |
| Incumbent weakness | ×1.0 |

Max weighted total = **72.5**.

**Constraints applied in scoring:** solo-founder-shaped and launchable this month (whole-platform rebuilds get buildability ≤3); local demo must be genuinely buildable (platform data-access barriers cut Eng's buildability); evidence confidence gates pain (Medium-confidence candidates capped, single-quote/inferred-WTP candidates capped on WTP); money-movement, medical, and legal-liability cores capped on buildability (C18 medical denials, C02 billing/payments audit).

## 2. Score matrix — weighted totals by persona (max 72.5)

Sorted by average. Personas disagree; average is a tiebreaker, not the verdict.

| ID | Name | Boot | Growth | VC | Eng | SMB | AVG |
|---|---|---|---|---|---|---|---|
| **C13** | Involuntary churn / failed-payment recovery | 56.5 | 55.0 | 51.5 | 56.2 | 52.5 | **54.3** |
| **C09** | Shopify inventory-sync data corruption | 53.2 | 53.2 | 48.2 | 53.2 | 51.2 | **51.8** |
| **C04** | SOC 2 readiness burden | 50.2 | 50.2 | 46.5 | 48.8 | 46.2 | **48.4** |
| **C14** | Freelancer scope creep & revisions | 50.8 | 50.8 | 44.8 | 49.2 | 44.8 | **48.1** |
| C01 | SMB bookkeeping document-chasing | 48.0 | 49.0 | 44.5 | 46.5 | 49.5 | 47.5 |
| C03 | Amazon FBA "DD+7" cash-flow crunch | 48.2 | 48.2 | 44.2 | 46.8 | 48.2 | 47.1 |
| C11 | Agency approval/version-control chaos | 47.2 | 47.2 | 41.2 | 47.2 | 47.2 | 46.0 |
| C08 | Amazon opaque fee & compliance chargebacks | 45.8 | 45.8 | 43.2 | 45.8 | 45.8 | 45.3 |
| C17 | WooCommerce booking plugin bugs | 46.2 | 43.8 | 41.2 | 46.2 | 45.2 | 44.5 |
| C05 | Field-service software fragmentation/traps | 41.8 | 41.8 | 40.8 | 41.8 | 43.2 | 41.9 |
| C12 | Amazon listing hijacking | 42.2 | 43.2 | 38.2 | 42.2 | 42.2 | 41.6 |
| C16 | Freelancer late-payment chasing/admin | 42.2 | 42.2 | 37.2 | 42.2 | 41.2 | 41.0 |
| C18 | Medical claim-denial appeals | 41.2 | 41.2 | 41.2 | 39.8 | 41.2 | 40.9 |
| C06 | Property management software patchwork | 40.2 | 40.2 | 39.2 | 40.2 | 41.5 | 40.3 |
| C15 | Etsy opaque ad algorithm | 40.5 | 40.5 | 34.5 | 40.5 | 39.5 | 39.1 |
| C10 | eBay return/refund abuse | 38.5 | 38.5 | 35.5 | 37.2 | 38.5 | 37.6 |
| C19 | Hiring overload from AI applications | 37.8 | 41.2 | 34.0 | 36.5 | 38.2 | 37.5 |
| C02 | Billing continues after cancel/uninstall | 37.5 | 38.5 | 34.5 | 36.0 | 37.5 | 36.8 |
| C07 | AI-chatbot support walls | 32.2 | 32.2 | 31.2 | 32.2 | 35.2 | 32.6 |
| C20 | QuickBooks Online account lockouts | 28.5 | 28.5 | 28.5 | 28.5 | 31.5 | 29.1 |

## 3. Per-persona top-3

**Boot (bootstrapper):** C13 (56.5) clean Stripe-API SaaS with a live $29–99/mo price band · C09 (53.2) buildable via Admin GraphQL, incumbents ship no rollback · C14 (50.8) validated $19–79/mo, narrow and shippable.

**Growth (distribution):** C13 (55.0) named buyers on IH + Stripe marketplace discovery · C09 (53.2) sits inside the App Store category where the buggy competitors already rank · C14 (50.8) dense, on-topic r/freelance threads with self-identifying buyers.

**VC (skeptic):** C13 (51.5) durable multi-year pattern, hardest WTP evidence, established band · C09 (48.2) proven ongoing spend, safety wedge is defensible · C04 (46.5) $15k consultant spend already incurred, multi-founder convergence.

**Eng (product engineer):** C13 (56.2) demo is a weekend against Stripe webhooks · C09 (53.2) the diff-preview/rollback safety layer is exactly an engineer's wedge · C14 (49.2) pure software, no external data gate.

**SMB (buyer):** C13 (52.5) would pay to stop silent revenue leak · C09 (51.2) catastrophic oversell is felt pain · C01 (49.5) document-chasing is the buyer's own daily grind.

## 4. FINALISTS — Top 4 overall

### C13 — Involuntary churn / failed-payment recovery for small SaaS (54.3)
Won every single persona — the only unanimous #1 in the field. It is the most solo-founder-shaped idea in the set: a Stripe-webhook-driven dunning tool with a genuinely buildable weekend demo, a *pre-existing* $29–99/mo price band, and named incumbents (ProfitWell Retain/Churnkey, $250+/mo or 15–30% of recovered revenue) that are explicitly priced out of the sub-$10K-MRR segment. The pattern is durable (2021 thread corroborated by March–April 2026), which neutralized the VC's usual "fad" objection. The one persona hesitation: VC docked incumbent-weakness because several small competitors (Stunning, RecoverKit, RecoveryMRR) already exist — proof of WTP but also a crowded lane.
- **Load-bearing claim:** "Involuntary churn from failed Stripe payments...erase 5-15% of MRR silently." — heze — https://www.indiehackers.com/post/where-is-your-revenue-quietly-disappearing-e620ea7771. If the recoverable-leak magnitude is materially smaller than this, the ROI pitch collapses. (Secondary anchor that must also hold: named competitors at $29–99/mo, same source thread https://www.indiehackers.com/post/i-went-looking-for-a-saas-opportunity-and-found-one-in-failed-payment-recovery-259e73871e.)

### C09 — Shopify multi-store inventory-sync corrupts data instead of failing safely (51.8)
Second everywhere. The wedge is unusually crisp: incumbents (Multi-Store Sync Power, Stock Sync, Easify) ship no dry-run, diff-preview, or rollback, so misfires silently zero/negative-out full catalogs — an engineering-shaped weakness a small team can out-build without rebuilding the whole sync engine. Buyers already pay $10–60/mo and *stay subscribed for years despite the bugs*, so the gap is reliability, not price. Buildable against the documented Shopify Admin GraphQL API, and discoverable inside the App Store category where the failing competitors already rank. VC's only reservation is platform dependency on Shopify.
- **Load-bearing claim:** "all inventory level for connected products in both stores is either zero or even negative" (2,000+ products needed manual adjustment after uninstall). — Kurti Connection USA — https://apps.shopify.com/easify-inventory-sync/reviews — 2026-06-21. The whole thesis is that catastrophic (not cosmetic) corruption recurs on *current* apps; this June-2026 quote is the freshest proof it is still happening.

### C04 — SOC 2 / security-compliance readiness burden (48.4)
Advanced on the strongest WTP evidence in the field: a founder who paid $15k to consultants, incumbents (Vanta/Drata) at ~$15k/yr that are overkill/unaffordable pre-Series A, and at least four independent builders converging on point solutions — a rare multi-founder validation signal. It is software-only and buildable as a readiness checklist + reusable questionnaire-answer library (no liability core if positioned as prep, not attestation). SMB persona scored it lowest because the buyer is a startup founder, not a classic SMB — but every other persona rated it a clear top-5.
- **Load-bearing claim:** "Paid consultants $15k just to tell us what controls we were missing." — andy89 — https://news.ycombinator.com/item?id=46495507. This dollar figure is the proof that a real, monetizable gap exists below the $15k/yr platforms; if the spend evidence is soft, WTP deflates toward the free-checker end.

### C14 — Freelancer scope creep & unbilled revisions (48.1)
Edged out C01 by 0.6. It is pure software with no external data gate (Eng liked it), reaches self-identifying buyers in high-comment r/freelance threads (Growth liked it), and carries a rare third-party market-sizing + price-test. It is the *shakiest* finalist: VC and SMB both scored it lowest of the four because freelancers are cheap, churny buyers and the WTP rests heavily on a single validation post. It advanced on buildability and reachability, not on evidence depth.
- **Load-bearing claim:** "Freelancers lose $7,800–$15,600/year to unbilled scope creep... 99% fail to bill for out-of-scope work" and a "$19–79/month tool concept tested well." — https://www.microgaps.com/gaps/2026-02-18-ai-scope-creep-detector-freelancers. This is a single-source, third-party market-sizing post doing most of the WTP work; if it does not survive verification, C14 has no hard price evidence left and should drop below C01/C03.

## 5. Notable eliminations

- **C02 (billing dark patterns), High confidence, finished 18th (36.8):** best evidence in the set, worst opportunity — unclear who pays, and an "audit the charge" product needs payment/bank data access that isn't solo-buildable. Confidence ≠ opportunity.
- **C19 (hiring overload):** the single most-engaged thread in the entire dataset (448 comments) yet near-bottom — no WTP (a founder asking "would you use this?" is soliciting, not proving) plus discrimination/bias liability. Growth loved the reach; VC gutted it on WTP (2/10).
- **C05/C06 (field-service & property-management platforms):** genuine, high pain but buildability capped at 3 — you cannot ship a ServiceTitan/AppFolio alternative in weeks with a tiny team. **C20 (QBO lockouts)** finished dead last: nothing product-shaped to build; it's Intuit's internal problem.

---

## Round 2 — Advocate vs Skeptic

### C13 — Involuntary churn / failed-payment recovery

**Advocate.** This is the most solo-shaped, fastest-to-revenue idea in the field, and verification strengthens the buildable core while trimming only the marketing gloss. Yes, the "5–15% of MRR erased" quote was misattributed — but the pain survives on *better* evidence: Greg Smethells' verified "2–5% of MRR disappears to involuntary churn every month," plus Baremetrics' own published "~9% of MRR lost to failed payments." So I re-cite to Baremetrics and the ROI pitch holds. The wedge is precise and confirmed: incumbents are genuinely priced out of the sub-$10K-MRR segment — Churnkey $250→$700+/mo, Churn Buster $249/mo, ProfitWell Retain "out of our price range" (verified verbatim from a real founder). A Stripe-webhook dunning tool is a weekend build against documented APIs — no money-movement core, no data gate. Price a flat $29–49/mo, undercutting the percentage-fee model founders explicitly reject. Distribution is unusually tractable: buyers self-identify in the exact IndieHackers threads cited, the pattern is durable (2021→2026), and the Stripe App Marketplace gives category discovery. Existing small players (RecoveryMRR $99, Stunning $120) aren't a threat — they're proof of a live, monetized band, clustered at the *top* of my target range, leaving room beneath. I differentiate on faster first-touch: davidjamess verified incumbents wait 24–48hrs before the first recovery email, "by then the customer is already mentally checked out." Land the first ten customers by hand from forum threads. Honest, narrow, shippable this month.

**Skeptic.** Kill it: the headline number was fabricated and what remains is a commodity. "5–15% of MRR erased" was REFUTED — heze actually said "5–9% of Stripe *charges* fail," a decline rate, not recoverable revenue. Recoverable leak is a fraction of a fraction: not every failed charge is winnable, so the real monthly upside to a $5K-MRR founder is tens of dollars — against which even $29 is a hard sell (nobody pays $50 to recover $40). "Durable" cuts the wrong way: the pattern persists *because* it's a solved, crowded category. Verification confirmed a dense field — RecoveryMRR, RecoverKit, Stunning, Churnkey, Churn Buster, Baremetrics Recover — atop Stripe's own free Smart Retries. Differentiating on "faster first email" is copyable in an afternoon, and Stripe can retune retry timing for free and erase the wedge overnight. Distribution cost is brutal: TAM is a soft, aggregator-guessed 5,000–10,000 sub-$10K-MRR Stripe shops — the cheapest, churniest, most price-sensitive buyers alive, who by definition have little revenue to protect — and to reach them you knife-fight every other dunning startup in the same three IndieHackers threads. Easy buildability is a liability: if a credible v1 is a weekend, there's no moat and the incumbents already finished. This is a feature, not a company.

### C09 — Shopify multi-store inventory-sync corruption

**Advocate.** The cleanest survivor in the tournament: all four evidence URLs verified verbatim/substance on re-fetch, zero refutations, plus two *new* independent corroborations (a Shopify Community thread and a Reddit multi-channel case) confirming the zero-out/overselling failure mode beyond the three named apps. That's a category-wide architecture gap, not one buggy vendor. The wedge is engineering-shaped — exactly what a solo technical founder out-builds. Incumbents (Multi-Store Sync Power, Stock Sync, Easify) ship no dry-run, diff-preview, or rollback, so misfires silently negative-out thousands of live SKUs — verified as recently as June 2026. I don't rebuild the sync engine; I add the safety layer they all lack: preview the diff before writes hit live inventory, plus one-click rollback. WTP is proven in the strongest form — merchants pay $10–60/mo and *stay subscribed for years despite catastrophic failures*, so the gap is reliability, not price, and I can charge a premium for safety. Buildable against the documented Shopify Admin GraphQL API, launchable this month. Distribution is favorable: the App Store gives built-in discovery in the exact "Inventory management" lane where the failing competitors rank and collect 1-star reviews I answer directly. TAM is real — 60,000–150,000 multi-store/multi-channel merchants anchored on Store Leads' verified Plus counts. Even the Easify root-cause dispute helps me: whether it's the app or the merchant's reconfigure loop, the answer is the same guardrail — preview and rollback — that I'm selling.

**Skeptic.** Kill it on platform risk and the crack verification left open. The whole business is a tenant in Shopify's house — distribution, API, and billing all run through the App Store — and the safety layer I'm selling (dry-run, diff-preview, rollback) is exactly the primitive Shopify ships natively the moment multi-location merchants matter to it, erasing the wedge in one release. That's how every "fix Shopify's gap" app dies. Second, verification exposed a live dispute on the freshest, load-bearing 2026 evidence: the Easify developer publicly attributes the June-2026 corruption to the merchant's own repeated install/uninstall/reconfigure, not an app bug. If catastrophic zero-outs are partly user-error and race conditions during reconfiguration, a third-party overlay sitting *further* from the data has less control, not more — and could itself trigger the circular loops the Community thread names ("Store A updates Store B, which triggers Store B to update Store A with empty data"). Buildability is deceptively hard: a credible v1 must reliably diff and roll back live inventory across stores in *weeks*, and if my safety tool ever corrupts a catalog I own thousands in merchant damage — fatal in a review-driven store. Demand durability is thin: merchants tolerate these bugs for years rather than switch — that's low switching urgency, not high WTP for safety. Cheap $7–60/mo anchors set the ceiling, and the forums where buyers live are where my failures get posted.

### C04 — SOC 2 readiness burden

**Advocate.** Build it now because the WTP evidence is the hardest in the field and it survived verification untouched: all four quotes checked out verbatim, including andy89's "paid consultants $15k just to tell us what controls we were missing" — a real dollar figure, real founder, plus his own note that "80% of the assessment was a standardized checklist." That 80% *is* the product. The wedge is readiness — sequencing and gap-diagnosis *before* committing to a platform or auditor — not evidence-automation, which Vanta/Drata own. Verification confirms the incumbents don't serve this: they assume you already know your gaps and still run $25–50k all-in year one. A solo founder ships a readiness-checker plus reusable questionnaire-answer library in weeks — pure software, no liability core if positioned as prep not attestation — and the verified "two weeks to two days" response-time win is an immediate, demonstrable value prop. Buyers self-identify in the exact channels the quotes came from: HN Show/Ask threads, IndieHackers enterprise-sales posts, YC founder Slacks. The convergence signal is unusually strong — four independent builders attacking this simultaneously validates demand cheaply. Price $99–299/mo, trivial against the $15k consultant bill founders already pay *in addition to* platform costs. Competitor Lumoar proves the wedge is monetizable, not closed; it's early, and a sharper, cheaper, more opinionated diagnostic aimed squarely at seed-stage founders can win the segment *beneath* the $7,500 platform floor. Launchable this month, against the best-documented spend in the whole set.

**Skeptic.** Kill it: verification turned "validated-and-open" into "validated-but-contested," and the contest is already lost on two fronts. The wedge is occupied — Lumoar sells the exact "readiness not tooling" pitch (claiming $45k consultant savings) and surfaced *by accident* during verification, meaning the space is more crowded than anyone checked. And the incumbents already moved: Drata and Secureframe now advertise ~$7,500/year floors, collapsing the "$15k/year platforms price us out" premise the candidate leans on. Vanta/Drata can bolt a free readiness diagnostic onto their funnel as lead-gen tomorrow — for them "tell me what's missing" is a customer-acquisition loss-leader, not a business, and they have the distribution to bury a solo tool. Demand durability is shaky: verification found "no new independent complaint threads on Reddit or review sites" — corroboration is concentrated in HN and IndieHackers founder-forums, an echo chamber of builders, not a broad buyer base. The buyer is worse than an SMB: a seed-stage founder buys SOC 2 readiness *once*, under deal pressure, then either fails the real audit (your liability if they blame your checklist) or graduates to Vanta anyway — brutal churn, no expansion. A checklist is trivially buildable, therefore trivially cloneable; the "four converging builders" are four competitors, not four proof points. A one-time info-product masquerading as SaaS, under a platform floor still dropping.

### C14 — Freelancer scope creep & revisions

**Advocate.** Build a lean v1 now — but honestly, on the real evidence, not the synthetic pricing. Verification confirmed the underlying pain verbatim in substance: a freelancer losing "$2,300 in unpaid work" on one landing page (43 hours, 20 billed), and a motion designer trapped in "5–6 versions... never a real final." That distress is genuine and actively discussed. Critically, verification also *validated a real third-party number*: Ignition's methodologically-sound 2025 survey (n=273) found 57% of agencies lose $1K–5K/month to unbilled scope creep and 78% rarely bill for it — hard evidence the under-billing behavior is chronic and monetizable. That reframes the wedge *upward*: sell to small agencies and creative studios, where budgets and pain are both larger, not only to solo freelancers. The product is pure software with no external data gate (the engineer's favorite trait) and launchable this month: a lightweight in-workflow tool that flags out-of-scope requests against a defined SOW and generates the "that's a change order at $X" nudge *in the moment* — precisely the intervention the verified advice ("write a better contract") never provides. Buyers self-identify in high-comment r/freelance and r/advertising threads under real usernames, and agencies already improvise the exact monetization (day-rates for extra rounds, capped revision windows) a tool would automate. I won't touch the discredited microgaps pricing — I'll price-test directly against agencies from day one. Advance it on buildability, reachability, and a *real* agency signal, not the synthetic freelancer one.

**Skeptic.** Kill it — the weakest finalist, and verification gutted its one piece of pricing evidence. The entire WTP case rested on microgaps.com, ruled synthetic and circular: a paid AI-idea directory whose business model depends on ideas *looking* validated. The "$7,800–15,600/year" loss is unsourced arithmetic (assumed rate × assumed 2 hrs/week); the "$19–79/month tested well" claim has zero methodology; and its "independent validation" (ScopeShield) is one of several near-identical clones — ScopeGuard AI, ScopeGuard.pro, ScopeLock — builders spun up chasing the same trending content. Verification even found Reddit seeded with low-engagement self-promo from throwaway accounts: guerrilla marketing dressed as grassroots demand. So there is *no* credible evidence freelancers will pay anything. Worse, the flagship post's engagement was inflated 2–3x in the source file (27/33, not 63/109), softening even the felt-pain signal. The one real number — Ignition's 57% — measures agencies, a population mismatch; pivoting to agencies means fighting entrenched PM and proposal tools (and the C11 approval-workflow idea) on their turf. Demand durability is illusory: freelancers are the cheapest, churniest buyers, and the fix they actually reach for is free (a better contract clause), not a $19/month subscription. The buildable v1 — detecting "out of scope" from fuzzy client messages — is either a brittle keyword matcher or an LLM feature any invoicing incumbent bolts on in a sprint. Crowded clone field, no proven WTP, fickle buyer, no moat.

## Round 3 — Final Vote

Three fresh judges, convened 2026-07-11. No stake in prior rounds; prior weighted scores are ignored. Decision frame: which ONE gets built THIS MONTH as a solo-shaped software business — judged on verified pain, provable WTP, reachable buyers, weeks-to-v1 buildability, and incumbent/platform risk. A wounded evidence base (refuted or synthetic claims) is a heavy negative.

### Judge personas

- **Judge A — Priya, indie-SaaS operator.** Has shipped and sold two Stripe-billed micro-SaaS solo. Cares above all about time-to-first-dollar and whether one person can build, sell, and support it without a team.
- **Judge B — Marco, e-commerce ecosystem veteran.** Ran a multi-store Shopify operation and built two App Store apps. Reads merchant pain and platform-risk instinctively; allergic to businesses that live or die by one platform's roadmap.
- **Judge C — Dana, cold-eyed investor.** Underwrites evidence integrity and defensibility first. Treats a refuted or synthetic claim as a red flag on the whole thesis, and asks "what stops the incumbent from doing this for free next quarter."

### Judge A — Priya (indie-SaaS operator) — VOTE: C13

C13 is the only finalist a solo founder can build, price, and ship this month with no data gate. The pain survives verification on *better* evidence than it was pitched on: heze's "5–15% of MRR" was refuted, but Greg Smethells' "2–5% of MRR disappears to involuntary churn" verified verbatim, and Baremetrics' own "~9% of MRR" independently rescues the ROI story. The price band is real and pre-existing — Churnkey $250→$700+/mo and Churn Buster $249/mo are verified as priced out of the sub-$10K-MRR segment, while founders explicitly reject the 15–30%-of-recovered model. A Stripe-webhook dunning tool with faster first-touch (davidjamess verified incumbents wait 24–48hrs) is a weekend build against documented APIs. Named buyers self-identify in the cited IndieHackers threads; I land the first ten by hand. Narrow, honest, monetizable now.

**Biggest fear about my own pick:** the recoverable leak on a $5K-MRR shop is genuinely small, so my $29–49/mo sits uncomfortably close to the dollars I recover — and Stripe can retune Smart Retries for free and erase my one differentiator overnight.

### Judge B — Marco (e-commerce ecosystem veteran) — VOTE: C09

C09 has the cleanest evidence base in the field — all four review URLs verified verbatim/substance with zero refutations, plus two *new* independent corroborations (the Shopify Community "zeroing out" thread and the TikTok Shop oversell case) proving a category-wide architecture gap, not one buggy vendor. The freshest proof is June 2026 (Kurti Connection, 2,000+ SKUs zeroed). The wedge is genuinely different: incumbents ship no dry-run, diff-preview, or rollback, so misfires silently negative-out live catalogs. WTP is proven in the strongest form — merchants pay $10–60/mo and *stay subscribed for years despite catastrophic failures*, so I sell reliability, not price. Buildable on documented Admin GraphQL; discoverable in the exact App Store category where the failing apps collect 1-star reviews I answer. TAM is a real 60,000–150,000 anchored on Store Leads counts. A contested-but-real market with a differentiated safety wedge.

**Biggest fear about my own pick:** the whole business is a tenant in Shopify's house — if Shopify ships native multi-location diff/rollback, or if my own overlay ever triggers a circular sync loop and corrupts a merchant's catalog, I own thousands in damages and my failures get posted in the same forums where my buyers live.

### Judge C — Dana (cold-eyed investor) — VOTE: C04

On raw evidence integrity C04 scores highest of the four — all four quotes verified *verbatim* with correct dates, including andy89's "$15k just to tell us what controls we were missing" and his "80% of the assessment was a standardized checklist," which is literally the product. The spend is real, incurred, and large; the buyer (seed-stage founder under enterprise-deal pressure) is reachable in HN and IndieHackers threads. The wedge — readiness/gap-diagnosis before committing to a platform or auditor — is one Vanta/Drata structurally don't serve. But I hold my vote loosely: verification turned this "validated-but-contested." Lumoar already sells the exact pitch, Drata/Secureframe dropped to ~$7,500 floors, and corroboration is concentrated in a founder-forum echo chamber with no fresh independent complaints.

**Biggest fear about my own pick:** it's a one-time, deal-pressure purchase with brutal churn and no expansion — and Vanta/Drata can bolt a free readiness diagnostic onto their funnel as lead-gen tomorrow, with the distribution to bury a solo tool overnight.

### Tally (round 1)

- C13 — 1 (Priya)
- C09 — 1 (Marco)
- C04 — 1 (Dana)
- C14 — 0

Split 1-1-1. C14 drew zero votes: its willingness-to-pay evidence was ruled synthetic and circular (microgaps.com arithmetic, not freelancer research), its one real number measures agencies not freelancers, and its flagship post's engagement was inflated 2–3x — a wounded evidence base, the frame's heavy negative. Judges deliberate.

### Deliberation

**Dana (C04):** I'll concede first, because the frame punishes exactly my pick's flaw. My evidence is the cleanest *verbatim*, but the opportunity is occupied on two fronts — Lumoar sells my wedge today and the incumbent price floor already collapsed from $15k to $7,500. "Validated-but-contested-and-shrinking" is the worst quadrant. And it's a one-time buy. I'm not going to win, and I shouldn't. The real contest is C13 vs C09.

**Priya (C13):** Then let me defend buildability. C09 asks a solo founder to reliably diff and roll back live inventory across multiple stores *in weeks* — and if my safety tool ever corrupts a catalog, I've caused the exact disaster I'm selling protection against. That's a heavier build and heavier liability than a Stripe webhook listener. Time-to-first-dollar favors me.

**Marco (C09):** Fair, but look at what the frame actually rewards: "a contested-but-real market beats a clean-but-tiny one only if the wedge is genuinely different." Your market is real but your wedge isn't — verification confirmed a crowded lane (RecoveryMRR, RecoverKit, Stunning, Churn Buster, Baremetrics Recover) sitting on top of Stripe's *free* Smart Retries, and "faster first email" is copyable in an afternoon. Mine is genuinely different: nobody in the category ships fail-safe/rollback, and merchants demonstrably tolerate the bug for *years*, which is latent WTP for the one thing none of them sell.

**Priya:** The counter is that "tolerate for years" reads as low switching urgency, not high WTP — and your evidence base, while clean, has a live root-cause dispute on the freshest quote (Easify blames the merchant's reconfigure loop).

**Marco:** The dispute cuts my way — bug or user-error, the fix is the same guardrail I'm selling: preview before write, one-click rollback. And the customer-visible damage (2,000+ products) is undisputed. On evidence integrity: mine is the only finalist with *zero* refutations and *two* new independent corroborations. Yours rests on a headline that was refuted and had to be re-sourced mid-defense.

**Dana:** That's decisive for me. Weighing the frame: C13 is the most buildable but its wedge is a feature in a crowded lane atop a free incumbent primitive — thin defensibility, cheapest/churniest buyers, and a refuted headline number. C09 carries the cleanest evidence base in the field, a genuinely differentiated safety wedge no incumbent ships, and years-long proven spend. The frame explicitly says a contested-but-real market with a genuinely different wedge wins. Its risk is platform dependency — real, but a known, survivable indie-app risk, not an evidence wound. I move to C09.

**Priya:** I still think C13 is the safer *build*, and I want that on record — but I accept the frame's logic. C09's wedge is the differentiated one and its evidence is the one that didn't bend under verification. I'll switch to make the majority clear, and I'll argue C13 as the insurance pick: if C09's build proves too heavy or too Shopify-exposed, C13 is the fastest fallback to revenue.

### Tally (round 2, after deliberation)

- **C09 — 3** (Marco, Dana, Priya)
- C13 — 0 (Priya moved; named as runner-up)
- C04 — 0 (Dana moved)
- C14 — 0

Unanimous for C09.

### WINNER: C09 — Shopify multi-store inventory-sync corrupts data instead of failing safely

**Decisive factors:**
1. **Cleanest evidence base in the field.** All four cited review URLs verified verbatim/substance with zero refutations, plus two *new* independent corroborations (Shopify Community "zeroing out" thread; TikTok Shop multi-channel oversell). C13's headline "5–15% of MRR" was refuted; C14's WTP was synthetic/circular; C04's wedge was found already occupied. C09 was the only finalist whose evidence strengthened, not weakened, under adversarial re-fetch — and the frame treats a wounded evidence base as a heavy negative.
2. **Genuinely differentiated wedge in a contested-but-real market.** No incumbent (Multi-Store Sync Power, Stock Sync, Easify) ships dry-run, diff-preview, or rollback; misfires silently zero/negative-out live catalogs, verified as recently as June 2026. Per the frame, a contested-but-real market beats a clean-but-tiny one precisely because the safety wedge is different — unlike C13's "faster first email" in a crowded lane atop free Stripe Smart Retries.
3. **Proven, durable WTP plus reachable buyers.** Merchants pay $10–60/mo and stay subscribed for *years despite catastrophic failures* — the gap is reliability, not price — and they're discoverable in the exact App Store "Inventory management" category where the failing apps already rank and collect the 1-star reviews a new entrant answers directly. TAM anchored at a real 60,000–150,000 merchants (Store Leads).

**Chief risk accepted:** platform dependency on Shopify (native diff/rollback could erase the wedge) and the liability of an overlay that touches live inventory. Judged a known, survivable indie-app risk — not an evidence wound.

### RUNNER-UP (insurance pick): C13 — Involuntary churn / failed-payment recovery

Fastest fallback to revenue if C09's build proves too heavy or too Shopify-exposed. Most solo-shaped and buildable in the set (weekend Stripe-webhook demo, no data gate), with a real pre-existing $29–99/mo price band and incumbents genuinely priced out below $10K MRR. Held back only because its wedge is a feature in a crowded lane sitting on Stripe's free Smart Retries, and its headline leak figure needed re-sourcing after the heze quote was refuted.
