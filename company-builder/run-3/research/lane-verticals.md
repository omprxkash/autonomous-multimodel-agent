# Lane: Niche Professional Verticals — Problem Research
Date: 2026-07-13. Researched inline (the dedicated lane agent was killed by an API spend limit mid-hunt; see record/decisions.md D-003). Evidence below was fetched directly in this run via curl against old.reddit.com (WebFetch is domain-blocked for reddit; curl HTML fetches work and were parsed with `_tools/reddit.js`).

## Candidate 1 — Home inspectors: report-software exodus (Spectora backlash)

**Problem statement.** Home inspectors' dominant report-writing software, Spectora (~$1,000+/yr), is in an active trust crisis: chronic bugs plus a March/April-2026 "Fixle" partnership that inserts third-party home-services upsells into the inspector's client portal with **no opt-out**. Inspectors feel their client relationship is being resold and are actively shopping for alternatives.

**Who hurts + how often.** Working home inspectors (solo and 2–5 person firms dominate, per thread participants), on every report they deliver. Spectora claims "over 10,000 home inspectors" (spectora.com marketing, surfaced in search).

**Evidence (all fetched and verified via curl on 2026-07-12/13):**
1. "Either they provide an option to Opt out all of my clients from Fixle or I cancel my subscription and move elsewhere. Spectora seems to have forgotten that we, the home inspectors that pay their monthly subscription, are their clients. Going behind our backs to sell additional services to the clients that trust us... is such a disrespectful business tactic." — u/DefNotAnotherChris, 31pts, 2026-04-01, https://old.reddit.com/r/homeinspectors/comments/1s9ok7f/spectora_opt_out_of_fixle_or_cancel_subscription/ — **fetched and verified**
2. "They said there's no opt out option at this time" — u/nbarry51278, same thread, 2026-04-01 — **fetched and verified**
3. "They're banking on us not being willing to deal with the hassle of changing software... The lying drives me crazy." — u/Cecil-twamps, same thread, 2026-04-01 — **fetched and verified**
4. "I just can't deal with all the bugs anymore. The last few months I've had one or more issues pop up on an almost daily basis... The subscription is almost $1,000 a year except I feel like I'm a beta tester." — u/DefNotAnotherChris, 13pts, 2025-10-28, https://old.reddit.com/r/homeinspectors/comments/1oic9mk/i_think_im_done_using_spectora/ — **fetched and verified**
5. "I've used them since the VERY beginning, but I too am getting quite tired of all these bugs... The problem is so far I can't find anyone that actually does what spectora can do." — u/Sherifftruman, same thread — **fetched and verified**
6. "the wagstaff bros have long ago left the building. They did what they set out to do. Make millions on the backs of inspectors." — u/FlowLogical7279, same thread — **fetched and verified** (founders sold; users perceive post-acquisition decay)

**Incumbents + pricing.** Spectora base ~$109/mo or ~$1,090/yr (spectora.com/pricing surfaced in search results; the $1,000/yr figure independently corroborated by verified quote #4). Alternatives already circling: HomeGauge, Tap Inspect, Inspector Toolbelt, Inspect Forge — all actively recommended inside the verified threads. InterNACHI forum thread "Forced Partnership" exists (surfaced in search) but is Cloudflare-blocked and has no Wayback snapshot — **UNVERIFIED directly**.

**The gap.** A report-writing tool whose pitch is trust: your report, your client, no third-party monetization of either. But note the crowding signal, verified: the r/homeinspectors moderator posted "I am tired of all these new AI software startups trying to organically advertise in discussions regarding Spectora. You will be banned..." (32pts, 2026-04-05, https://old.reddit.com/r/homeinspectors/comments/1scryrx/ — fetched and verified via search listing). The exodus is real AND already heavily farmed.

**Willingness-to-pay.** Very strong — ~$1,090/yr per inspector verified as the going rate, and quote #5 shows even furious users stay because nothing matches the feature set (high switching costs = high value).

**Buildability as local demo: 3.5/5.** A web report-editor demo is very doable (photo annotation, comment library, PDF-style output). But the real product's center of gravity is an offline-capable mobile app used on-site — a browser demo under-represents the actual job, and honest demo-to-product distance is wide.

**Pain score: 8.5/10.** Hot, current, money-backed betrayal pain — but the rescue market is crowded and the wedge (trust) is easily copied marketing rather than architecture.

---

## Candidate 2 — Therapists in private practice: practice-management price/trust complaints (NOT fully researched)

The lane agent died mid-hunt right after noting "Now therapists — SimplePractice pricing + reviews." Inline time was spent on the stronger inspector candidate. Known-but-unverified-in-this-run: SimplePractice's 2023–24 price restructuring caused documented practitioner anger. **No verified quotes were collected in this run; candidate excluded from the tournament per evidence bar D-002.**

## Ranking
1. Home inspectors / Spectora exodus (8.5/10 pain, 3.5/5 demo) — advanced to tournament.
2. Therapists — insufficient verified evidence in this run; not advanced.
