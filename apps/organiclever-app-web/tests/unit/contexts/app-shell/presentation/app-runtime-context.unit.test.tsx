import { describe, it, expect } from "vitest";
import { renderHook } from "@testing-library/react";
import type { ReactNode } from "react";
import {
  AppRuntimeProvider,
  useAppRuntime,
  type AppRuntimeContextValue,
} from "../../../../../src/contexts/app-shell/presentation/app-runtime-context";

describe("useAppRuntime", () => {
  it("throws when called outside an AppRuntimeProvider", () => {
    expect(() => renderHook(() => useAppRuntime())).toThrow("useAppRuntime must be called inside <AppRuntimeProvider>");
  });

  it("returns the provided context value inside an AppRuntimeProvider", () => {
    const value = {
      runtime: {} as AppRuntimeContextValue["runtime"],
      state: {} as AppRuntimeContextValue["state"],
      send: (() => {}) as AppRuntimeContextValue["send"],
      refreshKey: 0,
      refreshHome: () => {},
      openAddEntry: () => {},
      activeRoutine: null,
      setActiveRoutine: () => {},
      editingRoutine: null,
      setEditingRoutine: () => {},
      completedSession: null,
      setCompletedSession: () => {},
    } satisfies AppRuntimeContextValue;

    const wrapper = ({ children }: { children: ReactNode }) => (
      <AppRuntimeProvider value={value}>{children}</AppRuntimeProvider>
    );

    const { result } = renderHook(() => useAppRuntime(), { wrapper });

    expect(result.current).toBe(value);
  });
});
