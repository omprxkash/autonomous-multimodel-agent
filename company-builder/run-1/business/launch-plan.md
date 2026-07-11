# Launch Plan — Safe Sync (First 30 Days)

Date: 2026-07-11. Goal for day 30: a working safety-first sync installed on ≥3 real multi-store merchants (design partners), a live App Store listing in review or published, and ≥1 merchant applying real syncs through dry-run + diff + rollback. Companion docs: `business-plan.md`, `market-research.md`.

---

## 1. Build milestones (solo/tiny team)

**Week 1 — Foundation & safe write path**
- Register Shopify Partner account ($19), create the app, request `read_inventory`/`write_inventory`/`read_products` scopes; set up a dev store + a second dev store to simulate multi-store.
- OAuth install flow; store connection model (2 stores, SKU/barcode mapping table).
- Implement the **safe write core**: `inventorySetQuantities` with `compareQuantity` (compare-and-set) + idempotency keys. Prove it errors-not-clobbers on a simulated concurrent change.

**Week 2 — The wedge: dry-run + diff**
- Read both catalogs; compute the proposed change set (SKU, current→proposed, per store).
- **Dry-run mode**: run the full sync computation with zero writes.
- **Diff preview UI**: approvable table of proposed changes with flagged deltas. This is the demoable differentiator.

**Week 3 — Guardrails: circuit-breaker + rollback + audit**
- **Anomaly circuit-breaker**: configurable thresholds (e.g. halt if >X% of SKUs would go to 0/negative, or catalog value drops >Y%). Emit the "about to zero N SKUs — halted" state.
- **Journaled apply + one-click rollback**: persist prior values per batch; restore.
- **Audit log**: immutable, exportable record of proposed + applied changes.
- Wire **Shopify Billing API** (`appSubscriptionCreate`): Free / $29 / $49 / $99 plans, 14-day trial.

**Week 4 — Scale path, hardening, submit**
- Route full-catalog syncs through **Bulk Operations** (`bulkOperationRunMutation`, `bulk_operations/finish` webhook) so large catalogs bypass rate limits.
- Inventory-level webhooks (`inventory_levels/update`) for change detection (semi-auto apply).
- Deliberate destructive-scenario testing on dev stores (force a zero-out; confirm breaker halts and rollback restores). Submit App Store listing for review.

*Deliberately deferred (see business-plan §3): continuous full auto-sync, product/price/collection sync, multi-channel connectors, team roles.*

---

## 2. App Store listing plan

- **Category:** list under **"Inventory management"** / "Inventory sync" — the exact lane where Stock Sync, Multi-Store Sync Power, Easify, Syncio, Trunk rank (built-in high-intent discovery).
- **Name/tagline:** lead with the wedge — e.g. *"Safe Sync — inventory sync with dry-run, diff preview & instant rollback."*
- **Listing copy & keywords:** target post-disaster search intent — "safe inventory sync," "prevent overselling," "sync rollback / undo," "inventory backup," "diff preview." Open with the one line no competitor can: *"See every change before it happens. Undo any sync."*
- **Screenshots/video:** the diff preview, the circuit-breaker "about to zero 2,000 SKUs — halted" screen, and the one-click rollback. Show the fear, then the safety.
- **Pricing page:** Free (dry-run/diff/audit visible) + $29/$49/$99, via Shopify App Pricing (automated trials/proration).
- **Compliance:** meet Shopify app requirements; use Shopify billing (mandatory); prep for review turnaround.

---

## 3. Three channel plays (with concrete first actions)

**Play A — Reviewer/complaint interception (highest-intent).**
The 1-star zero-out reviews are public, dated, and pre-qualify buyers describing our value prop (Multi-Store Sync Power 11% 1-star; Stock Sync 48 one-star; Easify 7% 1-star).
- *First action (week 1):* pull the current 1-star reviews of all five apps citing zeroing/overselling; build a short list of merchants; reach the reachable ones (store URL → contact) with a plain "we built the undo/preview these apps lack — want to be a design partner free?" Aim: 3 design partners by day 21.

**Play B — Shopify Community + Reddit (the source communities).**
The pain is actively discussed where the evidence came from.
- *First action (week 2):* post a genuinely useful reply in the Shopify Community thread "How do multi-store merchants handle inventory syncing?" (community.shopify.com/t/…/629499) explaining circular-loop zero-outs and how dry-run/diff prevents them; engage r/shopify and multi-channel/TikTok-Shop seller threads with the same substance (help first, link second). Aim: 1–2 inbound design-partner conversations.

**Play C — App Store category SEO (compounding organic).**
- *First action (week 4, at submit):* ship a listing optimized for the safety keywords above; ask each design partner for an early review the day they avoid/recover a disaster; answer competitors' 1-star reviewers publicly where appropriate. Aim: first 3–5 organic installs + 2 five-star reviews within 2 weeks of publish.

---

## 4. Success metrics (day 30 / day 60)

| Metric | Day 30 target | Day 60 target |
|---|---|---|
| App live in App Store | In review / published | Published |
| Design-partner merchants installed | ≥3 | ≥8 |
| Merchants running real syncs via dry-run→apply | ≥1 | ≥5 |
| Circuit-breaker "halt" events / rollbacks demonstrated on real data | ≥1 documented "prevented a zero-out" story | ≥3 |
| Paying conversions (post-trial) | 0–1 (validation, not revenue, is the goal) | ≥3 paying |
| App Store reviews (organic, 4–5★) | ≥1 | ≥5 |
| Interception outreach → conversation rate | tracked (target ~10%+) | — |

**North-star for the month:** one documented case of Safe Sync *halting or reversing a catalog-wide zero-out on a real merchant's live data.* That single proof point is the marketing asset, the review magnet, and the validation that the wedge is real.
