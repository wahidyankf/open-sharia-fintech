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

import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@open-sharia-enterprise/web-ui";
import { dataset as defaultDataset, type Dataset } from "../core/data/models";
import { HARNESS_DISPLAY_NAMES, BENCHMARK_COLUMNS } from "../core/data/benchmarks";
import {
  classLabel,
  computeScoreViews,
  coverageCell,
  indexCell,
  integrityNotes,
  benchmarkCell,
  priceCells,
  renderBenchmarkFigures,
  renderStaticFigures,
} from "./model-figures";

const SLOT = "model-table";

export type ModelTableProps = {
  dataset?: Dataset;
  /**
   * The full unfiltered roster. Band thresholds (the anchor indices) and the roster-max map are
   * ALWAYS derived from this dataset, never from `dataset` — `dataset` may be a harness/class
   * filtered subset that excludes both anchor models, and re-deriving thresholds from it would
   * silently collapse every rated model to `haiku` (DD-5a: bands are roster-relative to the FULL
   * population; filtering governs display only). REQUIRED, not optional: an omitted `fullDataset`
   * reproduces the identical bug with identical silence, so this is a compile-time guard rather
   * than a silent self-fallback.
   */
  fullDataset: Dataset;
  locale: Locale;
};

export function ModelTable({ dataset = defaultDataset, fullDataset, locale }: ModelTableProps) {
  const views = computeScoreViews(dataset, fullDataset);
  const models = dataset.models;

  return (
    <section data-slot={SLOT} data-testid="model-table" className="space-y-4" aria-label={t(locale, "aiBenchTitle")}>
      {/* ── Desktop / tablet: semantic <table> (md and up), on the shared `libs/web-ui` table
          primitives (Rule-15 DWT-003 fix) — the same `Table`/`TableHeader`/`TableBody`/`TableRow`/
          `TableHead`/`TableCell`/`TableCaption` set `cost-of-living-calculator/shell/min-role.tsx`
          already uses, rather than a bespoke hand-rolled `<table>`. Sticky header/first-column and
          `scope="row"` are preserved via className overrides on top of the shared primitives; the
          row-hover intensity is the primitive's own `hover:bg-muted/50`. DD-27 (tech-docs.md) fixes
          R5 — the table bleeding past the viewport and forcing the whole document to scroll
          horizontally — in two steps: Unit 1 (here) removes the wrapper's `lg`-breakpoint overflow
          override so `overflow-x-auto` contains the table at every breakpoint, at the cost of the
          sticky `<thead>` no longer sticking at `lg` (a scroll container in both axes can't have a
          sticky descendant). Unit 2 restores that override once the column-reduction work shrinks
          the table below the `lg` viewport, making it safe again (AC-59). ─────────────────────── */}
      <div data-testid="model-table-desktop" className="hidden md:block">
        <Table className="w-max min-w-full border-collapse lg:w-full">
          <TableCaption className="sr-only">{t(locale, "aiBenchTableCaption")}</TableCaption>
          <TableHeader className="sticky top-0 z-10 bg-background">
            <TableRow>
              <TableHead scope="col" className="sticky left-0 bg-background text-foreground">
                {t(locale, "aiBenchColModel")}
              </TableHead>
              <TableHead scope="col">{t(locale, "aiBenchColVendor")}</TableHead>
              <TableHead scope="col">{t(locale, "aiBenchColHarnesses")}</TableHead>
              <TableHead scope="col">{t(locale, "aiBenchColClass")}</TableHead>
              {BENCHMARK_COLUMNS.map((col) => (
                <TableHead key={col.id} scope="col" className="text-right">
                  {t(locale, col.labelKey)}
                </TableHead>
              ))}
              <TableHead scope="col" className="text-right">
                {t(locale, "aiBenchColIndex")}
              </TableHead>
              <TableHead scope="col" className="text-right">
                {t(locale, "aiBenchColCoverage")}
              </TableHead>
              <TableHead scope="col" className="text-right">
                {t(locale, "aiBenchColInputPrice")}
              </TableHead>
              <TableHead scope="col" className="text-right">
                {t(locale, "aiBenchColOutputPrice")}
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {models.map((model) => {
              const view = views.get(model.id) ?? { band: "unrated" as const, index: undefined, coverage: 0 };
              const prices = priceCells(model, locale);
              const harnessNames = model.harnesses.map((h) => HARNESS_DISPLAY_NAMES[h] ?? h).join(", ");
              return (
                <TableRow key={model.id} data-model-id={model.id} className="align-top">
                  <TableHead
                    scope="row"
                    className="sticky left-0 bg-background text-left whitespace-normal text-foreground"
                  >
                    <span data-slot="model-name">{model.name}</span>
                    {integrityNotes(model, locale)}
                  </TableHead>
                  <TableCell>{model.vendor}</TableCell>
                  <TableCell className="text-muted-foreground">{harnessNames}</TableCell>
                  <TableCell>{classLabel(view.band, locale)}</TableCell>
                  {BENCHMARK_COLUMNS.map((col) => (
                    <TableCell key={col.id} className="text-right">
                      {benchmarkCell(model, col.id, locale)}
                    </TableCell>
                  ))}
                  <TableCell className="text-right">{indexCell(view, locale)}</TableCell>
                  <TableCell className="text-right">{coverageCell(view, locale)}</TableCell>
                  <TableCell className="text-right">{prices.input}</TableCell>
                  <TableCell className="text-right">{prices.output}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
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
              ...renderBenchmarkFigures(model, locale),
              ...renderStaticFigures(model, view, locale),
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
