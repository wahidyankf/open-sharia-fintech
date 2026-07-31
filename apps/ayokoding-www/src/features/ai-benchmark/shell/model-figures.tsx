// AI BENCHMARK — shared per-model figure builders (Phase 6, DD-28/W-26/W-30).
//
// The desktop table and the mobile roster card must render the IDENTICAL set of figures for every
// model (W-26), and — once the card gains a collapsed summary plus an expanded disclosure — the
// card's summary and its expanded content TOGETHER must still carry every figure the table's row
// carries (W-30, AC-54). Hoisting the per-model figure builders here, out of `model-table.tsx`,
// lets `model-table.tsx` and `model-card.tsx` both call the SAME functions rather than maintaining
// two copies that could drift apart — parity becomes structural rather than asserted by
// duplication.
//
// FCIS boundary: no literal score, price, model name, or threshold lives here — every number comes
// from the passed `model`/`dataset` via the pure `core/` selectors, formatted by `shell/format.ts`.

import type { ReactNode } from "react";
import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import { computeGroups, type Band, type ModelScore } from "../core/bands";
import { isConflictedFigure, type Dataset, type Figure, type Model } from "../core/data/models";
import { LOW_COVERAGE_THRESHOLD } from "../core/score";
import { lowestRate } from "../core/price";
import { BAND_LABEL_KEYS, BENCHMARK_COLUMNS } from "../core/data/benchmarks";
import { formatCoverage, formatIndex, formatPercent, formatPriceUsd } from "./format";
import { FigureCell, type FigureLayout } from "./figure-cell";

/** Per-model scored view: band, composite index, and coverage derived from the pure core. */
export type ScoreView = {
  band: ModelScore["band"];
  index: number | undefined;
  coverage: number;
};

/**
 * Build the roster-relative index/coverage/band for every model in one scoring pass. `fullDataset`
 * (defaulting to `dataset` itself) is ALWAYS the source for the anchor thresholds and roster-max
 * map — `dataset` may be a harness/class-filtered subset, and re-deriving thresholds from it would
 * silently collapse every rated model to `haiku` when the filter excludes both anchor models
 * (DD-5a: bands are roster-relative to the FULL population; filtering governs display only).
 */
export function computeScoreViews(dataset: Dataset, fullDataset: Dataset = dataset): Map<string, ScoreView> {
  const groups = computeGroups(dataset, fullDataset);
  const byId = new Map<string, ScoreView>();
  for (const list of [groups.opus, groups.sonnet, groups.haiku, groups.unrated]) {
    for (const s of list) {
      byId.set(s.model.id, { band: s.band, index: s.index, coverage: s.coverage });
    }
  }
  return byId;
}

/** The model's localized class label. */
export function classLabel(band: Band, locale: Locale): string {
  const key = BAND_LABEL_KEYS[band];
  return key ? t(locale, key) : band;
}

/** Find the model's published figure for a benchmark (absent → undefined, rendered as "not reported"). */
export function figureFor(model: Model, benchmark: string): Figure | undefined {
  return model.figures.find((f) => f.benchmark === benchmark);
}

/** A benchmark score cell: a range for a conflicted figure, otherwise a single value; "—" when absent. */
export function benchmarkCell(
  model: Model,
  benchmarkId: string,
  locale: Locale,
  layout: FigureLayout = "stacked",
): ReactNode {
  const f = figureFor(model, benchmarkId);
  if (!f) {
    return <span data-slot="figure-cell-value">{t(locale, "aiBenchNoFigure")}</span>;
  }
  if (isConflictedFigure(f)) {
    return (
      <FigureCell
        value={formatPercent(f.low, locale)}
        highValue={formatPercent(f.high, locale)}
        grade={f.grade}
        source={f.source}
        locale={locale}
        layout={layout}
      />
    );
  }
  return (
    <FigureCell
      value={formatPercent(f.value, locale)}
      grade={f.grade}
      source={f.source}
      locale={locale}
      layout={layout}
    />
  );
}

/** The composite-index cell, or "not reported" for an unrated model. */
export function indexCell(view: ScoreView, locale: Locale, layout: FigureLayout = "stacked"): ReactNode {
  if (view.index === undefined) {
    return <span data-slot="figure-cell-value">{t(locale, "aiBenchNoFigure")}</span>;
  }
  return (
    <FigureCell
      value={formatIndex(view.index, locale)}
      grade="verified"
      source={defaultSourceForIndex()}
      locale={locale}
      layout={layout}
    />
  );
}

/** Low-coverage flag derived from the score view's coverage ratio against the core threshold. */
export function isLowCoverageView(view: ScoreView): boolean {
  return view.index !== undefined && view.coverage > 0 && view.coverage < LOW_COVERAGE_THRESHOLD;
}

