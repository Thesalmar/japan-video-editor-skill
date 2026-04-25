# CONTEXT — `naiken_komu_tokyo`

This document captures the strategic context behind the content this skill is tuned for. It exists separately from the technical README so that defaults, prompts, and templates in the skill can be traced back to the underlying positioning and audience decisions.

If you fork this skill for a different account, replace this file. The skill mechanics will still work; only the assumptions documented here would need to change.

---

## Account

- **Handle:** `naiken_komu_tokyo` (Instagram, TikTok)
- **Operator:** こむ — bilingual real estate agent affiliated with Rakusumu
- **Service link:** rakusumu.jp/167080419
- **Conversion mechanic:** LINE add → personal consultation → property introduction
- **Side gig:** ~3–4 hours/week of content production capacity. Day job is IT Support Specialist; this is not a full-time creator account and the cadence reflects that.

## Niche

Tokyo rental real estate (賃貸 / 内見), with a bilingual lens. The space is crowded with Japanese-language accounts (`@tokyo.naiken`, `@naiken.girl`, `@simplenaiken_buy`, `@tokyo_naiken3`) targeting Japanese renters. The differentiator here is the foreigner-perspective angle delivered in fluent Japanese — a positioning none of the dominant accounts can credibly occupy.

## Audience

Bilingual targeting, both audiences weighted equally:

- **Foreigners in Japan or planning to move.** Want to navigate the rental system without getting overcharged or rejected. Pain points: guarantor companies, residence card requirements, language barriers at agencies, brokerage-fee opacity. They consume in EN as a comprehension aid but the JP delivery signals competence and trust.
- **Japanese viewers curious about a foreigner explaining 不動産.** The novelty of "a foreigner who knows the Japanese rental system better than most Japanese people" drives watch and share behavior. They consume in JP natively.

The audience split shapes every design decision in the skill — JP is algorithmically primary (search reach, Japanese hashtag distribution), EN is the comprehension layer.

## Content pillars

Three pillars rotate. Pillar identity is reinforced visually via a colored badge in the top-left of every cover image and (optionally) the opening frame.

| Pillar | Badge | Content type |
| --- | --- | --- |
| 【外国人の罠】 | red | Foreigner-specific traps: guarantor rejections, 在留カード requirements, application screening criteria, language pitfalls |
| 【裏ワザ】 | yellow | Money and process hacks: 仲介手数料 reduction, 礼金 negotiation, 更新料 avoidance, zero-fee agents |
| 【内見】 | blue | Apartment reveals — real footage, price upfront, "the catch" mid-video to drive saves and finishes |

Rotation order: trap → hack → reveal → trap. Each pillar earns roughly equal posting share. Reveals are the most visual and shareable; traps are the most uniquely positioned; hacks have the highest save rate.

## Content style

### Hook

Spoken JP hook fits in **2 seconds (≈10–14 morae)**. Pattern: `Topic + comma + verdict`. Examples that work:

- 「仲介手数料、半額にできます」
- 「外国人、ここで落ちます」
- 「神楽坂、1LDK、いくら?」

List-promise openings (「〜の3選」 as the literal first line) are deprecated for this account — they read as article titles, not video hooks. The list itself is fine; just don't lead with the promise.

### Length

Target **25–40 seconds**. Driven by observed retention: at v0.1 the account averaged 2 seconds of watch time on 60-second reels. Shorter format earns retention before extending. Once average watch time crosses 8 seconds consistently, experiment with 50–60s.

### Cover image

Pulled from a face-on-camera frame (mid-gesture, eyes engaged), with bold JP text overlay. Pillar-color badge top-left for series recognition. Cartoon clipart (irasutoya etc.) is **never** used — analytics-confirmed >85% skip rate on cartoon-thumbnail reels even when the underlying video is face-on-camera. The cover sets viewer expectation; viewers swipe based on the cover, not the content underneath.

### Cadence

1 reel per week minimum, 2 per week ceiling at side-gig capacity. Bundle filming (2 reels in one Sunday session) when possible; edit during weeknight downtime. Pairs of reels (cliffhanger + resolution) post a week apart with a comment teasing the next.

## Editing style

These choices are encoded in the skill's defaults; documented here so the rationale survives.

### Pacing

Cut every 2–4 seconds. Achieved automatically via `silence_cut.py` (Step 1.5) which removes pauses >0.4s, plus B-roll overlays at topic transitions. Talking-head footage with natural breathing pauses feels too slow on platform — the silence-cut step compensates.

### Subtitles

Bilingual JP + EN, rendered with size hierarchy: JP at 64px, EN at 44px below (1.45× ratio). JP is visually dominant because it drives algorithmic reach via Japanese hashtag and search distribution. EN is the comprehension layer for the foreigner audience. JP under 18 morae per segment, EN under 8 words — EN compresses meaning rather than translating literally.

### Style variants

Per-segment `style` tag in `edit_plan.json` controls visual treatment:

- `hook` — first 2–3s, JP scaled to 76px, punch-in animation
- `primary` — default talking-head dialogue
- `cta` — last segment, accent yellow, arrow icon
- `label` — on-screen labels (room names, prices), JP-only

### Audio

Background music at -18 to -20dB under voice. Soft whoosh SFX on pillar-badge appearance and major scene transitions. Voice is the foreground; music is texture.

## Approach to growth

Side-gig pace, six-month minimum to traction. The plan that fits the capacity:

- **Month 1:** Establish the format. New cover template, silence-cut pacing, dual subtitles. Goal is average watch time crossing 6 seconds on new-format reels.
- **Month 2:** First reel breaks 1k views. First organic LINE add traceable to Instagram.
- **Month 3:** ~300 followers, 3–5 LINE adds, clear signal on which pillar performs best. Double down on the winner.
- **Months 4–6:** Compounding. 12+ reels published. Apartment reveals (Pillar 3) bundled with actual 内見 work — content production piggybacks on the day-to-day of the agent role rather than competing with it.

## Conversion logic

Three goals run in parallel; reels serve different goals depending on pillar:

- **Pillar 1 (traps):** trust + LINE adds. The CTA is "DM or add LINE — I help with this." High conversion potential because the pain point is acute.
- **Pillar 2 (hacks):** saves + follows. Educational content; viewers save it and follow for more. Direct conversion is secondary.
- **Pillar 3 (reveals):** profile clicks → website. Specific listings drive specific inquiries. The CTA names the property: "DM 'Kagurazaka' on LINE."

The CTA never covers the speaker's face (deprecated v0.1 pattern). Corner overlay, ≤25% of frame area, face still visible — this preserves trust signaling at the moment of ask.

## What this skill does NOT cover

Documented so future-you doesn't expect features that aren't there:

- Posting and scheduling (manual via Instagram/TikTok apps)
- Caption and hashtag generation (manual; conventions in the README)
- Cover image generation (Canva/Figma template, separate from the editor pipeline)
- Cross-posting between IG and TikTok (export once, upload twice)
- Analytics ingestion or performance tracking (manual review of platform insights)
