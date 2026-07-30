// AI BENCHMARK — display-order comparators (Phase 1). Separate from `core/bands.ts` (DD-5):
// `bands.ts` owns the class-band DECISION; this module owns display ORDER within a band, which is
// a per-band, user-choosable concern (capability vs. price sort, DD-4).
//
// See `plans/in-progress/ayokoding-www-ai-benchmark-merged-chart/tech-docs.md` DD-3/DD-4/DD-5.

import type { HarnessId } from "./data/models";
import type { ModelScore } from "./bands";
import { lowestRate, rateForHarness } from "./price";

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
 * A model's metered output/input rate as a comparable number pair — via `price.ts`'s
 * `rateForHarness` when `harness` is active, else its `lowestRate` — the SAME rate the price bars
 * themselves plot (DD-8/AC-18), so sort order and displayed value never diverge even under a
 * harness filter. Passing the wrong selector here was exactly the regression this parameter
 * closes (pr-review-synthesis-maker HIGH finding: an ascending price sort could render a costlier
 * row above a cheaper one whenever a harness filter was active and the sorted model's cheapest
 * harness was not the selected one). A model with no metered rate at all (subscription-only or
 * unpriced) reads as `fallback` for both fields — callers pass `Infinity` (ascending: sorts last)
 * or `-Infinity` (descending: sorts last), so an unmetered model always sorts to the end
 * regardless of direction, never a false "cheapest" or "priciest" ranking (invariant 10: a
 * subscription is never treated as a numeric price). Shared by both {@link byPriceAsc} and
 * {@link byPriceDesc} so the comparator body is not duplicated.
 */
function meteredRateOrFallback(
  s: ModelScore,
  fallback: number,
  harness?: HarnessId,
): { output: number; input: number } {
  const rate = harness !== undefined ? rateForHarness(s.model, harness) : lowestRate(s.model);
  if (rate !== undefined && rate.kind === "metered") {
    return { output: rate.output, input: rate.input };
  }
  return { output: fallback, input: fallback };
}

/**
 * Ascending by output rate, input rate as tie-break (DD-3); unmetered models sort last. `harness`
 * (DD-8), when supplied, sorts by THAT harness's own rate rather than each model's lowest
 * available harness rate — matching whatever the price bars are plotting (AC-18).
 */
export function byPriceAsc(a: ModelScore, b: ModelScore, harness?: HarnessId): number {
  const ra = meteredRateOrFallback(a, Infinity, harness);
  const rb = meteredRateOrFallback(b, Infinity, harness);
  return ra.output - rb.output || ra.input - rb.input;
}

/**
 * Descending by output rate, input rate as tie-break (DD-3); unmetered models sort last. `harness`
 * (DD-8), when supplied, sorts by THAT harness's own rate rather than each model's lowest
 * available harness rate — matching whatever the price bars are plotting (AC-18).
 */
export function byPriceDesc(a: ModelScore, b: ModelScore, harness?: HarnessId): number {
  const ra = meteredRateOrFallback(a, -Infinity, harness);
  const rb = meteredRateOrFallback(b, -Infinity, harness);
  return rb.output - ra.output || rb.input - ra.input;
}