/** The coverage cell; low-coverage rated models carry an advisory marker (text, not colour alone). */
export function coverageCell(view: ScoreView, locale: Locale, layout: FigureLayout = "stacked"): ReactNode {
  const text = formatCoverage(view.coverage, locale);
  const low = isLowCoverageView(view);
  // Routes through the AyoKoding `--evidence-self-reported` token (an alias onto `--hue-honey-ink`,
  // `libs/web-ui-token/src/ayokoding.css`) rather than raw `text-amber-700 dark:text-amber-400`
  // (Rule-15 DWT-002 fix) — `--hue-honey-ink` already clears WCAG AA's 4.5:1 text minimum in both
  // themes (it is the same tone `hero.tsx` already uses for its own links), and resolves
  // automatically per-theme from the one class, no `dark:` variant needed.
  // Same `layout` contract as `FigureCell` (DD-34 Treatment 2) — this cell has its own
  // `inline-flex flex-col` shape rather than delegating to `FigureCell`, so it threads the prop
  // through independently rather than sharing a component.
  const layoutClass =
    layout === "inline"
      ? "inline-flex flex-row flex-wrap items-baseline gap-x-1.5"
      : "inline-flex flex-col items-start gap-0.5 leading-tight";
  return (
    <span data-slot="coverage-cell" className={layoutClass}>
      <span data-slot="figure-cell-value">{text}</span>
      {low ? (
        <span className="text-xs text-[var(--evidence-self-reported)]">{t(locale, "aiBenchCoverageLow")}</span>
      ) : null}
    </span>
  );
}

/** The source cited for the composite index — the dataset's own methodology page is not a figure. */
export function defaultSourceForIndex(): string {
  return "https://ayokoding.com/tools/ai-benchmark";
}

/** Input/output price cells from the model's lowest available rate. */
export function priceCells(
  model: Model,
  locale: Locale,
  layout: FigureLayout = "stacked",
): { input: ReactNode; output: ReactNode; isSubscription: boolean } {
  const rate = lowestRate(model);
  if (rate && rate.kind === "metered") {
    return {
      isSubscription: false,
      input: (
        <FigureCell
          value={formatPriceUsd(rate.input, locale)}
          grade={rate.grade}
          source={rate.source}
          locale={locale}
          layout={layout}
        />
      ),
      output: (
        <FigureCell
          value={formatPriceUsd(rate.output, locale)}
          grade={rate.grade}
          source={rate.source}
          locale={locale}
          layout={layout}
        />
      ),
    };
  }
  if (rate && rate.kind === "subscription") {
    // A flat-rate subscription is one price covering both directions — there is no separate
    // input/output split to report, so both cells show the same graded, sourced figure via the
    // shared FigureCell (grade marker for AC-21, source link for AC-30), never a bespoke unmarked
    // link.
    const subCell = (
      <FigureCell
        value={`${t(locale, "aiBenchSubscription")} (${formatPriceUsd(rate.planCostUsd, locale)})`}
        grade={rate.grade}
        source={rate.source}
        locale={locale}
        layout={layout}
      />
    );
    return { isSubscription: true, input: subCell, output: subCell };
  }
  // No price exists for this model at all (metered or subscription) — render exactly like an
  // absent benchmark figure: a plain "not reported" span, never a grade marker and never a source
  // link. A price that was never published must not resolve to a link (previously this fabricated
  // a self-referential citation via `defaultSourceForIndex()`, which was wrong — that helper is for
  // the composite index, whose source genuinely IS this page's own methodology, not for a missing
  // price).
  const notReported = <span data-slot="figure-cell-value">{t(locale, "aiBenchNoFigure")}</span>;
  return { input: notReported, output: notReported, isSubscription: false };
}

/** A model's integrity-note links, rendered beside its name (AC-33). */
export function integrityNotes(model: Model, locale: Locale): ReactNode {
  if (!model.notes || model.notes.length === 0) return null;
  return (
    <span data-slot="integrity-notes" className="mt-1 flex flex-wrap gap-2">
      {model.notes.map((note, i) => (
        <a
          key={`${note.modelId}-${i}`}
          data-slot="integrity-note"
          href={note.source}
          target="_blank"
          rel="noopener noreferrer nofollow"
          // Same `--evidence-self-reported` token as the coverage marker above (Rule-15 DWT-002 fix).
          className="text-xs font-medium text-[var(--evidence-self-reported)] underline decoration-dotted underline-offset-2"
          aria-label={`${t(locale, "aiBenchIntegrityLabel")}: ${note.text}`}
          title={note.text}
        >
          {t(locale, "aiBenchIntegrityLabel")}
        </a>
      ))}
    </span>
  );
}

/**
 * One shared per-model figure: a localized label paired with its rendered node. `reported`
 * (DD-34 Treatment 4, DN-4 fix) defaults to `true` — only a benchmark figure the model never
 * published sets it `false`, so `ModelDetailDisclosure` can collapse every unpublished figure in a
 * group into one shared "not reported" name-value pair instead of giving each one its own full
 * field slot at the same weight as a real, measured figure.
 */
export type ModelFigure = { label: string; node: ReactNode; reported?: boolean };

