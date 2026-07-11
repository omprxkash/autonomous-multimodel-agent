# ReconStock — Onboarding Email Sequence (5 emails)

Voice per brand-guidelines.md: calm, precise, zero hype. The sequence mirrors the product's trust ramp: install read-only → see value → first supervised sync → convert. No urgency theater, no fake scarcity.

---

## Email 1 — sent immediately on install
**Subject:** ReconStock is watching, not touching

Hi {{first_name}},

ReconStock is connected to {{store_count}} stores and running in **read-only dry-run mode**. That's the default, and nothing changes it until you do.

Right now it's building a baseline of your inventory across stores. In about an hour you'll be able to open the dashboard and see exactly what a sync *would* do — every SKU, old quantity → new quantity — without a single write happening.

No setup task for you today. Look around when you have five minutes.

— ReconStock

*You're on the Free plan. It stays free.*

---

## Email 2 — day 2, after first dry-run report exists
**Subject:** Your first dry-run report is ready

Hi {{first_name}},

Your stores drifted in {{drift_count}} places since yesterday. The dry-run report shows each one: which SKU, which store, what a sync would change.

Two things worth noticing while you read it:

1. Nothing was written. The report is the product working in its default posture.
2. If any row surprises you, that's the point. Surprises belong in a report — not in your live catalog.

[Open the report]

— ReconStock

---

## Email 3 — day 5
**Subject:** What the circuit breaker would have done

Hi {{first_name}},

A short story from the category you're standing in: last June, a merchant's sync app zeroed the inventory of 2,000+ products across two connected stores. Real review, public, verifiable — it's linked on our site.

ReconStock's circuit breaker exists for exactly that moment. If a sync would change more inventory than your threshold allows — say, zeroing 2,143 SKUs — it halts and shows you the diff instead of writing it.

Your breaker is currently set to halt anything touching more than {{threshold}}% of your catalog. You can tune it in Settings.

— ReconStock

---

## Email 4 — day 9, if user has viewed ≥1 diff
**Subject:** Ready to run your first supervised sync?

Hi {{first_name}},

You've reviewed {{diff_views}} diffs. When you're ready, the path from dry-run to live is deliberately short and deliberately supervised:

1. Open a pending diff.
2. Approve it. That exact diff is applied — nothing else.
3. Every applied sync lands in the audit log with one-click rollback.

Approve-to-apply stays on until you turn it off. Some merchants never do, and that's a fine way to run.

[Review pending diffs]

— ReconStock

---

## Email 5 — day 14, Free users approaching sync-volume limit
**Subject:** You're syncing more than Free covers

Hi {{first_name}},

This month you've approved {{synced_count}} syncs — past what the Free plan covers. Standard is $29/month: unlimited approved syncs, both stores, the breaker, the audit log, rollback. Nothing you've configured changes; the safety posture is identical on every plan.

If Free still fits how you work, ignore this. There's no expiry and we don't nag.

[Move to Standard — $29/mo]

— ReconStock

*Honest scope, v1: quantities only, 2 stores, approve-to-apply. If you need more stores or price/product sync, tell us and we'll tell you honestly where it is on the roadmap.*
