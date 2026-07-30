"use client";

// AI BENCHMARK — merged capability + price chart (Phase 2). Replaces the two separate,
// now-retired chart components (Phase 3 deleted them) with ONE chart where
// each rated model's row carries its capability bar and both price bars stacked together — see
// `tech-docs.md`'s "Prior-Plan Rejection Precedent" for why this is a genuinely different layout
// from the previously-rejected Option C, and DD-1/DD-2/DD-8 for the per-row rendering decisions
// this file implements.
//
// FCIS boundary: no literal benchmark score, price, model name, or class threshold lives here —
// every number and name comes from the passed `dataset` via `core/bands.ts`/`core/price.ts`; every
// colour comes from `chart-primitives.tsx`'s band-token maps.

import { useId } from "react";
import { t } from "@/features/i18n/core/translations";
import { SUPPORTED_LOCALES, type Locale } from "@/features/i18n/core/config";
import { dataset as defaultDataset, type Dataset, type HarnessId } from "../core/data/models";
import { computeGroups, type ModelScore } from "../core/bands";
import { BANDS } from "../core/filter";
import { COMPOSITE_INDEX_MAX, LOW_COVERAGE_THRESHOLD } from "../core/score";
import { lowestRate, rateForHarness } from "../core/price";
import { byCapabilityDesc, byPriceAsc, byPriceDesc, isKnownSortMode, SORT_MODES, type SortMode } from "../core/sort";
import { DEFAULT_SORT_STATE, type SortState } from "../core/url-state";
import { formatCoverage, formatIndex, formatPriceUsd } from "./format";
import { Axis, Bar, BandGroup, bandLabel, scaleLinear, type ChartBand } from "./chart-primitives";
import { FilterSelect, type FilterOption } from "./benchmark-filters";

const SLOT = "benchmark-chart";

// ─── Layout constants (display-only — never a benchmark score, price, or threshold) ───────────
//
// PLOT_WIDTH is DERIVED from a reserved right margin, never hardcoded — this is the DWT-001 fix
// (originally found and fixed in the retired `capability-chart.tsx`, then REGRESSED here when this
// file replaced it with a hardcoded `PLOT_WIDTH = 380`, which let the right margin fall out to 80
// — under the 140-unit clip floor this defect's live investigation found — and clipped the
// low-coverage marker text off the SVG's right edge for any sufficiently long capability bar).
// `MARKER_MIN_MARGIN` is a documented, generous estimate of the SVG user-unit width the longest
// localized low-coverage marker string (`aiBenchCoverageLow` + a worst-case "(100%)" percentage —
// wider than any real dataset value, used only as a safe upper bound) needs at `text-[9px]`,
// computed across every supported locale so none of them clips. `MARKER_CHAR_WIDTH_RATIO` is a
// conservative average glyph-advance-width-to-font-size ratio for a proportional sans-serif font;
// `MARKER_SAFETY_BUFFER` cushions the estimate above that ~140-unit clip threshold. See
// `benchmark-chart.test.tsx`'s "DWT-001 right-margin regression" block for the regression guard
// this margin is locked by, and delivery.md's Phase 6 evidence section for the live Playwright
// re-verification this fix required (screenshots regenerated after this change).
const SVG_WIDTH = 640;
const PLOT_X = 180; // left gutter reserved for the md/lg left-gutter label
const MARKER_FONT_SIZE = 9; // matches the marker `<text>`'s `text-[9px]`
const MARKER_GAP = 6; // matches `x={PLOT_X + capWidth + 6}` below — the gap before the marker text
const MARKER_CHAR_WIDTH_RATIO = 0.62;
const MARKER_SAFETY_BUFFER = 40;
const WORST_CASE_MARKER_LENGTH = Math.max(
  ...SUPPORTED_LOCALES.map((locale) => `${t(locale, "aiBenchCoverageLow")} (${formatCoverage(1, locale)})`.length),
);
export const MARKER_MIN_MARGIN =
  MARKER_GAP + Math.ceil(WORST_CASE_MARKER_LENGTH * MARKER_FONT_SIZE * MARKER_CHAR_WIDTH_RATIO) + MARKER_SAFETY_BUFFER;
const PLOT_WIDTH = SVG_WIDTH - PLOT_X - MARKER_MIN_MARGIN;
export { SVG_WIDTH, PLOT_X, PLOT_WIDTH };
const ROW_HEIGHT = 56; // room for the capability bar + two stacked price bars within one row
const BAR_HEIGHT = 12;
const BAR_GAP = 3;
const BAND_HEADER_HEIGHT = 22;
const BAND_GAP = 16;
const TOP_MARGIN = 24; // room for the always-visible axis-maximum label

