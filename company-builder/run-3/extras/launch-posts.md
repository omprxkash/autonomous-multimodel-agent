# Launch Post Drafts — Week 1 beachhead (drafts only, never posted)

Added post-run by the orchestrator (2026-07-13) so the launch plan's Week 1 is executable
the day a founder decides to go. Each draft follows its community's norms as researched in
`business/launch-plan.md` (show-and-tell, no hard sell, lead with the free thing). Nothing
here was published — guardrail: publish nothing. Claims in the drafts cite only facts this
run verified (see `research/verification.md` and the addendum).

---

## 1. r/selfpublish — show-and-tell launch post

**Title:** I got tired of checking five dashboards every morning, so I built a royalty
ledger that reads the report files you already download — everything stays on your machine

**Body:**

Wide author problem: KDP, D2D, Kobo, and the ads console each tell you a piece of the
story, none of them tell you what a *book* actually earned after ads, and the aggregator
tools that promise to fix this keep breaking because Amazon doesn't offer publishers an
API — the tools have to scrape dashboards, and every backend change knocks them over.

So I built WideTally differently: it doesn't log into anything. You drop in the CSV/XLSX
reports you already download from each store, and it builds a per-book, per-series ledger
locally — royalties by platform, KU pages priced at that month's rate (clearly marked as
estimates), and ad spend subtracted so you see *net* per book. Nothing uploads. There's no
account. You can watch the network tab while you use it.

There's a free playground with synthetic data if you just want to poke at it (link), and
the report-format documentation is free and public regardless of whether you ever use the
app (link) — it covers what's actually in each store's export, because half the battle is
that nobody documents these files.

It's $59 once, not a subscription. Happy to answer anything, including "why should I trust
a local app" — that's the right question to ask.

*(Mod note per sub rules: my own tool, first post about it.)*

---

## 2. Wide for the Win (Facebook) — value-first post

No product link in the first post, per group norms. Lead with the free asset:

I put together free documentation of every major store's royalty-report format — KDP
(sales, KENP, prior-months), Draft2Digital, Kobo Writing Life, and Amazon Ads campaign
exports: what columns they contain, what changed over time, and the gotchas (KU pages vs
dollars, refund timing, currency columns). It's the reference I wish existed when I started
reconciling my own numbers. Link in comments. If there's interest, I'll share the tool I
built on top of it — but the docs are free and standalone either way.

---

## 3. Kindlepreneur outreach email (Dave Chesson)

**Subject:** A royalty tracker built around the exact problem your ScribeCount review raised

Hi Dave,

Your ScribeCount review said what wide authors were experiencing: you'd open it and get
nothing, and you couldn't recommend it anymore. I think the cause is structural, not a bug —
there's no KDP API (Amazon confirmed this on the SP-API GitHub in writing), so every cloud
tracker has to scrape or ride browser cookies, and their own maintenance logs show what that
costs them.

I built WideTally to sidestep the fragile part entirely: it parses the report files authors
already download, locally, no login, no server. Same numbers, no scraping treadmill. $59
once.

I'd value your skepticism more than your endorsement — if you'll look at it, I'll send a
license and the format-registry docs, and if you conclude it's wrong for your readers, that
verdict is useful too. One email, one follow-up, then I'll leave you alone.

Thanks for the reviews — they're the only rigorous ones in this category.

---

## Posting rules the founder must keep

1. Never post any of these until the product is real (real parsers proven on real exports).
2. Disclose "my own tool" everywhere, every time.
3. The Reddit post's claims are all verified in this run — do not add new numbers without
   re-verifying them on posting day (formats and prices drift).
