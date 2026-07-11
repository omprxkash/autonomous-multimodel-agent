# Business Plan — Safe Sync (working name)

**A safety-first inventory-sync layer for multi-store / multi-channel Shopify merchants.**
Date: 2026-07-11 · Source problem: C09 (tournament winner, unanimous). Evidence: `run-1/research/candidates.md` §C09, `run-1/research/verification.md` §C09 (verdict: **SURVIVES**, all 4 URLs verbatim/substance-accurate, zero refutations), `run-1/research/tournament.md` Round 3.

---

## 1. Problem (verified)

Third-party apps that sync inventory across multiple Shopify stores/locations periodically misfire — misreading source data, hitting race conditions, or crashing mid-sync — and when they fail they **write catastrophic values to live inventory** (zeroing or negating thousands of SKUs) instead of failing safely. The damage is silent, full-catalog, and causes overselling plus multi-hour manual recovery. No incumbent ships a pre-write safety net.

Verified merchant quotes (re-fetched verbatim/substance in verification.md §C09):

- *"Don't install the app!!! Almost 2000 variants turned to negative qty… still not sure it messed up other items as well."* — Italy Station by GD, Multi-Store Inventory Sync, 2020-07-17. (VERIFIED-VERBATIM)
- App *"instantly and inexplicably set my entire inventory quantity to zero (0) across all products,"* needing *"3+ hours of manual restoration… thousands of dollars"* lost. — Babies Mart Australia, 2025-11-19. (VERIFIED-SUBSTANCE)
- *"Frequent synchronization errors have caused disruptions… leading to overselling and stockouts."* — Media Alliance CT (South Africa), Stock Sync, ~4 yrs on app, 2024-12-02. (VERIFIED-VERBATIM)
- *"all inventory level for connected products in both stores is either zero or even negative, now i have to adjust and check inventory update all my 2000+ products."* — Kurti Connection USA, Easify, 2026-06-21 (freshest proof; developer disputes root cause as merchant reconfigure-loop, but the 2,000+-SKU customer-visible damage is undisputed). (VERIFIED-VERBATIM)

Independent corroboration (verification.md): a May-2026 Shopify Community thread naming the exact failure mode — *"Store A updates Store B, which accidentally triggers Store B to update Store A with empty data"* — and a Reddit TikTok-Shop multi-channel oversell case. This is a **category-wide architecture gap**, not one buggy vendor.

**Key insight:** merchants pay $10–60/mo and *stay subscribed for years despite these failures*. The unmet need is **reliability/safety, not price** — which means a safety wedge can command a premium.

---

## 2. ICP (Ideal Customer Profile)

- **Primary:** Multi-store Shopify merchants running 2+ storefronts (per brand / region / wholesale / retail-vs-DTC) who depend on a third-party sync app because Shopify-native multi-location tooling does not cover cross-*store* sync. Catalog size where damage is felt: **500–20,000 SKUs**.
- **Secondary:** Multi-channel merchants syncing Shopify ↔ Amazon/eBay/Etsy/TikTok Shop (same failure mode, adjacent expansion).
- **Firmographics:** established enough to have real inventory value at risk; many on Shopify Plus (verification anchor: ~50,600 Plus merchants running ~76,000 Plus domains) but the majority are non-Plus merchants informally running a second store.
- **Buyer = operator/owner** who personally eats the 3-hour recovery. High felt-pain, self-identifies in App Store reviews and Shopify Community threads.

---

## 3. Product spec v1 — "safety-first sync"

Design principle: **we are the guardrail layer wrapped around a deliberately narrow sync engine.** Honest framing: to preview and apply writes we must *compute* the sync (read both catalogs, map SKUs/barcodes, map locations, resolve conflicts) — so v1 IS a small sync engine for the 2-store / inventory-quantity case, not a bolt-on. The narrowness (one channel pair, quantity only, approve-to-apply) is what keeps it weeks-buildable; the guardrail is the differentiator, not the excuse for a smaller build. Every write to live inventory passes through preview → validate → commit → (reversible). This is buildable because Shopify's own API now ships the primitives (see §Platform):

### Ships in weeks (v1 MVP — the wedge)
1. **Dry-run mode** — connect stores, run a sync that computes but does *not* apply changes; produce the full change set.
2. **Diff preview before apply** — a human-readable table: SKU, current qty → proposed qty, per store, flagged deltas. Merchant approves before any write. (No incumbent ships this.)
3. **Anomaly circuit-breaker** — configurable rules halt a sync before it writes when it detects mass-destructive patterns: *"About to zero 2,000 SKUs / set 1,800 SKUs negative / reduce catalog value 90% — halted, review required."* Directly answers the verified failure quotes.
4. **Safe writes** — use `inventorySetQuantities` with `compareQuantity` (compare-and-set): only write when the persisted quantity matches expectation, else error rather than clobber concurrent changes. Idempotency key on every mutation (required by Shopify as of April 2026). **Scope-honest caveat:** `compareQuantity` only defends against *concurrency* clobber — it does NOT prevent the dominant verified failure mode, which is *logic/mapping* error (wrong SKU map, circular Store-A↔Store-B loop, empty-data source read). Those write a "correct" expected→new value and pass compare-and-set happily. The real defense against mapping/logic disasters is the **diff preview (3) + anomaly circuit-breaker (3½)**, not compareQuantity. Don't over-sell the primitive.
5. **Instant rollback** — every applied batch is journaled with prior values; one-click restore to pre-sync state. **Correctness caveat:** a blind restore to pre-sync values can itself *cause* overselling by wiping legitimate sales/receipts that landed between apply and rollback. Rollback must therefore *reconcile* — restore prior value adjusted by real inventory movements since the batch (via `inventory_levels/update` deltas), or at minimum surface those deltas in the diff and require confirmation. Rollback is a guarded reconciliation, not a raw overwrite.
6. **Full audit log** — immutable record of every proposed and applied change, who/what/when, exportable. (Easify has a passive "sync history log"; none offer a true audit + rollback pairing.)

