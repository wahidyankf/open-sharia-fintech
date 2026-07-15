"use client";

import { useEffect, useState } from "react";

import { clampWidth, DEFAULT_WIDTH, MAX_PCT, MIN_PCT, parsePersistedWidth } from "./width-model";

export interface UseResizableWidthOptions {
  /** `localStorage` key under which the width is persisted. */
  storageKey: string;
  /** Width to use when no persisted value exists. Defaults to `DEFAULT_WIDTH`. */
  defaultWidth?: number;
  /** Lower band bound, as a percentage of the viewport, used to re-clamp a persisted value on mount. Defaults to `MIN_PCT`. */
  minPct?: number;
  /** Upper band bound, as a percentage of the viewport, used to re-clamp a persisted value on mount. Defaults to `MAX_PCT`. */
  maxPct?: number;
  /**
   * Viewport width in pixels, used to re-clamp a persisted value on mount. Defaults to
   * `window.innerWidth`, read inside the mount effect (never during render).
   */
  viewportPx?: number;
}

export interface UseResizableWidthResult {
  /** The current panel width, in pixels. */
  width: number;
  /**
   * Commits a new width: updates state and persists it to `localStorage`.
   *
   * Callers are responsible for clamping the value (via `width-model.ts`'s
   * `clampWidth`) before calling this — the hook itself performs no clamping
   * on this path. The mount-read path below clamps a persisted value itself,
   * since that value may be stale, corrupted, or tampered with.
   */
  commitWidth: (nextWidth: number) => void;
}

/**
 * Manages a resizable panel's width, mirroring `theme-toggle.tsx`'s mount-effect
 * `localStorage` pattern: read the persisted value once on mount, and persist on every commit.
 */
export function useResizableWidth({
  storageKey,
  defaultWidth = DEFAULT_WIDTH,
  minPct = MIN_PCT,
  maxPct = MAX_PCT,
  viewportPx,
}: UseResizableWidthOptions): UseResizableWidthResult {
  const [width, setWidth] = useState(defaultWidth);

  useEffect(() => {
    const persisted = parsePersistedWidth(localStorage.getItem(storageKey));
    if (persisted !== undefined) {
      const resolvedViewportPx = viewportPx ?? window.innerWidth;
      setWidth(clampWidth(persisted, resolvedViewportPx, minPct, maxPct));
    }
    // Intentionally mirrors theme-toggle.tsx: read once on mount / when the key changes.
  }, [storageKey, minPct, maxPct, viewportPx]);

  const commitWidth = (nextWidth: number) => {
    setWidth(nextWidth);
    localStorage.setItem(storageKey, String(nextWidth));
  };

  return { width, commitWidth };
}
