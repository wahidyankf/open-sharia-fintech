// AI BENCHMARK — price chart, "Diagram 2" (Phase 7, Y-1..Y-10).
//
// One input-token bar and one output-token bar per METERED model, grouped into the same
// opus/sonnet/light/unrated bands the capability chart uses (same order — AC-11), each bar
// carrying its labelled input/output rate as text (AC-15). A model priced only under a flat-rate
// subscription carries no per-token rate to plot — it is never rendered as a zero-length bar;
// instead every subscription-only model across the whole roster is listed, once, in a single
// labelled "subscription group" text list naming its plan cost and usage caps (AC-16), mirroring
// `capability-chart.tsx`'s unrated-group pattern (a model with no price at all — neither metered
// nor subscription — renders in neither the bands nor the subscription list; the data table
// already carries its "not reported" state). With no harness filter, every rate plotted is the
// model's LOWEST available harness rate (`lowestRate` from `core/price.ts`) — the chart states
// this as a localized subtitle (AC-17).
//
// The whole chart is one `<svg role="img">` whose accessible name is its own localized `<title>`
// (AC-36) — same pattern as `capability-chart.tsx`.
//
// FCIS boundary: no literal price, model name, or class threshold lives here — every number and
// name comes from the passed `dataset` via `core/price.ts` and `core/bands.ts`; every colour
// comes from `chart-primitives.tsx`'s band-token maps.

import { useId } from "react";
import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import { dataset as defaultDataset, type Dataset } from "../core/data/models";
import { computeGroups, type ModelScore } from "../core/bands";
import { lowestRate } from "../core/price";
import { formatPriceUsd } from "./format";
import { Axis, Bar, BandGroup, TickRow, bandLabel, evenTicks, scaleLinear, type ChartBand } from "./chart-primitives";

const SLOT = "price-chart";

// ─── Layout constants (display-only — never a benchmark score, price, or threshold) ───────────
const SVG_WIDTH = 620;
const PLOT_X = 220; // left gutter reserved for the input/output labels
const PLOT_WIDTH = 340;
const ROW_HEIGHT = 34; // room for the two-bar row and its label
const BAR_HEIGHT = 7;
const BAR_GAP = 2;
const BAND_HEADER_HEIGHT = 22;
const BAND_GAP = 14;
const TOP_MARGIN = 24; // room for the always-visible axis-maximum label
const BOTTOM_MARGIN = 20;
const TICK_COUNT = 4; // the lg-only tick row renders TICK_COUNT + 1 evenly spaced values

// All four bands are candidates for a price section — unlike the capability chart, a model with
// no composite index can still carry a real price, so `unrated` renders bars here (never a
// text-only placeholder) whenever at least one unrated model has a metered rate.
const ALL_BANDS: readonly ChartBand[] = ["opus", "sonnet", "light", "unrated"];

type MeteredRow = {
  score: ModelScore;
  input: number;
  output: number;
};

type SubscriptionRow = {
  score: ModelScore;
  planCostUsd: number;
  caps?: string;
};

/** Splits one band's models into those with a metered lowest rate and those on a subscription. */
function splitByRate(
  groups: Record<ChartBand, ModelScore[]>,
  band: ChartBand,
): { metered: MeteredRow[]; subscriptions: SubscriptionRow[] } {
  const metered: MeteredRow[] = [];
  const subscriptions: SubscriptionRow[] = [];
  for (const score of groups[band]) {
    const rate = lowestRate(score.model);
    if (rate === undefined) continue; // no price at all — nothing to plot or list
    if (rate.kind === "metered") {
      metered.push({ score, input: rate.input, output: rate.output });
    } else {
      subscriptions.push({ score, planCostUsd: rate.planCostUsd, caps: rate.caps });
    }
  }
  return { metered, subscriptions };
}

type BandLayout = {
  band: ChartBand;
  label: string;
  headerY: number;
  rows: { row: MeteredRow; rowTop: number }[];
};

/**
 * Stacks every band that has at least one metered-price model (a band with none renders no
 * header at all — the whole roster still reaches a reader via the subscription list or the data
 * table). Collects every subscription-only model across all four bands into one flat, canonically
 * ordered list.
 */
function computeLayout(
  groups: Record<ChartBand, ModelScore[]>,
  locale: Locale,
): { bands: BandLayout[]; subscriptions: SubscriptionRow[]; plotHeight: number } {
  let cursor = TOP_MARGIN;
  const bands: BandLayout[] = [];
  const subscriptions: SubscriptionRow[] = [];
  for (const band of ALL_BANDS) {
    const split = splitByRate(groups, band);
    subscriptions.push(...split.subscriptions);
    if (split.metered.length === 0) continue;
    const headerY = cursor + BAND_HEADER_HEIGHT - 8;
    const rowsTop = cursor + BAND_HEADER_HEIGHT;
    const rows = split.metered.map((row, i) => ({ row, rowTop: rowsTop + i * ROW_HEIGHT }));
    bands.push({ band, label: bandLabel(band, locale), headerY, rows });
    cursor = rowsTop + split.metered.length * ROW_HEIGHT + BAND_GAP;
  }
  return { bands, subscriptions, plotHeight: cursor + BOTTOM_MARGIN };
}

/** The highest input or output rate among every rendered bar — the axis's domain maximum. */
function axisMaxOf(bands: BandLayout[]): number {
  let max = 0;
  for (const b of bands) {
    for (const { row } of b.rows) {
      if (row.input > max) max = row.input;
      if (row.output > max) max = row.output;
    }
  }
  return max;
}

export type PriceChartProps = {
  dataset?: Dataset;
  locale: Locale;
};

