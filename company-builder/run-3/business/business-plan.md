# WideTally — Business Plan
*Version 1.0 — 2026-07-13. Every external claim links to a source fetched during this run; estimates are labeled ESTIMATE and inferences labeled INFERENCE. See `research/verification.md` for the claim-by-claim audit.*

## 1. One-paragraph thesis

Self-published authors who sell beyond Amazon ("wide" authors) reconcile money across 3–8 retailer dashboards that share no API and no common format. The tools that promise to fix this are cloud subscriptions built on scraping and credential-sharing — and the wide-author market leader is publicly failing on reliability. WideTally is a **local-first royalty and ad-ROI dashboard**: it parses the report files authors already download (KDP, Draft2Digital, Kobo, Apple, Google Play, Amazon Ads) entirely on the author's machine, produces one per-book, per-series profit picture, and never sees a password or a dollar figure. One-time price. Works offline. The author's income data never leaves their laptop.

## 2. The problem (verified)

- **The daily ritual.** "On average it takes me 15 minutes to adequately review all sales platforms... that would equate to 92 hours a year wasted" — Dave Chesson, Kindlepreneur ([source](https://kindlepreneur.com/book-sales-tracker/), fetched). A 10-year, 18-book author: "still refresh my sales page about a dozen times a day" — u/PluckyStitch, 2026-03 ([source](https://old.reddit.com/r/selfpublish/comments/1s02ax0/anyone_else_constantly_refreshing_their_kdp/), fetched).
- **KDP's own reporting is weak.** "KDP's own sales reporting platform is not great. It can be difficult to parse out the data in beneficial ways (dividing your books up by series, for example)" — Kindlepreneur (same source).
- **Ad ROI is opaque.** Authors run $81–$4,500/mo in marketing (Written Word Media 2025 survey, n=1,346, [fetched](https://www.writtenwordmedia.com/2025-indie-author-survey-results-insights-into-self-publishing-for-authors/)) and still can't tell if ads pay: "I've been running Amazon ads for 6 months... at the end of the day, I'm spending the same amount of money for no return" — u/uhoh_stinkyp, 2025-02 ([source](https://old.reddit.com/r/selfpublish/comments/1irnc2e/im_done_with_amazon_ads/), fetched). Amazon Ads reports ACOS against *sale price*, not royalty, and attributes nothing to Kindle Unlimited page reads — INFERENCE from product mechanics, flagged for the site FAQ rather than stated as fact anywhere.
- **The market leader is failing.** On ScribeCount: "Many times I myself have tried to open the program to see my data and got nothing... If you're a wide author, I would no longer recommend ScribeCount" — Kindlepreneur ([source](https://kindlepreneur.com/scribecount-review/), fetched).
- **No API exists to build on.** "Right now, Amazon Selling Partner API does not return any data related to Kindle Direct Publishing (KDP)." — official Amazon response, 2025-10-07 ([source](https://github.com/amzn/selling-partner-api-models/discussions/4975), fetched). Every tool in this category ultimately runs on the same files the author can download themselves.

## 3. The customer

**ICP:** working indie authors with 3+ titles earning $100–$5,000/mo, publishing wide or planning to go wide.
- 62% of surveyed working authors publish at least partly outside KDP Select (30% fully wide, ~32% mixed) — Written Word Media 2025 (fetched).
- 20% of surveyed authors earn $500–$5,000/mo; 13% earn $5,000+ (same source). These are people for whom royalty numbers are grocery money, not vanity metrics.
- Scale of the space: self-published ISBN registrations passed 2.6M titles in 2023 and 3.5M in 2024 (+38.7%) — Bowker figures via Publishers Weekly (search-verified).

**TAM/SAM/SOM (labeled):**
- TAM (ESTIMATE): all English-language working self-pub authors with recurring royalties — order of hundreds of thousands (no reliable published census exists; deliberately not inventing one).
- SAM: authors who already pay for sales tracking — bounded by the incumbent category's existence at $5–29/mo across five tools (verified pricing).
- SOM year-1 (ESTIMATE, defended in `pricing.md`): 1,000 licenses ≈ $59k revenue via the channels in `launch-plan.md`. Deliberately modest; this is a lifestyle-scale wedge that earns the right to expand.

## 4. The product

**WideTally v1 (what the demo in `product/` actually implements):**
1. **Drop your reports.** Drag in KDP royalty exports, Draft2Digital/Kobo/Apple/Google CSVs, Amazon Ads bulk CSVs. Parsing happens in the browser/local app — nothing uploads, no login, no credentials.
2. **One ledger.** Per-book and per-series earnings across every store and format (ebook/print/audio), KU page reads converted at the month's KENP rate, currency-normalized.
3. **Ads vs. royalties.** The number nobody has: *royalty-based* profit per book after ad spend — not ACOS against list price.
4. **Trends without the ritual.** Month-over-month movement, best/worst store per title, release-spike views — the 15-minute ritual becomes one glance.
5. **Your data stays yours.** A folder of files on the author's machine. Export everything to CSV at any time. No account required to use it.

**v1.1+ (roadmap, not demoed):** IngramSpark and ACX/Audible parsers; Facebook/BookBub ads import; tax-season export pack; optional encrypted sync between the author's own devices.

**Why local-first is a structural moat here (not a slogan):**
- No API exists (verified) → cloud adds fragility (scraping/extensions that break when Amazon redesigns) without adding data access.
- Incumbent reliability failures are the #1 verified complaint about the leader.
- Authors' income data + KDP credentials never leave home — an easy trust story against extension-based tools that require KDP re-authentication ("frequent KDP re-authentication required" is a verified Book Report complaint via Kindlepreneur).
- Precedent: **TrackerBox** sold this exact model (local Windows app, 21 retailer report formats, one-time purchase) and was abandoned in 2019 (storyboxsoftware.com, fetched; last release 2019-09-29). The slot is proven and empty. Named honestly as prior art.

## 5. Competition (all pricing fetched/verified this run)

| Tool | Model | Price | Weakness (verified where cited) |
|---|---|---|---|
| ScribeCount | Cloud, 30+ platforms | $9.99–19.99/mo ($185/yr) | Reliability: "tried to open the program... got nothing"; Kindlepreneur withdrew recommendation |
| Publisher Champ | Cloud, 24 integrations | $16.99–21.99/mo | Kindlepreneur's current pick; subscription-only; data lives with vendor |
| PublishWide | Cloud | $29/mo | "expensive for features offered... almost too simple" (Kindlepreneur) |
| Book Report | Browser extension | Free <$1k/mo, then tiered to $249/mo | Amazon-only; "frequent KDP re-authentication required" |
| BookTrakr | Cloud | $5–10/mo | Legacy |
| TrackerBox | **Local desktop** | One-time | Abandoned since 2019; .NET 4.0-era; formats stale |
| RoyaltyDesk (MS Store) | Local | — | Surfaced in search, not deeply verified; adjacent |
| Spreadsheets | DIY | Free | The thing everyone quits: "I was using Excel, but it is getting harder and harder as I publish more books" ([r/selfpublish, fetched](https://old.reddit.com/r/selfpublish/comments/108pa8r/what_accounting_software_do_you_use_to_track/)) |

**Positioning sentence:** *Every other tracker asks you to trust their servers with your income; WideTally is the only maintained tracker where that question never comes up.*

## 6. Business model

See `pricing.md` for full rationale. Summary:
- **WideTally License — $59 one-time**, includes 12 months of format updates (parsers for retailer report formats, which drift).
- **Format Updates Pass — $19/yr** after year one (optional; app keeps working forever on formats it already knows).
- **Free: WideTally Lite** — full app limited to 2 books, no time limit. The habit-forming tier and the honest trial.
- 3-year cost comparison: WideTally $97 vs ScribeCount ~$555 vs PublishWide ~$1,044.

Unit economics (ESTIMATES, labeled): COGS ≈ $0 marginal (local software); support estimated at 10–15 min/customer average founder time; parser maintenance is the real cost — budgeted as ~1 founder-week per quarter, funded by the updates pass. Break-even against a $2k/yr tools budget (ESTIMATE) at ~40 licenses.

## 7. Go-to-market

Full plan in `launch-plan.md`. Channel logic: sell where the verified complaints live — Kindlepreneur review pipeline (its "best tracker" roundup is the category's kingmaker and currently crowns a subscription tool), r/selfpublish, wide-author communities (Wide for the Win), author newsletters, and a "Report Format Registry" content moat (see `business/format-registry.md`) that earns permanent SEO for every "[retailer] royalty report explained" query.

## 8. Risks (expanded in record/red-team.md)

1. **Format drift treadmill** — retailers change report formats; mitigated by the updates-pass business model (it *funds* the treadmill) and registry-driven community reporting; residual risk real.
2. **Amazon ships better native reporting** — mitigated: wide authors' problem is cross-retailer by definition; Amazon has no incentive to aggregate competitors.
3. **Incumbent recovers** (ScribeCount stabilizes; Kindlepreneur notes "early 2026... some improvements") — mitigated by architectural differentiation, not feature race.
4. **Small ARPU / lifestyle-scale ceiling** — accepted deliberately; this is a wedge business.
5. **One-time pricing revenue decay** — mitigated by updates pass + Lite→paid upgrade path; modeled honestly in pricing.md.
6. **Trust bootstrap** — a local app asking authors to open financial files must earn trust: open-source the parsers (planned), checksum'd releases, no-network-calls verifiable by design.
