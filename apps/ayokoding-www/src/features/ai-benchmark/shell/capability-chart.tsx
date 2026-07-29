// AI BENCHMARK — capability chart, "Diagram 1" (Phase 6, A-4..A-16).
//
// One horizontal bar per RATED model (opus/sonnet/light), grouped by band, bar length
// proportional to the model's composite index (AC-13). Every bar carries its model name and
// numeric index as text (AC-14); a low-coverage model additionally carries a text marker stating
// its coverage ratio (AC-12). Every band group's class name is text, never colour alone (AC-37).
// The `unrated` group has no composite index to plot — it never renders as a zero-length bar;
// instead it is a plain, labelled text list beneath the three bands (A-13/A-14). Responsively: the
// label and value sit ABOVE each bar below `md`, in a left gutter at `md`/`lg`, with axis ticks
// every 20 units added at `lg` (A-15/A-16) — both placements render simultaneously in the DOM (CSS
// toggles which is visible), mirroring `model-table.tsx`'s desktop/mobile parity pattern.
//
// The whole chart is one `<svg role="img">` whose accessible name is its own localized `<title>`
// (AC-36) — the bars/labels inside are supplementary for sighted users; the FULL data, including
// every model's class, already lives in the accessible `<ModelTable>` (AC-20/AC-37).
//
// FCIS boundary: no literal benchmark score, price, model name, or class threshold lives here —
// every number and name comes from the passed `dataset` via `core/bands.ts` and `core/score.ts`;
// every colour comes from `chart-primitives.tsx`'s band-token maps.

import { useId } from "react";
import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import { dataset as defaultDataset, type Dataset } from "../core/data/models";
import { computeGroups, type ModelScore } from "../core/bands";
import { BANDS } from "../core/filter";
import { COMPOSITE_INDEX_MAX, LOW_COVERAGE_THRESHOLD } from "../core/score";
import { formatCoverage, formatIndex } from "./format";
import {
  Axis,
  Bar,
  BandGroup,
  Legend,
  TickRow,
  bandLabel,
  evenTicks,
  scaleLinear,
  type ChartBand,
} from "./chart-primitives";

const SLOT = "capability-chart";

// ─── Layout constants (display-only — never a benchmark score, price, or threshold) ───────────
const SVG_WIDTH = 600;
const PLOT_X = 160; // left gutter reserved for the md/lg left-gutter label
const PLOT_WIDTH = 380;
const ROW_HEIGHT = 30; // room for both the mobile "label above bar" line and the bar itself
const BAR_HEIGHT = 16;
const BAND_HEADER_HEIGHT = 22;
const BAND_GAP = 12;
const TOP_MARGIN = 24; // room for the always-visible axis-maximum label
const BOTTOM_MARGIN = 20; // room for the lg-only tick row
const TICK_COUNT = 5; // chart display granularity (0/20/40/60/80/100 over COMPOSITE_INDEX_MAX), not dataset data (A-16)

// Derived from `core/filter.ts`'s `BANDS` — the single source of truth for the full band list
// (F-9) — rather than re-declared here, so a new rated band is still added in exactly one place;
// only `unrated` is excluded by name, since it is the one band this chart never plots as a bar.
const RATED_BANDS: readonly ChartBand[] = BANDS.filter((band) => band !== "unrated");

type BandLayout = {
  band: ChartBand;
  label: string;
  headerY: number;
  rows: { score: ModelScore; rowTop: number }[];
};

/** Stacks the three rated bands top to bottom, each band's rows top to bottom within it. */
function computeLayout(
  groups: Record<ChartBand, ModelScore[]>,
  locale: Locale,
): { bands: BandLayout[]; plotHeight: number } {
  let cursor = TOP_MARGIN;
  const bands: BandLayout[] = [];
  for (const band of RATED_BANDS) {
    const scores = groups[band];
    const headerY = cursor + BAND_HEADER_HEIGHT - 8;
    const rowsTop = cursor + BAND_HEADER_HEIGHT;
    const rows = scores.map((score, i) => ({ score, rowTop: rowsTop + i * ROW_HEIGHT }));
    bands.push({ band, label: bandLabel(band, locale), headerY, rows });
    cursor = rowsTop + scores.length * ROW_HEIGHT + BAND_GAP;
  }
  return { bands, plotHeight: cursor + BOTTOM_MARGIN };
}

export type CapabilityChartProps = {
  dataset?: Dataset;
  /**
   * The full unfiltered roster. Band thresholds (the anchor indices) and the roster-max map are
   * ALWAYS derived from this dataset, never from `dataset` — `dataset` may be a harness/class
   * filtered subset that excludes both anchor models, and re-deriving thresholds from it would
   * silently collapse every rated model to `light` (DD-5a: bands are roster-relative to the FULL
   * population; filtering governs display only). Defaults to `dataset` itself when omitted.
   */
  fullDataset?: Dataset;
  locale: Locale;
};

