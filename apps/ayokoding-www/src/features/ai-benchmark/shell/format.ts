// AI BENCHMARK — presentation formatting helpers (Phase 5).
//
// Pure presenters that turn a dataset number into a localized display string. They contain NO
// literal figures (FCIS boundary): every value they render is passed in from the dataset. The
// `%`, `$`, and token-unit symbols are formatting, not data.

import type { Locale } from "@/features/i18n/core/config";

/** Format a 0–100 benchmark score as a locale-aware percentage with one decimal. */
export function formatPercent(value: number, locale: Locale): string {
  // Values are stored on a 0–100 scale and rendered with a literal percent sign and one decimal
  // place, so screen readers announce "percent". Intl 'percent' style would double-scale.
  const localeTag = locale === "id" ? "id-ID" : "en-US";
  const formatted = new Intl.NumberFormat(localeTag, {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  }).format(value);
  return `${formatted}%`;
}

/** Format a USD per-1M-tokens price as a localized currency string. */
export function formatPriceUsd(value: number, locale: Locale): string {
  const localeTag = locale === "id" ? "id-ID" : "en-US";
  return new Intl.NumberFormat(localeTag, {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

/** Format a coverage ratio (0–1) as a locale-aware percentage with no decimals. */
export function formatCoverage(ratio: number, locale: Locale): string {
  const localeTag = locale === "id" ? "id-ID" : "en-US";
  const formatted = new Intl.NumberFormat(localeTag, { maximumFractionDigits: 0 }).format(ratio * 100);
  return `${formatted}%`;
}

/** Format a composite index (0–100 scale) with one decimal. */
export function formatIndex(value: number, locale: Locale): string {
  const localeTag = locale === "id" ? "id-ID" : "en-US";
  return new Intl.NumberFormat(localeTag, {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  }).format(value);
}
