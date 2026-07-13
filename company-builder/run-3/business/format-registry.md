# The Royalty Report Format Registry
*WideTally's unexpected deliverable: free, public documentation of what's actually inside each retailer's royalty report. This is the founder asset — the product's core domain knowledge, published as a content moat (every "[store] royalty report explained" search lands here). It is also the run's honesty anchor: each field below is labeled by how it was verified.*

**Legend:** ✅ = verified this run from the platform's own published documentation (URL given). ◐ = standard practitioner knowledge of the file as downloaded, not re-verified from a fetched primary source this run (disclosed in record/honesty.md). Sample files in `product/sample-data/` are **synthetic** and modeled on the ✅ schema.

---

## Amazon KDP — Sales & Royalties Report
Source (fetched 2026-07-13): https://kdp.amazon.com/en_US/help/topic/G201488550

- ✅ Report is organized in tabs: **Combined Sales / eBook Royalty / Paperback Royalty / Hardcover Royalty / Orders / KENP Read** (workbook download ◐ commonly .xlsx).
- ✅ Royalty-tab fields, per Amazon's own term definitions:
  - **Royalty Date** — "Date (in local time zone) on which order payments are processed"
  - **Title**, **Author Name**, **ASIN/ISBN**, **Marketplace**
  - **Royalty Type** — "Type of royalty applicable (35% or 70%)"
  - **Transaction Type** — "Standard, Kindle Countdown Deal, Expanded Distribution" (MatchBook retired)
  - **Units Sold**, **Units Refunded**, **Net Units Sold** — "Net Units Sold = Units Sold – Units Refunded. This is the basis of your royalty calculation"
  - **Average List Price without tax**
- ✅ Orders tab: **Order Date, Title, Author Name, ASIN, Marketplace, Paid Units, Free Units**
- ✅ KENP tab: **Date, Title, ASIN, Marketplace, KENP Read** (pages read; paid from the monthly KDP Select Global Fund)
- ✅ Fund scale, from Amazon's own page footer (fetched): "Total KDP Select Author Earnings May 2026 • $70.3 Million"
- ◐ Royalty and Currency amount columns appear in the downloaded workbook per marketplace; KENP payout rate is announced monthly after the fact — which is exactly why month-to-date KU earnings are estimates in every tool, including WideTally (we label them).
- **Gotchas WideTally handles:** per-marketplace currencies; refunds as negative net units; KENP is pages not dollars until the fund rate posts; series roll-up absent ("dividing your books up by series" called out as missing by Kindlepreneur — ✅ https://kindlepreneur.com/book-sales-tracker/).

## Amazon Ads — Sponsored Products bulk/report CSV
- ◐ Campaign-level CSV export with campaign name, impressions, clicks, spend, sales (attributed at *list price*), ACOS. Not re-verified from a fetched Amazon Ads doc this run.
- **Gotcha (the product's core insight):** ACOS compares spend to attributed *sale price*, not the author's *royalty*, and attributes no KU page-read income. A "profitable" 60% ACOS on a $4.99 ebook at 70% royalty is actually losing money. WideTally recomputes ad ROI against royalty + estimated KENP. *(Mechanism labeled INFERENCE from documented royalty structures; the demo demonstrates the math transparently.)*

## Draft2Digital
Source (fetched 2026-07-13): https://draft2digital.com/faq/
- ✅ "Draft2Digital earns revenue primarily through commission on book sales, which equates to approximately 10% of the retail price of every book sale."
- ✅ "Draft2Digital shows estimated royalties on a store-by-store basis based on the list price you set."
- ◐ Authors can view/download per-store, per-title sales history (CSV) from the D2D dashboard; columns include sale date, store, title, units, list price, author earnings.

## Kobo Writing Life
- ◐ Dashboard offers CSV export of sales with date, title, ISBN, store country, units, list price, payable amount. Not re-verified this run (Kobo help center fetch not attempted within budget).

## Apple Books / Google Play Books
- ◐ Apple: monthly financial reports per storefront (tab-delimited) via iTunes Connect-style portal. Google: per-transaction CSV with buyer country and earnings. Not re-verified this run.

---

## Why this registry exists (the business logic)
1. **It is the moat made visible.** The hard part of this product is not charts — it's staying current as ~6 retailers silently change file layouts. TrackerBox (the abandoned 2019 predecessor, ✅ storyboxsoftware.com/tdownload.htm) died of exactly this treadmill. Publishing the registry recruits the community as format-change sentinels and funds the treadmill via the Updates Pass.
2. **It converts skeptics.** The ICP has been burned by tools demanding KDP credentials. Documentation that teaches them their own files — before any purchase — is trust-building the incumbents can't match without admitting their architecture needs your password.
3. **It ranks.** Nobody else wants to write "what's in a Kobo royalty CSV" content; WideTally needs to know it anyway.
