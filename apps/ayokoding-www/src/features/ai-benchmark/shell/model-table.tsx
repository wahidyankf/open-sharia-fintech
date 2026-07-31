// AI BENCHMARK — accessible model roster data table (Phase 5/6, W-6..W-18, W-26..W-27, DD-27/DD-28).
//
// Renders every roster model as a row carrying its primary figures — name, vendor, class, composite
// index, and input/output price — with the remaining figures (harnesses, each benchmark score,
// coverage) inside a per-row expandable detail region, each figure with its evidence grade and
// source link (AC-20/AC-21/AC-30), conflicted figures as a low–high range (AC-31), and each model's
// integrity notes reachable from its row (AC-33). The table is semantic: a `<caption>` and
// `scope` on every `<th>` (AC-19); colour is never the sole encoding (grades are text).
//
// DD-27 (R5, in two steps): Unit 1 (Phase 1) removed the wrapper's `lg`-breakpoint overflow
// override so `overflow-x-auto` contained the table at every breakpoint, at the cost of the sticky
// `<thead>` no longer sticking at `lg` (a scroll container in both axes can't have a sticky
// descendant). Unit 2 (here, Phase 6 cycle 6.3) restores that override — now safe because reducing
// the desktop table to its primary columns shrinks its intrinsic width below the `lg` viewport
// (AC-59), and DD-28 moves the remaining figures into the per-row detail region below.
//
// Responsive (prd §Responsive strategy): below `md` the roster renders as `model-card.tsx`'s
// collapsed summary cards; at `md`/`lg` a horizontally-scrollable table with a per-row detail
// disclosure. BOTH representations render the identical set of figures per model (W-26 invariant,
// summary + detail together per W-30) — CSS toggles which is visible, so the component test asserts
// parity without a real viewport.
//
// FCIS boundary: no literal figure, price, model name, or threshold lives here — every number
// comes from the passed `dataset` via the pure `core/` selectors, formatted by `shell/format.ts`.

import { Fragment } from "react";
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
import { HARNESS_DISPLAY_NAMES } from "../core/data/benchmarks";
import {
  classLabel,
  computeScoreViews,
  integrityNotes,
  partitionStaticFigures,
  renderBenchmarkFigures,
  renderStaticFigures,
  type ModelFigure,
} from "./model-figures";
import { ModelDetailDisclosure } from "./model-detail-disclosure";
import { ModelCard } from "./model-card";

const SLOT = "model-table";
/** Model, vendor, class, index, input price, output price — the desktop table's primary columns. */
const PRIMARY_COLUMN_COUNT = 6;

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
          row-hover intensity is the primitive's own `hover:bg-muted/50`. `wrapperClassName` restores
          the `lg`-breakpoint overflow override DD-27 Unit 1 (Phase 1) removed — safe now that the
          primary-column-only table fits below the `lg` viewport (AC-59). Each model renders as TWO
          `<tr>`s: the primary row, then an adjacent detail row whose single full-width `<td>` holds
          a native `<details>` disclosure (`ModelDetailDisclosure`, shared with `model-card.tsx`) —
          zero client JS, and the same disclosure semantics as the mobile card. ─────────────────── */}
      <div data-testid="model-table-desktop" className="hidden md:block">
        <Table className="w-max min-w-full border-collapse lg:w-full" wrapperClassName="lg:overflow-visible">
          <TableCaption className="sr-only">{t(locale, "aiBenchTableCaption")}</TableCaption>
          <TableHeader className="sticky top-0 z-10 bg-background">
            <TableRow>
              <TableHead scope="col" className="sticky left-0 bg-background text-foreground">
                {t(locale, "aiBenchColModel")}
              </TableHead>
              <TableHead scope="col">{t(locale, "aiBenchColVendor")}</TableHead>
              <TableHead scope="col">{t(locale, "aiBenchColClass")}</TableHead>
              <TableHead scope="col" className="text-right">
                {t(locale, "aiBenchColIndex")}
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
              const harnessNames = model.harnesses.map((h) => HARNESS_DISPLAY_NAMES[h] ?? h).join(", ");
              const staticFigures = renderStaticFigures(model, view, locale);
              const {
                index: indexFigure,
                input: inputFigure,
                output: outputFigure,
                rest: staticDetailFigures,
              } = partitionStaticFigures(staticFigures, locale);
              const detailFigures: ModelFigure[] = [
                { label: t(locale, "aiBenchColHarnesses"), node: <span>{harnessNames}</span> },
                ...renderBenchmarkFigures(model, locale),
                ...staticDetailFigures,
              ];
              return (
                <Fragment key={model.id}>
                  <TableRow data-model-id={model.id} className="align-top">
                    <TableHead
                      scope="row"
                      className="sticky left-0 bg-background text-left whitespace-normal text-foreground"
                    >
                      <span data-slot="model-name">{model.name}</span>
                      {integrityNotes(model, locale)}
                    </TableHead>
                    <TableCell>{model.vendor}</TableCell>
                    <TableCell>{classLabel(view.band, locale)}</TableCell>
                    <TableCell className="text-right">{indexFigure?.node}</TableCell>
                    <TableCell className="text-right">{inputFigure?.node}</TableCell>
                    <TableCell className="text-right">{outputFigure?.node}</TableCell>
                  </TableRow>
                  <TableRow data-model-detail-id={model.id} className="align-top">
                    <TableCell colSpan={PRIMARY_COLUMN_COUNT}>
                      <ModelDetailDisclosure slot={SLOT} modelId={model.id} figures={detailFigures} locale={locale} />
                    </TableCell>
                  </TableRow>
                </Fragment>
              );
            })}
          </TableBody>
        </Table>
      </div>

      {/* ── Mobile: `model-card.tsx`'s collapsed summary cards (below md) — the SAME shared figure
          list feeds both representations (W-26/W-30), so parity holds by construction. ────────── */}
      <div data-testid="model-table-mobile" className="md:hidden">
        <p className="sr-only">{t(locale, "aiBenchTableCaption")}</p>
        <ul className="space-y-3">
          {models.map((model) => {
            const view = views.get(model.id) ?? { band: "unrated" as const, index: undefined, coverage: 0 };
            return <ModelCard key={model.id} model={model} view={view} locale={locale} />;
          })}
        </ul>
      </div>
    </section>
  );
}
