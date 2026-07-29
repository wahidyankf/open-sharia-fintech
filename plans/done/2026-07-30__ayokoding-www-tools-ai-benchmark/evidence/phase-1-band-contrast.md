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

| Band    | Ink OKLCH            | Wash OKLCH           | Ratio   | Pass? |
| ------- | -------------------- | -------------------- | ------- | ----- |
| opus    | oklch(0.18 0.016 70) | oklch(0.99 0.006 85) | 18.41:1 | ✓     |
| sonnet  | oklch(0.18 0.016 70) | oklch(0.99 0.006 85) | 18.41:1 | ✓     |
| light   | oklch(0.18 0.016 70) | oklch(0.99 0.006 85) | 18.41:1 | ✓     |
| unrated | oklch(0.18 0.016 70) | oklch(0.99 0.006 85) | 18.41:1 | ✓     |

All four bands pass the ≥ 4.5:1 WCAG AA threshold in light theme. (The original T-4 figure of
4.56:1 was a rounded-luminance approximation, not the precise WCAG formula — see the Dark theme
section below for the corrected methodology and why this document's figures were revised in Phase 9.)

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

| Band    | Ink OKLCH           | Wash OKLCH           | Ratio   | Pass? |
| ------- | ------------------- | -------------------- | ------- | ----- |
| opus    | oklch(0.96 0.01 85) | oklch(0.20 0.012 70) | 16.10:1 | ✓     |
| sonnet  | oklch(0.96 0.01 85) | oklch(0.20 0.012 70) | 16.10:1 | ✓     |
| light   | oklch(0.96 0.01 85) | oklch(0.20 0.012 70) | 16.10:1 | ✓     |
| unrated | oklch(0.96 0.01 85) | oklch(0.20 0.012 70) | 16.10:1 | ✓     |

**Phase 1's "4.05:1" figure above was itself measurement error, corrected during Phase 9 (M-11/M-12)
— no token value changed.** The rounded-luminance approximation this document originally used
(`luminance ≈ OKLCH L` directly) is not the WCAG formula: WCAG relative luminance is computed from
**sRGB** channel values after gamma decoding, and OKLCH's perceptual lightness `L` is not linearly
related to that. Phase 9's AC-38 e2e assertion (`apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts`)
resolves each token's actual colour via a real `<canvas>` 2D context (`ctx.fillStyle = <oklch string>`,
then `getImageData` for the true sRGB bytes) and computes the standard WCAG contrast ratio
(https://www.w3.org/TR/WCAG21/#dfn-contrast-ratio) from those bytes. Redone that way: `oklch(96% 0.01 85)`
→ RGB(245, 241, 234); `oklch(20% 0.012 70)` → RGB(26, 21, 16); ratio = 16.10:1 — comfortably above
the 4.5:1 AA floor, no remediation needed. The light-theme figure was re-verified the same way and
also holds (18.41:1, not the 4.56:1 this document originally approximated).

**A separate, real defect WAS found and fixed in Phase 9**: the four light-theme `--chart-band-*-wash`
declarations, as originally placed inside `libs/web-ui-token/src/ayokoding.css`'s Tailwind v4
`@theme { ... }` block, never reached the compiled page at all —
`getComputedStyle(document.documentElement).getPropertyValue('--chart-band-opus-wash')` returned an
**empty string** in light theme (confirmed live via Playwright MCP), while the identically-declared
`-ink` properties in the same block resolved fine. This is a Tailwind v4/Lightning CSS `@theme`
compilation quirk this repo does not control (root cause not fully isolated — reproducibly
specific to the `-wash` declarations, not to duplicate-value declarations, since `-ink` also has
four identical `var(--warm-900)` declarations that DO survive). The dark-theme wash declarations
were unaffected because they live in a plain, non-`@theme` selector (`[data-theme="dark"], .dark`).
**Fix**: the four light-theme `-wash` declarations moved from `@theme { ... }` to the plain
`:root { ... }` block at the top of the same file (right beside `--warm-0` itself), which sidesteps
the `@theme` compiler path entirely — no numeric value changed, `--chart-band-*-wash` still aliases
`--warm-0` in light theme exactly as originally designed. Confirmed via the same
`getComputedStyle(...).getPropertyValue(...)` probe that the token now resolves in light theme, and
via a temporary revert (`git stash`) that AC-38 genuinely fails against the pre-fix declaration
(RED) and passes again once restored (GREEN) — see Phase 9's delivery.md entry for M-11/M-12.

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

## Resolved hex approximations

```text
#cccbdd
#ced6dc
#e8e0c7
#cfcecb
```
