# Candidate Problems — Synthesized Master List

Compiled 2026-07-11 from eight research lanes: reddit-ecommerce, freelance-agency, hackernews, review-sites, vertical-forums, app-marketplaces, founder-communities, smb-backoffice.

20 candidates kept (C01–C20), ranked by overall strength (evidence quality + cross-lane corroboration + recency + willingness-to-pay signal). 13 weaker candidates dropped — see Appendix. All quotes below are copied verbatim from the lane files; URLs are unmodified from source.

---

## C01: SMB bookkeeping stays manual — document chasing eats firm capacity despite steady spend

- **Problem**: Small businesses already pay hundreds of dollars a month for bookkeeping that remains substantially manual, and the specific bottleneck bookkeepers/accounting firms report is not the accounting work itself but chasing clients for receipts, statements, and answers to categorization questions — client portals sit unused while staff revert to manual email chasing.
- **Who**: SMB owners paying $300–$800/month for bookkeeping; small-to-mid accounting/tax practice owners and prep staff; outsourced/fractional bookkeepers serving multiple SMB clients monthly.
- **Evidence**:
  - "Most small businesses pay around $300–$800 per month just for bookkeeping" despite incomplete tax optimization across hundreds of monthly transactions. — bmadduma — https://news.ycombinator.com/item?id=46238354 — 2025-12-12 — thread: 64 points/55 comments
  - "A portal is a good system of record and a poor system of persuasion." — Stephen Findley, AccountingWEB, "Why clients ignore the portal you pay for" — https://www.accountingweb.co.uk/community/industry-insights/why-clients-ignore-the-portal-you-pay-for — 2026-07-08
  - Same article, corroborating third-party data: in Wolters Kluwer's annual survey of nearly 2,000 US accounting firms, "late and unprepared clients" ranked the #1 challenge, and nearly 70% of accounting firms report struggling with document collection specifically. — same URL — 2026-07-08
  - "I'm at my wits end. I have a team of 3 bookkeepers and it still takes them over 2 weeks to close our books each month. How can I get them to speed up?" — Quora question title (verbatim; full answers not retrievable, Quora blocked direct fetch) — https://www.quora.com/Im-at-my-wits-end-I-have-a-team-of-3-bookkeepers-and-it-still-takes-them-over-2-weeks-to-close-our-books-each-month-How-can-I-get-them-to-speed-up
- **Incumbents & failures**: QuickBooks-style tools handle basics but "specialized needs require significant customization"; dedicated client portals exist but require the client to log in and act on their own initiative — firms have "over-invested in the record and under-invested in the persuasion," so portals sit empty and staff revert to manual chasing "because... it works" but doesn't scale. Hubdoc/Keeper/Financial Cents/Karbon reduce but don't eliminate the bottleneck.
- **Willingness-to-pay**: Existing, non-hypothetical $300–$800/month SMB spend on bookkeeping; an entire bookkeeping-ops software sub-category (Hubdoc, Keeper, Financial Cents, Karbon) already monetizes "document chasing" as a feature.
- **Reachability**: HN Ask/Tell threads, AccountingWEB comments, QuickBooks ProAdvisor community, Bookkeeper Business Academy / Workflow Queen coaching audiences, Facebook bookkeeping groups.
- **Confidence: High** — verbatim, dated, corroborated across 3 independent lanes plus an independent third-party survey (~2,000 firms). Caveat carried forward: the AccountingWEB source is flagged by its lane as "vendor-adjacent content" (references a sponsoring portal company) — weight the Wolters Kluwer survey stat as the stronger independent evidence.
- **Source lanes**: hackernews, vertical-forums, smb-backoffice (3 lanes — merged from "SMB Accounting & Bookkeeping Automation," "Client Document Chasing Eats Small Accounting Firm Capacity," "Bookkeeping month-end close delayed by clients not sending documents")

---

## C02: Billing continues after cancellation/uninstall — no self-serve way to stop it

- **Problem**: Customers cancel or uninstall a SaaS product and continue to be charged — sometimes for months — because cancellation requires unwinding a bundled payments/software account or because the app never properly cancels its subscription object on uninstall. There is no self-serve way to audit or force-stop the charge; customers resort to bank disputes and regulatory complaints.
- **Who**: Small home-service businesses and independent restaurants using SaaS+payments bundles (Housecall Pro, Toast); Shopify merchants who uninstall third-party apps.
- **Evidence**:
  - "charged my Venmo Debit Card $189/month WITHOUT authorization for 3+ months totaling $567+" — BBB complaint against Housecall Pro, filed 03/24/2026 — https://www.bbb.org/us/ca/san-diego/profile/marketing-software/housecall-pro-1126-1000067843/complaints
  - "I cancelled my subscription 4 times now" (continued charges despite a bank dispute) — BBB complaint against Housecall Pro — same URL — 2026-05-28
  - "Why am I still billed for a deleted app?" — community.shopify.com thread — https://community.shopify.com/t/why-am-i-still-billed-for-a-deleted-app/300506 — most recent variant Oct 2025: merchant uninstalled Jul 24, 2025 but continued being charged in Sept and Oct 2025
  - "I do not have any active subscription, and I already cancelled the service and deleted the app completely. Despite this, I am still being charged" / "DONT USE THIS APP, ITS SCAM" — Poesiyan (Australia), Return Prime review — https://apps.shopify.com/return-prime/reviews — 2026-05-26 — 1-star, 3 months using app
- **Incumbents & failures**: Housecall Pro ($59–$329/mo) and Toast bundle SaaS subscription with payment processing, so cancellation requires unwinding two systems; BBB page shows 76+ complaints of "the same predatory billing pattern" with "only a 21% verified resolution rate." On Shopify, no self-serve tool exists — Shopify's own Help Center documents the root cause but offers only a manual, developer-by-developer refund-request process; community threads on this recur from 2022 through 2025.
- **Willingness-to-pay**: Customers dispute charges through banks and file BBB complaints rather than eat the cost; Shopify merchants start public community threads demanding refunds — real behavioral signal for a trust-focused "billing guardian"/audit layer.
- **Reachability**: BBB/Trustpilot reviewers (dates/amounts listed), home-service and restaurant owner Facebook groups, r/Plumbing, r/smallbusiness; Shopify community forums, searchable via "why am I still charged shopify app."
- **Confidence: High** — verbatim, dated through mid-2026, the identical dark pattern found independently on two unrelated platform types (vertical SaaS+payments bundles and a horizontal app marketplace).
- **Source lanes**: review-sites, app-marketplaces (2 lanes — merged from "Billing/Cancellation Dark Patterns" and "Shopify third-party app subscription billing continues after uninstall," with a corroborating Return Prime quote)

---

## C03: Amazon FBA "DD+7" payment-hold cash-flow crunch

