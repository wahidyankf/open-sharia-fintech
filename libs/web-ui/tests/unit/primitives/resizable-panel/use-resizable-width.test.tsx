import { act, renderHook } from "@testing-library/react";
import { describe, it, expect, beforeEach } from "vitest";

import { useResizableWidth } from "../../../../src/primitives/resizable-panel/use-resizable-width";
import { DEFAULT_WIDTH } from "../../../../src/primitives/resizable-panel/width-model";

describe("useResizableWidth", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("initializes to DEFAULT_WIDTH when localStorage is empty", () => {
    const { result } = renderHook(() => useResizableWidth({ storageKey: "test-width-empty" }));

    expect(result.current.width).toBe(DEFAULT_WIDTH);
  });

  it("reads a persisted value on mount", () => {
    localStorage.setItem("test-width-persisted", "300");

    const { result } = renderHook(() => useResizableWidth({ storageKey: "test-width-persisted" }));

    expect(result.current.width).toBe(300);
  });

  it("writes to localStorage key ayokoding-sidebar-width on resize-end", () => {
    const { result } = renderHook(() => useResizableWidth({ storageKey: "ayokoding-sidebar-width" }));

    act(() => {
      result.current.commitWidth(310);
    });

    expect(localStorage.getItem("ayokoding-sidebar-width")).toBe("310");
  });

  it("updates width without writing to localStorage when called via updateWidth (live drag feedback)", () => {
    const { result } = renderHook(() => useResizableWidth({ storageKey: "test-update-width-no-persist" }));

    act(() => {
      result.current.updateWidth(275);
    });

    expect(result.current.width).toBe(275);
    expect(localStorage.getItem("test-update-width-no-persist")).toBeNull();
  });

  it("re-clamps a persisted value above the max band to the maximum on mount", () => {
    localStorage.setItem("test-width-corrupted-above", "999999");

    const { result } = renderHook(() =>
      useResizableWidth({ storageKey: "test-width-corrupted-above", minPct: 15, maxPct: 35, viewportPx: 1000 }),
    );

    expect(result.current.width).toBe(350);
  });

  it("re-clamps a persisted value below the min band to the minimum on mount", () => {
    localStorage.setItem("test-width-corrupted-below", "-500");

    const { result } = renderHook(() =>
      useResizableWidth({ storageKey: "test-width-corrupted-below", minPct: 15, maxPct: 35, viewportPx: 1000 }),
    );

    expect(result.current.width).toBe(150);
  });
});
