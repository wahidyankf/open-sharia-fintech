// AI BENCHMARK — accessible model roster data table (Phase 5, W-6..W-18, W-26..W-27).
//
// Renders every roster model as a row carrying: harnesses, class, each benchmark score, composite
// index, coverage ratio, and per-harness prices — each figure with its evidence grade and source
// link (AC-20/AC-21/AC-30), conflicted figures as a low–high range (AC-31), and each model's
// integrity notes reachable from its row (AC-33). The table is semantic: a `<caption>` and
// `scope` on every `<th>` (AC-19); colour is never the sole encoding (grades are text).
//
// Responsive (prd §Responsive strategy): below `md` the roster renders as stacked definition
// cards; at `md` a horizontally-scrollable table; at `lg` full width. BOTH representations render
// the identical set of figures per model (W-26 invariant) — CSS toggles which is visible, so the
// component test asserts parity without a real viewport.
//
// FCIS boundary: no literal figure, price, model name, or threshold lives here — every number
// comes from the passed `dataset` via the pure `core/` selectors, formatted by `shell/format.ts`.

import type { ReactNode } from "react";
import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import {
  dataset as defaultDataset,
  isConflictedFigure,
  type Dataset,
  type Figure,
  type Model,
} from "../core/data/models";
import { LOW_COVERAGE_THRESHOLD } from "../core/score";
import { computeGroups, type ModelScore } from "../core/bands";
import { lowestRate } from "../core/price";
import { BAND_LABEL_KEYS, BENCHMARK_COLUMNS, HARNESS_DISPLAY_NAMES } from "../core/data/benchmarks";
import { formatCoverage, formatIndex, formatPercent, formatPriceUsd } from "./format";
import { FigureCell } from "./figure-cell";

const SLOT = "model-table";

/** Per-model scored view: band, composite index, and coverage derived from the pure core. */
type ScoreView = {
  band: ModelScore["band"];
  index: number | undefined;
  coverage: number;
};

/** Build the roster-relative index/coverage/band for every model in one scoring pass. */
function computeScoreViews(dataset: Dataset): Map<string, ScoreView> {
  const groups = computeGroups(dataset);
  const byId = new Map<string, ScoreView>();
  for (const list of [groups.opus, groups.sonnet, groups.light, groups.unrated]) {
    for (const s of list) {
      byId.set(s.model.id, { band: s.band, index: s.index, coverage: s.coverage });
    }
  }
  return byId;
}

/** Find the model's published figure for a benchmark (absent → undefined, rendered as "not reported"). */
function figureFor(model: Model, benchmark: string): Figure | undefined {
  return model.figures.find((f) => f.benchmark === benchmark);
}

/** The model's localized class label. */
function classLabel(band: ScoreView["band"], locale: Locale): string {
  const key = BAND_LABEL_KEYS[band];
  return key ? t(locale, key) : band;
}

