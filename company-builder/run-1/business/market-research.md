# Market Research — Safe Sync for Shopify

Date: 2026-07-11. Consolidates the verified pain trail (C09), a live competitor teardown, platform reality, and TAM/SAM/SOM. All competitor pricing/feature data fetched from live Shopify App Store listings on 2026-07-11. Platform facts fetched from shopify.dev.

---

## 1. Verified pain evidence trail

Provenance chain: discovered in `run-1/research/candidates.md` §C09 (app-marketplaces lane, Confidence: High) → adversarially re-verified in `run-1/research/verification.md` §C09 (**verdict: SURVIVES** — all four evidence URLs verbatim/substance-accurate on re-fetch, zero refutations, two *new* independent corroborations) → won `run-1/research/tournament.md` Round 3 (unanimous, 3-0 after deliberation).

| Evidence | Source | Date | Verification verdict |
|---|---|---|---|
| "Almost 2000 variants turned to negative qty" | apps.shopify.com/multi-store-inventory-sync/reviews (Italy Station by GD) | 2020-07-17 | VERIFIED-VERBATIM |
| App "set my entire inventory quantity to zero (0) across all products"; "3+ hours"; "thousands of dollars" | same listing (Babies Mart Australia) | 2025-11-19 | VERIFIED-SUBSTANCE |
| "Frequent synchronization errors… overselling and stockouts" | apps.shopify.com/stock-sync/reviews (Media Alliance CT, ~4 yrs on app) | 2024-12-02 | VERIFIED-VERBATIM |
| "all inventory level… is either zero or even negative… all my 2000+ products" | apps.shopify.com/easify-inventory-sync/reviews (Kurti Connection USA) | 2026-06-21 | VERIFIED-VERBATIM (dev disputes cause; 2,000+ SKU damage undisputed) |

**Independent corroboration (new, in verification.md):**
- Shopify Community thread "How do multi-store merchants handle inventory syncing?" (community.shopify.com/t/…/629499, ~May 2026): *"the 'zeroing out' nightmare… is usually caused by SKU mapping errors or circular sync loops, where Store A updates Store B, which accidentally triggers Store B to update Store A with empty data"* and *"Having to email a customer to apologize and cancel their order… completely ruins brand trust."*
- Reddit multi-channel case: sold "the same last 12 units on both Shopify and TikTok Shop," woke to "24 orders and zero inventory." **Caveat (per verification.md): this Reddit case was surfaced via search snippet and NOT independently re-fetched verbatim — treat as suggestive, not verified. The multi-channel "why now" (§5.2) should not be leaned on as proven until this or an equivalent source is re-fetched.**

**Conclusion:** category-wide architecture gap (no dry-run/diff/rollback/circuit-breaker), recurring 2020→2026, across ≥3 named apps + 2 independent channels. The willingness-to-pay is proven and durable: merchants pay $10–60/mo and stay for years *despite* the failures — the gap is safety, not price.

---

## 2. Competitor matrix (live App Store data, 2026-07-11)

| App | Pricing (mo) | Rating / reviews | 1-star signal | Dry-run | Diff preview | Rollback | Anomaly breaker | Audit log |
|---|---|---|---|:---:|:---:|:---:|:---:|:---:|
| **syncX Stock Sync** | Free (2k, manual) / $7 / $10 | 4.7★ / 860 | 48 one-star (6%), overselling cited | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Multi-Store Sync Power** | Free / $19.99 / $29.99 / $49.99 | 4.5★ / 139 | **11% one-star** | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Easify Inventory Sync** | Free / $9.99 / $29.99 / $59.99 | 4.5★ / 68 | 7% one-star | ✗ | ✗ | ✗ | ✗ | ~ (passive "sync history log" only) |
| **Syncio** | Free (25) / $19 / $29 / $39 (+add-ons) | 4.6★ / 161 | — | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Trunk – Stock Sync & Bundling** | $35 → $89 (Essential) / $39 → $119 (Pro), by order vol. | 4.8★ / 390 | — | ✗ | ✗ | ✗ | ✗ | ✗ |

