// src/components/DualSubtitle.tsx
//
// Renders bilingual JP/EN subtitles with the size hierarchy from
// references/dual-subtitle-schema.md. JP is visually dominant (1.45× EN size),
// EN sits below as a comprehension aid for the bilingual audience.
//
// Drop into the Remotion project and replace the old <Subtitle /> component
// in VideoEdit.tsx. Backward compatible with v1 segments via the `text` fallback.

import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

export type SubtitleStyle = 'primary' | 'hook' | 'cta' | 'label';

export interface SubtitleSegment {
  id: string;
  start: number;
  end: number;
  text_jp?: string;
  text?: string; // v1 fallback
  text_en?: string;
  style?: SubtitleStyle;
  emphasis?: string[];
  label_position?: 'top' | 'center' | 'bottom';
}

interface Props {
  segment: SubtitleSegment;
}

const STYLE_PRESETS: Record<SubtitleStyle, {
  jpSize: number;
  enSize: number;
  jpColor: string;
  enColor: string;
  showEn: boolean;
  bottomOffset: number;
}> = {
  primary: {jpSize: 64, enSize: 44, jpColor: '#FFFFFF', enColor: '#E0E0E0', showEn: true, bottomOffset: 280},
  hook: {jpSize: 76, enSize: 48, jpColor: '#FFFFFF', enColor: '#E0E0E0', showEn: true, bottomOffset: 320},
  cta: {jpSize: 64, enSize: 44, jpColor: '#FFD93D', enColor: '#FFFFFF', showEn: true, bottomOffset: 280},
  label: {jpSize: 56, enSize: 0, jpColor: '#FFFFFF', enColor: '#FFFFFF', showEn: false, bottomOffset: 280},
};

const ACCENT_COLOR = '#FFD93D';

function renderWithEmphasis(text: string, emphasis: string[] | undefined, color: string) {
  if (!emphasis || emphasis.length === 0) {
    return <span style={{color}}>{text}</span>;
  }
  // Split on emphasis substrings and recolor matches
  const pattern = new RegExp(`(${emphasis.map((e) => e.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})`, 'g');
  const parts = text.split(pattern);
  return (
    <>
      {parts.map((part, i) =>
        emphasis.includes(part) ? (
          <span key={i} style={{color: ACCENT_COLOR}}>{part}</span>
        ) : (
          <span key={i} style={{color}}>{part}</span>
        )
      )}
    </>
  );
}

export const DualSubtitle: React.FC<Props> = ({segment}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const startFrame = segment.start * fps;
  const endFrame = segment.end * fps;
  if (frame < startFrame || frame > endFrame) return null;

  const localFrame = frame - startFrame;
  const style = segment.style ?? 'primary';
  const preset = STYLE_PRESETS[style];

  const jpText = segment.text_jp ?? segment.text ?? '';
  const enText = segment.text_en ?? '';

  // Hook style: punch-in animation 0.8 → 1.0 over 200ms (≈6 frames at 30fps)
  const punchScale = style === 'hook'
    ? interpolate(localFrame, [0, fps * 0.2], [0.8, 1.0], {extrapolateRight: 'clamp'})
    : 1.0;

  const baseTextStyle: React.CSSProperties = {
    fontFamily: '"Noto Sans JP", sans-serif',
    fontWeight: 900,
    textAlign: 'center',
    textShadow: '0 0 4px #000, 0 0 4px #000, 0 0 4px #000, 0 0 4px #000',
    lineHeight: 1.2,
    margin: 0,
  };

  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: preset.bottomOffset}}>
      <div style={{transform: `scale(${punchScale})`, transformOrigin: 'bottom center'}}>
        <p style={{...baseTextStyle, fontSize: preset.jpSize}}>
          {renderWithEmphasis(jpText, segment.emphasis, preset.jpColor)}
          {style === 'cta' && <span style={{color: preset.jpColor}}> ↓</span>}
        </p>
        {preset.showEn && enText && (
          <p style={{
            ...baseTextStyle,
            fontSize: preset.enSize,
            fontWeight: 700,
            marginTop: 8,
            color: preset.enColor,
          }}>
            {enText}
          </p>
        )}
      </div>
    </AbsoluteFill>
  );
};