### Later (post-MVP, weeks 6–16)
- Scheduled/continuous auto-sync with the circuit-breaker armed (v1 can be approve-to-apply / semi-automatic).
- SKU/barcode mapping UI and mapping-conflict detection (circular-loop prevention).
- Multi-channel connectors (Amazon/eBay/Etsy/TikTok) beyond store↔store.
- Product/price/collection sync (v1 is **inventory-quantity only** — the highest-damage surface, deliberately narrow).
- Slack/email alerts on breaker trips; team roles.

**Scope discipline:** v1 does one thing — make inventory-quantity sync *safe and reversible* across 2 stores. We can be "installed and preventing a disaster" for a design partner within the first month.

---

## 4. Offer & pricing

Positioned **at the top of the established $10–60/mo band**, justified by selling reliability to a buyer who has proven they'll pay and stay. Trunk already sustains $35–39/mo base (4.8★, 390 reviews) proving the premium tier is tolerated when the product is trusted.

| Plan | Price/mo | Target | Includes |
|---|---|---|---|
| **Free** | $0 | trial / ≤50 SKUs, 2 stores | dry-run + diff preview + audit log (safety hook, no auto-apply cap issues) |
| **Standard** | **$29** | ≤2,000 SKUs, 2 stores | all safety features, rollback, circuit-breaker, semi-auto apply |
| **Pro** | **$49** | ≤10,000 SKUs, up to 5 stores | + scheduled auto-sync, priority breaker rules, faster sync |
| **Scale** | **$99** | 10k+ SKUs / multi-channel | + connectors, team roles, priority support (business-hours; no uptime SLA promised solo) |

Rationale: (a) undercuts nobody on the safety story because there is no competing safety product — we compete on *category*, not price; (b) Free tier that still exposes dry-run/diff makes the wedge visible before purchase and earns App Store installs (discovery ranking); (c) $99 Scale captures the Plus/multi-channel merchant with the most inventory value at risk. Billing must run through **Shopify App Pricing / Billing API** (mandatory for App Store apps — cannot use own Stripe).

---

## 5. Unit economics

- **Revenue share:** Shopify developers keep **100% of the first $1,000,000 USD** gross app revenue (per shopify.dev, effective Jan 1 2025), 15% above that. One-time **$19** Partner registration. *Caveat/risk: BetaKit reported Shopify moving to roll back the $1M exemption; policy is in flux — model a 15%-across-the-board downside sensitivity (§Risks).*
- **Infra ≈ $0 at start:** webhook-driven, serverless; full-catalog syncs run through **GraphQL Bulk Operations** (async JSONL, bypasses point rate-limits), so per-store compute is negligible. Realistic early infra: **<$50/mo** (hosting, DB, logs) until dozens of merchants.
- **Effective take-home per Standard seat:** ~$29 × ~0% rev share (under $1M) − Shopify payment handling (built into billing) ≈ **~$28/mo gross margin**, near-100% software margin at low volume.
- **Break-even:** with <$50/mo infra + solo founder, **~2 paying merchants** covers hard costs; the constraint is time, not capital.
- **CAC (labeled ASSUMPTION — unvalidated):** primary channel is App Store organic search + category placement (zero paid CAC) plus hand-selling to reviewers of failing apps. *Assume* blended CAC $0–50 early via content/community; paid acquisition untested and deferred. *Assume* App-Store-listing → install → trial → paid conversion in the low-single-digit-% range typical of the store (no authoritative public benchmark found; treat as assumption).
- **LTV signal (evidence-backed):** incumbent reviews show merchants staying "years"; even at modest churn, a $29–49/mo tool with multi-year retention implies LTV in the **$700–1,500+** range per merchant — attractive against ~$0 CAC.

---

## 6. Business model

Recurring SaaS subscription, billed monthly through Shopify's Billing API, distributed via the Shopify App Store. Land on the safety wedge (Standard $29), expand by SKU-count/store-count tiers and later multi-channel connectors. Single-product, solo-to-tiny-team shaped. No money movement, no medical/legal liability core — the only liability surface is inventory writes, which the safety architecture itself is designed to contain (dry-run + compareQuantity + rollback).

