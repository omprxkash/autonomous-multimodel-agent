# Claim Verification Log (orchestrator-direct, conserved fetch budget)

Date: 2026-07-12. After the pain hunt, sub-agent web budget was exhausted mid-phase; the
orchestrator completed verification directly with a small number of high-value calls.
Every entry lists how it was verified and at what confidence.

## VERIFIED — primary source, fetched directly this session

**V1. Working on an expired license = unlicensed work (California).**
CSLB (California Contractors State License Board, official .ca.gov):
> "Any work performed while the license is expired is considered to be unlicensed and
> disciplinary action can be taken against you."
Also: delinquent fee, break in licensing time, retroactive renewal only within 90 days and
only for circumstances beyond your control; after 5 years expired you reapply from scratch.
Source (fetched): https://www.cslb.ca.gov/Contractors/Maintain_License/Renew_License/Failing_To_Renew_Your_License.aspx
Confidence: HIGH (government primary source).

**V2. COI lapse case — 11 days off the job, $47,000 withheld.**
> "The sub was off the job for 11 days. The GC withheld $47,000 in progress payments. The
> project missed its certificate of occupancy deadline, triggering liquidated damages."
Plus their estimate: COI mistakes cost "North Texas contractors $18K–$75K+ per year," with
withheld progress payments of "$15,000 – $85,000" over "14–21 days."
Source (fetched): https://theagentsoffice.com/certificate-of-insurance-mistakes-texas-contractors/
Confidence: MEDIUM-HIGH for the anecdote's existence on the page (fetched verbatim);
note this is an insurance agency's marketing content — the anecdote is their client story,
not independently auditable. Labeled as such wherever used.

**V3. Trade employment counts (BLS May 2025 OEWS, via secondary that reprints them).**
Electricians 757,220; plumbers/pipefitters/steamfitters 465,840; HVAC mechanics/installers
541,070. Mean annual wages ≈ $71,490 / $72,170 / $68,120.
Source (fetched): https://skilledtradesiq.com/salaries/bls-2025-oews-release/
(bls.gov OOH page itself returned HTTP 403 to our fetcher; numbers also matched the search
result summary of bls.gov pages.) Confidence: HIGH for magnitudes; secondary reprint of BLS.

**V4. Direct competitor scan (license/CE/COI renewal tracking).**
WebSearch (2026-07-12) surfaced: ExpiryEdge, ExpiryKeeper, ExpiryGuard, RemindCal (generic
expiry-reminder SaaS, not trade-native); SimpleCerts, SkillSignal, TrackMyVendor (GC-side
subcontractor-compliance tools — the buyer is the GC verifying subs, not the tradesperson).
No VC-funded, contractor-side, trade-native license/CE/COI product surfaced.
Confidence: MEDIUM — absence of evidence from one search pass, not proof of absence.
Sources: https://expiryedge.com/solutions/license-management/ ,
https://expiryguard.app/contractor-license-renewal-tracker ,
https://remindcal.com/license-expiration-reminder ,
https://simplecerts.ai/contractor-license-verification ,
https://www.skillsignal.com/certification-management/ ,
https://trackmyvendor.com/resources/how-to-track-subcontractor-compliance

**V5. Penalty landscape for expired-license work (search-level).**
California: misdemeanor, up to 6 months jail and/or $5,000 fine plus administrative fine
$200–$15,000 (CSLB unlicensed-consequences page surfaced in search results:
https://www.cslb.ca.gov/contractors/journeymen/journeymen_unlicensed_consequences.aspx ).
Florida: administrative penalty up to $5,000/incident. Some states bar enforcing a contract
for work performed while unlicensed.
Confidence: MEDIUM-HIGH (state sources surfaced by search; CA page is .ca.gov).

**V6. COI/insurance-lapse standard practice (search-level).**
GCs commonly withhold payment and block site access until a valid COI is on file; a lapsed
sub COI can put the GC in breach of its owner contract; workers'-comp lapse liability flows
up to the GC in most states.
Sources surfaced: https://trackmyvendor.com/resources/how-to-track-subcontractor-insurance ,
https://fieldpass.io/blog/how-to-verify-subcontractor-certificate-of-insurance ,
https://gritinsurance.com/blog/subcontractor-insurance-gaps-general-contractor
Confidence: MEDIUM (industry/vendor content, consistent across 3+ independent sources).

## VERIFIED — by sub-agent fetch during pain hunt (orchestrator did not re-fetch)

**V7. ServiceTitan stress quotes** — forum.heatinghelp.com [fetched by researcher D].
**V8. Capterra review quotes** (AppFolio, Square, Open Dental) [fetched by researcher B].
**V9. Indie Hackers quotes** [fetched by researcher A].

## PARTIALLY VERIFIED — search-snippet only (disclosed wherever used)

**P1. NAHB 2025 Technology Adoption Survey "34% use dedicated permit tracking tools (11% in
2022)"** — cited via projul.com; sub-agent reported fetching it, orchestrator re-fetch failed
with a connection error (socket hang up, twice). Used only with attribution "per projul.com
citing NAHB"; flagged in honesty.md.
**P2. ElectricianTalk "Anybody else HATE!!! paperwork?"** quotes — real thread URL surfaced in
search; wording via snippet. https://www.electriciantalk.com/threads/anybody-else-hate-paperwork.68465/
**P3. ContractorTalk "scheduling software overbuilt"** theme — same status.
https://www.contractortalk.com/threads/scheduling-software.421853/
**P4. Census 2022: ~2.88M US construction businesses have no employees (~75% of construction
establishments)** — surfaced in search result summary (jobstackcrm.com research page citing
Census); not re-fetched. Used as directional TAM anchor only, labeled.
https://jobstackcrm.com/research/trades-statistics/

## NOT USED
Claims we could not trace to any fetchable source were dropped from all deliverables.
