# Lane: Creators / Prosumers — Problem Research
Date: 2026-07-12. Researcher note on method integrity, read this first.

## Research-environment caveats (honest disclosure)
- **Reddit was unfetchable from this environment.** Both `www.reddit.com` and `old.reddit.com` are hard-blocked by the fetch tool ("Claude Code is unable to fetch"), and reddit-restricted web searches returned zero links. **No Reddit quote below is verified; none are included as primary evidence.**
- **kboards.com (Writers' Cafe)** redirects to a Tollbit paywall (HTTP 402) — unfetchable.
- **Trustpilot** returns 403 — review pages unfetchable directly; Trustpilot stats below come via secondary sources and are marked as such.
- Primary verified sources that DID work: **Hacker News via the Algolia API** (full verbatim comment text fetched per-item), **Kindlepreneur** (fetched), **ScribeCount homepage** (fetched), and **web-search result summaries** (marked "search-verified" — weaker than a page fetch).
- Mid-research, WebFetch/WebSearch hit a monthly spend limit, which cut off pricing-page fetches for OpusClip/Castmagic. Those price points are marked UNVERIFIED or search-verified accordingly.
- Two of the strongest pain quotes are from **founders describing the pain that made them build a tool** (Show HN posts). That is real first-person pain plus a build-worthy signal, but it is self-interested testimony; labeled as such.

---

## Candidate 1 — Consolidated sales + ads dashboard for self-published (KDP/"wide") authors

**Problem statement.** Indie authors selling on Amazon KDP plus other retailers (Apple, Kobo, B&N, Google Play, Draft2Digital, IngramSpark, ACX audio) have no single reliable view of sales, royalties, and ad spend. KDP itself has **no public API** — reporting is a clunky dashboard plus CSV/XLSX exports — and the incumbent aggregators are either Amazon-only or notoriously unreliable.

**Who hurts + how often.** Every "wide" indie author (publishing beyond Amazon), daily — checking sales across 3–8 dashboards is a daily ritual for most working authors. KDP-only authors hurt too (parsing KDP's reports, matching ad spend to royalties).

**Evidence (quotes):**
1. "On average it takes me 15 minutes to adequately review all sales platforms... If done every day, that would equate to 92 hours a year wasted…eek!" — Dave Chesson, Kindlepreneur, https://kindlepreneur.com/book-sales-tracker/ — **fetched and verified.** Same page: "KDP's own sales reporting platform is not great" and "can be difficult to parse out the data."
2. "Although abundant that data reported isn't always reliable. Many times I myself have tried to open the program to see my data and got nothing." — Chesson on ScribeCount (the market-leading wide-author tracker), https://kindlepreneur.com/scribecount-review/ — **fetched and verified.** He explicitly **no longer recommends ScribeCount for wide authors** due to reliability; noted major downtime and "company stability concerns."
3. Cons list for the whole category, same verified Kindlepreneur pages: ScribeCount — "overwhelming UI, unresponsive support, major downtime issues"; Book Report — "Amazon only... frequent KDP re-authentication required"; PublishWide — "expensive for features offered... almost too simple in its reporting." — **fetched and verified.**
4. Reddit r/selfpublish complaints about the KDP dashboard exist in volume but were **UNVERIFIED** (Reddit blocked in this environment); excluded from the case.

**Existing tools + pricing (all from fetched Kindlepreneur pages + fetched scribecount.com):**
- **ScribeCount** — $9.99/mo (<$1k/mo earners), $19.99/mo or $185/yr above that (scribecount.com fetched; pricing figures from fetched Kindlepreneur review). Covers 30+ platforms incl. Amazon Ads/Meta/BookBub; "no passwords required" (i.e., report-file ingestion, not APIs).
- **Publisher Champ** — $16.99/mo or $182.99/yr (Standard); $21.99/mo (Plus). 24 platform integrations. Kindlepreneur's current #1 pick.
- **PublishWide** — $29/mo.
- **Book Report** — free under $1,000/mo earnings, then paid tiers; Amazon-only; works as a browser extension over the KDP dashboard (no API exists).
- **BookTrakr** — $5–10/mo.

**The gap.** The category leader for wide authors (ScribeCount) is publicly called unreliable by the space's most-read reviewer; the free/cheap option (Book Report) is Amazon-only; everything is subscription-only with no free tier for small authors. Nobody has nailed: reliable ingestion + ad-spend-vs-royalty ROI per book/series + works offline from the files authors already download.
**API feasibility (honest).** KDP has **no public API** — this is precisely why the whole category runs on browser extensions and report-file uploads. A local tool that parses the KDP/D2D/Kobo report exports the author already has is *the same data path incumbents use*, with zero platform risk. Amazon Ads has an API but it's gated (approval required); CSV export path is open.

**Willingness-to-pay.** Five paid tools coexist at $5–29/mo; ScribeCount and Book Report price-discriminate by author income (up to $249/mo tiers referenced for Book Report), meaning higher-earning authors demonstrably pay more. Verified via fetched pages.

**Buildability as local demo (static HTML/JS + Node): 5/5.** Drag-and-drop KDP royalty XLSX/CSV + Amazon Ads CSV → parse in Node/browser → per-book/series P&L dashboard. No API, no auth, fully offline demo with sample files.

**Pain score: 8/10.** Daily, money-adjacent pain with a verified quote that the market leader is failing its users — a rare open flank in a proven paid category.

---

## Candidate 2 — Podcast post-production packaging (show notes, chapters, titles, social posts)

**Problem statement.** After recording, podcasters must produce transcripts, show notes, chapter markers, episode titles/descriptions, and social promo posts — a fragmented, multi-tool slog that consumes more time than the creative work and is a leading cause of podfade.

**Who hurts + how often.** Every independent podcaster, every episode (weekly/biweekly). Also YouTubers/video creators for the descriptions-and-distribution half.

**Evidence (quotes):**
1. "I built Headroom out of frustration with how fragmented and time-consuming podcast publishing had become. Recording was always the fun part—but after that, I found myself stuck juggling transcripts, show notes, chapters, metadata, and audio exports across different tools, losing creative momentum every step of the way." — konstantint, HN, 2025-05-27, https://news.ycombinator.com/item?id=44109915 — **fetched and verified** (full text via Algolia item API). *Founder testimony — self-interested but first-person.*
2. "content creators spend more time writing descriptions, show notes, and social posts than actually creating content... spending 90+ minutes on content distribution for each video." — LevinGruenhagen, HN, 2024-11-25, https://news.ycombinator.com/item?id=42238443 — **fetched and verified** (excerpt via Algolia). *Founder testimony; also claimed 64-creator waitlist in 48h — demand signal, self-reported.*
3. "editing, transcribing, splicing ads, chapter-marking, compiling show notes, etc., are all manual processes right now, so automating or streamlining them would be great." — tedyoung, HN, 2017-01-06, https://news.ycombinator.com/item?id=13333847 — **fetched and verified.** (Old — 2017 — included to show this pain is chronic, not a fad.)
4. r/podcasting threads on editing hours per episode: **UNVERIFIED** (Reddit blocked); excluded.

**Existing tools + pricing:**
- **Descript** — Free (60 media min/mo); Hobbyist $16/mo annual ($24 monthly); Creator $24/mo annual ($35 monthly); Business $50/mo annual ($65 monthly). Sept 2025 repricing moved to "media minutes" + metered AI credits, "making real costs harder to predict." — **search-verified** (descript.com/pricing surfaced with consistent figures across Sonix, G2, Trebble sources; direct page fetch cut off by budget).
- **Castmagic / Podsqueeze / Capsho** — same category (audio in → notes/posts out), typically ~$20–40/mo. **UNVERIFIED** (pricing fetches blocked by spend limit) — flagging honestly rather than inventing numbers.

**The gap.** Incumbents are subscription + usage-metered cloud tools whose pricing became less predictable (Descript's 2025 credit change — search-verified). The verified complaint is *fragmentation*: transcript in one tool, notes in another, chapters in a third, socials in a fourth. A one-shot "episode in → complete publish kit out" flow, priced flat or local-first, is the underserved wedge. No platform API needed at all — podcasting runs on open RSS and the creator's own audio files.

**Willingness-to-pay.** Descript alone holds a large paying base at $16–50/user/mo (search-verified pricing); an entire secondary category (Castmagic, Podsqueeze, Capsho) exists only for this packaging step.

**Buildability as local demo: 4/5.** Node + local Whisper (or paste-in transcript for the static demo) → generate show notes, chapters, titles, social posts in one screen. Demo works fully offline with a bundled sample transcript; docked one point because real transcription of long audio is compute-heavy in a browser demo.

**Pain score: 7/10.** Per-episode recurring pain with proven spend; but the space is crowded and AI incumbents are moving fast — the wedge is pricing predictability and consolidation, not capability.

---

## Candidate 3 — Long-video → Shorts clipping without the credit-pricing squeeze (YouTube/Twitch)

**Problem statement.** Creators repurposing long videos/streams into Shorts/TikToks/Reels feel gouged by credit-metered AI clipping tools (OpusClip et al.): you pay by *source-video minutes* regardless of usable output, credits expire, and cancellation/reliability complaints are widespread.

**Who hurts + how often.** YouTubers and Twitch streamers doing shorts repurposing — for streamers this is brutal (a 4-hour VOD burns ~240 credits to extract 3 usable clips), multiple times per week.

**Evidence (quotes):**
1. "I built an app so that i don't have to pay for OpusClip or similar expensive tools" — Fr1tz1707, Show HN: Shortgen.io, 2025-08-01, https://news.ycombinator.com/item?id=44754637 — **fetched and verified** (full item text via Algolia). *Founder testimony.*
2. "tools like DaVinci Resolve, Captions, OpusClip, and Descript are all pretty expensive" — zhendlin, HN, 2025-10-09, https://news.ycombinator.com/item?id=45532213 — **fetched and verified** (Algolia excerpt).
3. "I built an OpusClip alternative with editor on the free tier" — WurifyPeak, HN, 2026-06-09, https://news.ycombinator.com/item?id=48468787 — **fetched and verified** (Algolia excerpt). Three independent "I built a cheaper OpusClip" posts within a year is itself a demand/dissatisfaction signal.
4. Trustpilot for opus.pro: 4.0/5 across 302 reviews with **22% one-star**, complaints centering on "processing failures, hidden credit mechanics, and cancellation difficulties"; credits charged on source length not output; paid credits expire after 60 days on monthly plans. — **search-verified only** (Trustpilot itself 403'd; figures via eesel.ai/ascynd.io/metadatamarketer.com review roundups surfaced in search). Treat as directionally solid, not quote-verified.

**Existing tools + pricing:**
- **OpusClip** — Free tier; Starter ~$15/mo (monthly-only, ≈$180/yr); Pro ~$29/mo (~$174/yr annual). Credit-metered by source minutes; credit expiry. — **search-verified** (opus.pro/pricing fetch blocked by spend limit; figures consistent across three roundups). Mark exact numbers UNVERIFIED-exact.
- **Descript, Captions, Submagic, Eklipse (Twitch-focused), Vizard** — same category, mostly $15–30/mo credit-metered. UNVERIFIED individually.

**The gap.** Nobody serves the high-volume/low-budget creator (esp. Twitch streamers with multi-hour VODs) with flat or local pricing; the per-source-minute credit model is exactly wrong for their shape of content. **API feasibility: genuinely open** — Twitch Helix API (clips, VODs) and YouTube Data API are public; and the core workload (download own VOD, transcribe, cut with ffmpeg) needs no API at all.

**Willingness-to-pay.** OpusClip's paid tiers and 302 Trustpilot reviews indicate a real paying base; multiple clone-builders monetizing "same thing cheaper" confirms price-driven churn (HN items fetched and verified).

**Buildability as local demo: 3/5.** A real clipper needs heavy video processing. A credible local demo: Node + ffmpeg + transcript-based highlight scoring on a sample VOD, with an HTML review/export UI. Doable, but the demo-to-product gap is the widest of the four.

**Pain score: 6.5/10.** Strong price-pain and open APIs, but capability incumbents are entrenched and the pain is "too expensive," which invites a race to the bottom.

---

## Candidate 4 — Thumbnail/title decision support for small YouTube channels (sub-A/B-test scale)

**Problem statement.** Thumbnails/titles decide 30%+ of a video's impressions, but YouTube's native "Test & Compare" A/B feature is statistically useless for the vast majority of channels that get under ~1,000 views per video — small creators are flying blind on their highest-leverage decision.

**Who hurts + how often.** Every small/growing YouTuber (the overwhelming majority of channels), every upload.

**Evidence (quotes):**
1. "...the same quality and subject matter in a given video without a dumb thumbnail gets at least 30% less impressions on YouTube... You have to hold your nose to do any marketing." — geerlingguy (Jeff Geerling, a working creator), HN, 2020-12-22, https://news.ycombinator.com/item?id=25511833 — **fetched and verified.**
2. "the average YouTube video isn't popular enough for an A/B test to be effective here" — with <1,000 average views, native testing "yields unreliable results" and creators "may adopt strategy changes based on insufficient data simply because the platform offers the feature." — CM30, HN, 2026-05-19, https://news.ycombinator.com/item?id=48191696 — **fetched and verified.**
3. "TubeBuddy's A/B Testing works by having you create a variation of a video's metadata (this could include the Thumbnail, Title...)" — Cipater, HN, 2021-08-22, https://news.ycombinator.com/item?id=28267765 — **fetched and verified** (Algolia excerpt; establishes the paid-tool category).

**Existing tools + pricing:** TubeBuddy (Legend tier holds A/B testing, ~$32–49/mo), ThumbnailTest.com, vidIQ — **UNVERIFIED pricing** (fetches cut off by spend limit before pricing pages; flagged honestly). YouTube native Test & Compare: free but ineffective at low view counts (verified quote #2).

**The gap.** Pre-publish decision support that doesn't require live traffic: simulated feed previews (home/search/mobile/dark-mode), side-by-side glance tests, legibility-at-120px checks, panel-based or model-based CTR prediction. Native A/B and TubeBuddy both need traffic the small creator doesn't have. YouTube Data API is open (thumbnail upload is an API call), so even the "rotate and measure" version is feasible.

**Willingness-to-pay.** TubeBuddy/vidIQ sustain large paid bases specifically on packaging/SEO features (category existence verified via quote #3); exact prices unverified in this run.

**Buildability as local demo: 5/5.** Pure static HTML/JS: drop in 2–3 thumbnail candidates → rendered mock YouTube home/search/suggested feeds at real sizes, blur/squint test, contrast and text-size linting. Zero backend needed.

**Pain score: 6/10.** Real, verified, every-upload pain — but it's an "anxiety" pain more than a "money leak" pain for people who mostly earn nothing yet; monetization ceiling is lower.

---

## Ranking

| Rank | Candidate | Pain | Demo buildability | Why |
|---|---|---|---|---|
| 1 | KDP/wide author sales+ads dashboard | 8/10 | 5/5 | Proven $5–29/mo paid category whose leader is verifiably failing on reliability; no-API constraint is a moat that favors a local/file-based tool; demo is trivial to build honestly |
| 2 | Podcast post-production packaging | 7/10 | 4/5 | Chronic (2017→2026 verified), per-episode pain; incumbents repriced into unpredictability; RSS/no-API space |
| 3 | Shorts clipping credit-pricing squeeze | 6.5/10 | 3/5 | Verified price revolt (3 clone-builders in 12 months) and open Twitch/YouTube APIs, but heavy compute and race-to-bottom risk |
| 4 | Thumbnail decision support for small channels | 6/10 | 5/5 | Verified statistical gap in native tooling, easiest demo of all, but weakest willingness-to-pay segment |

### Discarded lanes (and why)
- **Newsletter (Substack) automation** — Substack has no public API; excluded per feasibility rule.
- **Sponsorship-rate transparency** — no verifiable complaint evidence found via accessible sources in this run (HN search came up empty); dropped rather than padded with unverified Reddit lore.
- **Course-creator piracy** — enforcement product, not buildable as an honest local demo.