---

## 7. Channels

1. **App Store SEO / category placement** — list in **"Inventory management"** (and "Inventory sync"), the exact category where Multi-Store Sync Power, Stock Sync, Easify, Syncio, and Trunk already rank. Built-in high-intent discovery. Optimize listing around the terms merchants search after a disaster: "inventory sync safe," "rollback," "prevent overselling," "sync backup."
2. **Reviewer/complaint interception** — the 1-star reviews are public and dated: reply to / reach the merchants writing them (Multi-Store Sync Power 11% 1-star; Stock Sync 48 one-star reviews; Easify 7% 1-star). These are pre-qualified buyers describing our exact value prop.
3. **The communities the evidence came from** — Shopify Community (the "How do multi-store merchants handle inventory syncing?" thread, community.shopify.com/t/...629499), r/shopify, multi-channel/TikTok-Shop seller subreddits and Reddit e-commerce threads. Show up with the dry-run/diff/rollback story where the pain is discussed.

---

## 8. Positioning statement

> **For multi-store Shopify merchants who've been burned by sync apps that zero out live inventory, [Safe Sync] is the only inventory sync that shows you every change before it happens and lets you undo it — dry-run, diff preview, an anomaly circuit-breaker that halts before it zeroes your catalog, and one-click rollback. Unlike Stock Sync, Syncio, Multi-Store Sync Power, Easify, and Trunk, we treat your live inventory as something to protect, not overwrite.**

---

## 9. Moat & incumbent-response analysis

- **Why incumbents haven't shipped it:** every incumbent is architected as a *sync engine that writes* (fire-and-forget). Retrofitting the full stack — reversible journaled commits + audit + opinionated breaker — requires a different write path (stage → preview → journal → reversible commit). **Honest split:** a *diff-preview screen alone* is fast-followable (a competitor could bolt "preview changes" on in a quarter); the durable, harder-to-copy parts are the **journaled rollback + anomaly breaker + accumulated "never destroyed a catalog" track record as an integrated system**. Do not lean the moat on the preview screen. Also note (evidence caveat, see market-research §2): "none of the five ships this" is read from **listing copy**, not a hands-on trial of each app — treat as high-probability, not audited fact, until each is installed and checked. Being safety-native from day one is a real head-start, not a permanent lock.
- **Trust/brand moat:** in a review-driven store, "the sync that doesn't destroy your inventory" is a reputation that compounds. Our own reliability becomes the moat; a competitor bolting on a half-measure can't claim the same track record.
- **Switching-cost caveat (honest):** merchants tolerate bugs for years → low switching *urgency*. Mitigation: land them at the moment of pain (post-disaster reviewers) and via a Free tier that proves safety before they rip out an incumbent.

### The "Shopify ships it natively" risk (the chief accepted risk)
Shopify could add native multi-location diff/rollback and erase the wedge (this is how many "fix Shopify's gap" apps die). **Mitigations:**
1. Shopify's native tooling covers **multi-location within one store**, not cross-*store* sync — the exact gap that forces merchants to third parties; a native cross-store safety layer is not on any public roadmap and is off Shopify's core path.
2. Move fast to own the *category term* ("safe sync") and the reviewer relationships before any native move.
3. Expand into **multi-channel** (Amazon/eBay/Etsy/TikTok) where Shopify has no incentive to build safety — moving the moat off Shopify's roadmap surface.
4. Even if Shopify ships a primitive, the audit-log + cross-channel + opinionated breaker rules remain a product surface Shopify historically leaves to apps.

---

## 10. Top 5 risks & mitigations

| # | Risk | Mitigation |
|---|---|---|
| 1 | **Platform dependency** — Shopify ships native diff/rollback, or changes API/policy. | Own cross-store + multi-channel gap Shopify won't build; move moat off-platform (connectors); own category term & reviewer relationships early. |
| 2 | **Our own overlay corrupts a catalog** — a safety tool causing the disaster it sells against is fatal in a review-driven store. | Architecture *is* the mitigation: dry-run default, `compareQuantity` compare-and-set writes, idempotency keys, journaled reversible commits, circuit-breaker. Never auto-apply destructive batches in v1. Extensive staging tests against a dev store before any live write. |
| 3 | **Low switching urgency** — merchants tolerate bugs for years. | Intercept at moment of pain (dated 1-star reviewers); Free tier exposes dry-run/diff to prove value pre-switch; content around "sync backup / undo." |
| 4 | **Revenue-share policy tightening** (BetaKit-reported rollback of the $1M exemption). | Software margins absorb 15% comfortably at $29–99 pricing; model 15%-across sensitivity; keep infra ~$0. |
| 5 | **Fast-follow by an incumbent** bolting on a "preview" feature. | Speed + trust track record; audit log + rollback + breaker as an integrated *system* (not one feature) is harder to copy credibly; deepen into multi-channel before they react. |

*(Secondary risk: rate-limit/bulk-op complexity on very large catalogs — mitigated by Bulk Operations API which bypasses point limits; see market-research.md §Platform reality.)*
