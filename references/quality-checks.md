# Quality Verification Checks

Run after Remotion Studio preview (Step 8). Maximum 3 fix iterations before escalating to user.

## Check 1 — No black frames

**Pass:** No continuous black frame sequence > 0.5s  
**Fail:** Black segment detected

```bash
ffprobe -f lavfi -i "movie=output/final_v1.mp4,blackdetect=d=0.5:pix_th=.10" \
  -show_entries tags=lavfi.black_start,lavfi.black_end -of csv 2>&1 | grep black
```

**Fix:** Identify the timestamp, check which segment is blank, confirm `public/segments/seg_NN.mp4` exists and is not corrupt.

## Check 2 — No audio pops or clipping

**Pass:** Peak audio level ≤ −1 dBFS  
**Fail:** Clipping detected

```bash
ffmpeg -i output/final_v1.mp4 -af "volumedetect" -f null /dev/null 2>&1 | grep max_volume
```

**Fix:** Add fade to offending segment in Step 6 ffmpeg command:
```bash
-af "afade=t=in:d=0.05,afade=t=out:d=0.05"
```

## Check 3 — Caption sync

**Pass:** All captions start within 0.3s of corresponding transcript word  
**Fail:** Caption appears before or after speech by >0.3s

**How to check:** Scrub Remotion Studio at each highlighted caption. Compare `caption.start` in `edit_plan.json` with `transcript.json` word timestamps.

**Fix:** Adjust `start`/`end` in `edit_plan.json` captions and re-generate `VideoEdit.tsx`.

## Check 4 — Resolution

**Pass:** Exactly 1080 × 1920  
**Fail:** Any other resolution

```bash
ffprobe -v quiet -select_streams v:0 \
  -show_entries stream=width,height \
  -of csv=p=0 output/final_v1.mp4
```

**Fix:** Re-render with explicit `--width 1080 --height 1920` flags.

## Check 5 — Audio levels

**Pass:**
- BGM integrated loudness: −18 to −12 LUFS
- Voice/narration peak: −6 to −3 dBFS

```bash
ffmpeg -i output/final_v1.mp4 -af loudnorm=print_format=json -f null /dev/null 2>&1
```

**Fix:** Adjust `bgm.volume` in `edit_plan.json` (lower = quieter). Typical value: 0.08–0.12.

## Check 6 — Caption positioning

**Pass:** All captions at bottom 18% of frame, no overlap with speaker's face  
**Fail:** Caption covers face or is outside the safe zone

**How to check:** In Remotion Studio, scrub to segments where speaker moves.

**Fix:** Adjust `bottom` percentage in the Caption component in `VideoEdit.tsx` (default 18%). Never go below 10% (cuts into letterbox on some platforms).

## Check 7 — Total duration

**Pass:** Total duration ≤ 90s (Reels hard limit is 90s for full reach)  
**Fail:** Duration > 90s

```bash
ffprobe -v quiet -show_entries format=duration \
  -of default=noprint_wrappers=1 output/final_v1.mp4
```

**Fix:** Trim the longest `keep_segment` entries in `edit_plan.json`, re-cut that segment, and re-render.

## Check 8 — Silence-cut sanity

**Pass:** Cut output duration is 60%–90% of source duration  
**Fail:** < 60% (too aggressive, likely clipping speech) or > 90% (threshold too lax)

```bash
# Compare durations of raw and cut clips
ffprobe -v quiet -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 raw/INPUT.mp4
ffprobe -v quiet -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 segments/INPUT_cut.mp4
```

**Fix:** Re-run `scripts/silence_cut.py` with adjusted `--threshold` (higher = less aggressive). See `references/silence-cut.md`.

## Check 9 — Subtitle size hierarchy

**Pass:** JP subtitle font-size ≥ 1.4× EN subtitle font-size at every frame where both are visible  
**Fail:** EN rendered at equal or larger size than JP

**How to check:** In Remotion Studio, pause on any frame with bilingual subtitles. JP must visually dominate.

**Fix:** Verify the `style` field in `edit_plan.json` segments. `label` segments must omit `text_en`. Check `DualSubtitle.tsx` STYLE_PRESETS — default ratio is 64:44 = 1.45×.

## Verification Summary Table

| # | Check | Tool | Pass Criterion |
|---|-------|------|----------------|
| 1 | Black frames | ffprobe blackdetect | No sequence > 0.5s |
| 2 | Audio clipping | ffmpeg volumedetect | Peak ≤ −1 dBFS |
| 3 | Caption sync | Manual + edit_plan | Within 0.3s of speech |
| 4 | Resolution | ffprobe | Exactly 1080×1920 |
| 5 | Audio levels | ffmpeg loudnorm | BGM −18 to −12 LUFS |
| 6 | Caption position | Remotion Studio | Bottom 18%, no face overlap |
| 7 | Duration | ffprobe | ≤ 90.0 seconds |
| 8 | Silence-cut ratio | ffprobe | 60%–90% of source duration |
| 9 | Subtitle hierarchy | Remotion Studio | JP size ≥ 1.4× EN size |
