# Lane: Developers / Technical Users — Problem Research
Date: 2026-07-13. Researched inline (dedicated lane agent killed by API spend limit; see record/decisions.md D-003). Reddit evidence fetched via curl on old.reddit.com with `_tools/reddit.js`.

## Candidate 1 — Homelab/self-hosted documentation ("I build it. Forget what I built. Reinstall the OS. Start over.")

**Problem statement.** Homelab and self-hosting enthusiasts chronically fail to document their setups (IPs, configs, the one article that fixed everything), so every failure becomes archaeology. The "how do you document your homelab" question recurs from 2017 to 2026.

**Who hurts + how often.** r/homelab (~2M members) and r/selfhosted operators; pain spikes at every breakage/rebuild.

**Evidence (fetched and verified via curl, 2026-07-13):**
1. "I build it. Forget what I built. Reinstall the os. Start over." — u/Lower_Sun_7354, 541pts (top comment), 2024-07-25, https://old.reddit.com/r/homelab/comments/1ec2gdj/how_do_you_document_your_homelab/ — **fetched and verified**
2. "Don't forget the part where you frantically search your history for that one article that was so valuable and say 'I should write this down' and never do." — u/gscjj, 215pts, same thread — **fetched and verified**
3. "...realize it was you from 4 years ago when you had the same exact problem the first time" — u/Archeious, 74pts, same thread — **fetched and verified**
4. Adjacent, sharper variant — "digital estate/bus factor": "how are you making sure that your family... can actually recover and access this data if something happens to you?" — u/foegra, 117pts, 2026-01-04, https://old.reddit.com/r/homelab/comments/1q3qcz2/how_are_you_ensuring_your_family_can_recover/ — **fetched and verified**

**Existing tools.** Obsidian (free), wikis (BookStack, Wiki.js — free/self-hosted), NetBox (free, overkill), draw.io (free). Users repeatedly recommend free tools to each other in the verified thread.

**The gap.** Nothing auto-documents; everything requires the discipline nobody has. An agent-style auto-documenter (scan network/docker-compose → living runbook) is a real idea.

**Willingness-to-pay: WEAK — and this is disqualifying.** The audience's identity is self-hosting free software; the top-voted answer to the estate question is "They don't care. The next guy will hopefully figure it out... Nobody cares that much lol" (u/varnell_hill, 99pts, fetched and verified). No paid category exists here at hobbyist level (NetBox monetizes enterprises, not homelabbers).

**Buildability as local demo: 4/5.** A scan-and-generate runbook demo with seeded data is very doable.

**Pain score: 5.5/10.** Real, chronic, funny — but the sufferers are the least monetizable audience on the internet for a paid tool. Advanced to tournament for completeness; expected to lose on WTP.

## Ranking
1. Homelab auto-documentation (5.5/10) — advanced, weak WTP flagged.
(Other developer-lane hypotheses — client-site maintenance for agency devs, on-call tooling — were not researched to the evidence bar in the remaining budget and are not advanced.)
