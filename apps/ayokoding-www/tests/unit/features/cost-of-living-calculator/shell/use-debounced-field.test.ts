/**
 * Unit tests for useDebouncedField — the local-echo + debounced-commit hook that keeps
 * the calculator's number/text inputs responsive while the URL is the single source of
 * truth. Regression coverage for the "typing the salary stutters because every keystroke
 * writes the URL" bug.
 */

import { act, renderHook } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { useDebouncedField } from "../../../../../src/features/cost-of-living-calculator/shell/use-debounced-field";

describe("useDebouncedField", () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());

  it("echoes every keystroke locally but commits only once after the debounce window", () => {
    const commit = vi.fn();
    const { result } = renderHook(() => useDebouncedField<string>("", commit, 300));

    act(() => result.current.onChange("8"));
    act(() => result.current.onChange("80"));
    act(() => result.current.onChange("8000"));

    // Local echo tracks the latest keystroke immediately.
    expect(result.current.value).toBe("8000");
    // But no URL commit has happened yet — the window has not elapsed.
    expect(commit).not.toHaveBeenCalled();

    act(() => vi.advanceTimersByTime(300));

    // Exactly one commit, with the final value — the burst collapsed.
    expect(commit).toHaveBeenCalledTimes(1);
    expect(commit).toHaveBeenCalledWith("8000");
  });

  it("commits synchronously when delay <= 0 (uncontrolled/standalone path)", () => {
    const commit = vi.fn();
    const { result } = renderHook(() => useDebouncedField<string>("", commit, 0));

    act(() => result.current.onChange("500"));

    expect(result.current.value).toBe("500");
    expect(commit).toHaveBeenCalledTimes(1);
    expect(commit).toHaveBeenCalledWith("500");
  });

  it("flush() commits a pending value immediately (e.g. on blur)", () => {
    const commit = vi.fn();
    const { result } = renderHook(() => useDebouncedField<string>("", commit, 300));

    act(() => result.current.onChange("1200"));
    expect(commit).not.toHaveBeenCalled();

    act(() => result.current.flush());
    expect(commit).toHaveBeenCalledTimes(1);
    expect(commit).toHaveBeenCalledWith("1200");

    // The cleared timer must not fire a second, duplicate commit.
    act(() => vi.advanceTimersByTime(300));
    expect(commit).toHaveBeenCalledTimes(1);
  });

  it("ignores external updates while a commit is pending, then adopts them when idle", () => {
    const commit = vi.fn();
    const { result, rerender } = renderHook(({ ext }) => useDebouncedField<string>(ext, commit, 300), {
      initialProps: { ext: "100" },
    });

    // User is mid-edit: a competing external value must not clobber the local echo.
    act(() => result.current.onChange("999"));
    rerender({ ext: "100" });
    expect(result.current.value).toBe("999");

    // Once the pending commit fires and nothing is in-flight, a fresh external is adopted.
    act(() => vi.advanceTimersByTime(300));
    rerender({ ext: "7777" });
    expect(result.current.value).toBe("7777");
  });

  it("a late commit uses the freshest onCommit closure (no stale-state overwrite)", () => {
    const first = vi.fn();
    const second = vi.fn();
    const { result, rerender } = renderHook(({ cb }) => useDebouncedField<string>("", cb, 300), {
      initialProps: { cb: first },
    });

    act(() => result.current.onChange("42"));
    // An unrelated change re-rendered the consumer with a new commit closure.
    rerender({ cb: second });

    act(() => vi.advanceTimersByTime(300));

    expect(first).not.toHaveBeenCalled();
    expect(second).toHaveBeenCalledWith("42");
  });
});