**Read from live listing copy (2026-07-11): none of the five advertises dry-run, diff preview, rollback/undo, or an anomaly circuit-breaker.** Evidence caveat (flagged by red-team, not yet closed): this feature matrix was built from listing/marketing pages, **not** from installing and operating each app — the verification.md pass re-fetched only the *review quotes*, not the feature claims. Absence from marketing copy is strong but not proof of absence in-product (e.g. Easify's "sync history log" is a passive record, but only a hands-on trial confirms it is not a reversible journal). **Action before launch: install the top two threats (Trunk 4.8★/390, Syncio) and confirm no hidden preview/restore path.** Subject to that check, the category competes on connectors, channels, real-time speed, and price — **not on safety** — which is the open lane.

Price band spans **$7–$60/mo** base (Trunk scales to ~$119 at high order volume). Our $29 / $49 / $99 positioning sits at the top of the safety-justified premium end without exceeding what Trunk already proves merchants pay.

---

## 3. Platform reality — buildable against public APIs (shopify.dev, fetched 2026-07-11)

**Inventory write primitives (the safety architecture is API-supported):**
- `inventorySetQuantities` — absolute set, with built-in **compare-and-set (`compareQuantity`)**: writes only if the persisted quantity matches the expected value, else returns an error instead of clobbering concurrent changes. `ignoreCompareQuantity` opts out (we won't, by default). **As of April 2026 an idempotency key is required** (`@idempotent`), enabling safe retries. → This is the core enabler of "fail safely instead of corrupt."
- `inventoryAdjustQuantities` — relative deltas for non-authoritative sources.
- `inventoryBulkAdjustQuantityAtLocation` — multi-item adjust at a location.

**Bulk / scale:**
- **GraphQL Bulk Operations** (`bulkOperationRunMutation`): submit a JSONL file of mutations, runs async, **bypasses the point-based rate limits and the 1,000-point single-query cap entirely** — the correct path for full-catalog (1,000+ SKU) syncs. Completion monitored via the `bulk_operations/finish` webhook.

**Rate limits (GraphQL Admin API, calculated-query-cost / points-per-second):** Standard 100 pt/s · Advanced 200 · **Plus 1,000** · Enterprise 2,000. Objects cost 1, mutations cost 10, connections sized by `first`/`last`; single query ≤1,000 pts; unused cost refunded. → Non-bulk paths are viable for small stores; bulk ops remove the ceiling for large ones.

**Change detection:** inventory-level webhooks (e.g. `inventory_levels/update`) drive event-based sync; webhook subscriptions created via `webhookSubscriptionCreate`.

**App approval / distribution:** listing in the App Store requires meeting Shopify's app requirements and using a **Shopify-provided billing solution** (Billing API / Shopify App Pricing — cannot bill via own Stripe). One-time **$19** Partner registration.

**Billing mechanics:** `appSubscriptionCreate` supports recurring (every 30 / 365 days) and usage-based line items with capped amounts; combined plans supported on 30-day intervals. Shopify App Pricing (recommended default) hosts the plan page and automates trials, proration, upgrades/downgrades.

**Revenue share:** developers keep **100% of first $1M USD** gross/yr (effective Jan 1 2025), **15%** above; large devs ($20M+ prior-yr App Store revenue or $100M+ company revenue) pay 15% on all. *Caveat: BetaKit reported Shopify moving to roll back the $1M exemption — treat rev-share as a variable, model 15%-across downside.*

**Verdict: fully buildable against documented public APIs.** The platform even provides the concurrency-safety primitive (`compareQuantity` + idempotency) that the incumbents don't expose to merchants.

---

## 4. TAM / SAM / SOM (with soft-anchor caveat)

Anchored on `verification.md` §C09 market-size check (Store Leads, 2026): ~2.87M live Shopify storefronts; ~50,600 distinct Shopify Plus merchants running ~76,000 Plus domains.

- **TAM ≈ 60,000–150,000 merchants.** Estimate: if 2–5% of live Shopify stores are part of a multi-store/multi-channel operation needing sync (conservative — Plus alone is ~1.8% of live stores, and non-Plus multi-store setups are undercounted). **Soft-anchor caveat (verbatim from verification.md):** the Store Leads live-store/Plus counts are real and citable, but the "% needing sync" multiplier is *not* independently sourced — flagged as an estimate, not a verified count.
- **SAM ≈ 10,000–30,000.** Merchants on a paid third-party sync app today with catalogs large enough that a zero-out is materially damaging. *Derivation note (red-team M2): this is an inference from review counts (5 apps at 68–860 reviews each; reviews are an unknown, app-specific fraction of installs), stacked on the unsourced TAM multiplier — treat as an inference band, not a measured base.*
- **SOM (24-month realistic) ≈ 200–1,000 paying merchants.** At $29–99/mo blended ~$40 ARPU → **~$96K–$480K ARR**. A single solo-founder-viable business; capturing even ~2–5% of SAM. Bottom-up sanity: Multi-Store Sync Power has 139 reviews after years; a differentiated safety entrant plausibly reaches a few hundred paying merchants via category placement + reviewer interception.

*All three figures inherit the soft-anchor caveat: directionally sound, built on one citable anchor plus one unsourced multiplier. Treat as ranges, not forecasts.*

---

## 5. Why now

1. **Freshest damage is 2026** — the Easify zero-out (2,000+ SKUs) is dated 2026-06-21; the pattern is live, not historical.
2. **Multi-channel explosion widens the failure surface** — TikTok Shop / Amazon / Etsy syncing multiplies the desync-oversell risk beyond store↔store (verified Reddit TikTok case), expanding the addressable pain.
3. **Platform just shipped the safety primitives** — `inventorySetQuantities` compare-and-set + the April-2026 idempotency-key requirement make a genuinely safe write path newly first-class; a safety-native app is easier to build correctly today than two years ago.
4. **Incumbents are entrenched but complacent on safety** — five apps, years of 1-star zero-out reviews, and *not one* has shipped dry-run/diff/rollback. The lane is open and has stayed open.
