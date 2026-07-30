// AI BENCHMARK — display-order comparators (Phase 1). Separate from `core/bands.ts` (DD-5):
// `bands.ts` owns the class-band DECISION; this module owns display ORDER within a band, which is
// a per-band, user-choosable concern (capability vs. price sort, DD-4).
//
// See `plans/in-progress/ayokoding-www-ai-benchmark-merged-chart/tech-docs.md` DD-3/DD-4/DD-5.

import type { ModelScore } from "./bands";
import { lowestRate } from "./price";

/**
 * The three per-band display-order choices (DD-4): `"capability"` is the default (composite
 * index, descending); `"price-asc"`/`"price-desc"` order by output rate via {@link byPriceAsc} /
 * {@link byPriceDesc}.
 */
export type SortMode = "capability" | "price-asc" | "price-desc";

/**
 * The canonical known-value list for {@link SortMode} (mirrors `filter.ts`'s `HARNESS_IDS` /
 * `BANDS` pattern) — the single source of truth `url-state.ts`'s sanitizer imports for
 * validation, so a new sort mode is added in exactly one place.
 */
export const SORT_MODES: readonly SortMode[] = ["capability", "price-asc", "price-desc"];

/** Type guard: is `v` one of the known sort modes? Mirrors `filter.ts`'s `isKnownHarness`/`isKnownBand`. */
export function isKnownSortMode(v: string): v is SortMode {
  return (SORT_MODES as readonly string[]).includes(v);
}

/**
 * Descending composite index, undefined last, ascending id tie-break — mirrors `bands.ts`'s
 * private `compareForOrder` exactly, so the default (capability) sort matches the band's
 * canonical order.
 */
export function byCapabilityDesc(a: ModelScore, b: ModelScore): number {
  const ai = a.index ?? -Infinity;
  const bi = b.index ?? -Infinity;
  if (bi !== ai) {
    return bi - ai; // descending index
  }
  if (a.model.id < b.model.id) return -1; // ascending id
  if (a.model.id > b.model.id) return 1;
  return 0;
}

/**
 * A model's metered output/input rate as a comparable number pair, via `price.ts`'s `lowestRate`
 * — the SAME rate the price bars themselves plot (DD-8), so sort order and displayed value never
 * diverge. A model with no metered rate at all (subscription-only or unpriced) reads as
 * `fallback` for both fields — callers pass `Infinity` (ascending: sorts last) or `-Infinity`
 * (descending: sorts last), so an unmetered model always sorts to the end regardless of
 * direction, never a false "cheapest" or "priciest" ranking (invariant 10: a subscription is
 * never treated as a numeric price). Shared by both {@link byPriceAsc} and {@link byPriceDesc} so
 * the comparator body is not duplicated.
 */
function meteredRateOrFallback(s: ModelScore, fallback: number): { output: number; input: number } {
  const rate = lowestRate(s.model);
  if (rate !== undefined && rate.kind === "metered") {
    return { output: rate.output, input: rate.input };
  }
  return { output: fallback, input: fallback };
}

/** Ascending by output rate, input rate as tie-break (DD-3); unmetered models sort last. */
export function byPriceAsc(a: ModelScore, b: ModelScore): number {
  const ra = meteredRateOrFallback(a, Infinity);
  const rb = meteredRateOrFallback(b, Infinity);
  return ra.output - rb.output || ra.input - rb.input;
}

/** Descending by output rate, input rate as tie-break (DD-3); unmetered models sort last. */
export function byPriceDesc(a: ModelScore, b: ModelScore): number {
  const ra = meteredRateOrFallback(a, -Infinity);
  const rb = meteredRateOrFallback(b, -Infinity);
  return rb.output - ra.output || rb.input - ra.input;
}
