// AI BENCHMARK — shared chart primitives (Phase 6, A-2; refactored A-17; reused by Phase 7).
//
// The capability chart and the price chart share ONE set of SVG building blocks so neither chart
// re-derives its own scale, axis, bar, or band-header rendering (Y-11 proves this by hoisting
// anything the two charts still duplicate back here). `Legend` also lives here but is currently
// used by the capability chart only — see its own docstring below. Every colour reference resolves
// through the `--chart-band-*` design tokens declared in `<TOKENS>` (Phase 1) — no component in
// this file (or any file that imports it) may name a hue directly (A-17).
//
// FCIS boundary: this module holds NO literal benchmark score, price, model name, or class
// threshold — `ChartBand` is a closed four-value union (the same one `core/bands.ts` produces),
// and every numeric value a caller passes in comes from the dataset via `core/`.

import type { ReactNode } from "react";
import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import { BAND_LABEL_KEYS } from "../core/data/benchmarks";
import type { Band as ChartBand } from "../core/bands";

/**
 * The four capability classes a bar or band header can be coloured by — re-exported from
 * `core/bands.ts`'s `Band` rather than redeclared, so a future band added there is a compile
 * error here for every `Record<ChartBand, …>` map below (each becomes exhaustively unsatisfied).
 * That guarantee covers only this colour-token layer — it does NOT reach a chart's own
 * array-literal band list. `price-chart.tsx`'s `ALL_BANDS` and `capability-chart.tsx`'s
 * `RATED_BANDS` are current positive examples: both already derive from `core/filter.ts`'s
 * `BANDS` (the single source of truth, F-9) rather than hand-writing their own band array, so
 * neither is at risk today. The caveat this docstring records is a general one for any future
 * chart-owned band list: a hand-written array-literal band list (one that does not derive from
 * `BANDS`) can still silently omit a new band from rendering.
 */
export type { ChartBand };

// Tailwind's class scanner reads literal, unbroken strings out of the source text — a template
// literal built from a shared `band → token name` lookup would never be found by the scanner, so
// there is deliberately no single token-name registry these maps "read through". Each of the three
// maps below independently hardcodes its own complete, static class string per band and must be
// kept consistent with the others by hand — colour CAN drift if a future edit updates one map
// without the others.
const BAR_FILL_CLASS: Record<ChartBand, string> = {
  opus: "fill-[var(--chart-band-opus)]",
  sonnet: "fill-[var(--chart-band-sonnet)]",
  light: "fill-[var(--chart-band-light)]",
  unrated: "fill-[var(--chart-band-unrated)]",
};

const BAND_INK_FILL_CLASS: Record<ChartBand, string> = {
  opus: "fill-[var(--chart-band-opus-ink)]",
  sonnet: "fill-[var(--chart-band-sonnet-ink)]",
  light: "fill-[var(--chart-band-light-ink)]",
  unrated: "fill-[var(--chart-band-unrated-ink)]",
};

const BAND_SWATCH_CLASS: Record<ChartBand, string> = {
  opus: "bg-[var(--chart-band-opus)]",
  sonnet: "bg-[var(--chart-band-sonnet)]",
  light: "bg-[var(--chart-band-light)]",
  unrated: "bg-[var(--chart-band-unrated)]",
};

/** The Tailwind class that fills an SVG shape with a band's colour token. */
export function barFillClass(band: ChartBand): string {
  return BAR_FILL_CLASS[band];
}

/** The Tailwind class that colours SVG text with a band's "ink" (on-wash-background) token. */
export function bandInkFillClass(band: ChartBand): string {
  return BAND_INK_FILL_CLASS[band];
}

/** The Tailwind class that colours a small swatch (e.g. a legend dot) with a band's colour token. */
export function bandSwatchClass(band: ChartBand): string {
  return BAND_SWATCH_CLASS[band];
}

/**
 * A band's localized class-name label — the single place either chart looks up
 * `BAND_LABEL_KEYS[band] → t(locale, key)` (Y-11 refactor: `capability-chart.tsx` and
 * `price-chart.tsx` each carried their own identical copy of this lookup; the fallback-to-band-id
 * guard can no longer drift between the two charts now that it lives here once).
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
 */
export function scaleLinear(domainMax: number, pixelWidth: number): (value: number) => number {
  if (!(domainMax > 0)) {
    return () => 0;
  }
  return (value: number) => (value / domainMax) * pixelWidth;
}

export type AxisProps = {
  /** The domain maximum this axis represents — always rendered as text (AC-13). */
  max: number;
  /** Right edge of the plot area, in pixels — the axis-maximum label right-aligns to this. */
  width: number;
  /** A localized label placed before the number (e.g. "Axis maximum"). */
  label: string;
  /** The already-localized, formatted number to render (the caller owns number formatting). */
  formattedMax: string;
  y?: number;
};

