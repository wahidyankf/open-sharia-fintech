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
import { FigureCell } from "./figure-cell";

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
export function benchmarkCell(model: Model, benchmarkId: string, locale: Locale): ReactNode {
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
      />
    );
  }
  return <FigureCell value={formatPercent(f.value, locale)} grade={f.grade} source={f.source} locale={locale} />;
}

/** The composite-index cell, or "not reported" for an unrated model. */
export function indexCell(view: ScoreView, locale: Locale): ReactNode {
  if (view.index === undefined) {
    return <span data-slot="figure-cell-value">{t(locale, "aiBenchNoFigure")}</span>;
  }
  return (
    <FigureCell
      value={formatIndex(view.index, locale)}
      grade="verified"
      source={defaultSourceForIndex()}
      locale={locale}
    />
  );
}

/** Low-coverage flag derived from the score view's coverage ratio against the core threshold. */
export function isLowCoverageView(view: ScoreView): boolean {
  return view.index !== undefined && view.coverage > 0 && view.coverage < LOW_COVERAGE_THRESHOLD;
}

/** The coverage cell; low-coverage rated models carry an advisory marker (text, not colour alone). */
export function coverageCell(view: ScoreView, locale: Locale): ReactNode {
  const text = formatCoverage(view.coverage, locale);
  const low = isLowCoverageView(view);
  // Routes through the AyoKoding `--evidence-self-reported` token (an alias onto `--hue-honey-ink`,
  // `libs/web-ui-token/src/ayokoding.css`) rather than raw `text-amber-700 dark:text-amber-400`
  // (Rule-15 DWT-002 fix) — `--hue-honey-ink` already clears WCAG AA's 4.5:1 text minimum in both
  // themes (it is the same tone `hero.tsx` already uses for its own links), and resolves
  // automatically per-theme from the one class, no `dark:` variant needed.
  return (
    <span data-slot="coverage-cell" className="inline-flex flex-col items-start gap-0.5 leading-tight">
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
        />
      ),
      output: (
        <FigureCell
          value={formatPriceUsd(rate.output, locale)}
          grade={rate.grade}
          source={rate.source}
          locale={locale}
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

/** One shared per-model figure: a localized label paired with its rendered node. */
export type ModelFigure = { label: string; node: ReactNode };

/** The four composite-benchmark figures, in column order — shared by the table and the card (W-26). */
export function renderBenchmarkFigures(model: Model, locale: Locale): ModelFigure[] {
  return BENCHMARK_COLUMNS.map((col) => ({
    label: t(locale, col.labelKey),
    node: benchmarkCell(model, col.id, locale),
  }));
}

/**
 * The four non-benchmark figures — index, coverage, input price, output price — in a fixed order,
 * shared by the table and the card (W-26/W-30). The card's summary picks index/input/output price
 * out of this list by label match; the remaining entry (coverage) joins the card's expanded
 * content, so parity across summary + details holds by construction rather than by a second
 * hand-maintained list.
 */
export function renderStaticFigures(model: Model, view: ScoreView, locale: Locale): ModelFigure[] {
  const prices = priceCells(model, locale);
  return [
    { label: t(locale, "aiBenchColIndex"), node: indexCell(view, locale) },
    { label: t(locale, "aiBenchColCoverage"), node: coverageCell(view, locale) },
    { label: t(locale, "aiBenchColInputPrice"), node: prices.input },
    { label: t(locale, "aiBenchColOutputPrice"), node: prices.output },
  ];
}
