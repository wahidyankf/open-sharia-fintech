/**
 * Pure width-calculation core for the resizable-panel primitive.
 *
 * No React dependency, no DOM dependency — consumed later by a React hook
 * (`useResizableWidth`) that owns the stateful/side-effecting concerns
 * (localStorage, pointer events, keyboard events).
 */

/** Minimum panel width as a percentage of the viewport width. */
export const MIN_PCT = 15;

/** Maximum panel width as a percentage of the viewport width. */
export const MAX_PCT = 35;

/** Default panel width in pixels, used when no persisted value exists. */
export const DEFAULT_WIDTH = 250;

/**
 * Clamps a requested pixel width into a min/max percentage-of-viewport band.
 *
 * @param requestedPx - the width the user is requesting, in pixels
 * @param viewportPx - the current viewport width, in pixels
 * @param minPct - the lower band bound, as a percentage of the viewport
 * @param maxPct - the upper band bound, as a percentage of the viewport
 * @returns the requested width clamped into `[minPct, maxPct]` of the viewport, in pixels
 */
export function clampWidth(requestedPx: number, viewportPx: number, minPct: number, maxPct: number): number {
  const minPx = (minPct / 100) * viewportPx;
  const maxPx = (maxPct / 100) * viewportPx;

  return Math.min(Math.max(requestedPx, minPx), maxPx);
}

/**
 * Parses a raw string (e.g. read from `localStorage`) into a persisted width.
 *
 * @param raw - the raw stored value, or `null` if nothing was persisted
 * @returns the parsed width in pixels, or `undefined` if `raw` is unparseable
 */
export function parsePersistedWidth(raw: string | null): number | undefined {
  if (raw === null) {
    return undefined;
  }

  const parsed = Number(raw);

  return Number.isFinite(parsed) ? parsed : undefined;
}
