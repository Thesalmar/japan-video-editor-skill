# Japan Video Editor — Hermes Skill

A [Hermes Agent](https://github.com/NousResearch/hermes-agent) skill that automates the production of Japanese-language vertical short videos (TikTok / Instagram Reels / YouTube Shorts) from raw iPhone footage.

## What it does

Produces a 60–90s vertical video at **1080×1920** with:
- Japanese captions + English subtitles
- Animated title banner (punch-in animation, gold glow)
- Background music with fade in/out
- SFX triggered on highlighted captions
- B-roll overlays at topic transitions
- QR code / LINE CTA on the final segment

## Trigger phrases

Hermes activates this skill when you say:
- "edit this video"
- "make a short"
- "run the pipeline"
- "create a reel"
- Or when you drop a `.mp4` / `.MOV` file

## The 10-step pipeline

| Step | What happens |
|------|-------------|
| 1 | Convert source clips to h264/mp4 with ffmpeg |
| 2 | Transcribe with Whisper (Japanese, word timestamps) |
| 3 | Quality-check transcript (filler words, kanji misreads) |
| 4 | Generate `edit_plan.json` (segments, captions, SFX, B-roll) |
| 5 | Generate `src/VideoEdit.tsx` (Remotion composition) |
| 6 | Cut segments + wire `public/` symlinks |
| 7 | Preview in Remotion Studio (`npm start`) |
| 8 | Quality verification — 7 checks, up to 3 iterations |
| 9 | Export final render (`npx remotion render`) |
| 10 | (Optional) CapCut fine-tuning |

## Project folder structure

```
<project>/
├── raw/          ← source iPhone clips (.mp4)
├── segments/     ← trimmed segments (auto-generated)
├── sfx/          ← SFX library (shared across projects)
├── bgm/          ← background music (shared)
├── broll/        ← B-roll clips (auto-generated)
├── output/       ← final renders
├── public/       ← Remotion static assets (symlinks)
├── src/VideoEdit.tsx
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

- `ffmpeg`
- `python3` + `openai-whisper`
- `node >= 18` + `npm`
- `remotion` 4.0.290 (installed per project via `package.json`)

## References

| File | Contents |
|------|----------|
| `references/pipeline-steps.md` | Full commands for all 10 steps |
| `references/remotion-template.md` | Generic `VideoEdit.tsx` template |
| `references/edit-plan-schema.md` | `edit_plan.json` field reference |
| `references/quality-checks.md` | 7 quality checks with pass/fail criteria |
| `references/sfx-library.md` | 25 SFX files with recommended use cases |
