"use client";

// AI BENCHMARK — merged capability + price chart (Phase 2). Replaces the two separate,
// now-retired chart components (Phase 3 deleted them) with ONE chart where
// each rated model's row carries its capability bar and both price bars stacked together — see
// `tech-docs.md`'s "Prior-Plan Rejection Precedent" for why this is a genuinely different layout
// from the previously-rejected Option C, and DD-1/DD-2/DD-8 for the per-row rendering decisions
// this file implements.
//
// Phase 5 (DD-25): this file no longer emits any SVG element at all — every bar is a DOM `BarRow` (see
// `bar-row.tsx`) whose fill is a plain percentage-width `<div>`, so declared typography never
// scales with viewport width (DD-26 reverses the identical-DOM-at-every-breakpoint strategy the
// prior plan chose, because a `viewBox`'s uniform scale factor and breakpoint-independent
// typography are mutually exclusive). DD-31 retires DWT-001 (right-margin marker clip) and DWT-004
// (band-header/first-row baseline overlap) as SVG-geometry concerns — see
// `benchmark-chart.test.tsx`'s "DD-31 — replacements for the retired SVG-geometry guards" describe
// block for the DOM-sibling guards that now protect the same underlying regressions.
//
// FCIS boundary: no literal benchmark score, price, model name, or class threshold lives here —
// every number and name comes from the passed `dataset` via `core/bands.ts`/`core/price.ts`; every
// colour comes from `chart-primitives.tsx`'s band-token maps.

import { useId } from "react";
import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import { dataset as defaultDataset, type Dataset, type HarnessId } from "../core/data/models";
import { computeGroups, type ModelScore } from "../core/bands";
import { BANDS } from "../core/filter";
import { COMPOSITE_INDEX_MAX, LOW_COVERAGE_THRESHOLD } from "../core/score";
import { lowestRate, rateForHarness } from "../core/price";
import { byCapabilityDesc, byPriceAsc, byPriceDesc, isKnownSortMode, SORT_MODES, type SortMode } from "../core/sort";
import { DEFAULT_SORT_STATE, type SortState } from "../core/url-state";
import { formatCoverage, formatIndex, formatPriceUsd } from "./format";
import { bandInkTextClass, bandLabel, type ChartBand } from "./chart-primitives";
import { BarRow } from "./bar-row";
import { FilterSelect, type FilterOption } from "./benchmark-filters";

const SLOT = "benchmark-chart";

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

type BandLayout = {
  band: RatedBand;
  label: string;
  rows: ModelScore[];
};

/**
 * Each rated band gets its OWN independent row list — this is the UWT-002 fix (Rule-15
 * web-usability-tester retest, 2026-07-30): each band renders as its own DOM region (below, one
 * `<div role="group">` per `BandLayout`), so each band's own sort control sits directly above its
 * own rows rather than every control clustering together above one shared chart. `priceAxisMaxOf`
 * below still computes its max over ALL bands' rows combined (AC-40: the price axis is deliberately
 * SHARED across bands, not per-band) — Phase 5's DOM rewrite changed only how bands are RENDERED,
 * never how their bars are SCALED.
 */
function computeLayout(
  groups: Record<ChartBand, ModelScore[]>,
  sortState: SortState,
  locale: Locale,
  harness?: HarnessId,
): { bands: BandLayout[] } {
  const bands: BandLayout[] = [];
  for (const band of RATED_BANDS) {
    const rows = sortBand(groups[band], sortState[band], harness);
    bands.push({ band, label: bandLabel(band, locale), rows });
  }
  return { bands };
}

type BenchmarkRowProps = {
  score: ModelScore;
  band: ChartBand;
  locale: Locale;
  /** The chart's shared price-axis domain maximum (AC-40) — every price `BarRow` scales against it. */
  priceAxisMax: number;
  rate: ReturnType<typeof lowestRate>;
};

/**
 * One rated model's row: a name/index label, a capability `BarRow`, and either two price
 * `BarRow`s (metered), inline subscription text (DD-1), or a "not reported" placeholder.
 *
 * DD-31: the low-coverage marker renders as a sibling of the capability `BarRow`, never nested
 * inside its track — this is what makes it un-clippable (DWT-001's replacement guard) rather than
 * a margin big enough to avoid a `viewBox` edge that no longer exists.
 */
