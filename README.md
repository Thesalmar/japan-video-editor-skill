# Japan Video Editor — Hermes Skill

A [Hermes Agent](https://github.com/NousResearch/hermes-agent) skill that automates the production of bilingual (JP/EN) vertical short videos for TikTok / Instagram Reels / YouTube Shorts from raw iPhone footage.

Optimized for talking-head content in the Japanese real-estate / lifestyle niche, where the on-screen creator speaks Japanese and the EN subtitle serves the bilingual audience.

## What it does

Produces a 25–40s vertical video at **1080×1920** with:

* **Silence-cut pacing** — pauses >0.4s auto-removed for jump-cut feel
* **Bilingual subtitles** — JP at 64px (algorithmic priority), EN at 44px below (comprehension aid). Ratio 1.45×.
* **Animated title banner** with punch-in hook style for first 2 seconds
* **Background music** with fade in/out, ducked under voice
* **SFX triggered** on emphasized captions and scene transitions
* **B-roll overlays** at topic transitions (screenshots, graphics, room labels)
* **Style variants** per segment: `hook` / `primary` / `cta` / `label`

## Why these defaults

Defaults are tuned from real Instagram analytics on `naiken_komu_tokyo` (Tokyo bilingual real estate content):

| Lesson learned | Default it informs |
| --- | --- |
| 89% skip rate on cartoon-thumbnail reels | Cover frames now pulled from face-on-camera shots, not title cards |
| 2-second avg watch time on 60s reels | Target length cut to 25–40s, silence-cut on by default |
| JP-primary search drives algorithmic reach | JP subtitle 1.45× larger than EN |
| Talking-head-only feels slow | Cut-every-3-seconds rhythm enforced via silence-cut + B-roll |

## Trigger phrases

Hermes activates this skill when you say:

* "edit this video"
* "make a short"
* "run the pipeline"
* "create a reel"
* Or when you drop a `.mp4` / `.MOV` file

## The pipeline

| Step | What happens |
| --- | --- |
| 1 | Convert source clips to h264/mp4 with ffmpeg |
| 1.5 | **Silence auto-cut** on raw clips → `segments/<name>_cut.mp4` |
| 2 | Transcribe `segments/*_cut.mp4` with Whisper (Japanese, word timestamps) |
| 3 | Quality-check transcript (filler words, kanji misreads) |
| 4 | Generate `edit_plan.json` v2 (segments with `text_jp` + `text_en`, style tags, SFX, B-roll) |
| 5 | Generate `src/VideoEdit.tsx` (Remotion composition) using `<DualSubtitle />` |
| 6 | Cut segments + wire `public/` symlinks |
| 7 | Preview in Remotion Studio (`npm start`) |
| 8 | Quality verification — 9 checks, up to 3 iterations |
| 9 | Export final render (`npx remotion render`) |
| 10 | (Optional) CapCut fine-tuning |

## Project folder structure

```
<project>/
├── raw/          ← source iPhone clips (.mp4)
├── segments/     ← silence-cut clips (auto-generated, fed to Whisper)
├── sfx/          ← SFX library (shared across projects)
├── bgm/          ← background music (shared)
├── broll/        ← B-roll clips, screenshots, graphics
├── output/       ← final renders
├── public/       ← Remotion static assets (symlinks)
├── src/
│   ├── VideoEdit.tsx
│   └── components/
│       └── DualSubtitle.tsx
├── edit_plan.json
└── transcript.json
```

## Installation

Clone this repo into your Hermes skills directory:

```bash
mkdir -p ~/.hermes/skills/video-editing
git clone git@github.com:Thesalmar/japan-video-editor-skill.git \
  ~/.hermes/skills/video-editing/japan-video-editor
```

Hermes picks up the skill automatically on next launch — no config change needed.

## Dependencies

* `ffmpeg` (silence detection + final encoding)
* `python3` + `openai-whisper`
* `node >= 18` + `npm`
* `remotion` 4.0.290 (installed per project via `package.json`)

## Content philosophy (read this before you film)

The skill produces good-looking bilingual reels. Whether they perform is up to the script and the cover image, not the editor. A few hard-won rules:

### Hook discipline

* The spoken JP hook must fit in **2 seconds (≈10–14 morae)**. Anything longer kills retention.
* Pattern that works: `Topic + comma + verdict`. Examples: 「仲介手数料、半額にできます」 / 「外国人、ここで落ちます」.
* Avoid the list-promise opener (「〜の3選」) as the first line. Open with a verdict, *then* introduce the list.

### Cover image

* **Never** use cartoon clipart (irasutoya etc.) as the cover. Analytics-confirmed: cartoon thumbnails get >85% skip rate even when the underlying video is a real person on camera. The cover sets the expectation; viewers swipe based on the cover, not the content.
* Pull the cover frame from a moment of you on-camera, mid-gesture, eyes engaged.
* Bold JP text overlay. Optional small EN line beneath. Pillar-color badge top-left for series recognition.

### Length

* Target 25–40 seconds until your average watch time exceeds 8 seconds. Then experiment with 50–60s.
* The silence-cut step typically removes 25–35% of raw footage, so film for ~50s if you want a ~35s output.

### Series structure

Three content pillars rotate consistently:

1. **【外国人の罠】** (foreigner-specific traps) — red badge
2. **【裏ワザ】** (money/process hacks) — yellow badge
3. **【内見】** (apartment reveals with price + catch) — blue badge

The pillar badge is part of the cover template and signals the series at a glance.

### CTA placement

* **Don't** cover the speaker's face with a QR code or LINE banner.
* Place the CTA in the last 4–5 seconds, with the QR / link in a corner overlay (≤25% of frame area), face still visible.
* For paired reels (cliffhanger + resolution), end the first with 「続きは次の動画で」 and post the resolution within a week.

## References

| File | Contents |
| --- | --- |
| `references/pipeline-steps.md` | Full commands for all pipeline steps |
| `references/silence-cut.md` | Step 1.5 reference — tuning by recording environment |
| `references/remotion-template.md` | Generic `VideoEdit.tsx` template |
| `references/edit-plan-schema.md` | `edit_plan.json` field reference (v1, legacy) |
| `references/dual-subtitle-schema.md` | `edit_plan.json` v2 — bilingual subtitle schema |
| `references/quality-checks.md` | 9 quality checks with pass/fail criteria |
| `references/sfx-library.md` | 25 SFX files with recommended use cases |

## Versions

* **v0.2** — silence-cut preprocessor (Step 1.5), bilingual JP/EN subtitle component, expanded quality checks (9), content philosophy section
* **v0.1** — initial 10-step pipeline, JP-only subtitles, QR-on-face CTA pattern (deprecated)