// DD-34 Treatment 1 (DN-1 fix): a detail-region field's VALUE must out-rank its own LABEL on every
// one of the three encodings CSS offers — size, weight, and colour — never the label-first
// convention body text defaults to. Named here, beside the figure builders both `model-card.tsx`
// and `model-table.tsx`'s detail region already share, so the two callers cannot drift back apart
// on any one of the three (consumed by `model-detail-disclosure.tsx`, the one place both render
// through).
export const DETAIL_FIELD_LABEL_CLASS = "text-xs font-normal text-muted-foreground";
export const DETAIL_FIELD_VALUE_CLASS = "text-sm font-semibold text-foreground";

/**
 * The four composite-benchmark figures, in column order — shared by the table and the card (W-26).
 * `layout` (DD-34 Treatment 2) is passed straight through to each figure's own `FigureCell` — it
 * never changes which four figures are built, only how each one's value and badge lay out.
 */
export function renderBenchmarkFigures(model: Model, locale: Locale, layout: FigureLayout = "stacked"): ModelFigure[] {
  return BENCHMARK_COLUMNS.map((col) => ({
    label: t(locale, col.labelKey),
    node: benchmarkCell(model, col.id, locale, layout),
    reported: model.figures.some((f) => f.benchmark === col.id),
  }));
}

/**
 * The four non-benchmark figures — index, coverage, input price, output price — in a fixed order,
 * shared by the table and the card (W-26/W-30). The card's summary picks index/input/output price
 * out of this list by label match; the remaining entry (coverage) joins the card's expanded
 * content, so parity across summary + details holds by construction rather than by a second
 * hand-maintained list. `layout` (DD-34 Treatment 2) threads through identically to
 * `renderBenchmarkFigures` — callers build this list TWICE where the summary and the detail region
 * want different layouts for the SAME underlying figures (see `model-card.tsx`/`model-table.tsx`).
 */
export function renderStaticFigures(
  model: Model,
  view: ScoreView,
  locale: Locale,
  layout: FigureLayout = "stacked",
): ModelFigure[] {
  const prices = priceCells(model, locale, layout);
  return [
    { label: t(locale, "aiBenchColIndex"), node: indexCell(view, locale, layout) },
    { label: t(locale, "aiBenchColCoverage"), node: coverageCell(view, locale, layout) },
    { label: t(locale, "aiBenchColInputPrice"), node: prices.input },
    { label: t(locale, "aiBenchColOutputPrice"), node: prices.output },
  ];
}

/** One labelled group of detail-region figures, rendered as its own `<section>` (DD-34 Treatment 3). */
export type FigureGroup = { heading: string; figures: ModelFigure[] };

/**
 * DD-34 Treatment 3 (DN-3 fix): splits a model's detail-region figures into the two labelled groups
 * `ModelDetailDisclosure` renders as separate `<section>`s — a "Model" group (vendor/harnesses,
 * whatever metadata the caller passes) and a "Scores" group (every benchmark figure plus coverage).
 * Coverage groups with the benchmarks rather than with vendor/harnesses because it is DERIVED from
 * them — coverage measures how many of the composite benchmarks this model actually reports, so it
 * belongs with what it measures, not with unrelated metadata. One shared composition, called
 * identically by `model-card.tsx` and `model-table.tsx`'s detail region, so the two callers cannot
 * build a different grouping for the same figure set.
 */
export function buildDetailGroups(
  modelMetaFigures: ModelFigure[],
  scoreFigures: ModelFigure[],
  locale: Locale,
): FigureGroup[] {
  return [
    { heading: t(locale, "aiBenchCardGroupModel"), figures: modelMetaFigures },
    { heading: t(locale, "aiBenchCardGroupScores"), figures: scoreFigures },
  ];
}

/** The index/input-price/output-price figures picked out of `renderStaticFigures`'s list, plus everything else. */
export type StaticFigurePartition = {
  index: ModelFigure | undefined;
  input: ModelFigure | undefined;
  output: ModelFigure | undefined;
  rest: ModelFigure[];
};

/**
 * Splits `renderStaticFigures`'s output into the three figures a summary shows (index, input price,
 * output price) and everything else (coverage). Both `model-card.tsx`'s summary and
 * `model-table.tsx`'s primary columns need this exact split — sharing it here (rather than each
 * re-implementing its own label match) keeps the split the ONE place that decides what counts as
 * "primary" (W-30: parity holds by construction, not by two hand-synchronized lists).
 */
export function partitionStaticFigures(figures: ModelFigure[], locale: Locale): StaticFigurePartition {
  const indexLabel = t(locale, "aiBenchColIndex");
  const inputLabel = t(locale, "aiBenchColInputPrice");
  const outputLabel = t(locale, "aiBenchColOutputPrice");
  return {
    index: figures.find((f) => f.label === indexLabel),
    input: figures.find((f) => f.label === inputLabel),
    output: figures.find((f) => f.label === outputLabel),
    rest: figures.filter((f) => f.label !== indexLabel && f.label !== inputLabel && f.label !== outputLabel),
  };
}