function BenchmarkRow({ score, band, locale, priceAxisMax, rate }: BenchmarkRowProps) {
  const id = score.model.id;
  const index = score.index ?? 0;
  const isLowCoverage = score.coverage > 0 && score.coverage < LOW_COVERAGE_THRESHOLD;

  return (
    <div data-testid={`${SLOT}-row-${id}`} className="mb-3 lg:grid lg:grid-cols-[10rem_1fr] lg:items-start lg:gap-x-4">
      <p
        data-slot="chart-bar-label"
        data-testid={`${SLOT}-label-${id}`}
        className="text-[10px] font-medium text-foreground lg:col-start-1"
      >
        {score.model.name} — {formatIndex(index, locale)}
      </p>
      <div className="lg:col-start-2">
        <BarRow
          value={index}
          max={COMPOSITE_INDEX_MAX}
          band={band}
          label={t(locale, "aiBenchColIndex")}
          testId={`${SLOT}-bar-capability-${id}`}
        />
        {isLowCoverage ? (
          <p
            data-slot="chart-low-coverage-marker"
            data-testid={`${SLOT}-low-coverage-${id}`}
            className="text-[9px] text-muted-foreground"
          >
            {t(locale, "aiBenchCoverageLow")} ({formatCoverage(score.coverage, locale)})
          </p>
        ) : null}
        {rate?.kind === "metered" ? (
          <>
            <BarRow
              value={rate.input}
              max={priceAxisMax}
              band={band}
              label={`${t(locale, "aiBenchColInputPrice")}: ${formatPriceUsd(rate.input, locale)}`}
              testId={`${SLOT}-bar-price-in-${id}`}
            />
            <BarRow
              value={rate.output}
              max={priceAxisMax}
              band={band}
              label={`${t(locale, "aiBenchColOutputPrice")}: ${formatPriceUsd(rate.output, locale)}`}
              testId={`${SLOT}-bar-price-out-${id}`}
            />
          </>
        ) : rate?.kind === "subscription" ? (
          <p
            data-slot="chart-subscription-label"
            data-testid={`${SLOT}-subscription-${id}`}
            className="text-[10px] text-muted-foreground"
          >
            {t(locale, "aiBenchSubscription")} ({formatPriceUsd(rate.planCostUsd, locale)})
          </p>
        ) : (
          <p
            data-slot="chart-not-reported-label"
            data-testid={`${SLOT}-not-reported-${id}`}
            className="text-[10px] text-muted-foreground"
          >
            {t(locale, "aiBenchNoFigure")}
          </p>
        )}
      </div>
    </div>
  );
}

/** The highest metered input or output rate among every rendered row — the price axis's domain maximum. */
function priceAxisMaxOf(bands: BandLayout[], harness?: HarnessId): number {
  let max = 0;
  for (const b of bands) {
    for (const score of b.rows) {
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
  const { bands } = computeLayout(groups, sortState, locale, harness);
  const priceAxisMax = priceAxisMaxOf(bands, harness);
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

      {/* UWT-002 fix (Rule-15 web-usability-tester retest, 2026-07-30): each band gets its OWN
          sort control directly above its OWN labelled DOM region, instead of all three controls
          clustering together above one shared multi-band chart (previously the reordering a
          control caused could scroll 3000px+ out of view before the reader reached it). Each
          band's region below is independently self-contained. */}
      {bands.map((bandLayout) => {
        const bandTitleId = `${titleId}-${bandLayout.band}`;
        return (
          <div key={bandLayout.band} data-testid={`${SLOT}-band-wrapper-${bandLayout.band}`} className="mb-4">
            {onSortChange ? (
              <div className="mb-2">
                <FilterSelect
                  id={`${SLOT}-sort-${bandLayout.band}`}
                  label={`${sortLabelPrefix} — ${bandLayout.label}`}
                  value={sortState[bandLayout.band]}
                  options={sortOptions}
                  // No `allLabel` here (deliberately): sort has no "no sort" state, unlike a
                  // filter's legitimate "no filter on this axis" empty option — passing one
                  // produced a duplicate "Capability" option and an invalid `"" as SortMode` cast
                  // on change (pr-review-synthesis-maker HIGH finding). `isKnownSortMode` narrows
                  // instead.
                  onChange={(value) => {
                    if (isKnownSortMode(value)) onSortChange(bandLayout.band, value);
                  }}
                />
              </div>
            ) : null}

            {/* DD-31: the band header (`<h3>`) and axis-max caption (`<p>`) are ordinary block-level
                siblings of the first row's own `<div>` below, not fused into one element — this is
                what replaces DWT-004's overlap guard (block boxes cannot overlap without explicit
                negative margin or absolute positioning, neither of which this markup uses). */}
            <div
              data-slot="chart-band-group"
              data-testid={`${SLOT}-band-${bandLayout.band}`}
              data-band={bandLayout.band}
              role="group"
              aria-labelledby={bandTitleId}
            >
              <h3
                id={bandTitleId}
                data-slot="chart-band-group-label"
                data-testid={`${SLOT}-band-${bandLayout.band}-label`}
                className={`text-xs font-semibold ${bandInkTextClass(bandLayout.band)}`}
              >
                {bandLayout.label}
              </h3>
              <p
                data-slot="chart-axis-max"
                data-testid="chart-axis-max"
                className="mb-2 text-[10px] text-muted-foreground"
              >
                {axisLabel}: {formattedMax}
              </p>
              {bandLayout.rows.map((score) => (
                <BenchmarkRow
                  key={score.model.id}
                  score={score}
                  band={bandLayout.band}
                  locale={locale}
                  priceAxisMax={priceAxisMax}
                  rate={harness !== undefined ? rateForHarness(score.model, harness) : lowestRate(score.model)}
                />
              ))}
            </div>
          </div>
        );
      })}

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
                  ) : rate?.kind === "metered" ? (
                    // Rule-15 UWT-001 fix (2026-07-30, partial fix by user decision): show the
                    // price as TEXT (not a bar, no sort control) — this deliberately does not give
                    // Unrated the full bar+sort treatment the other three bands get, since DD-1
                    // already decided (Phase 2, reviewed) that unrated models render as plain text
                    // because they have no comparable capability score to bar against. Before this
                    // fix, a metered-priced unrated model showed ONLY its bare name here, even
                    // though the same price was visible two sections down in ModelTable.
                    <>
                      {score.model.name} — {t(locale, "aiBenchColInputPrice")}: {formatPriceUsd(rate.input, locale)},{" "}
                      {t(locale, "aiBenchColOutputPrice")}: {formatPriceUsd(rate.output, locale)}
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
