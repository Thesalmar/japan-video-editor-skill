# `edit_plan.json` — Dual Subtitle Schema (v2)

Adds bilingual JP/EN subtitle support to the existing schema. Backward compatible: clips without `text_en` render JP-only as before.

## Per-segment fields

```json
{
  "id": "seg_03",
  "start": 7.2,
  "end": 11.4,
  "text_jp": "外国人だから断られたわけじゃないです",
  "text_en": "You weren't rejected for being foreign.",
  "style": "primary",
  "emphasis": ["外国人だから"]
}
```

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `text_jp` | string | yes | Replaces the old `text` field. Migration: rename `text` → `text_jp`. |
| `text_en` | string | no | English subtitle. Omit for JP-only segments (e.g. on-screen labels, hooks where EN clutters). |
| `style` | enum | no | `primary` (default) / `hook` / `cta` / `label`. See style table below. |
| `emphasis` | string[] | no | Substrings of `text_jp` to render in the accent color. |

## Visual specification

The JP subtitle is the algorithmic-priority text — Japanese viewers are the primary search signal. EN is the trust signal for foreigners. Sizes encode that hierarchy.

| Element | Size (px @ 1080×1920) | Weight | Color | Position |
| --- | --- | --- | --- | --- |
| `text_jp` | 64 | Black (900) | `#FFFFFF` w/ 4px black outline | Center-bottom, 280px from bottom edge |
| `text_en` | 44 | Bold (700) | `#E0E0E0` w/ 3px black outline | Below JP, 8px gap |
| Emphasis word | inherit size | inherit weight | `#FFD93D` (yellow accent) | inline |

Ratio JP:EN = 64:44 ≈ **1.45×**. This is the sweet spot for bilingual readability — JP visually dominates without making EN unreadable on a phone.

## Style variants

| `style` | When to use | Visual difference |
| --- | --- | --- |
| `primary` | Default talking-head dialogue | Spec above |
| `hook` | First 2–3 seconds | JP scaled to 76px, animated punch-in (scale 0.8 → 1.0 over 200ms) |
| `cta` | Last segment, "follow / LINE" lines | JP color → accent yellow, small arrow icon ↓ appended |
| `label` | On-screen labels (room names, prices, point numbers) | No EN, JP at 56px, positioned per `label_position` field if provided |

## Migration from v1

Old:
```json
{ "text": "外国人だから断られたわけじゃないです" }
```

New:
```json
{ "text_jp": "外国人だから断られたわけじゃないです",
  "text_en": "You weren't rejected for being foreign." }
```

The Remotion template (`references/remotion-template.md`) reads `text_jp || text` so both schemas work during transition.

## Whisper → edit_plan mapping

In Step 4, when generating `edit_plan.json` from the Whisper transcript:

1. Each Whisper segment becomes one edit_plan segment
2. `text_jp` ← Whisper's transcribed text
3. `text_en` ← machine translation via Claude or DeepL API call
4. Default `style: "primary"` for all
5. Manually re-tag the first segment as `style: "hook"` and the last as `style: "cta"` during review

## Authoring tips

- **Keep `text_jp` under 18 morae per segment.** Longer than that and the subtitle wraps to 3 lines, which crowds the face.
- **Keep `text_en` under 8 words per segment.** It's a comprehension aid, not a translation. Compress aggressively. "外国人だから断られたわけじゃないです" → "Not rejected for being foreign."
- **Don't translate idioms literally.** 「ぶっちゃけ」 → "Honestly," not "frankly speaking."
- **Use `emphasis` sparingly** — 1 word per 3–4 segments. Overuse kills the visual hierarchy.
