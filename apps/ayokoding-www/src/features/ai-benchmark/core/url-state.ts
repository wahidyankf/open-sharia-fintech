// AI BENCHMARK — pure URL state encode/decode/sanitize (Phase 4, steps F-3..F-9).
//
// Mirrors `src/features/cost-of-living-calculator/core/url-state.ts`: the URL is the single
// source of truth, the two filter params (harness, class) are serialized with defaults OMITTED
// from the query string, and unknown values sanitize to the default rather than throwing. No
// React, no router, no side effects — every function is pure over `URLSearchParams`.
//
// The known-value unions live in `filter.ts` (F-9) so a new harness id or band is added in exactly
// one place; this module imports them.

import { BANDS, HARNESS_IDS, isKnownBand, isKnownHarness, type FilterState } from "./filter";

/** Query-string parameter keys. */
export const PARAM_KEYS = {
  harness: "harness",
  class: "class",
} as const;

/** The unfiltered state — what an empty or unrecognized query resolves to. */
export const DEFAULT_STATE: FilterState = {
  harness: undefined,
  class: undefined,
};

/**
 * Sanitize a (possibly untrusted) filter state to a valid one: drop any harness value that is not
 * one of {@link HARNESS_IDS} and any class value that is not one of {@link BANDS}. Idempotent and
 * total — never throws. This is the "unknown filter value falls back to the unfiltered view"
 * guarantee (AC-26).
 */
export function sanitizeState(state: Partial<FilterState>): FilterState {
  const harness = state.harness !== undefined && isKnownHarness(state.harness) ? state.harness : undefined;
  const bandClass = state.class !== undefined && isKnownBand(state.class) ? state.class : undefined;
  return { harness, class: bandClass };
}

/**
 * Parse raw URLSearchParams into a sanitized {@link FilterState}. Unknown keys are ignored;
 * unknown harness/class values resolve to `undefined` (unfiltered) rather than throwing (AC-26).
 */
export function decodeState(params: URLSearchParams): FilterState {
  const harnessRaw = params.get(PARAM_KEYS.harness);
  const classRaw = params.get(PARAM_KEYS.class);
  return sanitizeState({
    harness: harnessRaw !== null ? (harnessAsHarness(harnessRaw) ?? undefined) : undefined,
    class: classRaw !== null ? (classAsBand(classRaw) ?? undefined) : undefined,
  });
}

/** Parse a harness string, returning the typed id only if it is known. */
function harnessAsHarness(v: string): FilterState["harness"] {
  return isKnownHarness(v) ? v : undefined;
}

/** Parse a class string, returning the typed band only if it is known. */
function classAsBand(v: string): FilterState["class"] {
  return isKnownBand(v) ? v : undefined;
}

/**
 * Encode a filter state to URLSearchParams, OMITTING defaults so a clean, shareable URL is
 * produced (mirrors the calculator's contract). The default (unfiltered) state encodes to an
 * empty query string.
 */
export function encodeState(state: FilterState): URLSearchParams {
  const params = new URLSearchParams();
  if (state.harness !== undefined && state.harness !== DEFAULT_STATE.harness) {
    params.set(PARAM_KEYS.harness, state.harness);
  }
  if (state.class !== undefined && state.class !== DEFAULT_STATE.class) {
    params.set(PARAM_KEYS.class, state.class);
  }
  return params;
}
