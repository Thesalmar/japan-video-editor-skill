# Patch Notes — v0.2 (silence cut + dual subtitles)

These changes drop into the existing Hermes skill. Two features, both backward compatible.

## Files to add

```
scripts/silence_cut.py              ← new step 1.5 preprocessor
src/components/DualSubtitle.tsx     ← replaces existing <Subtitle /> component
references/silence-cut.md           ← step 1.5 reference
references/dual-subtitle-schema.md  ← edit_plan v2 schema
```

## SKILL.md updates

### Section "The 10-step pipeline"

Insert a row between Step 1 and Step 2:

```
| 1.5 | Silence auto-cut on raw clips → segments/<basename>_cut.mp4 |
```

Update Step 2 to read cut segments instead of raw:

```
| 2 | Transcribe segments/*_cut.mp4 with Whisper (Japanese, word timestamps) |
```

### Section "Dependencies"

No new dependencies — silence_cut.py uses ffmpeg + Python stdlib only.

### Section "Trigger phrases"

No changes.

## edit_plan.json migration

**Old segments:** `{ "text": "..." }` — still works, renders JP-only.

**New segments:** `{ "text_jp": "...", "text_en": "..." }` — renders bilingual.

Mass-rename old plans:
```bash
python -c "import json,sys; p=json.load(open(sys.argv[1])); \
  [s.update({'text_jp': s.pop('text')}) for s in p['segments'] if 'text' in s]; \
  json.dump(p, open(sys.argv[1],'w'), ensure_ascii=False, indent=2)" edit_plan.json
```

## VideoEdit.tsx changes

Replace the existing subtitle import + render:

```tsx
// Before
import {Subtitle} from './components/Subtitle';
// ...
{plan.segments.map((s) => <Subtitle key={s.id} segment={s} />)}

// After
import {DualSubtitle} from './components/DualSubtitle';
// ...
{plan.segments.map((s) => <DualSubtitle key={s.id} segment={s} />)}
```

The new component is a drop-in replacement. The `SubtitleSegment` type is wider than the old one — TypeScript will accept old segments without changes.

## Step 4 prompt update (Whisper → edit_plan generator)

Where the agent generates `edit_plan.json` from the transcript, update the system prompt to:

> For each segment, populate `text_jp` with the Whisper transcription. Generate `text_en` as a concise English subtitle — under 8 words, capturing meaning not literal translation. Tag the first segment as `style: "hook"` and the last as `style: "cta"`. Mark on-screen labels (room names, prices, point numbers) as `style: "label"` with `text_en` omitted.

## Quality check additions

In `references/quality-checks.md`, append two checks:

**Check 8 — Silence-cut sanity**
- Cut output's duration is between 60% and 90% of source duration. <60% means cuts are too aggressive (likely clipping speech); >90% means the threshold was too lax. Re-run with adjusted `--threshold`.

**Check 9 — Subtitle hierarchy**
- JP subtitle font-size is at least 1.4× EN subtitle font-size at any frame where both are visible. Catches accidental EN-dominant rendering.

## Test plan

1. Take one of your existing 60s reels.
2. Run silence_cut.py with defaults — expect output 35–45s.
3. Re-render with the new DualSubtitle component using the existing edit_plan (renamed `text` → `text_jp`, no `text_en`) — should render identically to v1.
4. Add `text_en` to 3 segments — confirm they render with size hierarchy.
5. Tag segment 0 as `style: "hook"` — confirm the punch-in animation plays in the first 200ms.
