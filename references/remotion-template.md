# Remotion VideoEdit.tsx — Generic Template

Use this as the base for `src/VideoEdit.tsx`. Fill in the `TODO` sections from `edit_plan.json`.

```tsx
import React from "react";
import {
  AbsoluteFill,
  Audio,
  Composition,
  Sequence,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import editPlan from "../edit_plan.json";

const FPS = 30;
const SPEED = 1.3; // segments play at 1.3× speed; BGM and SFX stay at 1×

// ── TODO: Fill in English subtitle translations keyed by caption id ──────────
const ENGLISH: Record<number, string> = {
  // 0: "When foreigners rent an apartment",
  // 1: "Things real estate agents won't tell you",
  // ...
};

// ── TODO: Map highlighted caption ids to SFX files ───────────────────────────
const CAPTION_SFX: Record<number, string> = {
  // 1: "sfx/シャキーン1.mp3",
  // 3: "sfx/和太鼓でカカッ.mp3",
  // ...
};

// TODO: Override volume for loud SFX (default is 0.6)
const CAPTION_SFX_VOLUME: Record<number, number> = {
  // 7: 0.28, // 呪いの旋律 is very loud
};

// ── TODO: Fill in B-roll slots from edit_plan.broll_slots ────────────────────
const BROLL_SLOTS: Array<{ startSeconds: number; durationSeconds: number; src: string }> = [
  // { startSeconds: 52.84, durationSeconds: 5, src: staticFile("broll/MY_BROLL.mp4") },
];

// ────────────────────────────────────────────────────────────────────────────

const Caption: React.FC<{
  text: string;
  englishText: string;
  highlight: boolean;
  durationInFrames: number;
}> = ({ text, englishText, highlight, durationInFrames }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [0, 3, durationInFrames - 3, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.ease }
  );

  return (
    <div
      style={{
        position: "absolute",
        bottom: "18%",
        left: "5%",
        right: "5%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 6,
        opacity,
        zIndex: 20,
      }}
    >
      {/* Japanese caption */}
      <div
        style={{
          background: "rgba(0,0,0,0.65)",
          borderRadius: 10,
          padding: "10px 22px",
          maxWidth: "90%",
          textAlign: "center",
        }}
      >
        <span
          style={{
            fontFamily: "Meiryo, メイリオ, 'Yu Gothic', sans-serif",
            fontSize: 44,
            fontWeight: 700,
            color: highlight ? "#FF3B3B" : "#FFFFFF",
            textShadow: "2px 2px 5px rgba(0,0,0,0.8)",
            lineHeight: 1.3,
            whiteSpace: "nowrap",
          }}
        >
          {text}
        </span>
      </div>

      {/* English subtitle */}
      {englishText ? (
        <div
          style={{
            background: "rgba(0,0,0,0.50)",
            borderRadius: 8,
            padding: "5px 16px",
            maxWidth: "92%",
            textAlign: "center",
          }}
        >
          <span
            style={{
              fontFamily: "Arial, Helvetica, sans-serif",
              fontSize: 26,
              fontWeight: 600,
              color: "#E0E0E0",
              textShadow: "1px 1px 4px rgba(0,0,0,0.9)",
              lineHeight: 1.3,
              whiteSpace: "nowrap",
            }}
          >
            {englishText}
          </span>
        </div>
      ) : null}
    </div>
  );
};

// ── Title overlay — punch-in animated pill, 7 seconds ────────────────────────
const TITLE_DURATION_FRAMES = 7 * FPS;
const TITLE_FADE_FRAMES = 20;

const TitleOverlay: React.FC = () => {
  const frame = useCurrentFrame();

  const scale = interpolate(
    frame, [0, 14, 22, 28], [0.65, 1.10, 0.95, 1.0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const translateY = interpolate(
    frame, [0, 14], [50, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }
  );
  const opacity = interpolate(
    frame,
    [0, 6, TITLE_DURATION_FRAMES - TITLE_FADE_FRAMES, TITLE_DURATION_FRAMES],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.ease }
  );
  const glowOpacity = interpolate(
    frame, [0, 14, 50], [0, 1, 0.3],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <Sequence from={0} durationInFrames={TITLE_DURATION_FRAMES}>
      <Audio src={staticFile("sfx/ニュースタイトル表示3.mp3")} volume={0.75} />
      <div
        style={{
          position: "absolute",
          top: "59%",
          left: "4%",
          right: "4%",
          display: "flex",
          justifyContent: "center",
          opacity,
          zIndex: 15,
          transform: `translateY(${translateY}px) scale(${scale})`,
        }}
      >
        <div
          style={{
            background: "linear-gradient(135deg, #0a1540 0%, #1a2e82 100%)",
            borderRadius: 16,
            padding: "16px 26px",
            maxWidth: "96%",
            textAlign: "center",
            border: `2px solid rgba(255, 215, 0, ${glowOpacity})`,
            boxShadow: `0 0 ${28 * glowOpacity}px rgba(255,215,0,${0.5 * glowOpacity}), 0 4px 16px rgba(0,0,0,0.7)`,
            position: "relative",
          }}
        >
          <div style={{
            position: "absolute", top: 0, left: "10%", right: "10%", height: 3,
            background: `rgba(255, 215, 0, ${glowOpacity})`,
            borderRadius: "0 0 4px 4px",
          }} />
          <span
            style={{
              fontFamily: "Meiryo, メイリオ, 'Yu Gothic', sans-serif",
              fontSize: 32,
              fontWeight: 700,
              color: "#FFFFFF",
              textShadow: `0 0 16px rgba(255,215,0,${0.7 * glowOpacity}), 1px 1px 4px rgba(0,0,0,0.9)`,
              lineHeight: 1.5,
              display: "block",
              whiteSpace: "pre-wrap",
              wordBreak: "break-all",
              letterSpacing: "0.02em",
            }}
          >
            {editPlan.title_banner.text}
          </span>
        </div>
      </div>
    </Sequence>
  );
};

// ── B-roll overlay — fades in/out over source footage (muted) ─────────────────
const BROLL_FADE = 8;

const BRollOverlay: React.FC<{ src: string; durationFrames: number }> = ({ src, durationFrames }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [0, BROLL_FADE, durationFrames - BROLL_FADE, durationFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.ease }
  );
  return (
    <AbsoluteFill style={{ opacity }}>
      <OffthreadVideo
        src={src}
        muted
        playbackRate={SPEED}
        style={{ width: "100%", height: "100%", objectFit: "cover" }}
      />
    </AbsoluteFill>
  );
};

// ── QR code overlay — shown during the last segment ──────────────────────────
const QROverlay: React.FC<{ durationFrames: number }> = ({ durationFrames }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [0, 8, durationFrames - 6, durationFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.ease }
  );
  return (
    <AbsoluteFill
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        opacity,
        zIndex: 25,
        paddingBottom: "32%",
      }}
    >
      <div
        style={{
          background: "rgba(255,255,255,0.93)",
          borderRadius: 20,
          padding: 20,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 10,
          boxShadow: "0 6px 32px rgba(0,0,0,0.5)",
        }}
      >
        <span style={{
          fontFamily: "Meiryo, メイリオ, 'Yu Gothic', sans-serif",
          fontSize: 28,
          fontWeight: 700,
          color: "#06C755",
          letterSpacing: "0.04em",
        }}>
          LINEでフォロー ↓
        </span>
        <img src={staticFile("qr.png")} style={{ width: 320, height: 320, display: "block" }} />
      </div>
    </AbsoluteFill>
  );
};

// ── Total duration ────────────────────────────────────────────────────────────
const totalFrames = Math.ceil(editPlan.total_duration_seconds / SPEED * FPS);

// ── Main composition ──────────────────────────────────────────────────────────
const JapanVideoEdit: React.FC = () => {
  const { width, height } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: "#000" }}>

      {/* Video segments */}
      {editPlan.keep_segments.map((seg) => {
        const startFrame     = Math.round(seg.output_start / SPEED * FPS);
        const durationFrames = Math.round((seg.output_end - seg.output_start) / SPEED * FPS);
        return (
          <Sequence key={seg.id} from={startFrame} durationInFrames={durationFrames}>
            <AbsoluteFill>
              <OffthreadVideo
                src={staticFile(`segments/seg_${String(seg.id).padStart(2, "0")}.mp4`)}
                playbackRate={SPEED}
                style={{ width, height, objectFit: "cover" }}
              />
            </AbsoluteFill>
          </Sequence>
        );
      })}

      {/* B-roll overlays */}
      {BROLL_SLOTS.map((slot, i) => {
        const startFrame     = Math.round(slot.startSeconds / SPEED * FPS);
        const durationFrames = Math.round(slot.durationSeconds / SPEED * FPS);
        return (
          <Sequence key={`broll-${i}`} from={startFrame} durationInFrames={durationFrames}>
            <BRollOverlay src={slot.src} durationFrames={durationFrames} />
          </Sequence>
        );
      })}

      {/* BGM */}
      <Audio
        src={staticFile(editPlan.bgm.source)}
        volume={(frame) => {
          const fadeInEnd = editPlan.bgm.fade_in_frames;
          const fadeOutStart = totalFrames - editPlan.bgm.fade_out_frames;
          if (frame < fadeInEnd)
            return interpolate(frame, [0, fadeInEnd], [0, editPlan.bgm.volume]);
          if (frame > fadeOutStart)
            return interpolate(frame, [fadeOutStart, totalFrames], [editPlan.bgm.volume, 0]);
          return editPlan.bgm.volume;
        }}
      />

      {/* Captions + English subtitles + SFX */}
      {editPlan.captions.map((cap) => {
        const startFrame     = Math.round(cap.start / SPEED * FPS);
        const durationFrames = Math.max(1, Math.round((cap.end - cap.start) / SPEED * FPS));
        const sfxFile   = CAPTION_SFX[cap.id];
        const sfxVolume = CAPTION_SFX_VOLUME[cap.id] ?? 0.6;
        return (
          <Sequence key={cap.id} from={startFrame} durationInFrames={durationFrames}>
            <Caption
              text={cap.text}
              englishText={ENGLISH[cap.id] ?? ""}
              highlight={cap.highlight}
              durationInFrames={durationFrames}
            />
            {cap.highlight && sfxFile && (
              <Sequence from={Math.floor(durationFrames / 2)}>
                <Audio src={staticFile(sfxFile)} volume={sfxVolume} />
              </Sequence>
            )}
          </Sequence>
        );
      })}

      {/* QR code on last segment */}
      {(() => {
        const lastSeg = editPlan.keep_segments[editPlan.keep_segments.length - 1];
        const startFrame     = Math.round(lastSeg.output_start / SPEED * FPS);
        const durationFrames = Math.round((lastSeg.output_end - lastSeg.output_start) / SPEED * FPS);
        return (
          <Sequence from={startFrame} durationInFrames={durationFrames}>
            <QROverlay durationFrames={durationFrames} />
          </Sequence>
        );
      })()}

      {/* Title overlay */}
      <TitleOverlay />

    </AbsoluteFill>
  );
};

// ── Root export ───────────────────────────────────────────────────────────────
export const VideoEdit: React.FC = () => (
  <>
    <Composition
      id="JapanVideoEdit"
      component={JapanVideoEdit}
      durationInFrames={totalFrames}
      fps={FPS}
      width={1080}
      height={1920}
    />
  </>
);
```

## Customisation Checklist

After generating `VideoEdit.tsx`, verify:

- [ ] `ENGLISH` map has a translation for every caption id in `edit_plan.json`
- [ ] `CAPTION_SFX` covers all `highlight: true` caption ids
- [ ] `BROLL_SLOTS` matches `edit_plan.broll_slots` with actual file paths
- [ ] `CAPTION_SFX_VOLUME[id] = 0.28` set for `呪いの旋律.mp3`
- [ ] `qr.png` exists in `public/` if `QROverlay` is enabled
- [ ] `public/sfx/ニュースタイトル表示3.mp3` exists (used by TitleOverlay)
