# Name Rationale

## Winner: ReconStock

**Domain:** reconstock.com — available (NXDOMAIN, no A record). reconstock.io and reconstock.app also available.

**Why it wins:**

- **On-brand mechanic, not just on-brand mood.** "Recon" reads two ways at once, and both are correct: *reconnaissance* (scout before you act) and *reconcile* (the accounting/ops term for verifying two records match before you trust them). Store operators already use "reconcile" for bank and inventory reconciliation — the word isn't a stretch, it's their existing vocabulary. "Stock" makes the category instantly legible. Together, "ReconStock" essentially says "verify your inventory before it changes," which is the literal product: diff preview, dry run, rollback, circuit breaker.
- **Clean legally and competitively.** No Shopify App Store listing, partner page, or product uses this exact name. The only adjacent hit was a generic Shopify partner handle "recon1" (unrelated storefront customization apps, not inventory sync) and a "The Recon Group Inc." trademark holder in an unrelated goods category — neither is a naming collision.
- **Full domain availability.** ReconStock is the only candidate that cleared .com, .io, *and* .app simultaneously. Every other short, evocative candidate had its .com already registered (many by direct or adjacent competitors in inventory/sync tooling).
- **Short, spellable, calm.** Two plain English words fused into one; no invented spelling, no hyphen needed, reads fine in a lowercase wordmark or a login screen.

**Runner-up worth banking:** SyncVault (clean trademark, .app available, .com/.io taken) and CalmStock (clean trademark, .io/.app available) — both retained as fallback names if ReconStock's domain is lost before purchase.

---

## Screening Method

- **Trademark/product collision:** WebSearch for `"<name> shopify app software"` (and a direct trademark search for the winner). Checked for: an existing Shopify App Store listing, an existing SaaS product, or a live trademark holder with the same or confusingly similar mark.
- **Domain availability:** `nslookup <name>.com` (and `.io`, `.app`) in Bash. A response with no `Name:`/`Address:` record, or an explicit `Non-existent domain` / `NXDOMAIN`, was treated as **likely available**. Any resolved `Name:` + `Address:` record was treated as **registered/taken**. This is a DNS-resolution proxy for availability, not a registrar check — final confirmation would need a WHOIS/registrar lookup before purchase (no purchase was made, per constraints).

## Full Candidate Table

| # | Name | .com | .io | .app | Trademark/product collision | Verdict |
|---|------|------|-----|------|------------------------------|---------|
| 1 | SyncGuard | taken | available | available | Clean — no exact app/product match (adjacent: Syncio, SyncLogic, Synkro) | Rejected — .com taken |
| 2 | StockGuard | ambiguous* | taken | taken | **Collision** — live Shopify app "StockGuard" (stockguard.app, apps.shopify.com/stockguard-1) + "AdStockGuard" | Rejected — collision + domains taken |
| 3 | SafeSync | taken | taken | taken | Weak collision — "SafeSync" personal safety alarm brand (different industry) | Rejected — all domains taken |
| 4 | SyncSentry | taken | taken | taken | Clean | Rejected — all domains taken |
| 5 | StockSentry | taken | taken | taken | Clean | Rejected — all domains taken |
| 6 | GuardRail | taken | taken | taken | **Collision** — existing Shopify app partner "guardrail2" + "GuardRails" AppSec software | Rejected — collision + domains taken |
| 7 | DriftGuard | taken | taken | taken | **Collision** — existing "DriftGuard" gamepad-calibration app (driftguard.app, Steam, Google Play) | Rejected — collision + domains taken |
| 8 | NoDrift | taken | available | taken | Clean | Rejected — .com/.app taken |
| 9 | SyncVault | taken | taken | available | Clean (adjacent: SkuVault, different name) | Backup candidate — .com/.io taken |
| 10 | StockVault | taken | taken | taken | Weak collision — "Stockvault.net" stock-photo site (different industry) | Rejected — all domains taken |
| 11 | Trustock | taken | taken | available | **Collision** — existing "TruStock" inventory platform (trustockapp.com) | Rejected — collision |
| 12 | CalmStock | ambiguous* | available | available | Clean | Backup candidate — .com uncertain |
| 13 | SyncProof | taken | available | taken | Clean | Rejected — .com/.app taken |
| 14 | StockProof | taken | taken | available | Clean | Rejected — .com/.io taken |
| 15 | **ReconStock** | **available** | **available** | **available** | Clean — no exact app/product/trademark match | **WINNER** |
| 16 | FailSafeSync | taken | available | available | Clean | Rejected — .com taken, name is long |
| 17 | SentinelStock | taken | available | available | Clean | Rejected — .com taken, name is long |
| 18 | CheckSync | taken | available | taken | Clean | Rejected — .com/.app taken |
| 19 | DiffGuard | taken | taken | available | Clean (adjacent: DiffMate, Diffy — theme-diff tools, different function) | Rejected — .com/.io taken |
| 20 | SteadySync | taken | available | taken | Clean | Rejected — .com/.app taken |

\* "ambiguous" = DNS query returned a `Name:` record with no clean `Address:` line in this environment (likely parked/registered); treated conservatively as taken/uncertain and not pursued further given a fully-clean alternative (ReconStock) was available.