/** A benchmark score cell: a range for a conflicted figure, otherwise a single value; "—" when absent. */
function benchmarkCell(model: Model, benchmarkId: string, locale: Locale): ReactNode {
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
function indexCell(view: ScoreView, locale: Locale): ReactNode {
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
function isLowCoverageView(view: ScoreView): boolean {
  return view.index !== undefined && view.coverage > 0 && view.coverage < LOW_COVERAGE_THRESHOLD;
}

/** The coverage cell; low-coverage rated models carry an advisory marker (text, not colour alone). */
function coverageCell(view: ScoreView, locale: Locale): ReactNode {
  const text = formatCoverage(view.coverage, locale);
  const low = isLowCoverageView(view);
  return (
    <span data-slot="coverage-cell" className="inline-flex flex-col items-start gap-0.5 leading-tight">
      <span data-slot="figure-cell-value">{text}</span>
      {low ? (
        <span className="text-xs text-amber-600 dark:text-amber-400">{t(locale, "aiBenchCoverageLow")}</span>
      ) : null}
    </span>
  );
}

/** The source cited for the composite index — the dataset's own methodology page is not a figure. */
function defaultSourceForIndex(): string {
  return "https://ayokoding.com/tools/ai-benchmark";
}

/** Input/output price cells from the model's lowest available rate. */
function priceCells(model: Model, locale: Locale): { input: ReactNode; output: ReactNode; isSubscription: boolean } {
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
  // Subscription-only (or no pricing): show the subscription marker; the source link still resolves.
  const subSource = rate && rate.kind === "subscription" ? rate.source : defaultSourceForIndex();
  const subText =
    rate && rate.kind === "subscription"
      ? `${t(locale, "aiBenchSubscription")} (${formatPriceUsd(rate.planCostUsd, locale)})`
      : t(locale, "aiBenchNoFigure");
  const subNode = (
    <span data-slot="subscription-cell" className="inline-flex flex-col items-start gap-0.5 leading-tight">
      <span data-slot="figure-cell-value">{subText}</span>
      <a
        data-slot="evidence-badge"
        href={subSource}
        target="_blank"
        rel="noopener noreferrer nofollow"
        className="text-xs text-muted-foreground underline decoration-dotted underline-offset-2 hover:text-foreground"
      >
        {t(locale, "aiBenchSourceLabel")}
      </a>
    </span>
  );
  return {
    input: subNode,
    output: <span data-slot="figure-cell-value">{t(locale, "aiBenchNoFigure")}</span>,
    isSubscription: true,
  };
}

/** A model's integrity-note links, rendered beside its name (AC-33). */
function integrityNotes(model: Model, locale: Locale): ReactNode {
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
          className="text-xs font-medium text-amber-600 underline decoration-dotted underline-offset-2 dark:text-amber-400"
          aria-label={`${t(locale, "aiBenchIntegrityLabel")}: ${note.text}`}
          title={note.text}
        >
          {t(locale, "aiBenchIntegrityLabel")}
        </a>
      ))}
    </span>
  );
}

export type ModelTableProps = {
  dataset?: Dataset;
  locale: Locale;
};

