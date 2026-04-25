#!/usr/bin/env python3
"""
silence_cut.py — Remove silent pauses from raw talking-head footage.

Runs as Step 1.5 in the pipeline (between source conversion and Whisper transcription).
Uses ffmpeg silencedetect to find gaps, then re-encodes keeping only the speech segments.

Why: Reels/TikTok retention demands jump-cut pacing. Manual jump-cutting in CapCut takes
30+ minutes per video. This automates it for ~3 seconds of compute per minute of footage.

Usage:
    python silence_cut.py raw/input.mp4 segments/input_cut.mp4
    python silence_cut.py raw/input.mp4 segments/input_cut.mp4 --threshold -30 --min-silence 0.4 --pad 0.08

Tunable parameters:
    --threshold     dB level below which audio is considered silent. Default -30dB.
                    Quieter rooms: try -35. Noisier rooms: try -25.
    --min-silence   Minimum silence duration in seconds to cut. Default 0.4.
                    Lower = more aggressive cuts (energetic feel).
                    Higher = preserves natural breathing pauses.
    --pad           Padding kept around speech segments in seconds. Default 0.08.
                    Prevents cutting off the very start/end of words.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def detect_silence(input_path: Path, threshold_db: int, min_silence: float) -> list[tuple[float, float]]:
    """Run ffmpeg silencedetect and return list of (silence_start, silence_end) tuples."""
    cmd = [
        "ffmpeg", "-i", str(input_path),
        "-af", f"silencedetect=noise={threshold_db}dB:d={min_silence}",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    stderr = result.stderr

    # ffmpeg writes silencedetect output to stderr
    silences = []
    current_start = None
    for line in stderr.splitlines():
        m = re.search(r"silence_start:\s*([\d.]+)", line)
        if m:
            current_start = float(m.group(1))
            continue
        m = re.search(r"silence_end:\s*([\d.]+)", line)
        if m and current_start is not None:
            silences.append((current_start, float(m.group(1))))
            current_start = None
    return silences


def get_duration(input_path: Path) -> float:
    """Return media duration in seconds."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(input_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def silences_to_keep_segments(
    silences: list[tuple[float, float]],
    total_duration: float,
    pad: float
) -> list[tuple[float, float]]:
    """Convert silence intervals to speech-keep intervals, applying padding."""
    keep = []
    cursor = 0.0
    for s_start, s_end in silences:
        seg_end = max(cursor, s_start + pad)
        seg_start = max(cursor, cursor - 0)  # cursor is always the prior keep-end
        if seg_end > seg_start:
            keep.append((seg_start, seg_end))
        cursor = max(cursor, s_end - pad)
    # final tail
    if cursor < total_duration:
        keep.append((cursor, total_duration))
    # filter zero/negative-length segments
    return [(a, b) for a, b in keep if b - a > 0.05]


def build_filter_complex(segments: list[tuple[float, float]]) -> str:
    """Build a ffmpeg filter_complex string that selects and concatenates the keep segments."""
    parts = []
    for i, (start, end) in enumerate(segments):
        parts.append(f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{i}];")
        parts.append(f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{i}];")
    concat_inputs = "".join(f"[v{i}][a{i}]" for i in range(len(segments)))
    parts.append(f"{concat_inputs}concat=n={len(segments)}:v=1:a=1[outv][outa]")
    return "".join(parts)


def write_cut_log(log_path: Path, silences, segments, total_duration, kept_duration):
    """Persist the cut decisions for later inspection / Whisper-timestamp remapping."""
    log = {
        "source_duration_sec": round(total_duration, 3),
        "kept_duration_sec": round(kept_duration, 3),
        "removed_sec": round(total_duration - kept_duration, 3),
        "compression_ratio": round(kept_duration / total_duration, 3) if total_duration else 0,
        "silences_removed": [
            {"start": round(s, 3), "end": round(e, 3), "duration": round(e - s, 3)}
            for s, e in silences
        ],
        "kept_segments": [
            {"start": round(s, 3), "end": round(e, 3)} for s, e in segments
        ],
    }
    log_path.write_text(json.dumps(log, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--threshold", type=int, default=-30, help="Silence threshold in dB (default: -30)")
    ap.add_argument("--min-silence", type=float, default=0.4, help="Min silence to cut, seconds (default: 0.4)")
    ap.add_argument("--pad", type=float, default=0.08, help="Padding around speech, seconds (default: 0.08)")
    ap.add_argument("--log", type=Path, help="Optional path to write cut decisions JSON")
    args = ap.parse_args()

    if not args.input.exists():
        sys.exit(f"Input not found: {args.input}")

    print(f"[silence_cut] Analyzing {args.input.name} (threshold={args.threshold}dB, min_silence={args.min_silence}s)")
    total_duration = get_duration(args.input)
    silences = detect_silence(args.input, args.threshold, args.min_silence)
    print(f"[silence_cut] Found {len(silences)} silent regions")

    if not silences:
        print("[silence_cut] No silences detected; copying source unchanged.")
        subprocess.run(["cp", str(args.input), str(args.output)], check=True)
        return

    segments = silences_to_keep_segments(silences, total_duration, args.pad)
    kept_duration = sum(e - s for s, e in segments)
    print(f"[silence_cut] Keeping {len(segments)} segments — {kept_duration:.1f}s of {total_duration:.1f}s "
          f"({100*kept_duration/total_duration:.0f}%)")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    filter_complex = build_filter_complex(segments)
    cmd = [
        "ffmpeg", "-y", "-i", str(args.input),
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(args.output)
    ]
    subprocess.run(cmd, check=True)
    print(f"[silence_cut] Wrote {args.output}")

    if args.log:
        write_cut_log(args.log, silences, segments, total_duration, kept_duration)
        print(f"[silence_cut] Cut log: {args.log}")


if __name__ == "__main__":
    main()