export function PriceChart({ dataset = defaultDataset, locale }: PriceChartProps) {
  const titleId = useId();
  const subscriptionHeadingId = useId();

  const groups = computeGroups(dataset);
  const { bands, subscriptions, plotHeight } = computeLayout(groups, locale);
  const axisMax = axisMaxOf(bands);
  const scale = scaleLinear(axisMax, PLOT_WIDTH);
  const axisLabel = t(locale, "aiBenchChartAxisMaxLabel");
  const formattedMax = formatPriceUsd(axisMax, locale);
  const tickRowY = plotHeight - 4;

  return (
    <div data-slot={SLOT} data-testid={SLOT}>
      <h2 data-testid={`${SLOT}-heading`} className="mb-1 text-lg font-semibold">
        {t(locale, "aiBenchPriceChartTitle")}
      </h2>
      <p data-testid={`${SLOT}-subtitle`} className="mb-2 text-xs text-muted-foreground">
        {t(locale, "aiBenchPriceLowestSubtitle")}
      </p>

      <svg
        data-testid={`${SLOT}-svg`}
        role="img"
        aria-labelledby={titleId}
        viewBox={`0 0 ${SVG_WIDTH} ${plotHeight}`}
        className="w-full"
      >
        <title id={titleId}>{t(locale, "aiBenchPriceChartTitle")}</title>

        <Axis max={axisMax} width={SVG_WIDTH} label={axisLabel} formattedMax={formattedMax} y={14} />

        {bands.map((bandLayout) => (
          <BandGroup
            key={bandLayout.band}
            band={bandLayout.band}
            label={bandLayout.label}
            x={PLOT_X}
            y={bandLayout.headerY}
            testId={`${SLOT}-band-${bandLayout.band}`}
          >
            {bandLayout.rows.map(({ row, rowTop }) => {
              const id = row.score.model.id;
              const inputValue = formatPriceUsd(row.input, locale);
              const outputValue = formatPriceUsd(row.output, locale);
              const inBarY = rowTop + 4;
              const outBarY = inBarY + BAR_HEIGHT + BAR_GAP;
              const inWidth = scale(row.input);
              const outWidth = scale(row.output);
              const inputLabelText = `${row.score.model.name} — ${t(locale, "aiBenchColInputPrice")}: ${inputValue}`;
              const outputLabelText = `${t(locale, "aiBenchColOutputPrice")}: ${outputValue}`;
              return (
                <g key={id} data-testid={`${SLOT}-row-${id}`}>
                  {/* Mobile (below `md`): a two-line in/out text block per model — no bars, the
                      two stacked bars would be too small to read at that width. */}
                  <text
                    data-slot="chart-bar-label"
                    data-testid={`${SLOT}-mobile-in-${id}`}
                    x={PLOT_X}
                    y={rowTop + 8}
                    className="fill-foreground text-[10px] md:hidden"
                  >
                    {inputLabelText}
                  </text>
                  <text
                    data-slot="chart-bar-label"
                    data-testid={`${SLOT}-mobile-out-${id}`}
                    x={PLOT_X}
                    y={rowTop + 20}
                    className="fill-foreground text-[10px] md:hidden"
                  >
                    {outputLabelText}
                  </text>

                  {/* `md`/`lg`: two bars sharing a row, with left-gutter labels beside them. */}
                  <g className="hidden md:block">
                    <text
                      data-slot="chart-bar-label"
                      data-testid={`${SLOT}-label-in-${id}`}
                      x={PLOT_X - 8}
                      y={inBarY + BAR_HEIGHT - 1}
                      textAnchor="end"
                      className="fill-foreground text-[9px]"
                    >
                      {inputLabelText}
                    </text>
                    <text
                      data-slot="chart-bar-label"
                      data-testid={`${SLOT}-label-out-${id}`}
                      x={PLOT_X - 8}
                      y={outBarY + BAR_HEIGHT - 1}
                      textAnchor="end"
                      className="fill-foreground text-[9px]"
                    >
                      {outputLabelText}
                    </text>
                    <Bar
                      x={PLOT_X}
                      y={inBarY}
                      width={inWidth}
                      height={BAR_HEIGHT}
                      band={bandLayout.band}
                      testId={`${SLOT}-bar-in-${id}`}
                    />
                    <Bar
                      x={PLOT_X}
                      y={outBarY}
                      width={outWidth}
                      height={BAR_HEIGHT}
                      band={bandLayout.band}
                      testId={`${SLOT}-bar-out-${id}`}
                    />
                  </g>
                </g>
              );
            })}
          </BandGroup>
        ))}

        {/* `lg`-only tick row — {@link TICK_COUNT} + 1 evenly spaced values over the axis max. */}
        <TickRow
          testId={`${SLOT}-ticks`}
          tickTestId={`${SLOT}-tick`}
          values={evenTicks(axisMax, TICK_COUNT)}
          x={(v) => PLOT_X + scale(v)}
          y={tickRowY}
          format={(v) => formatPriceUsd(v, locale)}
        />
      </svg>

      {subscriptions.length > 0 ? (
        <div data-slot={`${SLOT}-subscription`} data-testid={`${SLOT}-subscription`} className="mt-3">
          <h3 id={subscriptionHeadingId} data-testid={`${SLOT}-subscription-heading`} className="text-sm font-semibold">
            {t(locale, "aiBenchPriceSubscriptionHeading")}
          </h3>
          <ul
            aria-labelledby={subscriptionHeadingId}
            className="mt-1 flex flex-col gap-1 text-sm text-muted-foreground"
          >
            {subscriptions.map((row) => (
              <li key={row.score.model.id} data-testid={`${SLOT}-subscription-${row.score.model.id}`}>
                {row.score.model.name} — {t(locale, "aiBenchSubscription")}: {formatPriceUsd(row.planCostUsd, locale)}
                {row.caps ? ` (${row.caps})` : ""}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
