"use client";

import { useEffect, useState } from "react";

import { DEFAULT_WIDTH, parsePersistedWidth } from "./width-model";

export interface UseResizableWidthOptions {
  /** `localStorage` key under which the width is persisted. */
  storageKey: string;
  /** Width to use when no persisted value exists. Defaults to `DEFAULT_WIDTH`. */
  defaultWidth?: number;
}

export interface UseResizableWidthResult {
  /** The current panel width, in pixels. */
  width: number;
  /**
   * Commits a new width: updates state and persists it to `localStorage`.
   *
   * Callers are responsible for clamping the value (via `width-model.ts`'s
   * `clampWidth`) before calling this — the hook itself performs no clamping.
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
}: UseResizableWidthOptions): UseResizableWidthResult {
  const [width, setWidth] = useState(defaultWidth);

  useEffect(() => {
    const persisted = parsePersistedWidth(localStorage.getItem(storageKey));
    if (persisted !== undefined) {
      setWidth(persisted);
    }
    // Intentionally mirrors theme-toggle.tsx: read once on mount / when the key changes.
  }, [storageKey]);

  const commitWidth = (nextWidth: number) => {
    setWidth(nextWidth);
    localStorage.setItem(storageKey, String(nextWidth));
  };

  return { width, commitWidth };
}
