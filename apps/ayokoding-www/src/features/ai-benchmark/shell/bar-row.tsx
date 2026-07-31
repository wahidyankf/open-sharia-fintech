// AI BENCHMARK — DOM proportional-fill bar row (Phase 5, cycle 5.1, DD-25).
//
// `benchmark-chart.tsx` used to render each bar as an SVG `<Bar>` (a `<rect>` whose `width` was a
// pixel offset from `chart-primitives.tsx`'s `scaleLinear`) with a separately-positioned `<text>`
// label. `BarRow` is the DOM replacement: ONE component renders both the label and the bar, and the
// bar's fill is a plain `<div>` whose CSS `width` is a `%` string — `scaleLinear(max, 100)(value)`
// (DD-25's percentage-scale contract; see `chart-primitives.tsx`'s own `scaleLinear` docstring and
// `chart-primitives.test.tsx`'s "percentage contract" describe block). `benchmark-chart.tsx` renders
// one `BarRow` per bar (capability, price-in, price-out) rather than a shared name/index header
// positioned above a separate bar — the label text differs per bar instead.
//
// FCIS boundary: this module holds NO literal benchmark score, price, model name, or class
// threshold — every number, every string, and the colour token all come from the caller.

import { bandBarBgClass, scaleLinear, type ChartBand } from "./chart-primitives";

export type BarRowProps = {
  /** The value plotted, on `[0, max]` — a composite index or a price. */
  value: number;
  /** The domain maximum this bar's value is scaled against. */
  max: number;
  /** Which capability band's colour token fills the bar. */
  band: ChartBand;
  /** The already-localized, formatted label rendered above the bar (the caller owns formatting). */
  label: string;
  /** The row's own `data-testid` — the label and fill each derive their own suffixed testid from it. */
  testId?: string;
};

/** One labelled, proportional-fill DOM bar (DD-25) — replaces the retired SVG `<Bar>` + `<text>` pair. */
export function BarRow({ value, max, band, label, testId }: BarRowProps) {
  const widthPct = `${scaleLinear(max, 100)(value)}%`;
  return (
    <div data-slot="chart-bar-row" data-testid={testId}>
      <span
        data-slot="chart-bar-row-label"
        data-testid={testId ? `${testId}-label` : undefined}
        className="block text-[10px] text-foreground"
      >
        {label}
      </span>
      <div data-slot="chart-bar-row-track" className="h-3 w-full rounded bg-muted">
        <div
          data-slot="chart-bar-row-fill"
          data-testid={testId ? `${testId}-fill` : undefined}
          className={`h-3 rounded ${bandBarBgClass(band)}`}
          style={{ width: widthPct }}
        />
      </div>
    </div>
  );
}
