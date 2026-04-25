# Changelog

All notable changes to this skill are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-04-25

Bilingual rendering, automated jump-cut pacing, and content-philosophy guidance derived from real Instagram analytics on `naiken_komu_tokyo`.

### Added
- **Step 1.5 — Silence auto-cut.** New `scripts/silence_cut.py` preprocessor runs between source conversion and Whisper transcription. Removes pauses >0.4s by default, tunable via `--threshold` / `--min-silence` / `--pad`. Typical reduction: 25–35% of raw runtime.
- **Bilingual subtitle component.** New `src/components/DualSubtitle.tsx` renders JP at 64px and EN at 44px (1.45× hierarchy) with optional emphasis-word recoloring.
- **Subtitle style variants.** Per-segment `style` field in `edit_plan.json`: `primary` (default), `hook` (76px JP + punch-in animation), `cta` (accent yellow + arrow), `label` (JP-only on-screen labels).
- **Quality checks 8 and 9.** Silence-cut sanity (output 60–90% of source duration) and subtitle hierarchy (JP ≥ 1.4× EN size).
- **Content philosophy section in README.** Hook discipline (≤14 morae JP), cover image rules, length targets, series pillar structure, CTA placement.
- **Pillar badge convention.** Three series colors documented: red 【外国人の罠】 / yellow 【裏ワザ】 / blue 【内見】.
- **Cut-decision logging.** `silence_cut.py --log <path>` writes a JSON sidecar mapping cut-output timestamps back to source timestamps.

### Changed
- **`edit_plan.json` schema → v2.** `text` field renamed to `text_jp`, optional `text_en` field added. v1 segments still render (backward compatible via `text_jp || text` fallback).
- **Target reel length: 60–90s → 25–40s.** Driven by observed 2-second average watch time on 60s reels at v0.1; shorter format earns retention before extending.
- **Step 2 input.** Whisper now transcribes silence-cut output (`segments/*_cut.mp4`), not raw clips. Whisper timestamps map to the cut video.
- **Subtitle font weight.** Bumped JP from 700 to 900 (Black) for stronger legibility against varied backgrounds.

### Deprecated
- **QR-code-on-face CTA pattern.** Covering the speaker's face with the LINE QR in the final segment is no longer the recommended CTA layout. Use a corner overlay (≤25% of frame area) with face visible instead. The old pattern still renders if specified manually but is removed from default templates.
- **Cartoon / irasutoya cover images.** No longer recommended as cover frames. Analytics confirmed >85% skip rate on reels with cartoon thumbnails even when the underlying video was face-on-camera. Pull cover frames from talking-head footage instead.
- **List-promise opening hooks.** Patterns like 「〜の3選」 as the literal first line are deprecated in favor of `Topic + comma + verdict` openings (e.g. 「仲介手数料、半額にできます」). The list itself is fine; just don't lead with the promise.

### Migration from v0.1
1. Pull the patch and copy `scripts/silence_cut.py` and `src/components/DualSubtitle.tsx` into your project.
2. In `VideoEdit.tsx`, replace `import {Subtitle}` with `import {DualSubtitle}` and the corresponding render call.
3. Rename `text` → `text_jp` in existing `edit_plan.json` files (one-liner provided in `PATCH_NOTES.md`).
4. Update `SKILL.md` pipeline table to insert Step 1.5 and adjust Step 2's input path.
5. Optional: re-render any reels under 60 days old with the new pipeline if cover and pacing matter for the campaign.

### Known issues
- `silence_cut.py` re-encodes (libx264 CRF 18) rather than stream-copying, costing ~3s of compute per minute of input. Stream-copy would be faster but produces frame-accurate boundary issues at concat points; the re-encode is the safer default until the concat demuxer pathway is proven on iPhone HEVC sources.
- The DeepL/Claude translation step in Step 4 is not yet automated — `text_en` fields still require manual review for idioms and length compression.

---

## [0.1.0] — 2026-03-28

Initial release.

### Added
- 10-step Hermes pipeline: source conversion → Whisper transcription → quality check → `edit_plan.json` generation → Remotion composition → segment cutting → preview → quality verification → final render → optional CapCut polish.
- Japanese-only subtitle rendering at 1080×1920.
- Animated title banner with punch-in animation and gold glow.
- Background music with fade in/out.
- SFX triggered on highlighted captions.
- B-roll overlay support at topic transitions.
- QR-code / LINE CTA overlay on the final segment (deprecated in v0.2).
- Reference docs: `pipeline-steps.md`, `remotion-template.md`, `edit-plan-schema.md`, `quality-checks.md` (7 checks), `sfx-library.md`.
- Project folder convention: `raw/`, `segments/`, `sfx/`, `bgm/`, `broll/`, `output/`, `public/`.

[0.2.0]: https://github.com/Thesalmar/japan-video-editor-skill/releases/tag/v0.2.0
[0.1.0]: https://github.com/Thesalmar/japan-video-editor-skill/releases/tag/v0.1.0
