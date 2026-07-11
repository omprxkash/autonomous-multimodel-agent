# MASTER PROMPT — Autonomous Company Builder


> /goal Read projects/company-builder-experiment/master-prompt.md and execute everything below the divider line as your goal. That file is your full instruction set: mission, guardrails, phases, deliverables, and definition of done. Follow it exactly, including the never-ask rule. Do not report back to me until the definition of done is met. Start now.

---

## Mission

Build me a complete company from scratch. Start with nothing but the open internet. Find a real, painful, underserved problem that real people are complaining about right now, design a business around it, build the product and the brand and the website, and hand me a finished package I could take to market this month. Then prove to me why it would work.

This is a test of how far you can go on your own. I am not going to answer questions mid-run. Make every call yourself, write down why you made it, and keep moving. Within the guardrails below, you have total creative freedom. Do whatever you want. Surprise me. I want to see your best work, not your safest work.

## Guardrails

1. **No new spending.** APIs whose keys already exist in `.env` are fair game (Kie.ai via `KIE_AI_API_KEY` for image generation, ElevenLabs via `ELEVENLABS_API_KEY` for voice and sound, HeyGen via `HEYGEN_API_KEY` for avatar video). Beyond those: no new paid services, no purchases, no signups that require payment info, no domain registration. Check domain availability, don't buy.
2. **Publish nothing.** Everything stays local or in this repo. No deploying to the public internet, no posting anywhere, no emailing or messaging any real person.
3. **Invent nothing.** Every quote, stat, complaint, competitor fact, and market claim in your deliverables must trace to a real URL you actually fetched. If you infer something, label it as inference. If you couldn't verify something, say so. A smaller thesis built on real evidence beats a grand one built on plausible fiction.
4. **Work inside** `projects/company-builder-experiment/run-1/`. All artifacts go there.
5. **Never ask me anything.** I will not be watching. Every question you'd ask me, answer yourself with research and reasoning, then log the question, your answer, and why in the build log. Blocked is not an option: if a tool or approach fails, find another route. If a phase stalls, ship the strong 80% version, note what got cut, and keep moving. Do not stop until the definition of done is met.

## What "orchestrate" means here

Use multi-agent workflows aggressively. Fan out parallel researchers across different sources and angles. Run tournaments where independent agents pitch competing business ideas and judge panels score them. Adversarially verify every important claim with skeptic agents whose only job is to refute it. Use a completeness critic before you call any phase done. Design whatever orchestration shapes the work calls for; the patterns above are a floor, not a ceiling.

## The arc

1. Hunt for pain.
2. Pick the winner.
3. Design the business.
4. Build the brand.
5. Build the thing.
6. Make the launch video.
7. Make the founder video.
8. Try to kill it.
9. Package it.

## The deliverables list is a floor, not a ceiling

Everything above is the minimum. I want to see how far you can push this. If a real founder launching this company would make something, and you can make it with the tools you have, make it. Ideas to steal or beat: ad creatives for the top channel in your launch plan, a one-page investor teaser, social profile assets (banners, avatars, first-week post drafts), a product walkthrough video, an onboarding email sequence, a pitch deck. Don't do all of them; do the ones that make this company feel most real, and invent at least one deliverable nobody would expect. Every extra goes in the recap page's deliverables map like everything else, and quality still beats quantity: one more polished, verified artifact beats three rushed ones.

## Definition of done

You're done when a stranger could open `recap.html`, understand the business in five minutes, run the site locally, watch the launch video, and walk away either convinced or precisely informed about why they're not convinced. Before you finish, grade yourself against this list and fix anything failing: every guardrail held, every claim in the thesis has a live URL, the site is screenshot-verified on mobile and desktop, both videos render and you actually watched them, the founder script passes my voice rules, the recap page links to every deliverable and every link works, the brand guidelines are complete enough that a stranger could make a new on-brand asset from them alone, the red team ran and its objections are visible in the final docs, and nothing in the package is a placeholder pretending to be finished work.

Now go build me a company.
