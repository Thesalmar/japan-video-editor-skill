# Pipeline Steps — Detailed Reference

Full command reference for each of the 10 pipeline steps.

## Prerequisites

```bash
# Check all tools are available
ffmpeg -version
python3 -c "import whisper; print('whisper ok')"
node --version  # must be >= 18
```

## Step 1 — Convert source clips to MP4 (h264)

Run for every clip that isn't already h264/aac:

```bash
ffmpeg -i raw/INPUT.MOV \
  -c:v libx264 -crf 18 -preset fast \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  raw/INPUT.mp4
```

- CRF 18 = near-lossless quality
- `faststart` = web-optimised (playback starts before full download)
- Keep originals; output alongside them in `raw/`

## Step 2 — Transcribe with Whisper

```python
#!/usr/bin/env python3
import whisper, json
from pathlib import Path

model = whisper.load_model("small")
clips = sorted(Path("raw").glob("*.mp4"))

all_segments = []
offset = 0.0

for clip in clips:
    result = model.transcribe(
        str(clip),
        language="ja",
        word_timestamps=True,
        initial_prompt="日本の不動産、賃貸、礼金、敷金、保証会社、在留カード、仲介手数料"
    )
    for seg in result["segments"]:
        seg["source_file"] = str(clip)
        seg["start"] += offset
        seg["end"] += offset
        if seg.get("words"):
            for w in seg["words"]:
                w["start"] += offset
                w["end"] += offset
        all_segments.append(seg)
    # Get clip duration to advance offset
    import subprocess, re
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(clip)]
    ).decode().strip())
    offset += dur

Path("transcript.json").write_text(
    json.dumps(all_segments, ensure_ascii=False, indent=2)
)
print(f"Transcribed {len(clips)} clips, {len(all_segments)} segments")
```

**`initial_prompt` tip:** Add video-specific terms to improve recognition accuracy. For real estate videos always include: `礼金、敷金、保証会社、在留カード、仲介手数料`.

## Step 3 — Transcript quality check (delegate)

```
delegate_task(
    goal="Fix transcript.json for a Japanese real estate video",
    context="""
    Read transcript.json. For each segment text:
    1. Remove filler words: えーと、あのー、えっと、まあ、なんか (keep if meaningful)
    2. Fix duplicate phrases (stutters): "これは、これは" → "これは"
    3. Fix real estate kanji misreads:
       - 例金 → 礼金
       - 補償 → 保証 (in 保証会社 context)
       - 中介 → 仲介
       - 居住 → 在住 (in 在住外国人 context)
    4. Do NOT change meaning or rephrase sentences
    Write the fixed JSON back to transcript.json.
    """,
    toolsets=["file", "terminal"]
)
```

## Step 4 — Generate edit_plan.json (delegate)

```
delegate_task(
    goal="Create edit_plan.json for a Japanese real estate short video",
    context="""
    Read transcript.json.
    
    RULES:
    - Target duration: 60–90s (at 1.3x speed)
    - Select the BEST takes — cut dead air, hesitations, and off-topic tangents
    - Output resolution: 1080x1920 (9:16 vertical)
    - FPS: 30
    - Playback speed: 1.3x (applied to segments only, not BGM/SFX)
    - Captions: ≤15 Japanese chars per caption
    - Highlight ~35% of captions (numbers, section headers, key action phrases)
    - Include 2–3 broll_slots at topic transitions
    - Map SFX to highlighted captions (see sfx/ folder for available files)
    - BGM volume: 0.10
    - Title banner: use 【hook word】 format

    Output: write edit_plan.json to project root
    Schema: see references/edit-plan-schema.md
    """,
    toolsets=["file"]
)
```

## Step 5 — Generate VideoEdit.tsx (delegate)

```
delegate_task(
    goal="Generate src/VideoEdit.tsx from edit_plan.json",
    context="""
    Read edit_plan.json.
    Write src/VideoEdit.tsx using the Remotion template.
    
    REQUIRED customisations:
    1. ENGLISH map: translate every caption.text to English (keyed by caption id)
    2. CAPTION_SFX: map each highlighted caption id to an sfx filename
    3. BROLL_SLOTS: array from edit_plan.broll_slots with startSeconds and src
    4. CAPTION_SFX_VOLUME: override vol 0.28 for 呪いの旋律.mp3
    5. QR code src: set to staticFile("qr.png") if qr.png exists in public/
    
    Template is at references/remotion-template.md
    """,
    toolsets=["file"]
)
```

## Step 6 — Cut segments and wire public/ symlinks

```bash
# 1. Create symlinks in public/
cd <project-dir>
mkdir -p public
ln -sf "$(pwd)/segments" public/segments
ln -sf "$(pwd)/bgm"      public/bgm
ln -sf "$(pwd)/broll"    public/broll
ln -sf "$(pwd)/sfx"      public/sfx

# 2. Cut each segment from edit_plan.json keep_segments[]
# Example for segment id=0:
ffmpeg -ss 8.9 -to 11.92 -i raw/IMG_6856.mp4 \
  -c:v libx264 -crf 18 -preset fast \
  -c:a aac -b:a 128k \
  -af "afade=t=in:d=0.05,afade=t=out:d=0.05" \
  segments/seg_00.mp4
```

Automate with Python:

```python
import json, subprocess
from pathlib import Path

plan = json.loads(Path("edit_plan.json").read_text())
Path("segments").mkdir(exist_ok=True)

for seg in plan["keep_segments"]:
    out = f"segments/seg_{seg['id']:02d}.mp4"
    if Path(out).exists():
        continue
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(seg["source_start"]),
        "-to", str(seg["source_end"]),
        "-i", seg["source_file"],
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "aac", "-b:a", "128k",
        "-af", "afade=t=in:d=0.05,afade=t=out:d=0.05",
        out
    ], check=True)
    print(f"Cut: {out}")
```

## Step 7 — Remotion Studio preview

```bash
npm start
# → opens http://localhost:3000
# → composition: JapanVideoEdit
```

Scrub through the full timeline. Check:
- All segments play (no black frames)
- Captions appear at correct time
- BGM fades in and out smoothly
- SFX fires on highlighted captions
- Title banner appears for ~7s

## Step 8 — Quality verification

Run each check from `references/quality-checks.md` in sequence.
Stop and fix on any failure. Re-run failed checks after fixing.
Maximum 3 full iterations.

## Step 9 — Export

```bash
npx remotion render src/index.ts JapanVideoEdit output/final_v1.mp4 \
  --codec=h264 \
  --crf=18 \
  --overwrite
```

Output: `output/final_v1.mp4`

For subsequent versions:

```bash
npx remotion render src/index.ts JapanVideoEdit output/final_v2.mp4 \
  --codec=h264 --crf=18 --overwrite
```

## Step 10 — CapCut (optional)

Import `output/final_v1.mp4` into **CapCut Desktop**.

Common post-processing:
- Sticker overlays on key captions
- Speed ramp at the hook moment
- Final audio normalise (CapCut's auto-normalise)
- Platform-specific crop/resize if needed
