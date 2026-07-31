// AI BENCHMARK — shared chart primitives (Phase 6, A-2; refactored A-17; reused by Phase 7; DOM
// class maps added Phase 4/5, cycle 4.2/DD-25).
//
// `benchmark-chart.tsx` (the merged chart, Phase 2) is the sole consumer of this shared scale/
// colour-token/label logic today — it never re-derives its own scale or band-label lookup. This
// module predates the merge: the retired `capability-chart.tsx` and `price-chart.tsx` (deleted,
// Phase 3c — see git history) used to share it (Y-11 hoisted anything they duplicated back here),
// which is why the primitives still live in their own module rather than being folded into
// `benchmark-chart.tsx` directly. `Legend` also lives here but is currently used by
// `how-to-read.tsx` only — see its own docstring below. Every colour reference resolves through the
// `--chart-band-*` design tokens declared in `<TOKENS>` (Phase 1) — no component in this file (or
// any file that imports it) may name a hue directly (A-17).
//
// FCIS boundary: this module holds NO literal benchmark score, price, model name, or class
// threshold — `ChartBand` is a closed four-value union (the same one `core/bands.ts` produces),
// and every numeric value a caller passes in comes from the dataset via `core/`.

import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import { BAND_LABEL_KEYS } from "../core/data/benchmarks";
import type { Band as ChartBand } from "../core/bands";

/**
 * The four capability classes a bar or band header can be coloured by — re-exported from
 * `core/bands.ts`'s `Band` rather than redeclared, so a future band added there is a compile
 * error here for every `Record<ChartBand, …>` map below (each becomes exhaustively unsatisfied).
 * That guarantee covers only this colour-token layer — it does NOT reach a chart's own
 * array-literal band list. The retired price chart's `ALL_BANDS` and the retired capability
 * chart's `RATED_BANDS` were current positive examples: both already derived from `core/filter.ts`'s
 * `BANDS` (the single source of truth, F-9) rather than hand-writing their own band array, so
 * neither is at risk today. The caveat this docstring records is a general one for any future
 * chart-owned band list: a hand-written array-literal band list (one that does not derive from
 * `BANDS`) can still silently omit a new band from rendering.
 */
export type { ChartBand };

// Tailwind's class scanner reads literal, unbroken strings out of the source text — a template
// literal built from a shared `band → token name` lookup would never be found by the scanner, so
// there is deliberately no single token-name registry these maps "read through". Each of the three
// maps below (`BAND_SWATCH_CLASS`, and — added in Phase 4, cycle 4.2, for the DOM bar row —
// `BAND_BAR_BG_CLASS`/`BAND_INK_TEXT_CLASS`) independently hardcodes its own complete, static class
// string per band and must be kept consistent with the others by hand — colour CAN drift if a
// future edit updates one map without the others. (Phase 5's DOM rewrite deleted the SVG-only
// `fill-*` siblings of these maps — `BAR_FILL_CLASS`/`BAND_INK_FILL_CLASS` — once the DOM chart left
// them with zero consumers; see DD-32 in this plan's `tech-docs.md`.)
const BAND_SWATCH_CLASS: Record<ChartBand, string> = {
  opus: "bg-[var(--chart-band-opus)]",
  sonnet: "bg-[var(--chart-band-sonnet)]",
  haiku: "bg-[var(--chart-band-haiku)]",
  unrated: "bg-[var(--chart-band-unrated)]",
};

// DOM (non-SVG) equivalents of the deleted SVG `fill-*` maps above (DD-32) — a Phase 5 `<div>`-based
// bar row cannot use `fill-*` (an SVG-only Tailwind utility); it needs `bg-*` for its own background
// and `text-*` for its ink-coloured label instead. Consumed by cycle 5.1's `BarRow`.
const BAND_BAR_BG_CLASS: Record<ChartBand, string> = {
  opus: "bg-[var(--chart-band-opus)]",
  sonnet: "bg-[var(--chart-band-sonnet)]",
  haiku: "bg-[var(--chart-band-haiku)]",
  unrated: "bg-[var(--chart-band-unrated)]",
};

