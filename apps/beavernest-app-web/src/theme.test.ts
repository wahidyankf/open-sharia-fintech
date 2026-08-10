import { afterEach, describe, expect, it, vi } from "vitest";
import { bootstrapTheme } from "./theme";

function mockSystemTheme(initialDark: boolean) {
  let listener: ((event: MediaQueryListEvent) => void) | undefined;
  const media = {
    matches: initialDark,
    addEventListener: vi.fn((_event: string, callback: (event: MediaQueryListEvent) => void) => {
      listener = callback;
    }),
    removeEventListener: vi.fn(),
  };

  vi.stubGlobal(
    "matchMedia",
    vi.fn(() => media),
  );
  return { media, change: (matches: boolean) => listener?.({ matches } as MediaQueryListEvent) };
}

afterEach(() => {
  document.documentElement.removeAttribute("data-theme");
  vi.unstubAllGlobals();
});

describe("bootstrapTheme", () => {
  it("applies the system preference before React mounts and cleans up its listener", () => {
    const systemTheme = mockSystemTheme(true);

    const cleanup = bootstrapTheme();

    expect(document.documentElement.dataset.theme).toBe("dark");
    expect(systemTheme.media.addEventListener).toHaveBeenCalledOnce();

    systemTheme.change(false);
    expect(document.documentElement.dataset.theme).toBe("light");

    cleanup();
    expect(systemTheme.media.removeEventListener).toHaveBeenCalledOnce();
  });

  it("is idempotent across repeated bootstrap calls", () => {
    const systemTheme = mockSystemTheme(false);

    const firstCleanup = bootstrapTheme();
    const secondCleanup = bootstrapTheme();

    expect(document.documentElement.dataset.theme).toBe("light");
    expect(systemTheme.media.addEventListener).toHaveBeenCalledTimes(1);

    firstCleanup();
    secondCleanup();
    expect(systemTheme.media.removeEventListener).toHaveBeenCalledOnce();
  });
});
