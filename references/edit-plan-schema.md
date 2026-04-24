# edit_plan.json Schema

Complete field reference for the edit plan JSON produced in Step 4 of the pipeline.

## Root fields

```json
{
  "source_clips": ["IMG_6856.mp4", "..."],
  "output_resolution": { "width": 1080, "height": 1920 },
  "fps": 30,
  "total_duration_seconds": 76.74,
  "title_banner": { ... },
  "keep_segments": [ ... ],
  "captions": [ ... ],
  "broll_slots": [ ... ],
  "sfx": { ... },
  "bgm": { ... }
}
```

## `title_banner`

Animated pill shown for the first 7 seconds of the video.

```json
{
  "text": "【即節約】仲介手数料を\n無料にする方法",
  "background_color": "#0D1B4B",
  "text_color": "#FFFFFF",
  "height_px": 80,
  "font_size": 32
}
```

Rules:
- Use `【brackets】` for hook word at the start
- Max 2 lines (use `\n` to split)
- Background: dark navy `#0D1B4B` or dark blue `#0a1540`
- Font size 28–34px depending on title length

## `keep_segments[]`

Each object represents one trimmed clip:

```json
{
  "id": 0,
  "source_file": "raw/IMG_6856.mp4",
  "source_start": 8.9,
  "source_end": 11.92,
  "output_start": 0.0,
  "output_end": 3.02,
  "crossfade_ms": 50
}
```

- `id`: sequential integer starting at 0
- `source_file`: path relative to project root
- `source_start` / `source_end`: seconds in the original clip
- `output_start` / `output_end`: seconds in the assembled timeline (before speed adjustment)
- `crossfade_ms`: always 50 (hard cut with tiny crossfade)

The output segment file must be `segments/seg_NN.mp4` where NN = zero-padded id.

## `captions[]`

Each caption is shown for its duration at the bottom of the frame.

```json
{
  "id": 0,
  "segment_id": 0,
  "text": "礼金なしの物件を狙いましょう",
  "start": 27.4,
  "end": 29.82,
  "highlight": true
}
```

- `id`: sequential integer
- `segment_id`: which keep_segment this caption belongs to
- `text`: Japanese text, **max 15 characters**
- `start` / `end`: seconds on the output timeline (pre-speed)
- `highlight`: `true` → text renders in red (`#FF3B3B`), SFX plays mid-caption

Caption rules:
- Keep to one clause per caption — split long sentences
- Numbers and amounts always highlighted
- Action imperatives always highlighted (〜ましょう, 〜してください)
- Section headers always highlighted (一つ目、二つ目…)

## `broll_slots[]`

B-roll overlays inserted at topic transitions.

```json
{
  "id": 0,
  "insert_after_segment": 7,
  "duration_seconds": 4,
  "prompt": "Japanese apartment contract and keys on a table, Tokyo, vertical 9:16",
  "type": "video",
  "file_path": "broll/Japanese_Guarantor_Company_B_Roll.mp4"
}
```

- `insert_after_segment`: which segment the B-roll follows
- `duration_seconds`: 3–6s recommended
- `prompt`: Genspark/image-gen prompt for generating the B-roll
- `type`: `"video"` or `"image"` (image is auto-converted to video)
- `file_path`: null until generated, then set to the actual path

## `sfx`

```json
{
  "at_cuts": false,
  "note": "SFX mapped per caption in VideoEdit.tsx"
}
```

SFX are mapped per-caption in `VideoEdit.tsx` via the `CAPTION_SFX` map.

## `bgm`

```json
{
  "source": "bgm/Taking_It_Slow.mp3",
  "volume": 0.10,
  "fade_in_frames": 30,
  "fade_out_frames": 60
}
```

- `volume`: 0.08–0.12 for background music under speech
- `fade_in_frames`: frames at 30fps (30 = 1 second)
- `fade_out_frames`: 60 = 2 second fadeout at the end
