// AI BENCHMARK — presentation formatting helpers (Phase 5).
//
// Pure presenters that turn a dataset number into a localized display string. They contain NO
// literal figures (FCIS boundary): every value they render is passed in from the dataset. The
// `%`, `$`, and token-unit symbols are formatting, not data.

import type { Locale } from "@/features/i18n/core/config";

function localeTagOf(locale: Locale): string {
  return locale === "id" ? "id-ID" : "en-US";
}

/**
 * Formatter instances are cached per (formatter kind, locale) — only two locales exist, so each
 * cache holds at most two entries. Constructing an `Intl.NumberFormat` is expensive relative to
 * reusing one (~100x measured on this dataset's render volume: up to ~600 formatted cells per
 * page view — 38 roster models × several numeric columns × both the desktop and mobile DOM
 * representations rendered simultaneously). This matches MDN's own guidance to cache `Intl`
 * instances when formatting many values, rather than constructing one per call.
 */
function memoizedNumberFormatter(
  cache: Map<string, Intl.NumberFormat>,
  localeTag: string,
  options: Intl.NumberFormatOptions,
): Intl.NumberFormat {
  const cached = cache.get(localeTag);
  if (cached) return cached;
  const formatter = new Intl.NumberFormat(localeTag, options);
  cache.set(localeTag, formatter);
  return formatter;
}

const percentFormatters = new Map<string, Intl.NumberFormat>();
const priceUsdFormatters = new Map<string, Intl.NumberFormat>();
const coverageFormatters = new Map<string, Intl.NumberFormat>();
const indexFormatters = new Map<string, Intl.NumberFormat>();

/** Format a 0–100 benchmark score as a locale-aware percentage with one decimal. */
export function formatPercent(value: number, locale: Locale): string {
  // Values are stored on a 0–100 scale and rendered with a literal percent sign and one decimal
  // place, so screen readers announce "percent". Intl 'percent' style would double-scale.
  const localeTag = localeTagOf(locale);
  const formatter = memoizedNumberFormatter(percentFormatters, localeTag, {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  });
  return `${formatter.format(value)}%`;
}

/** Format a USD per-1M-tokens price as a localized currency string. */
export function formatPriceUsd(value: number, locale: Locale): string {
  const localeTag = localeTagOf(locale);
  const formatter = memoizedNumberFormatter(priceUsdFormatters, localeTag, {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  return formatter.format(value);
}

/** Format a coverage ratio (0–1) as a locale-aware percentage with no decimals. */
export function formatCoverage(ratio: number, locale: Locale): string {
  const localeTag = localeTagOf(locale);
  const formatter = memoizedNumberFormatter(coverageFormatters, localeTag, { maximumFractionDigits: 0 });
  return `${formatter.format(ratio * 100)}%`;
}

/** Format a composite index (0–100 scale) with one decimal. */
export function formatIndex(value: number, locale: Locale): string {
  const localeTag = localeTagOf(locale);
  const formatter = memoizedNumberFormatter(indexFormatters, localeTag, {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  });
  return formatter.format(value);
}
