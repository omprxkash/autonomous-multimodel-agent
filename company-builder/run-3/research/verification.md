# Skeptic Verification Pass — WideTally thesis
Date: 2026-07-13. Every load-bearing claim of the winning thesis was independently re-fetched in the main session (not trusted from the lane agent). Result: **thesis holds; one new competitor found and absorbed into positioning.**

## Claims re-verified first-hand

| # | Claim | Source | Status |
|---|-------|--------|--------|
| 1 | Checking sales across platforms costs authors ~15 min/day ≈ 92 hrs/yr | https://kindlepreneur.com/book-sales-tracker/ | **VERIFIED verbatim** ("On average it takes me 15 minutes to adequately review all sales platforms... 92 hours a year wasted…eek!") |
| 2 | "KDP's own sales reporting platform is not great. It can be difficult to parse out the data in beneficial ways (dividing your books up by series, for example)" | same page | **VERIFIED verbatim** |
| 3 | ScribeCount (wide-author market leader) unreliable; reviewer no longer recommends it | https://kindlepreneur.com/scribecount-review/ | **VERIFIED verbatim** ("Many times I myself have tried to open the program to see my data and got nothing"; "If you're a wide author, I would no longer recommend ScribeCount"; "I currently can't support the program with the status it's at today") |
| 4 | Category pricing: ScribeCount $9.99–19.99/mo ($185/yr); Publisher Champ $16.99–21.99/mo; PublishWide $29/mo; Book Report free→$249/mo tiered; BookTrakr $5–10/mo | both Kindlepreneur pages above | **VERIFIED** |
| 5 | KDP has **no public API** for sales/royalty data | https://github.com/amzn/selling-partner-api-models/discussions/4975 — official Amazon answer, 2025-10-07: "Right now, Amazon Selling Partner API does not return any data related to Kindle Direct Publishing (KDP)." | **VERIFIED verbatim** |
| 6 | Author-voice pain quotes (ads ROI confusion; dashboard-refresh ritual incl. 18-book veteran checking "a dozen times a day") | https://old.reddit.com/r/selfpublish/comments/1irnc2e/im_done_with_amazon_ads/ ; https://old.reddit.com/r/selfpublish/comments/1s02ax0/anyone_else_constantly_refreshing_their_kdp/ | **VERIFIED** (fetched via curl in this session; full text in research/lane-creators.md addendum below) |
| 7 | Market size: 2.6M+ self-published ISBN titles (2023), 3.5M+ (2024, +38.7%); Written Word Media 2025 survey n=1,346: 30% fully wide + ~32% mixed (62% multi-platform), 44% earn ≤$100/mo, 20% earn $500–5k/mo; marketing spend $81–$4,500/mo by income band | https://www.publishersweekly.com/pw/by-topic/industry-news/publisher-news/article/96468-self-publishing-s-output-and-infuence-continue-to-grow.html (search-surfaced Bowker figures); https://www.writtenwordmedia.com/2025-indie-author-survey-results-insights-into-self-publishing-for-authors/ (fetched) | **VERIFIED (survey page fetched; Bowker figures via Publishers Weekly search summary — marked search-verified)** |

## Disconfirming-evidence hunt (what could kill this?)
- **Found: TrackerBox** (storyboxsoftware.com/tdownload.htm, fetched) — a Windows desktop app doing exactly file-based multi-retailer sales import (21 platforms), one-time purchase, 45-day trial. **Last version 1.0.74, released 2019-09-29** — abandoned ~7 years; requires .NET 4.0/Windows XP-era stack; predates current KDP report formats. Verdict: *validates* the local file-based model (people paid for it) and proves the modern slot is empty, but it must be named honestly in competition docs. Also fetched: **RoyaltyDesk** exists in Microsoft Store (surfaced in search; not deeply verified) — flagged in competition table as adjacent.
- **Why did no cloud incumbent win wide authors?** Best evidence: reliability/scraping fragility (claim 3) — their architecture depends on scraping/extension access to dashboards Amazon keeps changing, or on authors uploading files anyway. Inference, labeled as such: a local parser of the author's own report files avoids the fragile part entirely.
- **Could Amazon ship this natively?** KDP dashboard improved (2021 redesign) but remains Amazon-only by definition; wide authors' problem is cross-platform. Risk noted in red-team file.

## Name/domain check
- **WideTally** chosen. RDAP: `widetally.com` → HTTP 404 at rdap.verisign.com = **available as of 2026-07-13** (checked, not purchased, per guardrails). Web search for "WideTally" software: no collisions found (only generic Tally products).
- Also available per RDAP: shelftotals.com, bookledgerapp.com, inkandsum.com (backups).

## Verdict
No load-bearing claim failed. Winner confirmed. TrackerBox finding strengthens the one-time-purchase pricing thesis and is disclosed everywhere competition is discussed.