export function CapabilityChart({ dataset = defaultDataset, fullDataset, locale }: CapabilityChartProps) {
  const titleId = useId();
  const unratedHeadingId = useId();

  const groups = computeGroups(dataset, fullDataset ?? dataset);
  const { bands, plotHeight } = computeLayout(groups, locale);
  const scale = scaleLinear(COMPOSITE_INDEX_MAX, PLOT_WIDTH);
  const axisLabel = t(locale, "aiBenchChartAxisMaxLabel");
  const formattedMax = formatIndex(COMPOSITE_INDEX_MAX, locale);
  const legendItems = RATED_BANDS.map((band) => ({ band, label: bandLabel(band, locale) }));
  const tickRowY = plotHeight - 4;

  return (
    <div data-slot={SLOT} data-testid={SLOT}>
      <h2 data-testid={`${SLOT}-heading`} className="mb-2 text-lg font-semibold">
        {t(locale, "aiBenchCapabilityChartTitle")}
      </h2>

      <svg
        data-testid={`${SLOT}-svg`}
        role="img"
        aria-labelledby={titleId}
        viewBox={`0 0 ${SVG_WIDTH} ${plotHeight}`}
        className="w-full"
      >
        <title id={titleId}>{t(locale, "aiBenchCapabilityChartTitle")}</title>

        <Axis max={COMPOSITE_INDEX_MAX} width={SVG_WIDTH} label={axisLabel} formattedMax={formattedMax} y={14} />

        {bands.map((bandLayout) => (
          <BandGroup
            key={bandLayout.band}
            band={bandLayout.band}
            label={bandLayout.label}
            x={PLOT_X}
            y={bandLayout.headerY}
            testId={`${SLOT}-band-${bandLayout.band}`}
          >
            {bandLayout.rows.map(({ score, rowTop }) => {
              const index = score.index ?? 0; // an anchor pinned by id can lack an index (bands.ts:56-58); 0 keeps the bar total
              const barY = rowTop + 12;
              const barWidth = scale(index);
              const valueText = formatIndex(index, locale);
              const labelText = `${score.model.name} — ${valueText}`;
              const isLowCoverage = score.coverage > 0 && score.coverage < LOW_COVERAGE_THRESHOLD;
              return (
                <g key={score.model.id} data-testid={`${SLOT}-row-${score.model.id}`}>
                  {/* Mobile: label + value ABOVE the bar (below `md`). */}
                  <text
                    data-slot="chart-bar-label"
                    data-testid={`${SLOT}-label-mobile-${score.model.id}`}
                    x={PLOT_X}
                    y={rowTop + 8}
                    className="fill-foreground text-[10px] md:hidden"
                  >
                    {labelText}
                  </text>
                  {/* `md`/`lg`: left-gutter label beside the bar. */}
                  <text
                    data-slot="chart-bar-label"
                    data-testid={`${SLOT}-label-desktop-${score.model.id}`}
                    x={PLOT_X - 8}
                    y={barY + BAR_HEIGHT - 4}
                    textAnchor="end"
                    className="hidden fill-foreground text-[10px] md:block"
                  >
                    {labelText}
                  </text>
                  <Bar
                    x={PLOT_X}
                    y={barY}
                    width={barWidth}
                    height={BAR_HEIGHT}
                    band={bandLayout.band}
                    testId={`${SLOT}-bar-${score.model.id}`}
                  />
                  {isLowCoverage ? (
                    <text
                      data-slot="chart-low-coverage-marker"
                      data-testid={`${SLOT}-low-coverage-${score.model.id}`}
                      x={PLOT_X + barWidth + 6}
                      y={barY + BAR_HEIGHT - 4}
                      className="fill-muted-foreground text-[9px]"
                    >
                      {t(locale, "aiBenchCoverageLow")} ({formatCoverage(score.coverage, locale)})
                    </text>
                  ) : null}
                </g>
              );
            })}
          </BandGroup>
        ))}

        {/* `lg`-only tick row — {@link TICK_COUNT} + 1 evenly spaced values over the axis max. */}
        <TickRow
          testId={`${SLOT}-ticks`}
          tickTestId={`${SLOT}-tick`}
          values={evenTicks(COMPOSITE_INDEX_MAX, TICK_COUNT)}
          x={(v) => PLOT_X + scale(v)}
          y={tickRowY}
          format={(v) => formatIndex(v, locale)}
        />
      </svg>

      <Legend items={legendItems} />

      {groups.unrated.length > 0 ? (
        <div data-slot={`${SLOT}-unrated`} data-testid={`${SLOT}-unrated`} className="mt-3">
          <h3 id={unratedHeadingId} data-testid={`${SLOT}-unrated-heading`} className="text-sm font-semibold">
            {bandLabel("unrated", locale)}
          </h3>
          <ul
            aria-labelledby={unratedHeadingId}
            className="mt-1 flex flex-wrap gap-x-3 gap-y-1 text-sm text-muted-foreground"
          >
            {groups.unrated.map((score) => (
              <li key={score.model.id} data-testid={`${SLOT}-unrated-model-${score.model.id}`}>
                {score.model.name}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
