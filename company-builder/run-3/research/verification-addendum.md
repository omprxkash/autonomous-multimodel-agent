# Verification Addendum — post-run evidence strengthening (orchestrator, 2026-07-13)

The run's self-identified weakest evidence points (`record/gap-analysis.md`, "Honest overall
assessment" #2 and #4) were: (a) the "failing incumbent" pillar leaned on one authoritative
reviewer, and (b) parsers were proven only against synthetic schema-modeled files. Both are
now strengthened with primary sources fetched 2026-07-13.

## A. Incumbent fragility, corroborated first-party (ScribeCount's own blog)

The scraping/cookie fragility mechanism the thesis inferred is documented by the incumbent
itself, across years and multiple platforms:

1. **B&N syncing breakage via browser cookies** — blog.scribecount.com/b-n-syncing-issue/
   (2021-07-23, fetched): cause described as "one of old cookies that refuse to function as
   they should"; B&N backend changes intermittently revive/break them; recommended user
   workaround is "persistent clearing of Cookies and the Cache at both Firefox and Chrome";
   unresolved as of the post, with B&N not responding to ScribeCount's contact attempts.
   This is the architecture WideTally's thesis calls fragile, described by its operator.
2. **Google Play report-format change broke sales display**; **Apple data misinterpretation
   showed free books "where there should be none"**; **D2D trouble tracked** — per
   ScribeCount's own updates/maintenance posts (blog.scribecount.com, surfaced 2026-07-13
   via search; the B&N post above was fetched directly). Together with the Kindlepreneur
   withdrawal of recommendation (verified verbatim in `verification.md` claim 3), the
   "failing incumbent" pillar now rests on two independent source families: the reviewer
   AND the vendor's own incident log.

Inference, labeled: these incidents are the *mechanism* (scraping/cookies/format drift),
not proof the product is failing today. The reviewer quote covers present status; the blog
covers mechanism and history.

## B. Parser schema fidelity, anchored to Amazon's official documentation

KDP's official help page for the Historical Report (kdp.amazon.com/en_US/help/topic/
G200641170, fetched 2026-07-13) documents the downloadable report's columns:

> Title · ASIN · Units Sold · Units Refunded · Net Units Sold · Kindle Edition Normalized
> Pages (KENP) Read · Free Units-Promo · Free Units-Price Match

Additional official pages document the Sales and Royalties Report (six tabs) and the Prior
Months' Royalties Report (generated near the 15th monthly; marketplace, currency, royalty,
format, KENP read, All Stars Bonus, total earnings) — kdp.amazon.com help topics G201488550
and G200641190, surfaced 2026-07-13.

The synthetic sample files' KDP schema aligns with the officially documented column
families. Remaining honest gap (unchanged): only real export files from real accounts can
prove the parsers end-to-end; that is the top pre-launch task and the reason the Format
Registry exists.
