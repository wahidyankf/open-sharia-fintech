// AI BENCHMARK — per-figure cell (Phase 5, W-18 refactor).
//
// The single unit used by EVERY numeric column in the data table: it renders the formatted value
// (or the low–high range for a conflicted figure), the evidence-grade marker, and the source link.
// Grade, source link, and range handling all live here so they cannot drift apart across columns.
//
// For a benchmark figure, pass `value` and (for a conflicted figure) `highValue` to render a range.
// For a price, pass `value` alone. The caller formats the numbers via `shell/format.ts`.

import type { ReactNode } from "react";
import type { Locale } from "@/features/i18n/core/config";
import { t } from "@/features/i18n/core/translations";
import type { EvidenceGrade } from "../core/data/models";
import { EvidenceBadge } from "./evidence-badge";

const SLOT = "figure-cell";

/**
 * `"stacked"` (the default) puts the value above its evidence badge on separate line boxes — the
 * desktop table's own primary columns must keep this so their column widths do not grow (DD-27's
 * "the table must fit below `lg`" precondition depends on it — flipping this default widens the
 * table and fails AC-52/AC-59 alongside it). `"inline"` flows the badge onto the same line as the
 * value instead (DD-34 Treatment 2, DN-2 fix) — used ONLY inside the roster card/table detail
 * region's rail rows, where a field already has its own `<dt>` label doing the vertical stacking.
 * Neither value changes WHICH figures render, only how a rendered figure's own value and badge lay
 * out relative to each other (W-26/W-30 parity is unaffected either way).
 */
export type FigureLayout = "stacked" | "inline";

export type FigureCellProps = {
  /** Primary formatted value (a localized percentage or USD price). For a conflicted figure this is the LOW. */
  value: string;
  /** When set, render as a localized "low–high" range instead of a single value. */
  highValue?: string;
  grade: EvidenceGrade;
  /** Source URL the figure came from — rendered as the anchor on the badge (AC-30). */
  source: string;
  locale: Locale;
  layout?: FigureLayout;
};

/**
 * One figure cell: value (or range) + evidence badge. Used verbatim by both the desktop `<table>`
 * cells and the mobile stacked-card cells so both representations show identical figures (W-26).
 */
export function FigureCell({
  value,
  highValue,
  grade,
  source,
  locale,
  layout = "stacked",
}: FigureCellProps): ReactNode {
  const valueText = highValue !== undefined ? `${value} ${t(locale, "aiBenchRangeSeparator")} ${highValue}` : value;
  const layoutClass =
    layout === "inline"
      ? "inline-flex flex-row flex-wrap items-baseline gap-x-1.5"
      : "inline-flex flex-col items-start gap-0.5 leading-tight";
  return (
    <span data-slot={SLOT} className={layoutClass}>
      <span data-slot={`${SLOT}-value`}>{valueText}</span>
      <EvidenceBadge grade={grade} source={source} locale={locale} />
    </span>
  );
}
