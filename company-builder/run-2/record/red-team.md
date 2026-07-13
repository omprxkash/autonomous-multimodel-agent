# Red Team — Try to Kill DueCrew

Method: adversarial self-pass under a kill-the-company rubric (crowding, WTP, churn, moat,
distribution, legal, evidence quality), run after the build so it could attack the real
artifacts, not a strawman. Objections were written first; rebuttals only where honest.
Sub-agent budget was exhausted, so this was one adversary, not a panel — itself listed as a
weakness (R8). Objections below are also surfaced in RECAP.html and the investor teaser.

## R1 — "This is a reminder app. The moat is a spreadsheet column."
The core loop (date in, alert out) is replicable in a weekend; four near-identical generic
"expiry tracker" microtools already exist (ExpiryEdge, ExpiryKeeper, ExpiryGuard,
RemindCal), which proves the barrier is low.
**Standing rebuttal:** the defensible asset is not the alert, it's the maintained, cited,
per-state per-trade rules dataset plus trade-native workflows (CE math, COI share loop).
**What still stands:** that dataset is replicable by any funded team in months. This is a
speed-and-focus wedge, not a structural moat. UNRESOLVED at seed scale.

## R2 — "Jobber ships this as a feature and you're dead."
Jobber/Housecall Pro have the users, the data, and could add license/COI tracking in a
quarter. **Standing rebuttal:** their buyers are 2–20 person shops already paying for
suites; the solo operator who refuses suites is a segment they've structurally deprioritized
(their pricing starts where our user tops out). But if DueCrew proves the market, a free
tier from an FSM suite compresses us. PARTIALLY STANDS.

## R3 — "WTP is asserted, not demonstrated."
Zero customers were interviewed; no pricing test was run (run constraint: publish nothing,
contact no one). The $12/mo threshold argument is analogy, not evidence. The strongest WTP
signal found is indirect: humans pay license-renewal *services* (contractor-state-license.com)
and an $9-course CE industry thrives. STANDS — this is the first thing a real founder must
test, and the GTM's founding-member offer (cash, not surveys) is designed as that test.

## R4 — "Annual value events → brutal churn."
The save happens once a year; subscribers rationally churn after renewal and resubscribe
later — or never. Mitigations built (CE ledger monthly touch, COI share weekly utility,
annual-first pricing) are plausible but unproven. Vendor-blog retention claims were
deliberately not cited as evidence. STANDS as the #1 business-model risk.

## R5 — "If the rules data is wrong, the product is negligent."
A tool whose pitch is "we know your state's rules" owns the failure when a rule is stale
and a license lapses anyway. Mitigations: per-row source + last-verified date in the UI
(built into the demo), alerts always fire from the user's own document dates even where
rules are unverified, and ToS disclaiming legal advice. Residual liability and the ~$20k/yr
maintenance cost STAND as real operating burdens.

## R6 — "Your competitor scan was one search pass."
True. Budget limited the scan; a niche trade-native competitor with poor SEO could exist,
and the GC-side players (SimpleCerts et al.) could flip to serve subs cheaply — their OCR
tech transfers directly. STANDS as an evidence gap; disclosed in verification.md and
honesty.md.

## R7 — "Several load-bearing quotes are search-snippet-corroborated, not fetched."
The ElectricianTalk/ContractorTalk quotes and the NAHB 34% stat could not be re-fetched
directly (403s/socket errors). The thesis was deliberately structured so the *verified*
anchors (CSLB government source, $47k COI case page, BLS numbers, TDLR CE rule) carry the
argument, and every snippet-level claim is flagged inline. Residual risk: a flagged quote
is materially wrong. MITIGATED, disclosed.

## R8 — "One adversary, judged by its author."
This red team was written by the same agent that built the company, after sub-agent budget
ran out. Self-adversarialism has blind spots (e.g., emotional attachment to the name, the
board metaphor). STANDS as a process limitation.

## R9 — "The $47,000 story is an insurance agency's marketing anecdote."
Correct — it's the most vivid number in the deck and it comes from a vendor with an
incentive to dramatize. It is real content on a real page (fetched verbatim), labeled as an
agency client account everywhere it appears, and the structural claim it illustrates (GCs
withhold payment over lapsed COIs) is corroborated by three independent industry sources.
But no court record or news report verifies the specific figures. STANDS as a
source-quality caveat; a real founder should replace it with a first-party customer story
ASAP.

## Verdict
The company survives the red team as a **credible bootstrap/small-seed wedge with honest,
material risks**: unproven WTP (R3) and seasonal churn (R4) are the kill-shots to test
first; the moat (R1/R2) is speed + data maintenance, not defensibility. Nothing found in
the evidence base is fabricated; the weakest evidence is flagged, not hidden. If the first
200 founding seats don't sell to real tradespeople in ~90 days, that is the falsification
event — shut it down or reprice.
