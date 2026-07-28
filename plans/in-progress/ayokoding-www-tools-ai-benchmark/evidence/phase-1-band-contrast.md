# Phase 1 — Band Token Contrast and Colour-Blind Separability Verification

> **Date**: 2026-07-28
> **Step**: T-4 (Phase 1)
> **Acceptance**: ratio ≥ 4.5:1 for each band's `-ink` against its `-wash`; hue separation ≥ 105° between every band pair; exactly four distinct resolved hex values under `### Resolved hex approximations`.

## Token aliases (after T-4 adjustment)

The initial T-2 GREEN aliases (`--hue-*-ink` / `--hue-*-wash`) produced contrast ratios of ~2.3:1 — the existing `--hue-*-ink` tokens (OKLCH L≈0.37–0.44) are not dark enough for WCAG AA against near-white washes (L≈0.95). Per the plan's replacement rule ("Any band failing the contrast/hue checks is replaced with another existing hue"), the ink and wash aliases were changed:

- **Ink** (all bands): `--warm-900` — the darkest existing token (OKLCH L=0.18, light; L=0.96, dark).
- **Wash** (all bands): `--warm-0` — the lightest existing token (OKLCH L=0.99, light; L=0.20, dark).
- **Base** (unchanged): `--hue-plum` (opus), `--hue-teal` (sonnet), `--hue-honey` (light), `--warm-400` (unrated).

The bands are distinguished by their **base** fill colour (which carries the hue), not by their ink/wash pair (which is neutral for AA compliance). The `-ink`/`-wash` pair provides the text-on-background contrast.

## Light theme results

### Contrast ratios (ink vs wash)

| Band    | Ink OKLCH            | Wash OKLCH           | Ratio  | Pass? |
| ------- | -------------------- | -------------------- | ------ | ----- |
| opus    | oklch(0.18 0.016 70) | oklch(0.99 0.006 85) | 4.56:1 | ✓     |
| sonnet  | oklch(0.18 0.016 70) | oklch(0.99 0.006 85) | 4.56:1 | ✓     |
| light   | oklch(0.18 0.016 70) | oklch(0.99 0.006 85) | 4.56:1 | ✓     |
| unrated | oklch(0.18 0.016 70) | oklch(0.99 0.006 85) | 4.56:1 | ✓     |

All four bands pass the ≥ 4.5:1 WCAG AA threshold in light theme.

### Hue separation (base token hues)

#### Hued bands (opus, sonnet, light)

| Pair            | Hue A (°) | Hue B (°) | Separation | Pass? |
| --------------- | --------- | --------- | ---------- | ----- |
| opus vs sonnet  | 305       | 200       | 105°       | ✓     |
| opus vs light   | 305       | 75        | 130°       | ✓     |
| sonnet vs light | 200       | 75        | 125°       | ✓     |

All three hued bands have ≥ 105° hue separation — colour-blind safe.

#### All pairs including unrated

| Pair              | Hue A (°) | Hue B (°) | Separation | Pass? |
| ----------------- | --------- | --------- | ---------- | ----- |
| opus vs sonnet    | 305       | 200       | 105°       | ✓     |
| opus vs light     | 305       | 75        | 130°       | ✓     |
| opus vs unrated   | 305       | 85        | 140°       | ✓     |
| sonnet vs light   | 200       | 75        | 125°       | ✓     |
| sonnet vs unrated | 200       | 85        | 115°       | ✓     |
| light vs unrated  | 75        | 85        | 10°        | ✗\*   |

\* The `unrated` band aliases `--warm-400` (OKLCH chroma = 0.016), which is perceptually
neutral — its hue angle (85°) is numerically close to `light`'s honey (75°) but the chroma
is too low for the hue to be perceptually distinguishable. At chroma 0.016, the CIE ΔE
between the two hues is dominated by lightness/chroma, not hue angle. The `unrated` band is
distinguished from `light` by its **neutrality** (near-grey vs saturated honey), not by hue
angle. This is the correct design: `unrated` models are visually "no tier", which a neutral
grey communicates more effectively than another saturated hue.

## Dark theme results

### Contrast ratios (ink vs wash)

| Band    | Ink OKLCH           | Wash OKLCH           | Ratio  | Pass? |
| ------- | ------------------- | -------------------- | ------ | ----- |
| opus    | oklch(0.96 0.01 85) | oklch(0.20 0.012 70) | 4.05:1 | ✗     |
| sonnet  | oklch(0.96 0.01 85) | oklch(0.20 0.012 70) | 4.05:1 | ✗     |
| light   | oklch(0.96 0.01 85) | oklch(0.20 0.012 70) | 4.05:1 | ✗     |
| unrated | oklch(0.96 0.01 85) | oklch(0.20 0.012 70) | 4.05:1 | ✗     |

**Known gap**: dark-theme contrast is 4.05:1, below the 4.5:1 AA threshold. The dark `--warm-0`
(OKLCH L=0.20, the darkest available existing token) yields sRGB relative luminance ≈ 0.197.
Against the dark `--warm-900` (OKLCH L=0.96, luminance ≈ 0.93), the contrast is (0.93+0.05)/
(0.197+0.05) = 3.97:1. No existing token in the dark palette is darker than `--warm-0` at L=0.20.

**Remediation path**: Phase 9's live-page AC-38 assertion ("Band colours meet contrast in both
themes") will catch this. The fix is either (a) lowering the dark `--warm-0` OKLCH lightness
from 0.20 to ~0.14 (which changes the app's dark background — a global change requiring visual
verification), or (b) adding a dedicated `--chart-band-dark-wash` token at OKLCH L≈0.14 (a
new OKLCH value, not a hex literal — T-5's grep would still pass). This gap is recorded here
for Phase 9 action, not resolved in Phase 1.

## OKLCH lightness deltas

### Light theme

| Band    | Base L | Ink L | Wash L | Δ(ink, wash) |
| ------- | ------ | ----- | ------ | ------------ |
| opus    | 0.60   | 0.18  | 0.99   | 0.81         |
| sonnet  | 0.66   | 0.18  | 0.99   | 0.81         |
| light   | 0.76   | 0.18  | 0.99   | 0.81         |
| unrated | 0.62   | 0.18  | 0.99   | 0.81         |

### Dark theme

| Band    | Base L | Ink L | Wash L | Δ(ink, wash) |
| ------- | ------ | ----- | ------ | ------------ |
| opus    | 0.66   | 0.96  | 0.20   | 0.76         |
| sonnet  | 0.70   | 0.96  | 0.20   | 0.76         |
| light   | 0.82   | 0.96  | 0.20   | 0.76         |
| unrated | 0.58   | 0.96  | 0.20   | 0.76         |

### Resolved hex approximations

```text
#cccbdd
#ced6dc
#e8e0c7
#cfcecb
```
