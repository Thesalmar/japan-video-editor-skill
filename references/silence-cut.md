# Step 1.5 — Silence Auto-Cut

Inserts between Step 1 (source conversion) and Step 2 (Whisper transcription).

## Why this exists

Modern Reels/TikTok pacing demands a cut every 2–4 seconds. Talking-head footage with natural breathing pauses feels too slow on platform. Manually jump-cutting in CapCut burns ~30 minutes per minute of footage. This step automates ~80% of that work so the editor only fine-tunes.

## What it does

Scans the source clip with `ffmpeg silencedetect`, removes pauses longer than `--min-silence` (default 0.4s), keeps `--pad` of headroom (default 0.08s) around each speech region so words aren't clipped. Output is a re-encoded mp4 ready for Whisper.

## Usage

```bash
# Default settings — works for ~80% of clips
python scripts/silence_cut.py raw/take1.mp4 segments/take1_cut.mp4

# With a cut log for debugging or later remapping
python scripts/silence_cut.py raw/take1.mp4 segments/take1_cut.mp4 \
    --log segments/take1_cuts.json

# Aggressive — for high-energy content
python scripts/silence_cut.py raw/take1.mp4 segments/take1_cut.mp4 \
    --min-silence 0.25 --pad 0.05

# Conservative — for educational / authoritative tone
python scripts/silence_cut.py raw/take1.mp4 segments/take1_cut.mp4 \
    --min-silence 0.6 --pad 0.12
```

## Tuning by environment

| Recording setup | `--threshold` | Notes |
| --- | --- | --- |
| Quiet apartment, lapel mic | -35 | Default -30 may leave breath sounds |
| Quiet apartment, iPhone mic | -30 | Default works |
| Cafe / outdoor | -25 | Higher floor noise; aggressive cuts will clip speech |
| Echo-y room | -28 | Plus increase `--pad` to 0.12 to keep tails |

## Pipeline integration

In `SKILL.md`, insert after Step 1:

```
| 1.5 | Silence auto-cut on `raw/*.mp4` → `segments/*_cut.mp4` |
```

In the Hermes invocation, the agent should:
1. Run `silence_cut.py` on each raw clip in `raw/`
2. Write cut output to `segments/<basename>_cut.mp4`
3. Pass the cut files to Whisper in Step 2 (not the originals)

## Failure modes & checks

- **Output has audible word-clipping at edits:** increase `--pad` to 0.12 or 0.15.
- **Output still feels slow:** lower `--min-silence` to 0.3 or 0.25.
- **Output sounds chopped / unnatural:** the threshold is too sensitive; raise `--threshold` from -30 to -25.
- **Whisper transcription breaks word boundaries afterward:** that's expected; Whisper will retime everything against the cut output. The original timestamps don't carry over.

## Performance

~3 seconds of compute per minute of input footage on M-series Mac.