export function ModelTable({ dataset = defaultDataset, locale }: ModelTableProps) {
  const views = computeScoreViews(dataset);
  const models = dataset.models;

  // Shared per-model figure set so the table and the card render identical figures (W-26).
  const renderBenchmarkFigures = (model: Model): { label: string; node: ReactNode }[] =>
    BENCHMARK_COLUMNS.map((col) => ({
      label: t(locale, col.labelKey),
      node: benchmarkCell(model, col.id, locale),
    }));

  const renderStaticFigures = (model: Model, view: ScoreView): { label: string; node: ReactNode }[] => {
    const prices = priceCells(model, locale);
    return [
      { label: t(locale, "aiBenchColIndex"), node: indexCell(view, locale) },
      { label: t(locale, "aiBenchColCoverage"), node: coverageCell(view, locale) },
      { label: t(locale, "aiBenchColInputPrice"), node: prices.input },
      { label: t(locale, "aiBenchColOutputPrice"), node: prices.output },
    ];
  };

  return (
    <section data-slot={SLOT} data-testid="model-table" className="space-y-4" aria-label={t(locale, "aiBenchTitle")}>
      {/* ── Desktop / tablet: semantic <table> (md and up) ───────────────────────────── */}
      <div data-testid="model-table-desktop" className="hidden md:block">
        <div className="overflow-x-auto lg:overflow-visible">
          <table data-slot={`${SLOT}-grid`} className="w-max min-w-full border-collapse text-sm lg:w-full">
            <caption className="sr-only">{t(locale, "aiBenchTableCaption")}</caption>
            <thead className="sticky top-0 z-10 bg-background">
              <tr>
                <th scope="col" className="sticky left-0 border-b bg-background px-3 py-2 text-left font-semibold">
                  {t(locale, "aiBenchColModel")}
                </th>
                <th scope="col" className="border-b px-3 py-2 text-left font-semibold">
                  {t(locale, "aiBenchColVendor")}
                </th>
                <th scope="col" className="border-b px-3 py-2 text-left font-semibold">
                  {t(locale, "aiBenchColHarnesses")}
                </th>
                <th scope="col" className="border-b px-3 py-2 text-left font-semibold">
                  {t(locale, "aiBenchColClass")}
                </th>
                {BENCHMARK_COLUMNS.map((col) => (
                  <th key={col.id} scope="col" className="border-b px-3 py-2 text-right font-semibold">
                    {t(locale, col.labelKey)}
                  </th>
                ))}
                <th scope="col" className="border-b px-3 py-2 text-right font-semibold">
                  {t(locale, "aiBenchColIndex")}
                </th>
                <th scope="col" className="border-b px-3 py-2 text-right font-semibold">
                  {t(locale, "aiBenchColCoverage")}
                </th>
                <th scope="col" className="border-b px-3 py-2 text-right font-semibold">
                  {t(locale, "aiBenchColInputPrice")}
                </th>
                <th scope="col" className="border-b px-3 py-2 text-right font-semibold">
                  {t(locale, "aiBenchColOutputPrice")}
                </th>
              </tr>
            </thead>
            <tbody>
              {models.map((model) => {
                const view = views.get(model.id) ?? { band: "unrated" as const, index: undefined, coverage: 0 };
                const prices = priceCells(model, locale);
                const harnessNames = model.harnesses.map((h) => HARNESS_DISPLAY_NAMES[h] ?? h).join(", ");
                return (
                  <tr key={model.id} data-model-id={model.id} className="align-top hover:bg-muted/40">
                    <th scope="row" className="sticky left-0 border-b bg-background px-3 py-2 text-left font-medium">
                      <span data-slot="model-name">{model.name}</span>
                      {integrityNotes(model, locale)}
                    </th>
                    <td className="border-b px-3 py-2">{model.vendor}</td>
                    <td className="border-b px-3 py-2 text-muted-foreground">{harnessNames}</td>
                    <td className="border-b px-3 py-2">{classLabel(view.band, locale)}</td>
                    {BENCHMARK_COLUMNS.map((col) => (
                      <td key={col.id} className="border-b px-3 py-2 text-right">
                        {benchmarkCell(model, col.id, locale)}
                      </td>
                    ))}
                    <td className="border-b px-3 py-2 text-right">{indexCell(view, locale)}</td>
                    <td className="border-b px-3 py-2 text-right">{coverageCell(view, locale)}</td>
                    <td className="border-b px-3 py-2 text-right">{prices.input}</td>
                    <td className="border-b px-3 py-2 text-right">{prices.output}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* ── Mobile: stacked definition cards (below md) ─────────────────────────────── */}
      <div data-testid="model-table-mobile" className="md:hidden">
        <p className="sr-only">{t(locale, "aiBenchTableCaption")}</p>
        <ul className="space-y-3">
          {models.map((model) => {
            const view = views.get(model.id) ?? { band: "unrated" as const, index: undefined, coverage: 0 };
            const harnessNames = model.harnesses.map((h) => HARNESS_DISPLAY_NAMES[h] ?? h).join(", ");
            const figures = [
              { label: t(locale, "aiBenchColVendor"), node: <span>{model.vendor}</span> },
              { label: t(locale, "aiBenchColHarnesses"), node: <span>{harnessNames}</span> },
              { label: t(locale, "aiBenchColClass"), node: <span>{classLabel(view.band, locale)}</span> },
              ...renderBenchmarkFigures(model),
              ...renderStaticFigures(model, view),
            ];
            return (
              <li key={model.id} data-model-id={model.id} className="rounded-md border p-3">
                <div className="mb-2">
                  <h3 className="text-base font-semibold" data-slot="model-name">
                    {model.name}
                  </h3>
                  {integrityNotes(model, locale)}
                </div>
                <dl className="grid grid-cols-2 gap-x-3 gap-y-2 text-sm">
                  {figures.map((fig) => (
                    <div key={fig.label} className="flex flex-col gap-0.5">
                      <dt className="text-xs font-medium text-muted-foreground">{fig.label}</dt>
                      <dd className="text-right">{fig.node}</dd>
                    </div>
                  ))}
                </dl>
              </li>
            );
          })}
        </ul>
      </div>
    </section>
  );
}