- **Problem**: Amazon's March 2026 migration to a "DD+7" reserve policy (funds released 7 days *after delivery*, not 3–4 days after shipment), combined with a new 3.5% fuel surcharge and removal of credit-card ad payment (killing a 30–60 day float), created a sudden, severe working-capital squeeze that sellers say they weren't warned about in advance.
- **Who**: FBA private-label and multi-SKU sellers, solo operators to 7-figure brands, especially thin-margin or heavily-reinvesting sellers.
- **Evidence**:
  - "I was expecting a 25k dump into my bank account and only received 5k... On April 9, I got a larger dump into my bank account but it looks like around 20k is still being held onto." — u/scithe — https://www.reddit.com/r/FulfillmentByAmazon/comments/1sk0uqc/ — 2026-04-13 — 38 comments
  - "April 3 – Amazon implemented their new DD+7 reserve policy, which has resulted in roughly a 66% drop in payouts for many sellers, creating a significant cash flow crunch... April 15 – Amazon is removing the ability to pay for ads using a credit card, eliminating the typical 2–3% cashback/rewards and the 30–60 day payment float... April 17 – Amazon is introducing a 3.5% fuel surcharge on FBA and AWD fulfillment fees." — u/jdubs703 — https://www.reddit.com/r/FulfillmentByAmazon/comments/1sh2a8n/ — 2026-04-09 — 59 comments (highest-engagement thread in this lane)
  - "I am planning to use one of those Amazon financing companies because DD+7 policy holds the payments too long... I have around $150k balance in one of my accounts, and I have to pay 15k to cover the current sales' expenses." — u/Swimming-Culture-474 — https://www.reddit.com/r/FulfillmentByAmazon/comments/1u46pe3/ — 2026-06-12 — 14 comments
  - "Amazon's new DD+7 policy kicked in March 5th (Germany March 12th)... Payment cycle went from 3-4 days to 8-9 days... Harder for new sellers to scale." — u/Dense-Panic7112 — https://www.reddit.com/r/FulfillmentByAmazon/comments/1s33i50/ — 2026-03-25 — 18 comments
- **Incumbents & failures**: Third-party "Amazon financing" firms (Payability, Storefund) advance cash against held balances but charge fees on an already-squeezed margin; Amazon's own guidance offers no mitigation beyond "review your cash reserves"; no native tool forecasts exactly when funds unlock per order.
- **Willingness-to-pay**: Sellers already pay third-party cash-advance/financing firms; a tool-builder (u/Electrical_Green6261) is prototyping a payout-prediction feature ("MarginGuard") citing DD+7 as the driver and seeking beta testers.
- **Reachability**: r/FulfillmentByAmazon and r/AmazonSeller (daily suspension/fee/cashflow threads); FBA Facebook groups/Discords not audited.
- **Confidence: High** — verbatim (pulled via Arctic Shift Reddit-data mirror since reddit.com itself was unreachable), dated across 3 months, quantified dollar figures, still actively discussed 4+ months after rollout. Caveat: Reddit score fields are noted by the lane as fuzzed/capped on this mirror — comment counts were used as the primary engagement signal.
- **Source lanes**: reddit-ecommerce

---

## C04: SOC 2 / security-compliance readiness burden on early-stage startups

- **Problem**: Startups closing enterprise deals are forced into SOC 2 (or similar) compliance with no clear order of operations, discover the true scope only after paying consultants, and end up doing reactive, spreadsheet-driven remediation. The underlying gap is "readiness" (process/ownership), not tooling — and it recurs every time an upstream vendor changes its own subprocessor list.
- **Who**: Early-stage/seed-stage startup founders and first ops/security hire hitting a compliance requirement from an enterprise customer; bootstrapped B2B SaaS founders moving upmarket.
- **Evidence**:
  - "Paid consultants $15k just to tell us what controls we were missing." — andy89, "Free SoC 2 readiness checker – built after spending $15k on consultant" — https://news.ycombinator.com/item?id=46495507 — 3 points — 2026-01-05
  - "it's extremely unclear how to start" — asdxrfx, "Ask HN: Why does SOC 2 feel so hard for early-stage startups?" — https://news.ycombinator.com/item?id=46706083 — 12 points/5 comments — 2026-01-21
  - "the moment you start selling to bigger customers, the security review shows up" — Salah Eddine Boussettah, "Founders selling to enterprise: how are you handling the security-questionnaire + subprocessor asks?" — https://www.indiehackers.com/post/founders-selling-to-enterprise-how-are-you-handling-the-security-questionnaire-subprocessor-asks-bcff95f018 — 5 likes/21 comments — 2026-05-26
  - "slow incomplete responses kill deals, honest fast ones don't" — comment, same thread, reporting a cut in response time "from two weeks to two days" once a reusable answer library was built — 2026-05-26
