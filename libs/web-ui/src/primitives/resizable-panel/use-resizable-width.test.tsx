import { act, renderHook } from "@testing-library/react";
import { describe, it, expect, beforeEach } from "vitest";

import { useResizableWidth } from "./use-resizable-width";
import { DEFAULT_WIDTH } from "./width-model";

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
});