// Only rated bands render rows (a row needs a capability bar) — mirrors the retired capability chart's
// `RATED_BANDS`, derived from `core/filter.ts`'s `BANDS` (F-9) rather than re-declared here.
//
// `RatedBand` (excludes `"unrated"` at the TYPE level, not just at runtime) is what lets
// `sortState[band]` below type-check against {@link SortState}, which has no `unrated` key — the
// `unrated` band has no sort state to index (it is never sorted; see `SORT_PARAM_KEYS`'s docstring
// in `core/url-state.ts`).
type RatedBand = Exclude<ChartBand, "unrated">;
const RATED_BANDS: readonly RatedBand[] = BANDS.filter((band): band is RatedBand => band !== "unrated");

/**
 * Applies a band's chosen {@link SortMode} to its `computeGroups()` array — DD-4. `harness`
 * (DD-8/AC-18) is threaded through to the price comparators so an active harness filter sorts by
 * THAT harness's own rate, matching the same rate `rate={harness !== undefined ? rateForHarness(...)
 * : lowestRate(...)}` plots per row below — otherwise sort order and displayed price can diverge
 * (pr-review-synthesis-maker HIGH finding).
 */
function sortBand(scores: ModelScore[], mode: SortMode, harness?: HarnessId): ModelScore[] {
  const comparator =
    mode === "price-asc"
      ? (a: ModelScore, b: ModelScore) => byPriceAsc(a, b, harness)
      : mode === "price-desc"
        ? (a: ModelScore, b: ModelScore) => byPriceDesc(a, b, harness)
        : byCapabilityDesc;
  return [...scores].sort(comparator);
}

type RowLayout = {
  score: ModelScore;
  rowTop: number;
};

type BandLayout = {
  band: RatedBand;
  label: string;
  headerY: number;
  rows: RowLayout[];
};

function computeLayout(
  groups: Record<ChartBand, ModelScore[]>,
  sortState: SortState,
  locale: Locale,
  harness?: HarnessId,
): { bands: BandLayout[]; plotHeight: number } {
  let cursor = TOP_MARGIN;
  const bands: BandLayout[] = [];
  for (const band of RATED_BANDS) {
    const scores = sortBand(groups[band], sortState[band], harness);
    const headerY = cursor + BAND_HEADER_HEIGHT - 8;
    const rowsTop = cursor + BAND_HEADER_HEIGHT;
    const rows = scores.map((score, i) => ({ score, rowTop: rowsTop + i * ROW_HEIGHT }));
    bands.push({ band, label: bandLabel(band, locale), headerY, rows });
    cursor = rowsTop + scores.length * ROW_HEIGHT + BAND_GAP;
  }
  return { bands, plotHeight: cursor };
}

type BenchmarkRowProps = {
  score: ModelScore;
  rowTop: number;
  band: ChartBand;
  locale: Locale;
  capabilityScale: (value: number) => number;
  priceScale: (value: number) => number;
  rate: ReturnType<typeof lowestRate>;
};

/**
 * One rated model's row: name/index label, a capability bar, and either two price bars (metered),
 * inline subscription text (DD-1), or a "not reported" placeholder — extracted from the four-band
 * loop above so that loop stays readable (REFACTOR step).
 */
