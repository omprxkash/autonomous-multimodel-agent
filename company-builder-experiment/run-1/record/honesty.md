# Honesty File — run-1

Everything in this run that is simulated, assumed, synthesized, or otherwise not a verified real-world fact. If it's not disclosed here and not linked to a source, it shouldn't be in the package.

## Standing disclosures

1. **No paid APIs / no cloned voice.** This workspace has no API keys. Voiceovers are Windows built-in TTS, not a human or cloned voice. The "founder" persona in any video/site copy is fictional and labeled as such.
2. **Demo data is synthetic.** The product demo ships with realistic but invented seed data (names, orders, amounts). No real customer data exists or is implied.
3. **Nothing is published.** Domain availability is checked, not purchased. No accounts were created anywhere.
4. **Testimonials:** the landing page will not display fabricated testimonials. Verified public complaints/quotes may be shown *as market evidence with links*, never as customer endorsements of this product.

## Run-specific disclosures

1. **C13 quote misattribution (caught and corrected).** The candidate file cited "erase 5–15% of MRR silently" against an Indie Hackers comment that actually says "5–9% of monthly Stripe charges fail." The 5–15% range exists independently in a Baremetrics post but was wrongly sourced. Caught by the verification pass; the tournament judged C13 on the corrected figure. (`research/verification.md ## C13`)
2. **C14 engagement inflation (caught).** Reported Reddit scores/comments for the scope-creep candidate were ~2–3× live values, and its willingness-to-pay evidence traced to a paid AI-idea site's unsourced arithmetic. C14 was judged with that on the record and lost. (`research/verification.md ## C14`)
3. **"No incumbent ships dry-run/diff/rollback" is listing-copy-verified only.** Confirmed against all five competitors' live App Store listings/pricing pages on 2026-07-11, but no in-product audit was performed (that requires installs on a live store). Red team made a pre-launch install-and-audit of Trunk and Syncio mandatory. (`research/red-team.md`)
4. **TAM/SAM are soft estimates.** The 60k–150k multi-store merchant anchor is real (Store Leads), but the "% needing sync" multiplier is an assumption, labeled as such in `business/market-research.md`.
5. **Brand fonts approximated.** Guidelines specify Inter/JetBrains Mono (free Google fonts); the local site/product use system-stack approximations because the build is fully offline (no CDN calls).
6. **Domain availability = DNS proxy.** reconstock.com/.io/.app returned NXDOMAIN on 2026-07-11 — a strong signal, but registrar/WHOIS confirmation is still required before purchase. Nothing was bought.
7. **Reddit/X crawler blocks.** Several research lanes accessed Reddit via the Arctic Shift mirror or old.reddit.com and could not access X at all; all mirror-sourced evidence was flagged and the finalists' evidence was re-fetched adversarially.
8. **The product is a local demo.** It implements the full core workflow against seeded data in the browser; it is not connected to Shopify's API. The business plan's technical feasibility section cites the real API primitives it would use.
