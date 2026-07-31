// AI BENCHMARK — pure URL state encode/decode/sanitize (Phase 4, steps F-3..F-9).
//
// Mirrors `src/features/cost-of-living-calculator/core/url-state.ts`: the URL is the single
// source of truth, the two filter params (harness, class) are serialized with defaults OMITTED
// from the query string, and unknown values sanitize to the default rather than throwing. No
// React, no router, no side effects — every function is pure over `URLSearchParams`.
//
// The known-value unions live in `filter.ts` (F-9) so a new harness id or band is added in exactly
// one place; this module imports them.

import { isKnownBand, isKnownHarness, type FilterState } from "./filter";
import { isKnownSortMode, type SortMode } from "./sort";

/** Query-string parameter keys. */
export const PARAM_KEYS = {
  harness: "harness",
  class: "class",
} as const;

/**
 * The three per-band sort query-string parameter keys (DD-4) — one per RATED band; `unrated` never
 * had one (pr-review-synthesis-maker MEDIUM finding: a since-removed `sortUnrated` param used to
 * round-trip here despite having no rendering effect — the `unrated` band excludes itself from
 * `RATED_BANDS` in `benchmark-chart.tsx`, is never sorted by `computeLayout`, and never had a
 * dropdown, so the param was dead on arrival; see `prd.md`/`tech-docs.md` for the corrected DD-4/
 * PS-4 claims). Kept as their own map, distinct from {@link PARAM_KEYS}, so `SORT_PARAM_KEYS` can
 * be iterated over uniformly (all three bands share the same shape) without mixing in the two
 * unrelated filter keys.
 */
export const SORT_PARAM_KEYS = {
  opus: "sortOpus",
  sonnet: "sortSonnet",
  light: "sortLight",
} as const;

/** One {@link SortMode} per RATED capability band — the per-band sort choice (DD-4). The `unrated`
 * band has no sort state: it is never sorted (see {@link SORT_PARAM_KEYS}'s docstring). */
export type SortState = {
  opus: SortMode;
  sonnet: SortMode;
  haiku: SortMode;
};

/** The default sort mode for every band: capability (composite index), matching the band's own canonical order. */
export const DEFAULT_SORT_MODE: SortMode = "capability";

/** The default, all-capability sort state — what an empty or unrecognized query resolves to. */
export const DEFAULT_SORT_STATE: SortState = {
  opus: DEFAULT_SORT_MODE,
  sonnet: DEFAULT_SORT_MODE,
  haiku: DEFAULT_SORT_MODE,
};

/** The unfiltered state — what an empty or unrecognized query resolves to. */
export const DEFAULT_STATE: FilterState & SortState = {
  harness: undefined,
  class: undefined,
  ...DEFAULT_SORT_STATE,
};

/**
 * An untrusted, possibly-raw-string per-band sort state — what a URL param actually hands
 * {@link sanitizeState} before validation narrows it to {@link SortMode}.
 */
type UntrustedSortState = { opus?: string; sonnet?: string; haiku?: string };

/**
 * Sanitize a (possibly untrusted) filter + sort state to a valid one: drop any harness value that
 * is not a known harness id, any class value that is not a known band, and any per-band sort value
 * that is not a known {@link SortMode} (falling back to `"capability"`, DD-4). Idempotent and
 * total — never throws. This is the "unknown filter/sort value falls back to the default view"
 * guarantee (AC-26 and its sort-param analogue).
 */
export function sanitizeState(state: Partial<FilterState> & UntrustedSortState): FilterState & SortState {
  const harness = state.harness !== undefined && isKnownHarness(state.harness) ? state.harness : undefined;
  const bandClass = state.class !== undefined && isKnownBand(state.class) ? state.class : undefined;
  return {
    harness,
    class: bandClass,
    opus: sanitizeSortMode(state.opus),
    sonnet: sanitizeSortMode(state.sonnet),
    haiku: sanitizeSortMode(state.haiku),
  };
}

/**
 * Sanitize a single per-band sort value, falling back to the default (`"capability"`) when
 * missing OR unrecognized (mirrors `isKnownHarness`/`isKnownBand`'s fallback pattern above).
 * Idempotent and total — never throws.
 */
function sanitizeSortMode(v: string | undefined): SortMode {
  return v !== undefined && isKnownSortMode(v) ? v : DEFAULT_SORT_MODE;
}

/**
 * Parse raw URLSearchParams into a sanitized {@link FilterState} & {@link SortState}. Unknown
 * keys are ignored; unknown harness/class/sort values resolve to their defaults rather than
 * throwing (AC-26 and its sort-param analogue).
 */
export function decodeState(params: URLSearchParams): FilterState & SortState {
  const harnessRaw = params.get(PARAM_KEYS.harness);
  const classRaw = params.get(PARAM_KEYS.class);
  return sanitizeState({
    harness: harnessRaw !== null ? (harnessAsHarness(harnessRaw) ?? undefined) : undefined,
    class: classRaw !== null ? (classAsBand(classRaw) ?? undefined) : undefined,
    opus: params.get(SORT_PARAM_KEYS.opus) ?? undefined,
    sonnet: params.get(SORT_PARAM_KEYS.sonnet) ?? undefined,
    haiku: params.get(SORT_PARAM_KEYS.haiku) ?? undefined,
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
 * Encode a filter + sort state to URLSearchParams, OMITTING defaults so a clean, shareable URL is
 * produced (mirrors the calculator's contract, and DD-4's per-band sort params follow the same
 * omit-the-default rule as `harness`/`class`). The default (unfiltered, all-capability) state
 * encodes to an empty query string. Sort fields are OPTIONAL on the input (like `harness`/`class`
 * already are) — an omitted band defaults to `"capability"` and is therefore not emitted.
 */
export function encodeState(state: FilterState & Partial<SortState>): URLSearchParams {
  const params = new URLSearchParams();
  if (state.harness !== undefined && state.harness !== DEFAULT_STATE.harness) {
    params.set(PARAM_KEYS.harness, state.harness);
  }
  if (state.class !== undefined && state.class !== DEFAULT_STATE.class) {
    params.set(PARAM_KEYS.class, state.class);
  }
  const opus = state.opus ?? DEFAULT_SORT_MODE;
  const sonnet = state.sonnet ?? DEFAULT_SORT_MODE;
  const haiku = state.haiku ?? DEFAULT_SORT_MODE;
  if (opus !== DEFAULT_SORT_MODE) {
    params.set(SORT_PARAM_KEYS.opus, opus);
  }
  if (sonnet !== DEFAULT_SORT_MODE) {
    params.set(SORT_PARAM_KEYS.sonnet, sonnet);
  }
  if (haiku !== DEFAULT_SORT_MODE) {
    params.set(SORT_PARAM_KEYS.haiku, haiku);
  }
  return params;
}