function BenchmarkRow({ score, rowTop, band, locale, capabilityScale, priceScale, rate }: BenchmarkRowProps) {
  const id = score.model.id;
  const index = score.index ?? 0;
  const capBarY = rowTop + 4;
  const priceInY = capBarY + BAR_HEIGHT + BAR_GAP;
  const priceOutY = priceInY + BAR_HEIGHT + BAR_GAP;
  const capWidth = capabilityScale(index);
  const isLowCoverage = score.coverage > 0 && score.coverage < LOW_COVERAGE_THRESHOLD;

  return (
    <g data-testid={`${SLOT}-row-${id}`}>
      <text
        data-slot="chart-bar-label"
        data-testid={`${SLOT}-label-${id}`}
        x={PLOT_X}
        y={rowTop - 2}
        className="fill-foreground text-[10px]"
      >
        {score.model.name} — {formatIndex(index, locale)}
      </text>
      <Bar
        x={PLOT_X}
        y={capBarY}
        width={capWidth}
        height={BAR_HEIGHT}
        band={band}
        testId={`${SLOT}-bar-capability-${id}`}
      />
      {isLowCoverage ? (
        <text
          data-slot="chart-low-coverage-marker"
          data-testid={`${SLOT}-low-coverage-${id}`}
          x={PLOT_X + capWidth + 6}
          y={capBarY + BAR_HEIGHT - 4}
          className="fill-muted-foreground text-[9px]"
        >
          {t(locale, "aiBenchCoverageLow")} ({formatCoverage(score.coverage, locale)})
        </text>
      ) : null}
      {rate?.kind === "metered" ? (
        <>
          <text
            data-slot="chart-bar-label"
            data-testid={`${SLOT}-label-in-${id}`}
            x={PLOT_X - 8}
            y={priceInY + BAR_HEIGHT - 2}
            textAnchor="end"
            className="fill-muted-foreground text-[9px]"
          >
            {t(locale, "aiBenchColInputPrice")}: {formatPriceUsd(rate.input, locale)}
          </text>
          <Bar
            x={PLOT_X}
            y={priceInY}
            width={priceScale(rate.input)}
            height={BAR_HEIGHT}
            band={band}
            testId={`${SLOT}-bar-price-in-${id}`}
          />
          <text
            data-slot="chart-bar-label"
            data-testid={`${SLOT}-label-out-${id}`}
            x={PLOT_X - 8}
            y={priceOutY + BAR_HEIGHT - 2}
            textAnchor="end"
            className="fill-muted-foreground text-[9px]"
          >
            {t(locale, "aiBenchColOutputPrice")}: {formatPriceUsd(rate.output, locale)}
          </text>
          <Bar
            x={PLOT_X}
            y={priceOutY}
            width={priceScale(rate.output)}
            height={BAR_HEIGHT}
            band={band}
            testId={`${SLOT}-bar-price-out-${id}`}
          />
        </>
      ) : rate?.kind === "subscription" ? (
        <text
          data-slot="chart-subscription-label"
          data-testid={`${SLOT}-subscription-${id}`}
          x={PLOT_X}
          y={priceInY + BAR_HEIGHT}
          className="fill-muted-foreground text-[10px]"
        >
          {t(locale, "aiBenchSubscription")} ({formatPriceUsd(rate.planCostUsd, locale)})
        </text>
      ) : (
        <text
          data-slot="chart-not-reported-label"
          data-testid={`${SLOT}-not-reported-${id}`}
          x={PLOT_X}
          y={priceInY + BAR_HEIGHT}
          className="fill-muted-foreground text-[10px]"
        >
          {t(locale, "aiBenchNoFigure")}
        </text>
      )}
    </g>
  );
}

/** The highest metered input or output rate among every rendered row — the price axis's domain maximum. */
function priceAxisMaxOf(bands: BandLayout[], harness?: HarnessId): number {
  let max = 0;
  for (const b of bands) {
    for (const { score } of b.rows) {
      const rate = harness !== undefined ? rateForHarness(score.model, harness) : lowestRate(score.model);
      if (rate?.kind !== "metered") continue;
      if (rate.input > max) max = rate.input;
      if (rate.output > max) max = rate.output;
    }
  }
  return max;
}

export type BenchmarkChartProps = {
  dataset?: Dataset;
  /**
   * The full unfiltered roster — band thresholds are ALWAYS derived from this, never from
   * `dataset` alone (DD-5a, mirrored from both former charts). REQUIRED, not optional.
   */
  fullDataset: Dataset;
  locale: Locale;
  /** Per-band display-order choice (DD-4); defaults to all-capability when omitted. */
  sortState?: SortState;
  /**
   * The active harness filter (DD-8) — mirrors the retired price chart's existing `harness` prop
   * exactly. When set, every price bar shows THAT harness's own rate instead of each model's
   * lowest available harness rate.
   */
  harness?: HarnessId;
  /** Reports a per-band sort change (DD-4) — the caller owns merging it into its own `sortState`. */
  onSortChange?: (band: ChartBand, mode: SortMode) => void;
};

/** A sort mode's localized dropdown label (DD-4's three known modes — mirrors `bandLabel`'s pattern). */
function sortModeLabel(mode: SortMode, locale: Locale): string {
  const key =
    mode === "price-asc"
      ? "aiBenchSortPriceAsc"
      : mode === "price-desc"
        ? "aiBenchSortPriceDesc"
        : "aiBenchSortCapability";
  return t(locale, key);
}

