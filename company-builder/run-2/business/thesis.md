# DueCrew — Business Thesis

**One line:** DueCrew is a compliance deadline guard for solo and small-crew licensed trade
contractors — it watches license renewals, CE-credit progress, insurance (COI) and bond
expirations, and makes noise long before anything lapses.

---

## 1. The problem

A licensed tradesperson's ability to earn is gated by a stack of expiring documents:

- **The trade license itself.** Every state's cycle is different; many require continuing
  education before renewal. Texas electricians must complete 4 hours of TDLR-approved CE
  each renewal, covering the NEC, NFPA 70E safety, and state law
  ([tdlr.texas.gov](https://www.tdlr.texas.gov/electricians/elecce.htm)).
- **Certificates of insurance.** GCs require current COIs; a lapsed COI means blocked site
  access and withheld payment. Documented case: a sub was off the job **11 days** while the
  GC withheld **$47,000** in progress payments over an expired certificate
  ([theagentsoffice.com](https://theagentsoffice.com/certificate-of-insurance-mistakes-texas-contractors/) — insurance-agency client story, labeled as such).
- **Bonds, local registrations, permits** — each with its own clock.

Miss the license date and the consequences are not "late fee" — they are regulatory.
California's CSLB states plainly:

> "Any work performed while the license is expired is considered to be unlicensed and
> disciplinary action can be taken against you."
> — [CSLB, Failing to Renew Your License](https://www.cslb.ca.gov/Contractors/Maintain_License/Renew_License/Failing_To_Renew_Your_License.aspx) (fetched 2026-07-12)

In California, unlicensed contracting is a misdemeanor carrying up to six months jail and/or
a $5,000 fine plus administrative fines of $200–$15,000
([CSLB](https://www.cslb.ca.gov/contractors/journeymen/journeymen_unlicensed_consequences.aspx)).
Several states also bar contractors from enforcing a contract — i.e., suing to get paid —
for work performed while unlicensed.

## 2. The person

The solo electrician, plumber, or HVAC tech — often licensed in 2+ states or
jurisdictions — with no office manager. The three core trades alone employ **1.76M people**
(BLS May 2025 OEWS: 757,220 electricians; 465,840 plumbers/pipefitters/steamfitters;
541,070 HVAC — via [skilledtradesiq.com](https://skilledtradesiq.com/salaries/bls-2025-oews-release/)).
Roughly **2.88M US construction businesses have no employees** (Census 2022, via
[jobstackcrm.com](https://jobstackcrm.com/research/trades-statistics/) — search-corroborated, see honesty.md).

How they cope today, in their own words:

- "When it comes time to get all this paperwork done, I fold like a cheap suit." — member,
  ElectricianTalk, thread *"Anybody else HATE!!! paperwork?"*
  ([electriciantalk.com](https://www.electriciantalk.com/threads/anybody-else-hate-paperwork.68465/), snippet-corroborated)
- One ElectricianTalk member said the paperwork burden is the reason he stays an employee
  instead of going out on his own (same thread).
- Small contractors reject scheduling/FSM software as "way too involved… for a small
  company," keeping dates "in their head, pen and paper, spreadsheet, or Google calendar"
  ([contractortalk.com](https://www.contractortalk.com/threads/scheduling-software.421853/), snippet-corroborated)
- Per projul.com citing an NAHB 2025 Technology Adoption Survey, only **34%** of residential
  contractors use dedicated permit-tracking tools — up from 11% in 2022, i.e. ~two-thirds
  still track compliance dates by hand or not at all
  ([projul.com](https://projul.com/blog/best-construction-permit-tracking-software/) — re-fetch failed, see honesty.md).

## 3. The product

One screen answers one question: **"Am I good to work?"**

- **Standing board** — every credential (license, CE, COI, bond, registration) as a
  red/amber/green card with days remaining.
- **Escalating alerts** — 90/60/30/14/7/1 days out, by SMS and email, that get louder as the
  date gets closer. The 7-day alert includes the renewal link and fee for your state.
- **CE ledger** — hours logged vs. hours required for your state and license class, with
  approved-provider links. (Real demand signal: an entire ecosystem of $9–$10 TDLR-approved
  CE course sellers exists — e.g. [expertce.com](https://expertce.com/ce/electrician/texas/),
  [hlonlinece.com](https://hlonlinece.com/product/texas4hrelectriciancourse/).)
- **COI locker + share link** — a live link that always serves your *current* certificates,
  so GCs stop emailing "send me your COI again."
- **State rules library** — renewal cycle, CE requirement, fee, and grace-period rules per
  state per trade, maintained by us (initially 10 states × 3 trades; roadmap to 50).
- **Crew plan** — add employees' cards and med certs; the owner sees the whole crew's board.

Explicitly NOT: scheduling, dispatch, invoicing, CRM. Solo operators have told the market
repeatedly they don't want a suite. DueCrew is one job done completely.

## 4. Why now

1. **The compliance-tooling wave reached construction but skipped the little guy.**
   PermitFlow raised a **$54M Series B (Dec 2025)** automating permit *submission* for
   larger GCs ([businesswire.com](https://www.businesswire.com/news/home/20251202551013/en/PermitFlow-Raises-$54-Million-to-Solve-Constructions-Biggest-Bottlenecks-With-AI)).
   GC-side sub-compliance tools (SkillSignal, SimpleCerts, TrackMyVendor) are multiplying.
   Every one of them polices the tradesperson from above; none serves him.
2. **GC enforcement is tightening**, which converts "annoying" into "income-stopping":
   GC-side tooling now auto-blocks subs with lapsed COIs at the gate
   ([skillsignal.com](https://www.skillsignal.com/certification-management/)).
3. **Licensing burden keeps growing** — states keep adding CE requirements, and
   multi-jurisdiction work is increasingly normal for trades near state lines.

## 5. Competition (honest summary — full analysis in competitors.md)

Generic expiry-reminder SaaS (ExpiryEdge, RemindCal, ExpiryGuard) — not trade-aware, no
state rules, no CE ledger, no COI share. GC-side compliance platforms (SkillSignal,
SimpleCerts, TrackMyVendor) — wrong buyer. FSM suites (ServiceTitan, Jobber, Housecall
Pro) — rejected by solos as overbuilt; ServiceTitan's own users report add-on stacking of
$12–33k/yr ([capterra.com](https://www.capterra.com/p/150053/ServiceTitan/reviews/), snippet).
No trade-native, contractor-side product found (search pass 2026-07-12; absence of evidence
≠ proof — see red team).

## 6. The wedge

**Be the tradesperson's side of the table.** The GC has a compliance department; the sub has
a glovebox. DueCrew's state-rules dataset (maintained, accurate, per-trade) is the working
moat: reminders are a commodity, *knowing what Texas requires of a journeyman electrician
and when* is a curated data asset that compounds. The COI share link creates a viral loop:
every GC who receives one sees the brand.

## 7. The honest risks (previewed; full red team in record/red-team.md)

- A reminder product is feature-sized; Jobber could ship it in a quarter.
- WTP for "peace of mind" products is unproven at $12/mo for this audience.
- State-rules maintenance is a real ongoing cost and a liability surface if wrong.
- Direct-competitor scan was one search pass on a constrained budget.