/**
 * Renders the axis maximum as text — always visible, regardless of viewport — so the chart states
 * its scale in a form a screen reader or a search-in-page can find (AC-13).
 */
export function Axis({ width, label, formattedMax, y = 0 }: AxisProps) {
  return (
    <text
      data-slot="chart-axis-max"
      data-testid="chart-axis-max"
      x={width}
      y={y}
      textAnchor="end"
      className="fill-muted-foreground text-[10px]"
    >
      {label}: {formattedMax}
    </text>
  );
}

export type BarProps = {
  x: number;
  y: number;
  /** Bar length in pixels — already scaled by the caller via {@link scaleLinear}. */
  width: number;
  height: number;
  band: ChartBand;
  testId?: string;
};

/** A single bar rect, filled from the shared band token — the only place a `<rect>` is emitted. */
export function Bar({ x, y, width, height, band, testId }: BarProps) {
  return (
    <rect
      data-slot="chart-bar"
      data-testid={testId}
      x={x}
      y={y}
      width={Math.max(width, 0)}
      height={height}
      rx={2}
      className={barFillClass(band)}
    />
  );
}

export type BandGroupProps = {
  band: ChartBand;
  /** The band's localized class name — rendered as text so class is never colour-only (AC-37). */
  label: string;
  x?: number;
  y: number;
  testId?: string;
  children?: ReactNode;
};

/** One capability/price band section: a text header naming the band, then its children (bars). */
export function BandGroup({ band, label, x = 0, y, testId, children }: BandGroupProps) {
  return (
    <g data-slot="chart-band-group" data-band={band} data-testid={testId}>
      <text
        data-slot="chart-band-group-label"
        data-testid={testId ? `${testId}-label` : undefined}
        x={x}
        y={y}
        className={`text-xs font-semibold ${bandInkFillClass(band)}`}
      >
        {label}
      </text>
      {children}
    </g>
  );
}

export type LegendItem = {
  band: ChartBand;
  label: string;
};

export type LegendProps = {
  items: readonly LegendItem[];
};

/**
 * A compact swatch + text legend, currently used by the capability chart only (`price-chart.tsx`
 * does not render one — each of its band groups already carries a text header via `BandGroup`, so
 * AC-37's "class is never colour-only" holds there without a legend). The swatch is `aria-hidden`
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

/**
 * `count + 1` evenly spaced values from `0` to `max`, inclusive — the domain values an lg-only
 * tick row renders (Y-11 refactor target: both charts built their own near-identical
 * "even ticks up to a max" generator; `capability-chart.tsx`'s fixed-20-unit-interval ticks over
 * `COMPOSITE_INDEX_MAX` (100) are exactly `evenTicks(100, 5)`, so no chart's tick VALUES change,
 * only where the generator lives). A non-positive `max` or non-positive `count` degenerates to a
 * single `[0]` tick rather than dividing by zero or looping forever.
 */
export function evenTicks(max: number, count: number): number[] {
  if (!(max > 0) || count <= 0) return [0];
  const out: number[] = [];
  for (let i = 0; i <= count; i++) {
    out.push((max * i) / count);
  }
  return out;
}

export type TickRowProps = {
  /** The outer `<g>`'s `data-testid` (the whole row, e.g. `"capability-chart-ticks"`). */
  testId: string;
  /** Each individual tick's `data-testid` prefix — the tick's own testid is `${tickTestId}-${value}`. */
  tickTestId: string;
  values: readonly number[];
  /** Maps a domain value to its pixel x-offset (typically the chart's own {@link scaleLinear} plus the plot's left gutter). */
  x: (value: number) => number;
  y: number;
  /** The already-localized, formatted string for one tick value (the caller owns number formatting). */
  format: (value: number) => string;
};

/**
 * An lg-only row of axis ticks — always visible ABOVE `lg` in the DOM (jsdom applies no CSS, so a
 * test can assert its content regardless of viewport), only visually shown at `lg` via the
 * `hidden lg:block` class. The one place either chart renders its tick-value `<text>` row (Y-11
 * refactor target: both charts previously carried their own copy of this exact markup).
 */
export function TickRow({ testId, tickTestId, values, x, y, format }: TickRowProps) {
  return (
    <g data-testid={testId} className="hidden lg:block">
      {values.map((v) => (
        <text
          key={v}
          data-slot="chart-axis-tick"
          data-testid={`${tickTestId}-${v}`}
          x={x(v)}
          y={y}
          textAnchor="middle"
          className="fill-muted-foreground text-[9px]"
        >
          {format(v)}
        </text>
      ))}
    </g>
  );
}
