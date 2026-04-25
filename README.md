# Japan Video Editor — Hermes Skill

A [Hermes Agent](https://github.com/NousResearch/hermes-agent) skill that automates the production of bilingual (JP/EN) vertical short videos for TikTok / Instagram Reels / YouTube Shorts from raw iPhone footage.

Optimized for talking-head content where the on-screen creator speaks Japanese and the EN subtitle serves a bilingual audience. The strategic context behind these defaults — niche, audience, content style — is documented separately in [`CONTEXT.md`](CONTEXT.md).

## What it does

Produces a 25–40s vertical video at **1080×1920** with:

* **Silence-cut pacing** — pauses >0.4s auto-removed for jump-cut feel
* **Bilingual subtitles** — JP at 64px (algorithmic priority), EN at 44px below. Ratio 1.45×.
* **Animated title banner** with punch-in hook style for first 2 seconds
* **Background music** with fade in/out, ducked under voice
* **SFX triggered** on emphasized captions and scene transitions
* **B-roll overlays** at topic transitions (screenshots, graphics, room labels)
* **Style variants** per segment: `hook` / `primary` / `cta` / `label`

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
| 1.5 | Silence auto-cut on raw clips → `segments/<n>_cut.mp4` |
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

## Documentation

| File | Contents |
| --- | --- |
| [`CONTEXT.md`](CONTEXT.md) | Account, niche, audience, content pillars, editing style, approach |
| [`CHANGELOG.md`](CHANGELOG.md) | Version history |
| `references/pipeline-steps.md` | Full commands for all pipeline steps |
| `references/silence-cut.md` | Step 1.5 reference — tuning by recording environment |
| `references/remotion-template.md` | Generic `VideoEdit.tsx` template |
| `references/edit-plan-schema.md` | `edit_plan.json` field reference (v1, legacy) |
| `references/dual-subtitle-schema.md` | `edit_plan.json` v2 — bilingual subtitle schema |
| `references/quality-checks.md` | 9 quality checks with pass/fail criteria |
| `references/sfx-library.md` | 25 SFX files with recommended use cases |