const BAND_INK_TEXT_CLASS: Record<ChartBand, string> = {
  opus: "text-[var(--chart-band-opus-ink)]",
  sonnet: "text-[var(--chart-band-sonnet-ink)]",
  haiku: "text-[var(--chart-band-haiku-ink)]",
  unrated: "text-[var(--chart-band-unrated-ink)]",
};

/** The Tailwind class that colours a small swatch (e.g. a legend dot) with a band's colour token. */
export function bandSwatchClass(band: ChartBand): string {
  return BAND_SWATCH_CLASS[band];
}

/** A `<div>` bar's own `bg-*` background, colouring it with a band's colour token. */
export function bandBarBgClass(band: ChartBand): string {
  return BAND_BAR_BG_CLASS[band];
}

/** A DOM label's `text-*` ink colour, colouring it with a band's "ink" (on-wash-background) token. */
export function bandInkTextClass(band: ChartBand): string {
  return BAND_INK_TEXT_CLASS[band];
}

/**
 * A band's localized class-name label — the single place the chart looks up
 * `BAND_LABEL_KEYS[band] → t(locale, key)` (Y-11 refactor: the two now-retired charts each used to
 * carry their own identical copy of this lookup; the fallback-to-band-id guard cannot drift
 * between duplicate copies now that it lives here once).
 */
export function bandLabel(band: ChartBand, locale: Locale): string {
  const key = BAND_LABEL_KEYS[band];
  return key ? t(locale, key) : band;
}

/**
 * Maps a value on `[0, domainMax]` to a pixel offset on `[0, pixelWidth]` — the one place either
 * chart converts a domain value (a composite index, a price) into a bar length. Monotonic: a
 * larger domain value always yields an offset ≥ a smaller one's. A non-positive `domainMax`
 * degenerates to always-zero rather than dividing by zero or producing `NaN`.
 *
 * Doubles as a PERCENTAGE scale when `pixelWidth` is exactly `100` (DD-25) — Phase 5's DOM bar
 * rows call `scaleLinear(COMPOSITE_INDEX_MAX, 100)` to turn a composite index into the `${n}%`
 * inline `width` a percentage-based (non-SVG) bar needs, rather than a pixel offset into a fixed
 * SVG viewBox. No new code path exists for this — it is the SAME function, at the SAME contract,
 * called with `100` for the second argument; `chart-primitives.test.tsx`'s "percentage contract"
 * describe block characterizes exactly this call shape.
 */
export function scaleLinear(domainMax: number, pixelWidth: number): (value: number) => number {
  if (!(domainMax > 0)) {
    return () => 0;
  }
  return (value: number) => (value / domainMax) * pixelWidth;
}

export type LegendItem = {
  band: ChartBand;
  label: string;
};

export type LegendProps = {
  items: readonly LegendItem[];
};

/**
 * A compact swatch + text legend, used by `how-to-read.tsx` — the merged chart itself does not
 * render one, since each of its DOM band regions already carries its own visible text heading
 * (`benchmark-chart.tsx`'s per-band `<h3>`), so AC-37's "class is never colour-only" holds there
 * without a legend. The swatch is `aria-hidden`
 * decoration — the label text beside it is what actually carries the band's identity (never colour
 * alone).
 */
export function Legend({ items }: LegendProps) {
  return (
    <ul data-slot="chart-legend" className="flex flex-wrap gap-x-4 gap-y-1 text-xs">
      {items.map((item) => (
        <li key={item.band} data-slot="chart-legend-item" className="flex items-center gap-1.5">
          <span aria-hidden="true" className={`inline-block h-2.5 w-2.5 rounded-full ${bandSwatchClass(item.band)}`} />
          <span data-slot="chart-legend-label">{item.label}</span>
        </li>
      ))}
    </ul>
  );
}
