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

export type FigureCellProps = {
  /** Primary formatted value (a localized percentage or USD price). For a conflicted figure this is the LOW. */
  value: string;
  /** When set, render as a localized "low–high" range instead of a single value. */
  highValue?: string;
  grade: EvidenceGrade;
  /** Source URL the figure came from — rendered as the anchor on the badge (AC-30). */
  source: string;
  locale: Locale;
};

/**
 * One figure cell: value (or range) + evidence badge. Used verbatim by both the desktop `<table>`
 * cells and the mobile stacked-card cells so both representations show identical figures (W-26).
 */
export function FigureCell({ value, highValue, grade, source, locale }: FigureCellProps): ReactNode {
  const valueText = highValue !== undefined ? `${value} ${t(locale, "aiBenchRangeSeparator")} ${highValue}` : value;
  return (
    <span data-slot={SLOT} className="inline-flex flex-col items-start gap-0.5 leading-tight">
      <span data-slot={`${SLOT}-value`}>{valueText}</span>
      <EvidenceBadge grade={grade} source={source} locale={locale} />
    </span>
  );
}
