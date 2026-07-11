/* ReconStock demo — seed data
   Pure data + a small in-memory "backend" that the UI (app.js) talks to.
   Everything here is deterministic and reseedable so the demo always
   starts from the same known-good state (and so Playwright can rely on it).
*/

const SEED = {
  meta: {
    generatedAt: "2026-07-11T09:00:00-05:00",
    version: 1
  },

  stores: [
    {
      id: "main",
      domain: "mainstore.myshopify.com",
      label: "US Main Store",
      region: "United States",
      connected: true,
      plan: "Shopify Plus",
      lastSync: "2026-07-11T08:42:00-05:00"
    },
    {
      id: "eu",
      domain: "eu-store.myshopify.com",
      label: "EU Store",
      region: "European Union",
      connected: true,
      plan: "Shopify",
      lastSync: "2026-07-11T08:40:00-05:00"
    }
  ],

  // ~30 visible SKUs, realistic apparel catalog, quantities per store.
  skus: [
    { sku: "RS-TEE-BLK-S",  product: "Classic Crew Tee",       variant: "Black / S",   category: "Tops",     main: 142, eu: 58  },
    { sku: "RS-TEE-BLK-M",  product: "Classic Crew Tee",       variant: "Black / M",   category: "Tops",     main: 210, eu: 96  },
    { sku: "RS-TEE-BLK-L",  product: "Classic Crew Tee",       variant: "Black / L",   category: "Tops",     main: 188, eu: 74  },
    { sku: "RS-TEE-WHT-S",  product: "Classic Crew Tee",       variant: "White / S",   category: "Tops",     main: 121, eu: 45  },
    { sku: "RS-TEE-WHT-M",  product: "Classic Crew Tee",       variant: "White / M",   category: "Tops",     main: 176, eu: 63  },
    { sku: "RS-TEE-NVY-M",  product: "Classic Crew Tee",       variant: "Navy / M",    category: "Tops",     main: 98,  eu: 31  },
    { sku: "RS-HOD-GRY-S",  product: "Fleece Pullover Hoodie",  variant: "Heather Grey / S", category: "Outerwear", main: 64,  eu: 22 },
    { sku: "RS-HOD-GRY-M",  product: "Fleece Pullover Hoodie",  variant: "Heather Grey / M", category: "Outerwear", main: 87,  eu: 39 },
    { sku: "RS-HOD-GRY-L",  product: "Fleece Pullover Hoodie",  variant: "Heather Grey / L", category: "Outerwear", main: 71,  eu: 28 },
    { sku: "RS-HOD-BLK-M",  product: "Fleece Pullover Hoodie",  variant: "Black / M",   category: "Outerwear", main: 93,  eu: 41 },
    { sku: "RS-JKT-OLV-M",  product: "Waxed Field Jacket",      variant: "Olive / M",   category: "Outerwear", main: 34,  eu: 19 },
    { sku: "RS-JKT-OLV-L",  product: "Waxed Field Jacket",      variant: "Olive / L",   category: "Outerwear", main: 29,  eu: 14 },
    { sku: "RS-JKT-BLK-M",  product: "Waxed Field Jacket",      variant: "Black / M",   category: "Outerwear", main: 41,  eu: 17 },
    { sku: "RS-JNS-IND-30", product: "Straight Fit Denim",      variant: "Indigo / 30", category: "Bottoms",  main: 56,  eu: 20 },
    { sku: "RS-JNS-IND-32", product: "Straight Fit Denim",      variant: "Indigo / 32", category: "Bottoms",  main: 88,  eu: 33 },
    { sku: "RS-JNS-IND-34", product: "Straight Fit Denim",      variant: "Indigo / 34", category: "Bottoms",  main: 79,  eu: 27 },
    { sku: "RS-JNS-BLK-32", product: "Straight Fit Denim",      variant: "Black / 32",  category: "Bottoms",  main: 61,  eu: 21 },
    { sku: "RS-CHN-KHK-32", product: "Tapered Chino",           variant: "Khaki / 32",  category: "Bottoms",  main: 47,  eu: 16 },
    { sku: "RS-CHN-KHK-34", product: "Tapered Chino",           variant: "Khaki / 34",  category: "Bottoms",  main: 52,  eu: 18 },
    { sku: "RS-SNK-WHT-9",  product: "Low-Top Canvas Sneaker",  variant: "White / US 9",  category: "Footwear", main: 38,  eu: 12 },
    { sku: "RS-SNK-WHT-10", product: "Low-Top Canvas Sneaker",  variant: "White / US 10", category: "Footwear", main: 44,  eu: 15 },
    { sku: "RS-SNK-BLK-9",  product: "Low-Top Canvas Sneaker",  variant: "Black / US 9",  category: "Footwear", main: 31,  eu: 10 },
    { sku: "RS-BOT-BRN-9",  product: "Leather Chelsea Boot",    variant: "Brown / US 9",  category: "Footwear", main: 22,  eu: 9   },
    { sku: "RS-BOT-BRN-10", product: "Leather Chelsea Boot",    variant: "Brown / US 10", category: "Footwear", main: 26,  eu: 11  },
    { sku: "RS-DRS-BLK-S",  product: "Wrap Midi Dress",         variant: "Black / S",   category: "Dresses",  main: 33,  eu: 27  },
    { sku: "RS-DRS-BLK-M",  product: "Wrap Midi Dress",         variant: "Black / M",   category: "Dresses",  main: 41,  eu: 34  },
    { sku: "RS-DRS-RED-M",  product: "Wrap Midi Dress",         variant: "Red / M",     category: "Dresses",  main: 24,  eu: 19  },
    { sku: "RS-CAP-BLK-OS", product: "Structured Twill Cap",    variant: "Black / OS",  category: "Accessories", main: 118, eu: 46 },
    { sku: "RS-CAP-NVY-OS", product: "Structured Twill Cap",    variant: "Navy / OS",   category: "Accessories", main: 96,  eu: 38 },
    { sku: "RS-BLT-BRN-M",  product: "Full-Grain Leather Belt", variant: "Brown / M",   category: "Accessories", main: 54,  eu: 21 }
  ],

  // Two queued syncs. "daily" is a normal, safe sync worth reviewing.
  // "restock" is the seeded disaster: a malformed feed that would zero
  // 2,143 SKUs on the EU store. It never reaches a normal diff screen —
  // the circuit breaker halts it first.
  pendingSyncs: [
    {
      id: "sync-daily-0711",
      kind: "normal",
      title: "Daily inventory pull",
      subtitle: "mainstore.myshopify.com → eu-store.myshopify.com",
      queuedAt: "2026-07-11T08:45:00-05:00",
      source: "Scheduled sync · webhook: inventory_levels/update",
      // Each entry: which SKU, which store gets written, old -> new, why.
      diffs: [
        { sku: "RS-TEE-BLK-M", store: "eu", oldQty: 96,  newQty: 132, source: "Restock webhook" },
        { sku: "RS-TEE-WHT-S", store: "eu", oldQty: 45,  newQty: 45,  source: "No change" , skip: true},
        { sku: "RS-HOD-GRY-M", store: "eu", oldQty: 39,  newQty: 52,  source: "Restock webhook" },
        { sku: "RS-HOD-BLK-M", store: "eu", oldQty: 41,  newQty: 33,  source: "POS sale adjustment" },
        { sku: "RS-JKT-OLV-M", store: "eu", oldQty: 19,  newQty: 11,  source: "POS sale adjustment" },
        { sku: "RS-JNS-IND-32",store: "eu", oldQty: 33,  newQty: 45,  source: "Restock webhook" },
        { sku: "RS-JNS-BLK-32",store: "eu", oldQty: 21,  newQty: 14,  source: "POS sale adjustment" },
        { sku: "RS-CHN-KHK-32",store: "eu", oldQty: 16,  newQty: 24,  source: "Restock webhook" },
        { sku: "RS-SNK-WHT-9", store: "eu", oldQty: 12,  newQty: 7,   source: "POS sale adjustment" },
        { sku: "RS-BOT-BRN-9", store: "eu", oldQty: 9,   newQty: 15,  source: "Restock webhook" },
        { sku: "RS-DRS-BLK-M", store: "eu", oldQty: 34,  newQty: 29,  source: "Manual count (warehouse)" },
        { sku: "RS-CAP-BLK-OS",store: "eu", oldQty: 46,  newQty: 61,  source: "Restock webhook" },
        { sku: "RS-BLT-BRN-M", store: "eu", oldQty: 21,  newQty: 16,  source: "POS sale adjustment" }
      ].filter(d => !d.skip)
    },
    {
      id: "sync-restock-0711",
      kind: "danger",
      title: "Bulk restock import",
      subtitle: "3rd-party feed → eu-store.myshopify.com",
      queuedAt: "2026-07-11T09:12:00-05:00",
      source: "CSV import · supplier feed \"eu-warehouse-master.csv\"",
      // The dangerous batch: malformed feed returned empty quantity for
      // nearly the whole EU catalog. We only *sample* rows for the UI —
      // the total affected count is what the circuit breaker reports.
      breaker: {
        rule: "Mass-zero pattern: >2,000 SKUs would be set to 0 in a single batch",
        affectedSkuCount: 2143,
        storeLabel: "EU Store",
        storeId: "eu",
        catalogValueDropPct: 97,
        reason: "Supplier feed \"eu-warehouse-master.csv\" returned an empty quantity column for 2,143 of 2,210 mapped SKUs. Treating a blank field as zero would wipe live EU inventory.",
        sampleDiffs: [
          { sku: "RS-TEE-BLK-S", store: "eu", oldQty: 58, newQty: 0, source: "Supplier feed (blank qty)" },
          { sku: "RS-TEE-BLK-M", store: "eu", oldQty: 96, newQty: 0, source: "Supplier feed (blank qty)" },
          { sku: "RS-TEE-WHT-M", store: "eu", oldQty: 63, newQty: 0, source: "Supplier feed (blank qty)" },
          { sku: "RS-HOD-GRY-L", store: "eu", oldQty: 28, newQty: 0, source: "Supplier feed (blank qty)" },
          { sku: "RS-JKT-OLV-L", store: "eu", oldQty: 14, newQty: 0, source: "Supplier feed (blank qty)" },
          { sku: "RS-JNS-IND-30",store: "eu", oldQty: 20, newQty: 0, source: "Supplier feed (blank qty)" },
          { sku: "RS-SNK-BLK-9", store: "eu", oldQty: 10, newQty: 0, source: "Supplier feed (blank qty)" },
          { sku: "RS-DRS-RED-M", store: "eu", oldQty: 19, newQty: 0, source: "Supplier feed (blank qty)" },
          { sku: "RS-CAP-NVY-OS",store: "eu", oldQty: 38, newQty: 0, source: "Supplier feed (blank qty)" },
          { sku: "RS-BLT-BRN-M", store: "eu", oldQty: 21, newQty: 0, source: "Supplier feed (blank qty)" }
        ]
      }
    }
  ],

  // Applied-sync history, each reversible via rollback.
  auditLog: [
    {
      id: "audit-0709",
      title: "Weekly restock sync",
      subtitle: "mainstore.myshopify.com → eu-store.myshopify.com",
      appliedAt: "2026-07-09T07:15:00-05:00",
      status: "applied",
      skuCount: 11,
      changes: [
        { sku: "RS-TEE-NVY-M", store: "eu", oldQty: 24, newQty: 31 },
        { sku: "RS-CHN-KHK-34",store: "eu", oldQty: 13, newQty: 18 },
        { sku: "RS-BOT-BRN-10",store: "eu", oldQty: 8,  newQty: 11 }
      ]
    },
    {
      id: "audit-0705",
      title: "Manual warehouse recount",
      subtitle: "mainstore.myshopify.com",
      appliedAt: "2026-07-05T14:30:00-05:00",
      status: "applied",
      skuCount: 4,
      changes: [
        { sku: "RS-JNS-IND-34", store: "main", oldQty: 82, newQty: 79 },
        { sku: "RS-DRS-BLK-S",  store: "main", oldQty: 30, newQty: 33 }
      ]
    }
  ],

  // Recent activity feed (most recent first, ids for dedupe on reseed).
  activity: [
    { id: "act-1", at: "2026-07-11T08:45:00-05:00", type: "info", text: "Daily inventory pull queued for review — 12 changes detected." },
    { id: "act-1b", at: "2026-07-11T09:12:00-05:00", type: "warn", text: "Bulk restock import queued from supplier feed — flagged for circuit breaker check on review." },
    { id: "act-3", at: "2026-07-09T07:16:00-05:00", type: "success", text: "Weekly restock sync applied — 11 SKUs updated on EU Store." },
    { id: "act-4", at: "2026-07-05T14:31:00-05:00", type: "success", text: "Manual warehouse recount applied — 4 SKUs updated on US Main Store." },
    { id: "act-4b", at: "2026-07-08T10:05:00-05:00", type: "info", text: "Write access granted for both stores. ReconStock ran read-only (dry-run only) for the first 7 days." },
    { id: "act-5", at: "2026-07-01T06:02:00-05:00", type: "info", text: "ReconStock connected to eu-store.myshopify.com — installed read-only by default." }
  ]
};

if (typeof module !== "undefined") { module.exports = SEED; }