export function BenchmarkChart({
  dataset = defaultDataset,
  fullDataset,
  locale,
  sortState = DEFAULT_SORT_STATE,
  harness,
  onSortChange,
}: BenchmarkChartProps) {
  const titleId = useId();

  const groups = computeGroups(dataset, fullDataset);
  const { bands, plotHeight } = computeLayout(groups, sortState, locale, harness);
  const priceAxisMax = priceAxisMaxOf(bands, harness);
  const capabilityScale = scaleLinear(COMPOSITE_INDEX_MAX, PLOT_WIDTH);
  const priceScale = scaleLinear(priceAxisMax, PLOT_WIDTH);
  const axisLabel = t(locale, "aiBenchChartAxisMaxLabel");
  const formattedMax = formatIndex(COMPOSITE_INDEX_MAX, locale);
  const sortLabelPrefix = t(locale, "aiBenchSortLabel");
  const sortOptions: FilterOption[] = SORT_MODES.map((mode) => ({ value: mode, label: sortModeLabel(mode, locale) }));

  return (
    <div data-slot={SLOT} data-testid={SLOT}>
      <h2 data-testid={`${SLOT}-heading`} className="mb-2 text-lg font-semibold">
        {t(locale, "aiBenchMergedChartTitle")}
      </h2>

      {/* AC-18: once a specific harness is selected, every row shows THAT harness's own rate, not
          the lowest across harnesses — the "lowest rate" subtitle would misstate that, so it only
          renders when no harness filter is active (mirrors the retired price chart's AC-17 subtitle). */}
      {harness === undefined ? (
        <p data-testid={`${SLOT}-subtitle`} className="mb-2 text-xs text-muted-foreground">
          {t(locale, "aiBenchPriceLowestSubtitle")}
        </p>
      ) : null}

      {onSortChange ? (
        <div data-testid={`${SLOT}-sort-controls`} className="mb-3 flex flex-wrap gap-3">
          {bands.map((bandLayout) => (
            <FilterSelect
              key={bandLayout.band}
              id={`${SLOT}-sort-${bandLayout.band}`}
              label={`${sortLabelPrefix} — ${bandLayout.label}`}
              value={sortState[bandLayout.band]}
              options={sortOptions}
              // No `allLabel` here (deliberately): sort has no "no sort" state, unlike a filter's
              // legitimate "no filter on this axis" empty option — passing one produced a
              // duplicate "Capability" option and an invalid `"" as SortMode` cast on change
              // (pr-review-synthesis-maker HIGH finding). `isKnownSortMode` narrows instead.
              onChange={(value) => {
                if (isKnownSortMode(value)) onSortChange(bandLayout.band, value);
              }}
            />
          ))}
        </div>
      ) : null}

      <svg
        data-testid={`${SLOT}-svg`}
        role="img"
        aria-labelledby={titleId}
        viewBox={`0 0 ${SVG_WIDTH} ${plotHeight}`}
        className="w-full"
      >
        <title id={titleId}>{t(locale, "aiBenchMergedChartTitle")}</title>

        <Axis
          max={COMPOSITE_INDEX_MAX}
          width={PLOT_X + PLOT_WIDTH}
          label={axisLabel}
          formattedMax={formattedMax}
          y={14}
        />

        {bands.map((bandLayout) => (
          <BandGroup
            key={bandLayout.band}
            band={bandLayout.band}
            label={bandLayout.label}
            x={PLOT_X}
            y={bandLayout.headerY}
            testId={`${SLOT}-band-${bandLayout.band}`}
          >
            {bandLayout.rows.map(({ score, rowTop }) => (
              <BenchmarkRow
                key={score.model.id}
                score={score}
                rowTop={rowTop}
                band={bandLayout.band}
                locale={locale}
                capabilityScale={capabilityScale}
                priceScale={priceScale}
                rate={harness !== undefined ? rateForHarness(score.model, harness) : lowestRate(score.model)}
              />
            ))}
          </BandGroup>
        ))}
      </svg>

      {groups.unrated.length > 0 ? (
        <div data-slot={`${SLOT}-unrated`} data-testid={`${SLOT}-unrated`} className="mt-3">
          <h3 data-testid={`${SLOT}-unrated-heading`} className="text-sm font-semibold">
            {bandLabel("unrated", locale)}
          </h3>
          <ul className="mt-1 flex flex-wrap gap-x-3 gap-y-1 text-sm text-muted-foreground">
            {groups.unrated.map((score) => {
              // DD-1: an unrated model has no row to attach inline subscription text to, so the
              // retired price chart's global subscription list per-item text is preserved
              // here for exactly this subset (a rated+subscription-only model instead gets the
              // inline `BenchmarkRow` treatment above — never both).
              const rate = harness !== undefined ? rateForHarness(score.model, harness) : lowestRate(score.model);
              return (
                <li key={score.model.id} data-testid={`${SLOT}-unrated-model-${score.model.id}`}>
                  {rate?.kind === "subscription" ? (
                    <>
                      {score.model.name} — {t(locale, "aiBenchSubscription")}:{" "}
                      {formatPriceUsd(rate.planCostUsd, locale)}
                      {rate.caps ? ` (${rate.caps})` : ""}
                    </>
                  ) : (
                    score.model.name
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
