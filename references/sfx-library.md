# SFX Library

All SFX files are in `sfx/`. Default volume: 0.6. Override per-caption with `CAPTION_SFX_VOLUME`.

## Available Files

| Filename | Character | Best used for |
|----------|-----------|---------------|
| `シャキーン1.mp3` | Sharp metallic sting | Section headers, important announcements |
| `和太鼓でカカッ.mp3` | Taiko drum hit | Strong section openers (一つ目、二つ目…) |
| `呪いの旋律.mp3` | Eerie melody | Negative facts ("絶対戻ってきません") — use vol 0.28 |
| `金額表示.mp3` | Cash register | Money amounts (1〜2ヶ月分, fees) |
| `きらーん2.mp3` | Sparkle/shine | Positive tips, solutions, "狙いましょう" |
| `パパッ.mp3` | Quick pop | Fast reveals, company names |
| `ニュースタイトル表示3.mp3` | News jingle | Section reveals matching visual theme |
| `不安（ピアノ演奏）.mp3` | Anxious piano | Warnings, rejection scenarios |
| `ヒーローの決めポーズ.mp3` | Hero fanfare | Final tip, success outcome |
| `キラッ1.mp3` | Twinkle | Light positive moments |
| `キラッ2.mp3` | Twinkle alt | Alternate twinkle |
| `クイズ正解2.mp3` | Quiz correct | When revealing the right answer |
| `グサッ1.mp3` | Stab sound | Shocking facts |
| `スイッチを押す.mp3` | Button press | Transition between topics |
| `チーン2.mp3` | Bell ding | End of section, gentle conclusions |
| `パッ.mp3` | Flash pop | Quick single-word reveal |
| `パフ.mp3` | Puff | Light casual moments |
| `ペタッ.mp3` | Stamp | Sticking point, key rule |
| `ぷよん.mp3` | Boing | Cute/casual moments |
| `伸びる.mp3` | Stretching | Building suspense |
| `可愛く輝く1.mp3` | Cute sparkle | CTA, follow/LINE outro |
| `小鼓（こつづみ）.mp3` | Kotsuzumi drum | Traditional Japanese accent |
| `歓声と拍手.mp3` | Cheers | Final victory/solution |
| `鈴を鳴らす.mp3` | Bell shake | Topic transition |
| `ピアノの単音.mp3` | Piano note | Subtle accent |

## Volume Guidelines

- `呪いの旋律.mp3` → vol **0.28** (very loud by default)
- `歓声と拍手.mp3` → vol **0.4** (crowd is loud)
- All others → vol **0.6** (default)

## Mapping Pattern

Assign SFX to `highlight: true` captions only. Typical mapping pattern for a 3-point Japan real estate video:

```
Caption type         → Recommended SFX
Section header       → 和太鼓でカカッ
Negative fact        → 呪いの旋律 (vol 0.28)
Money amount         → 金額表示
Positive action tip  → きらーん2
Company/name reveal  → パパッ
Warning/rejection    → 不安（ピアノ演奏）
Final CTA            → ヒーローの決めポーズ
```