- **Incumbents & failures**: Vanta/Drata/HeyLaika-style platforms run ~$15K/year — overkill/unaffordable pre-Series A, and they answer "tooling," not "readiness"; consultants are effective but expensive and front-loaded before a company knows what it's missing; manual trust pages and copy-paste answers rot as vendors change subprocessors.
- **Willingness-to-pay**: $15k consultant spend already incurred by one poster; at least 4 independent builders (asdxrfx/Lumoar, andy89/soc.tools, plus two earlier 2024 posts) are independently building point solutions — a multi-founder convergence signal; separately, "$10k/y + 1-3 months is...challenging for small bootstrapped SaaS" (Andrew G, "SOC2 as a solo founder," https://www.indiehackers.com/post/soc2-as-a-solo-founder-868b173ed4, 2022-02-08) shows the same spend pressure years earlier.
- **Reachability**: HN Ask/Tell HN threads, Indie Hackers B2B/enterprise-sales threads, YC/founder Slack communities, SOC2-adjacent SaaS review sites.
- **Confidence: High** — verbatim, dated, persistent complaint pattern spanning Sept 2024 → May 2026, corroborated across 2 independent lanes.
- **Source lanes**: hackernews, founder-communities (2 lanes — merged from "SOC 2 / Security-Compliance Readiness" and "Enterprise Security-Questionnaire / Subprocessor Documentation Burden")

---

## C05: Field-service management software — fragmentation, onboarding traps, and pricing backlash (trades)

- **Problem**: Small trade/construction/home-service businesses are stuck between disconnected point tools and "all-in-one" platforms (ServiceTitan, Jobber) that are sold like enterprise software — deceptive sales claims, multi-month implementations, and long contracts with no easy exit — while the accounting backbone (QuickBooks) they're locked into keeps raising prices.
- **Who**: Owners/VPs of small trade/construction/home-service businesses (1–15+ people).
- **Evidence**:
  - "The reason they give you 3 months free...is because it will take minimum 3 months to figure out how to use it" — Tyler B., President, Construction, ServiceTitan review, Capterra, rating 1.0 — https://www.capterra.com/p/150053/ServiceTitan/reviews/ — 2025-09-25
  - "not worth five times the cost of Housecall Pro" and "support team struggles with minimally complex tasks... can't wait a week or more" — Edward K., VP of Operations, Construction, ServiceTitan review, Capterra, rating 2.0 — same URL — 2026-03-10
  - "I'm getting tired of juggling Google Calendar, Trello, and a few other random tools" — ContractorTalk, "Invoicing software" thread — https://www.contractortalk.com/threads/invoicing-software.457830/ — Oct 2024 — 1.1K views/6 replies
  - "I've been finding it way too expensive for what it offers" (re: Jobber) — same ContractorTalk thread — Oct 2024
- **Incumbents & failures**: ServiceTitan (est. $245–$500+/technician/month plus $5,000–$50,000+ implementation fees, "typically 3-6 months," some users reporting 12+ months) is priced/sold like enterprise software to small trade businesses who lack capacity for a multi-month rollout; a separate G2 1-star reviewer reported not being told about a 2-year contract and the company "refusing cancellation and threatening collections." Jobber is "way too expensive for what it offers" at small scale; QuickBooks raised prices 15–20% in July 2025.
- **Willingness-to-pay**: Businesses already pay $39+/mo (Jobber), $150–500+/mo (ServiceTitan tiers), $30–90+/mo (QuickBooks Online) — real budget spent on partial solutions; multiple ServiceTitan reviewers are actively comparison-shopping against Housecall Pro, proving a live, priced-in switching evaluation.
- **Reachability**: ContractorTalk (public, searchable "Business"/software sub-forums), G2/Capterra review sections, trade Facebook/Reddit groups (r/HVAC, r/Plumbing, r/Construction).
- **Confidence: Medium-high** — verbatim, dated (Sept 2025–Mar 2026 for ServiceTitan; Oct 2024 for ContractorTalk), corroborated across 2 lanes. Caveat: exact dates for the two G2 quotes referenced in the review-sites lane are unconfirmed (G2 blocked direct fetch).
- **Source lanes**: review-sites, vertical-forums (2 lanes — merged from "Field Service Software Onboarding/Contract Trap" and "Field-Service Software Fragmentation & Pricing Backlash")

---

## C06: Property management software is a patchwork, not a system

- **Problem**: No single PM platform covers the full operating loop (communication, maintenance history, CAM/commercial accounting, compliance) — landlords and property managers end up manually stitching together multiple tools and spreadsheets, describe platforms as "developer-built with no PM domain depth," and get surprised by hidden percentage-based fees on "free" tiers.
- **Who**: Small-to-mid property managers and self-managing landlords (single SFRs up to 100+ unit portfolios), including a commercial PM segment.
- **Evidence**:
  - "Overly complex workflows — lots of clicks for simple tasks" — Yanik Parsch, BiggerPockets, "What property management software are you using — and what frustrates you most about it" — https://www.biggerpockets.com/forums/80/topics/1279418-what-property-management-software-are-you-using-and-what-frustrates-you-most-about — ~March 2026 — 80 votes
  - "None of the mainstream tools actually help you stay compliant. You end up Googling statutes yourself" and "A lot of platforms advertise as 'free' but then charge percentage-based fees on rent payments, which adds up fast" — Kyle S. (RentSolve AI), same thread — ~March 2026
  - "Developers... do not have the depth of subject knowledge in the operations of the full PM spectrum" — Richard F., same thread — ~March 2026 — 2,163 votes (highest-engagement single comment found across the entire research pass)
  - "Every tool solves one piece and nothing connects... You end up being the integration layer" and "Tenant reports a problem... three months later you can't remember if that unit's water heater was the one you already replaced" — Ryan D., same thread — ~March 2026 — 32 votes
- **Incumbents & failures**: AppFolio, Buildium, Rent Manager, Propertyware — complaints center on complexity for simple tasks, disjointed reporting requiring manual export-combining, "free" tiers converting to percentage-of-rent fees, and a mismatch between software product teams and real PM operations knowledge.
- **Willingness-to-pay**: This population already pays for AppFolio/Buildium/Rent Manager subscriptions or percentage-of-rent-collected fees — active, ongoing spend; the frustration is incompleteness, not refusal to pay.
- **Reachability**: BiggerPockets forums — large, public, professionally moderated (this single thread drew vote counts in the hundreds/thousands).
- **Confidence: High** — verbatim, very recent (~March 2026, 4 months before research date), exceptionally high engagement, but single lane.
- **Caveat**: Older (~2022–23) BiggerPockets evidence on maintenance-history tracking and informal-payment-app compliance risk was folded in as supporting context, not treated as independently current.
- **Source lanes**: vertical-forums (merged from "Property Management Software Is a Patchwork" + "Maintenance/Repair History Tracking & Rent Collection Compliance Risk")

---

## C07: AI-chatbot support walls — can't reach a human when the software breaks

- **Problem**: Category-leading SaaS across at least three unrelated verticals replaced human-accessible support with AI chatbots/ticket queues in 2025 as a cost-cutting move; paying customers on mid-tier plans describe being functionally unable to get help when the software breaks something affecting their livelihood.
- **Who**: Small business owners/operators paying $50–$300+/month for "core operations" software (property managers, home-service owners, solo/group therapy practices) with no IT department to fall back on.
- **Evidence**:
  - "Zero support, horrible interface, useless AI. If you want to talk to a human it'll take you about a week" — Ari W., President, 1 employee, AppFolio Property Manager review, Capterra — https://www.capterra.com/p/92228/AppFolio-Property-Manager/reviews/ — 2025-02-21
  - "The AI chatbot that took over the maintenance request section. It is very difficult to use" — Leah M., Executive Editor, AppFolio Property Manager review, Capterra — same URL — 2026-01-07
  - "Its customer service is dreadful. You'll be chatting with robots that can't understand your question." — Harry A., Psychotherapist, SimplePractice review, Capterra — https://www.capterra.com/p/130710/SimplePractice/reviews/ — 2025-07-08
  - Housecall Pro: "Beginning in 2025, customers reported that tech support became AI-only, with no option to talk to a human. Phone support on Basic and Essentials plans is not a feature — only MAX gets escalated phone support" (WebSearch synthesis of Trustpilot/BBB coverage of Housecall Pro's rating drop from 3.7 to 2.9/5) — https://www.trustpilot.com/review/housecallpro.com
- **Incumbents & failures**: AppFolio Property Manager ($1.49–$5/unit/month, 50-unit minimum ≈ $298–$1,500/month floor), SimplePractice ($49–$99+/month), Housecall Pro ($59–$329/month) all gate phone/human support behind top pricing tiers, routing lower tiers into AI-first chat to cut support headcount.
- **Willingness-to-pay**: Reviewers explicitly frame this as a reason to leave, from paying President-level customers; Housecall Pro's Trustpilot rating cratered coincident with the support-model change (3.7→2.9 in ~15 months) — a measurable willingness to punish/switch.
- **Reachability**: The review platforms themselves, plus niche Facebook groups (BiggerPockets/property manager groups, therapist private-practice groups, home-service contractor groups).
- **Confidence: High** — verbatim, dated Feb 2025–Jan 2026, cross-category evidence within one lane (3 unrelated verticals) plus a measurable rating-collapse data point.
- **Source lanes**: review-sites

---

## C08: Amazon opaque fee & compliance-chargeback errors — manual dispute burden on sellers

- **Problem**: Amazon periodically introduces or misapplies fees (Inbound Placement Fees on split shipments, Weight & Dimension reimbursement disputes) and separately issues automated compliance chargebacks (packaging/labeling/SIPP mis-enrollment) — in both cases sellers only catch the charge by manually auditing ledgers, with no proactive alert and a short window to dispute.
- **Who**: FBA sellers shipping via AWD/split-shipment; sellers with W&D reimbursement disputes; small Amazon 3P sellers/consumer brands hit by SIPP/labeling compliance chargebacks.
- **Evidence**:
  - "Heads up: Amazon is back-charging Inbound Placement Fees on complete split shipments. Check your ledgers!... I almost lost $420 this week without realizing it." — u/Original_Morning25 — https://www.reddit.com/r/FulfillmentByAmazon/comments/1uge63w/ — 2026-06-26 — 20 comments
  - "Looking for advice from veteran sellers who have successfully bypassed the 90-day Weight & Dimension reimbursement policy" after "MD Office admitted fault but keeping 99% of a confirmed overcharge" — u/Independent-Bunch-16 — https://www.reddit.com/r/FulfillmentByAmazon/comments/1t0uqe0/ — 2025-12-31
  - "A compliance chargeback is a financial penalty a retailer issues to a supplier for failing to follow operational, shipping, or labeling rules"... such chargebacks "may represent 2-10% of manufacturer revenue" — Seller_ToPPYvOWlyp9j, Amazon Seller Central forum — https://sellercentral.amazon.com/seller-forums/discussions/t/c95a4d15-e2e9-4d94-8e88-85400ea14d46 — ~Sept 2025 — 20 reactions, thread 955 views/20 replies
  - A seller reported a **$2,000 loss across two orders** after Amazon flipped a chargeback from "not responsible" to "you are responsible" a week later — Seller_hScgwR6TE3i5B, same thread — ~Dec 2025
- **Incumbents & failures**: A cottage industry of paid FBA reimbursement-auditing services (Getida/Refunds Manager-style) already exists, but auto-replenished single-case-pack AWD shipments structurally never qualify for investigation, and Amazon-admitted-valid disputes still only recover 1% of the overcharge. On compliance chargebacks, sellers manually watch the Account Health dashboard and open one Seller Support case at a time with ad hoc rep replies; no tool auto-monitors SIPP/labeling status per ASIN or drafts dispute evidence within the 7-day window.
- **Willingness-to-pay**: Existing spend on percentage-of-recovered-funds reimbursement services; sellers already pay for FBA prep/barcode compliance tools; quantified vendor figure: $1.80–$4.40 per-unit SIPP non-compliance chargeback, i.e. $3,200/month ($38,400/year) for a seller shipping 1,000 units/month of a 3lb uncertified product.
- **Reachability**: r/FulfillmentByAmazon, Amazon Seller Central forums, SIPP/FNSKU-focused blogs (Packwire, Carbon6, SellerLabs).
- **Confidence: Medium-high** — verbatim, dated, quantified dollar figures, corroborated across 2 lanes, though it spans two related-but-distinct Amazon financial-friction mechanisms (fee-reimbursement disputes vs. compliance chargebacks) bundled here as one structural pattern.
- **Source lanes**: reddit-ecommerce, smb-backoffice (2 lanes — merged from "Amazon fee-billing errors" and "Retail/Amazon compliance chargebacks on small suppliers")

---

## C09: Shopify multi-store/multi-location inventory sync apps corrupt data instead of failing safely

- **Problem**: Apps that sync inventory/products across multiple Shopify stores or locations periodically go out of sync, misread source data, or crash mid-sync — and when they fail, they zero out or negative-out live inventory across thousands of SKUs, causing overselling and multi-hour manual recovery. This recurs across at least three unrelated apps, indicating a category-wide architecture gap (no dry-run/rollback/change-diff safety net before writes hit live inventory).
- **Who**: Multi-location or multi-brand Shopify merchants relying on third-party sync apps because Shopify's native multi-location tools don't cover cross-store sync.
- **Evidence**:
  - "Don't install the app!!! Almost 2000 variants turned to negative qty...I need to fix up the whole inventory which will take me a while" — Italy Station by GD — https://apps.shopify.com/multi-store-inventory-sync/reviews — 2020-07-17
  - "This was a catastrophic failure. It took me over 3 hours of manual effort...This operational loss...cost my business thousands of dollars." — Babies Mart Australia — same URL — 2025-11-19
  - "I am extremely disappointed with the service I received from Stock Sync...frequent synchronization errors causing overselling and stockouts" — Media Alliance CT (South Africa) — https://apps.shopify.com/stock-sync/reviews — 2024-12-02
  - "all inventory level for connected products in both stores is either zero or even negative" (2,000+ products needed manual adjustment after uninstall) — Kurti Connection USA — https://apps.shopify.com/easify-inventory-sync/reviews — 2026-06-21
- **Incumbents & failures**: Multi-Store Sync Power (Free / $19.99–$49.99/mo, 4.5★/139 reviews, 11% 1-star), syncX Stock Sync (Free / $7–$10/mo, 4.7★/860 reviews, 48 one-star reviews citing overselling), Easify Inventory Sync (Free / $9.99–$59.99/mo, 4.5★/68 reviews) — none ship an undo/rollback or pre-write diff-preview for bulk inventory changes, so sync-engine misfires cause silent, full-catalog damage.
- **Willingness-to-pay**: Merchants already pay $10–$60/mo for these tools and stay subscribed for years despite the bugs — proven willingness to pay for sync infrastructure; the gap is safety/reliability, not price.
- **Reachability**: Shopify App Store's "Inventory management" category (built-in discovery where the 3 competitors already live); buildable via Shopify Admin GraphQL API.
- **Confidence: High** — verbatim, dated (recurring 2020–2026, most damaging reviews Nov 2025 and Jun 2026), independently repeated across 3 unrelated apps within one lane.
- **Source lanes**: app-marketplaces

---

## C10: eBay serial return/refund abuse with no visibility into buyer history

- **Problem**: Buyers file false "item not as described"/damage/tampering claims to extract free items or partial refunds, and eBay's tools give sellers almost no way to see a buyer's return-abuse pattern before accepting an order, nor reliable recourse afterward — negative feedback cannot be left for buyers at all.
- **Who**: eBay sellers of resellable/collectible or higher-value goods (LEGO, designer handbags, electronics).
- **Evidence**:
  - "the point is a buyer lied, used my bag, tampered with the evidence, and is being rewarded for it while i'm left cleaning up her mess on a deadline... I sold this to fund a medical procedure and i'm watching the clock run out." — u/mrrogerstheleviathan — https://www.reddit.com/r/eBaySellerAdvice/comments/1uligg5/ — 2026-07-02 — 19 comments, score 23
  - "Caught my first truly nasty buyer after 350 items sold over the past 20 years... When I look at their feedback left for others the count says 95 but only three are visible (all negative of course)... Not being able to leave negative feedback for buyers is wild." — u/supinterwebs — https://www.reddit.com/r/eBaySellerAdvice/comments/1u9cv1c/ — 2026-06-18 — 10 comments, score 12
  - "Ebay always approves up to 50% deduction for weird return issues and tells me this will have no effect on my seller account. I just don't want to wake up one day where my TRS account is penalized or suspended..." — u/Fragrant_Lettuce9855 — https://www.reddit.com/r/eBaySellerAdvice/comments/1uafqp7/ — 2026-06-19 — 14 comments
  - "Buyer claims sealed lego has been opened... My listing includes pics of untampered seals so idk if they are just trying to scam" — u/Chilorious — https://www.reddit.com/r/eBaySellerAdvice/comments/1uqcjom/ — 2026-07-08 — 21 comments, score 21
- **Incumbents & failures**: eBay's Seller Protections approve claims despite contradicting photo/report evidence; buyer return-abuse history isn't surfaced usably (raw feedback-left-for-others count vs. visible count mismatch, no aggregate "return rate" flag pre-sale).
- **Willingness-to-pay**: No explicit dollar figures were found, but the volume of duplicate/near-duplicate distress posts and ad hoc evidence-bundling workflows point to unmet demand for a return-risk/buyer-history screening tool.
- **Reachability**: r/eBaySellerAdvice — small but highly engaged (double-digit comments common relative to subscriber base).
- **Confidence: Medium-high** — verbatim, very recent (through 2026-07-08), single lane, no explicit price/WTP quote.
- **Source lanes**: reddit-ecommerce

---

## C11: Client approval & feedback chaos / version control at agencies

- **Problem**: Agencies lose track of who approved what, when — clients "lose" approval emails, sign off on one version but reference another weeks later — with no single source of truth, causing rework, disputes, and slipped timelines.
- **Who**: Small-to-mid marketing/creative/dev agency owners and account managers juggling multiple concurrent clients.
- **Evidence**:
  - "Lately we seem to struggle with clients losing approval requests in their emails, and it's hard to keep a clear record of what was actually approved, when, and by who." — https://www.reddit.com/r/agency/comments/1k9iiz9/how_are_you_all_managing_client_approvals/ — 2025-04-28 — score 23, 87 comments
  - "instead of revision rounds, you give clients a time-scoped 'feedback window.' 10 business-days of unlimited feedback... After the 10 days, any additional feedback is completed at an agreed-upon day rate... Since changing this policy, I have never once had to bill a client for an additional day of work." — https://www.reddit.com/r/agency/comments/1rko6rg/anyone_else_deal_with_slow_client_feedback_and/ — 2026-03-04 — score 51, 74 comments
  - "What you're describing version 2 approved instead of version 7, three weeks gone — that's not a tools problem... I've looked at a few of those 'project management for agencies' type apps, but they always seemed like overkill for what I needed." — https://www.reddit.com/r/Entrepreneur/comments/1rnbglu/agency_people_how_are_you_not_losing_your_mind/ — 2026-03-07 — score 4, 39 comments
- **Incumbents & failures**: Agencies cobble together email threads and shared Google Drive folders with manual naming conventions, explicitly because "project management for agencies" apps "seemed like overkill." Marker.io mentioned once favorably for in-context commenting, but most rely on ad hoc, undisciplined processes.
- **Willingness-to-pay**: Agencies self-invented a "10-day feedback window, then day-rate" monetization pattern — a product that automated/enforced this would map directly onto a workflow already valued enough to build manually; agencies already pay for Marker.io and evaluate PM tools.
- **Reachability**: r/agency — small but highly on-topic (74–146 comments on relevant threads), owners identify themselves and describe real operational detail.
- **Confidence: High** — verbatim, dated, high engagement, single lane.
- **Source lanes**: freelance-agency

---

## C12: Amazon listing hijacking with no reliable recovery path

- **Problem**: Third parties (often overseas sellers) take over an existing product listing — changing title/brand/images or riding the buy box — and Amazon's stated remedy (Brand Registry, file a report) is slow, inconsistent, and frequently doesn't stop repeat hijacks.
- **Who**: Private-label FBA sellers, especially newer or non-trademarked/generic-product sellers without Brand Registry protection.
- **Evidence**:
  - "Apologies for the long post but this is my Hijacker Nightmare..." — u/NormalDevelopment148, "Hijacker threatened to 'treat my listing like a dog and kill it'" — https://www.reddit.com/r/FulfillmentByAmazon/comments/1qu2hik/ — 2026-02-02
  - "My listing was recently hijacked by a Chinese seller and they changed the title and brand..." Amazon told the seller it would only act "until I'm in Brand Registry." — u/brennybaseball — https://www.reddit.com/r/FulfillmentByAmazon/comments/1oht8ql/ — 2025-10-27 — 9 comments
  - Two separate sellers posted the identical question "Has anyone successfully recovered a hijacked Amazon listing?" on the same day, hours apart — u/CompetitiveDrop8022 (https://www.reddit.com/r/FulfillmentByAmazon/comments/1usqkrt/) and u/ProtectionCultural18 (https://www.reddit.com/r/FulfillmentByAmazon/comments/1usq7vi/) — both 2026-07-10
- **Incumbents & failures**: Brand Registry + Transparency Program are Amazon's official answer, but hijacking still happens to registered/trademarked brands; Amazon's own in-thread reply admits "Amazon doesn't prevent hijackers from accessing listings" — only a reporting path after the fact. Manual 24/7 listing monitoring is the informal workaround, which doesn't scale for solo sellers.
- **Willingness-to-pay**: Existing chatter about SaaS "alert" tools for listing changes suggests a nascent paid-monitoring market forming, though current tools address detection, not recovery/response.
- **Reachability**: r/FulfillmentByAmazon, r/AmazonSeller — hijacking questions appear multiple times per month.
- **Confidence: Medium-high** — verbatim, very recent (2026-07-10, day before research), single lane, WTP is inferred from behavior rather than an explicit price quote.
- **Source lanes**: reddit-ecommerce

---

## C13: Involuntary churn / failed-payment recovery for small SaaS

- **Problem**: Small SaaS/subscription businesses lose 2–15% of MRR every month to failed card payments that go unrecovered because dunning is absent, generic, or too slow (24–48hr first-touch) — operators often don't discover the leak until they manually dig through Stripe.
- **Who**: Solo/small-team SaaS founders running $2K–10K+ MRR subscription businesses on Stripe.
- **Evidence**:
  - "Involuntary churn from failed Stripe payments...erase 5-15% of MRR silently" — heze, comment on [Where is your revenue quietly disappearing?] — https://www.indiehackers.com/post/where-is-your-revenue-quietly-disappearing-e620ea7771 — 2026-03-09 — thread: 6 likes, 1 bookmark, 95 comments
  - "most dunning tools fire their first recovery email 24 to 48 hours after a failure. By then the customer is already mentally checked out." — davidjamess (founder of RecoveryMRR), comment on [I went looking for a SaaS opportunity and found one in failed-payment recovery] — https://www.indiehackers.com/post/i-went-looking-for-a-saas-opportunity-and-found-one-in-failed-payment-recovery-259e73871e — 2026-04-29 — post: 2 likes, 15 comments
  - Original post (Greg Smethells, same thread): existing tools "charge percentage fees (15–30%), fixed high minimums ($250+/month), or require manual implementation," while roughly 2–5% of monthly MRR silently disappears to involuntary churn for founders in the $2K–10K MRR range — 2026-04-29
  - Greg Kopyltsov (KeywordSearch.com founder), "[Is there a service for recovering Stripe failed payments?]" — https://www.indiehackers.com/post/is-there-a-service-for-recovering-stripe-failed-payments-6bde0e94c4 — 2021-09-26 — describes "a significant amount of failed payments on subscriptions," ProfitWell's Retain priced out of reach for an early-stage founder
- **Incumbents & failures**: Stripe's native Smart Retries (free but limited, generic timing); enterprise tools (ProfitWell Retain/Churnkey/Churn Buster, ~$250+/mo or 15–30% of recovered revenue) too expensive/complex for sub-$10K MRR founders; hand-rolled retry logic rarely gets built.
- **Willingness-to-pay**: Multiple named competitors already charging $29–99/mo with users citing them approvingly (Stunning.co $50/mo, RecoverKit $29/mo, RecoveryMRR $99/mo); explicit statements that $249+/mo is "too expensive for indie founders."
- **Reachability**: Indie Hackers Ideas/Validation and SaaS groups, Stripe App Marketplace listings, SaaS founder newsletters.
- **Confidence: High** — verbatim, dated, durable multi-year pattern (2021 thread corroborated by March–April 2026 threads), established price band.
- **Source lanes**: founder-communities

---

## C14: Scope creep & unlimited revisions — freelancers do free extra work

- **Problem**: Freelancers repeatedly do free extra work — "one more revision," "can you also add X" — because they have no clean, low-friction way to flag it as out-of-scope and bill for it in the moment; creative freelancers specifically get pulled into open-ended revision cycles with no defined "done."
- **Who**: Solo freelance web/graphic designers and developers on fixed-price/flat-fee projects (Upwork and direct-client), and creative freelancers (branding, motion, video) doing client-facing work.
- **Evidence**:
  - "Client hired me for a landing page: $2,000 for 20 hours of work (my rate is $100/hr). Then the extras started... Final tally: 43 hours worked, $2,000 paid. That's $2,300 in unpaid work" — https://www.reddit.com/r/freelance/comments/1ozc3zq/lost_2300_to_scope_creep_on_one_project_how_do/ — 2025-11-17 — score 63, 109 comments
  - "The issue isn't just the number of revisions, it's the overall chaos. One day they want something, the next day it's the opposite... I end up making 5–6 versions of the same video, and it feels like there's never a real 'final.'" — https://www.reddit.com/r/advertising/comments/1nuir9m/how_do_you_deal_with_endless_chaotic_feedback/ — 2025-09-30 — score 35, 52 comments
  - Third-party validation post: "Freelancers lose $7,800–$15,600/year to unbilled scope creep... 57% of agencies lose $1K–$5K monthly [to it]... 99% fail to bill for out-of-scope work" and a $19–79/month tool concept tested well — https://www.microgaps.com/gaps/2026-02-18-ai-scope-creep-detector-freelancers — accessed 2026-07-11
  - Commenters cite concrete billing rates for enforcement: "$50/hr for extra rounds," "not less than $50 per round of revisions," "10% of project fee" per extra round — r/GraphicDesigning and r/graphic_design threads, 2025-08-18 and 2025-09-21
- **Incumbents & failures**: Advice is purely after-the-fact ("write a better contract," "define scope upfront") — nothing intervenes in the moment a scope-creep request arrives; general invoicing/accounting tools (Wave, FreshBooks, Zoho) don't track scope at all; manual workarounds (capping rounds in the SOW, watermarking drafts) exist but aren't enforced automatically.
- **Willingness-to-pay**: Freelancers already improvise paid mitigations (day-rate billing for extra rounds, 50% deposits); the MicroGaps validation post found freelancers would pay $19–79/month for a dedicated scope-creep tracker.
- **Reachability**: r/freelance, r/Upwork, r/GraphicDesigning, r/graphic_design, r/advertising — active, high-comment threads (25–109 comments), freelancers post under real usernames.
- **Confidence: Medium-high** — verbatim, dated, single lane, but includes independent third-party market-sizing/pricing data.
- **Source lanes**: freelance-agency (merged from "Scope Creep / Unbilled Work" + "Endless / Unlimited Revision Loops")

---

## C15: Etsy's opaque, seemingly-broken ad algorithm eating seller margin

- **Problem**: Etsy's offsite-ads program becomes mandatory once a shop crosses $10k in trailing annual sales (15% fee, no opt-out), and separately on-site Etsy Ads budgets get algorithmically capped for opaque "risk factor" reasons that support cannot explain or fix — sometimes flipping on and off within 24 hours.
- **Who**: Established Etsy sellers ($1k–$70k+ lifetime sales) — i.e., sellers who've proven traction and are now squeezed on the way up.
- **Evidence**:
  - "6 years, 67k sales, Star Seller... my ad budget got capped at $100/day for a FULL MONTH. Yesterday the limit was finally lifted. Today, less than 24 hours later, I'm capped at $100 again. Same vague garbage message about 'risk factors in your recent shop or order activity'... I'm tired of shouting into a script." — u/ThePsychicArtist — https://www.reddit.com/r/Etsy/comments/1tqxw0b/ — 2026-05-29 — 4 comments
  - "In that time I have made close to $1000 in sales on small items and they took $327 dollars in marketing fees and $93 dollars in Etsy fees. Damn near eating up almost my entire profit which makes it damn near impossible to continue producing new items..." — u/Successful-Train-259 — https://www.reddit.com/r/Etsy/comments/1tpmef6/ — 2026-05-27 — 45 comments (highest-engagement Etsy thread found)
  - "the fees stack to about thirty percent of the sale price by the time you add transaction, payment processing, listing, and offsite ad fees... etsy offsite ads are mandatory once you cross ten thousand in sales in a year. you cannot opt out." — u/EntranceMaster8099 — https://www.reddit.com/r/Etsy/comments/1tt5kdy/
- **Incumbents & failures**: No native mitigation — Etsy support gives templated "your account is in good standing" replies that directly contradict the visible ad cap. A seller built and gave away a free tool to "scan your whole Etsy shop and flags which listings are secretly losing money after fees" (u/SubstantialSky3154).
- **Willingness-to-pay**: No explicit price quotes, but the free fee-profitability tool being built/shared shows the underlying "what's my real margin after fees" question is unanswered by Etsy's own dashboard.
- **Reachability**: r/Etsy — large, very active; fee/ads complaints recur constantly.
- **Confidence: Medium** — verbatim, dated, single lane, no explicit price/WTP quote (inferred from behavior only).
- **Source lanes**: reddit-ecommerce

---

## C16: Late payment chasing & freelancer/contractor administrative overhead

- **Problem**: Clients routinely pay late or not at all, and the emotional labor of chasing payment (multiple reminder emails) is a recurring, named pain point; more broadly, freelancer admin (contracts, invoicing, payment chasing) is fragmented across Gmail/WhatsApp/Notion/spreadsheets because tools don't talk to each other.
- **Who**: Freelancers and small agencies (dev, design, marketing) including international freelancers with weak legal recourse (e.g., India); solo freelancers/independent contractors without an agency or ops team.
- **Evidence**:
  - "According to Remote's 2025 report, 85% of freelancers get paid late at least sometimes. 21% get paid late MORE THAN HALF THE TIME... 'I hate chasing payments. It's awkward. I forget to follow up. I waste hours writing "just checking in" emails.'" — https://www.reddit.com/r/Entrepreneur/comments/1pjtqd9/found_a_validated_problem_85_of_freelancers_paid/ — 2025-12-11 — score 2, 28 comments
  - "Legal notice thn civil suit for breach of contract." / "But there was no written contract" / "The financials was discussed on the call" — https://www.reddit.com/r/LegalAdviceIndia/comments/1sbc4z7/im_a_freelancer_and_my_client_is_not_paying_up/ — 2026-04-03 — score 12, 16 comments
  - "Projects sit in Gmail or WhatsApp, portfolios in Notion, payments on random links, and invoices in spreadsheets." Based on research with 60+ freelancers; cites a concrete case of a ₹70,000 client payment dispute loss tied to this fragmentation. — Abhijeetp_Singh — https://news.ycombinator.com/item?id=46197005 — 2025-12-08
  - "smart invoicing that learns when your clients pay," built "to reduce time spent chasing overdue payments" via adaptive reminders — "Show HN: Uaryn" — https://news.ycombinator.com/item?id=47102030 — 2026-02-21
- **Incumbents & failures**: Existing tools "(Wave, FreshBooks, Zoho) have payment reminders, but they're buried in massive accounting suites with 50+ features. The reminders are generic and nobody really uses them effectively." Freelancers without contracts have essentially no recourse beyond small-claims court, which most won't pursue for smaller sums.
- **Willingness-to-pay**: The Entrepreneur-thread builder targeted "$15-19/month, aiming for $5K MRR in 6-12 months" for a single-purpose "chase your payments" tool; Trustora priced at flat $150/contract, Uaryn at $9/month Pro — two independent builders shipped priced products within a 6-week window of each other.
- **Reachability**: r/Freelancers, r/Entrepreneur, HN Show/Ask threads, Indie Hackers, r/consulting.
- **Confidence: Medium** — verbatim, dated, corroborated across 2 lanes, though the hackernews threads show thin organic engagement (low points/comments) per that lane's own caveat, and one commenter warned automated reminders could "sour" the client relationship.
- **Source lanes**: freelance-agency, hackernews (2 lanes — merged from "Late & Non-Payment — Chasing Invoices" and "Freelancer/Contractor Administrative Overhead")

---

## C17: WooCommerce/WordPress booking & appointment plugins — broken multi-channel sync at premium prices

- **Problem**: Booking/appointment plugins fail at the two things merchants need most: reliably preventing double-bookings across channels (e.g., Booking.com plus the business's own site) and staying stable through paid upgrades — freezing, infinite loops, and broken calendar APIs are recurring complaints on the category's most expensive plugin.
- **Who**: Small service businesses (salons, tutors, rental/equipment businesses, clinics) running WordPress/WooCommerce sites.
- **Evidence**:
  - "The calendar never work for me, it got stuck in an infinite loop loosing a lot of money due to the inability to make bookings" — jonathan2138 — https://wordpress.org/support/plugin/bookings-and-appointments-for-woocommerce/reviews/ — 2025-08-26 — 1-star
  - "For a plugin of this price it's really disappointing...bug with email notification and WPML...API that isn't working at all" — belperroud — same URL — 2025-06-05 — 1-star
  - "It only synchronizes with a single calendar...you cannot independently synchronize reservations made through the Booking.com portal with those made on the business's official website." — Jairo — same URL — 2026-02-23 — 3-star
  - Overall rating for this listing: 2.7★ out of 5 across 60 reviews, with 38% at 1-star and only 20% at 5-star.
- **Incumbents & failures**: WooCommerce Bookings — ₹23,900/year (~$280) 1-year plan (woocommerce.com/products/woocommerce-bookings), 2.7★/60 reviews, single-calendar sync only. Amelia ($49–$199/yr) — 4.6★/774 reviews but 56 one-star + 14 two-star citing recurring double-booking-on-reschedule bugs. BookingPress (free/freemium competitor) was removed from the WordPress.org directory Feb 1, 2025, leaving a hole in the low end.
- **Willingness-to-pay**: Merchants pay up to $280/year for WooCommerce Bookings despite a 2.7-star rating — price isn't the barrier, reliability is.
- **Reachability**: wordpress.org support forums (organic SEO/support-forum indexing), WooCommerce Marketplace.
- **Confidence: Medium-high** — verbatim, dated (Aug 2025–Feb 2026, all within the last 12 months), single lane.
- **Source lanes**: app-marketplaces

---

## C18: Opaque, manual claim-denial appeals burn medical billers' time

- **Problem**: Medical billers/coders fight claim denials from payers (Zelis, BCBS, Humana) whose denial logic is undocumented or inconsistent, forcing manual, code-by-code appeals with no clear rulebook; industry data shows automated payer denials are wrong roughly 9 times out of 10 when actually contested.
- **Who**: Medical billing/coding staff and practice managers at small-to-mid physician practices.
- **Evidence**:
  - "I am getting increasingly frustrated with Zelis coding denials." — Jessie W, CPC, AAPC forum, "ZELIS HELP!" — https://www.aapc.com/discuss/threads/zelis-help.199631/ — 2024-08-08
  - "Zelis is horrible to get any answer's as to why they do edit's, pricing, etc." — Woakes73, same thread — 2025-03-23
  - "They can't even figure out how to use our claim number in their system so we can cross reference a claims they are inquiring about." — Woakes73, same thread — 2025-03-23
  - Corroborating context: at HBMA's 2025 fall conference, insurer use of AI to deny claims "at an alarming scale" dominated every panel, and Cigna's algorithm reportedly denied 300,000 claims in two months at 1.2 seconds per review with a 90% appeal-reversal rate — AAPC blog, "Taking a Stand Against AI Denials" — https://www.aapc.com/blog/93960-taking-a-stand-against-ai-denials/
- **Incumbents & failures**: Billers rely on manual research, peer forum crowdsourcing, and case-by-case phone calls to payers that "provide zero help." Existing billing software surfaces the denial but doesn't help predict or systematically fight it.
- **Willingness-to-pay**: Indirect but structural — denial management/appeals is a recognized paid service category (billing companies/RCM vendors already charge percentage-of-recovered-revenue fees for exactly this work); the forum thread's raw engagement is modest, but every post represents a distinct paid professional with real dollars at stake per denied claim.
- **Reachability**: AAPC discussion forum (public, searchable, tag-organized), large certified-professional membership base.
- **Confidence: Medium** — verbatim, dated (Aug 2024–Mar 2025, persistent not one-off), single lane, corroborated by independent industry conference/data context.
- **Source lanes**: vertical-forums

---

## C19: Employer-side hiring overload from AI-generated applications

- **Problem**: Hiring managers are drowning in application volume inflated by AI-generated/tailored resumes and easy-apply spam, to the point that automated ATS/keyword filtering screens out the most qualified candidates and hiring has "reverted to nepotism."
- **Who**: Hiring managers/founders at small-to-mid companies running lean (no dedicated recruiting team).
- **Evidence**:
  - "We had 1200 applications for an extremely niche role... in practice, we couldn't find folks we didn't already know because various keyword-focused searches and AI filtering tend to filter out the most qualified candidates... The process is so broken right now that we're 100% back to nepotism." — jofer — https://news.ycombinator.com/item?id=45261848 — 2025-09-16 — thread: 283 points/448 comments
  - "If you're a team of 5, handling 1,200 resumes, how much money are you expected to invest in this process?" — mionhe — same thread — 2025-09-17
  - "~40% of applications have obvious, major inconsistencies...~90% of remaining applications fail to meet basic qualifications." — hansvm — same thread — 2025-09-17
  - "When you get 200+ applicants in a SWE role, what do you actually do to narrow it down?... If you had a tool that sat in front of your ATS that helped filter hundreds of applicants down to 25 applicants, would that be a tool you would use?" — dark7, "Ask HN: What do you hate about hiring?" — https://news.ycombinator.com/item?id=45854849 — 2025-11-08
- **Incumbents & failures**: Standard ATS keyword filters and generic "AI filtering" both over- and under-filter — spam gets through while qualified candidates get screened out; manual review is infeasible at 1000+ applications for a small team; automated ranking risks discrimination/bias liability, which incumbents haven't solved ("Lawsuit heaven for apprehended bias in hiring" — ggm, same thread).
- **Willingness-to-pay**: Weakest signal in this set — no explicit dollar figure quoted by any employer; a founder directly asking "would that be a tool you would use?" is soliciting validation, not proving it.
- **Reachability**: HN Ask/Tell HN (one of HN's most recurring topics), recruiting-ops subreddits.
- **Confidence: Medium** — verbatim, dated, very high engagement (448 comments — one of the most-engaged threads in the entire dataset), but explicitly flagged by its own lane as having the "weakest direct willingness-to-pay evidence" of its candidate set.
- **Source lanes**: hackernews

---

## C20: QuickBooks Online account lockouts freezing payroll/financial operations

- **Problem**: Identity-verification processes lock business owners out of their own QuickBooks Online accounts, in at least one case forcing a company to run payroll manually by paper check — an acute operational failure, not a UX gripe.
- **Who**: Small business owners/office managers (11–50 employees) running payroll and invoicing through QuickBooks Online, paying $38–$275+/month depending on tier.
- **Evidence**:
  - "lock us out of payroll so now we have to pay all of our employees by paper check" — Julie F., Office Manager - Payroll Coordinator, Construction, 11-50 employees, QuickBooks Online review, Capterra, rating 1.0 — https://www.capterra.com/p/190778/QuickBooks-Online/reviews/ — 2026-06-03
  - "recurring connection issues with financial institutions, occasional backend glitches, and poor customer support" — Jonathan S., Founder, Apparel & Fashion, QuickBooks Online review, Capterra, rating 2.0 — same URL — 2026-06-02
  - "Poor Customer Support" flagged as a complaint category with 49 mentions in aggregated G2 user reviews of QuickBooks Online; support described as "really frustrating" because it's difficult to reach a live person, and "not always guaranteed that they speak English very well" (WebSearch synthesis of G2 QuickBooks Online pages) — https://www.g2.com/products/quickbooks-online/reviews
- **Incumbents & failures**: QuickBooks Online ($38–$275/month across tiers) is the default accounting system for millions of small businesses; its fraud/verification systems appear to trigger false positives that cut off payroll access with no fast remediation path, and support is routed through chat before reaching a human.
- **Willingness-to-pay**: This is the most entrenched, hardest-to-switch category (accounting data, tax filings, bank connections) — continued high pay despite acute failures (manual paycheck runs) signals customers are trapped rather than satisfied, a "captive but furious" signal.
- **Reachability**: r/smallbusiness, r/Bookkeeping, QuickBooks user Facebook groups, Capterra reviewer profiles.
- **Confidence: Medium** — verbatim, the most recent dates of any single-source candidate in this set (June 2026), single lane, only 2 direct quotes plus one aggregated-mentions data point.
- **Source lanes**: review-sites

---

## Appendix: Dropped candidates

| Candidate | Lane(s) | Reason dropped |
|---|---|---|
| Amazon seller-account suspension bureaucracy | reddit-ecommerce | Weakest recency in its lane (newest evidence Dec 2025) and most crowded competitively — established paid reinstatement-consultant industry already addresses the core need, per the lane's own ranking. |
| Client ghosting during proposals | freelance-agency | No willingness-to-pay signal surfaced; the fix is behavioral/sales-process, not clearly product-shaped. |
| Vendor-continuity risk for solo/small SaaS vendors | hackernews | Sourced from a single thread only; WTP is a one-off bespoke-legal-cost inference, not a repeatable signal. |
| Inventory/accounting data integrity failures (Cin7) | review-sites | Thinner evidence base; the key $80k figure is only secondary-sourced; the lane itself flagged this for further verification. |
| Manual/spreadsheet scheduling for hourly workforces | smb-backoffice | Mature, well-served incumbent category (Homebase, 7shifts, Deputy, When I Work already monetize this); no clear underserved wedge in the evidence. |
| Zapier + QuickBooks Online trigger reliability | app-marketplaces | Narrow niche whose root cause (Intuit's webhook infrastructure) sits outside a single marketplace listing; moderate evidence only. |
| Support-ticket overload for solo/small-team founders | founder-communities | Real pain but crowded incumbent market (Intercom called "the most valuable expense" despite cost); weaker evidence than other founder-community candidates. |
| Qualified Overtime (2025 OBBBA) tracking in QuickBooks payroll | smb-backoffice | Evidence quality explicitly flagged weak by its own researcher: paraphrased only, direct fetch blocked, no verbatim text or engagement counts obtained. |
| Multi-vendor billing reconciliation for AI/automation agencies | founder-communities | Evidence from a single named commenter repeated across two threads; not corroborated by a second independent voice. |
| Analytics-to-decision gap | founder-communities | Thin engagement (1 like/2 comments) and no explicit pricing/WTP statement; flagged by its own lane as the weakest-validated candidate. |
| Carrier onboarding paperwork duplication (small trucking carriers) | smb-backoffice | No verbatim quotes, dates, or engagement counts obtainable (site blocked direct fetch); needs manual re-verification. |
| Small machine shop manual tooling/raw-material inventory tracking | smb-backoffice | Explicitly exploratory/lowest-confidence per its own researcher; no quantified evidence, dates unconfirmed. |
| Shopify returns/exchange app friction beyond billing (label fees, restocking bugs) | app-marketplaces | The phantom-billing-after-cancellation evidence was folded into C02; remaining label-fee/restocking-bug complaints are a concentrated minority within an already 4.8–4.9★ category, insufficiently corroborated to stand alone. |

---

## Summary table

| ID | Name | One-line problem | Confidence | # Source lanes |
|---|---|---|---|---|
| C01 | SMB bookkeeping document-chasing | Firms pay for bookkeeping/portals that stay manual because clients won't self-serve document collection | High | 3 |
| C02 | Billing continues after cancel/uninstall | Customers keep getting charged after cancelling, with no self-serve way to stop it | High | 2 |
| C03 | Amazon FBA "DD+7" cash-flow crunch | New Amazon reserve policy holds seller payouts 7 days after delivery, creating a working-capital squeeze | High | 1 |
| C04 | SOC 2 readiness burden | Early-stage startups hit enterprise compliance requirements with no clear path and costly consultants | High | 2 |
| C05 | Field-service software fragmentation/traps | Small trade businesses face overpriced, slow-onboarding field-service platforms and disconnected point tools | Medium-high | 2 |
| C06 | Property management software patchwork | No PM platform covers the full operating loop; managers stitch together tools and spreadsheets | High | 1 |
| C07 | AI-chatbot support walls | Category-leading SaaS replaced human support with AI chat, leaving paying SMBs unable to get help | High | 1 |
| C08 | Amazon opaque fee & compliance chargebacks | Amazon fees/chargebacks are misapplied with no proactive alert, forcing manual audit and dispute | Medium-high | 2 |
| C09 | Shopify inventory-sync data corruption | Multi-store sync apps zero out live inventory on failure instead of failing safely | High | 1 |
| C10 | eBay return/refund abuse | Sellers can't see buyer return-abuse history and have no recourse against serial false claims | Medium-high | 1 |
| C11 | Agency approval/version-control chaos | Agencies lose track of what clients approved, causing rework and disputes | High | 1 |
| C12 | Amazon listing hijacking | Third parties hijack listings with no reliable, fast recovery path | Medium-high | 1 |
| C13 | Involuntary churn/failed-payment recovery | Small SaaS lose 2-15% of MRR to failed payments with no affordable fast dunning tool | High | 1 |
| C14 | Freelancer scope creep & revisions | Freelancers do unbilled extra work due to no in-the-moment scope enforcement | Medium-high | 1 |
| C15 | Etsy opaque ad algorithm | Etsy's ad-budget caps and mandatory offsite fees erode seller margin unpredictably | Medium | 1 |
| C16 | Freelancer late-payment chasing/admin | Freelancers lose time and money chasing late payments across fragmented tools | Medium | 2 |
| C17 | WooCommerce booking plugin bugs | Premium booking plugins fail at multi-channel double-booking prevention and stability | Medium-high | 1 |
| C18 | Medical claim-denial appeals | Billers manually fight opaque, inconsistent payer claim denials | Medium | 1 |
| C19 | Hiring overload from AI applications | AI-generated application volume overwhelms small-team hiring managers and breaks ATS filtering | Medium | 1 |
| C20 | QuickBooks Online account lockouts | Identity-verification false positives freeze payroll/financial access for QBO customers | Medium | 1 |
