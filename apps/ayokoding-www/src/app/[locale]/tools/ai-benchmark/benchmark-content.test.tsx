// Regression test for Rule-15 EWT-003: `router.push` is asynchronous, so changing the harness
// filter then the class filter in rapid succession — before Next.js commits the first navigation
// and re-renders with updated `searchParams` — previously dropped whichever filter was set first.
// `useSearchParams` is deliberately mocked to a FIXED value for the whole test (never updated by
// `mockPush`), simulating exactly that "no re-render has happened yet" window between the two
// calls; the fix must still compose both changes into the final pushed URL.

import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

const mockPush = vi.fn();

vi.mock("next/navigation", () => ({
  usePathname: () => "/en/tools/ai-benchmark",
  useRouter: () => ({ push: mockPush }),
  // Fixed, never updated by mockPush — simulates the real async gap where Next.js has not yet
  // committed the previous navigation nor re-rendered this component with a fresh searchParams.
  useSearchParams: () => new URLSearchParams(),
}));

vi.mock("@/features/i18n/shell/use-locale", () => ({
  useLocale: () => "en",
}));

afterEach(() => {
  cleanup();
  mockPush.mockClear();
});

describe("BenchmarkContent — rapid successive filter changes (Rule-15 EWT-003)", () => {
  it("composes a harness change followed immediately by a class change into one final URL with both filters", async () => {
    const { BenchmarkContent } = await import("./benchmark-content");
    render(<BenchmarkContent />);

    // Both mobile and desktop variants render simultaneously (jsdom applies no CSS) with matching
    // accessible names — scope to the desktop bar to get a single unambiguous element per control.
    const desktop = within(screen.getByTestId("benchmark-filters-desktop"));
    const harnessSelect = desktop.getByRole("combobox", { name: "Harness" });
    const classSelect = desktop.getByRole("combobox", { name: "Class" });

    // Fire both changes back-to-back, with no intervening render/flush — reproduces the race.
    (harnessSelect as HTMLSelectElement).value = "cursor";
    harnessSelect.dispatchEvent(new Event("change", { bubbles: true }));
    (classSelect as HTMLSelectElement).value = "sonnet";
    classSelect.dispatchEvent(new Event("change", { bubbles: true }));

    expect(mockPush).toHaveBeenCalledTimes(2);
    const finalUrl = mockPush.mock.calls[1]?.[0] as string;
    const finalParams = new URLSearchParams(finalUrl.split("?")[1] ?? "");
    expect(finalParams.get("harness")).toBe("cursor");
    expect(finalParams.get("class")).toBe("sonnet");
  });

  it("composes a class change followed immediately by a harness change into one final URL with both filters", async () => {
    const { BenchmarkContent } = await import("./benchmark-content");
    render(<BenchmarkContent />);

    // Both mobile and desktop variants render simultaneously (jsdom applies no CSS) with matching
    // accessible names — scope to the desktop bar to get a single unambiguous element per control.
    const desktop = within(screen.getByTestId("benchmark-filters-desktop"));
    const harnessSelect = desktop.getByRole("combobox", { name: "Harness" });
    const classSelect = desktop.getByRole("combobox", { name: "Class" });

    (classSelect as HTMLSelectElement).value = "opus";
    classSelect.dispatchEvent(new Event("change", { bubbles: true }));
    (harnessSelect as HTMLSelectElement).value = "claude-code";
    harnessSelect.dispatchEvent(new Event("change", { bubbles: true }));

    expect(mockPush).toHaveBeenCalledTimes(2);
    const finalUrl = mockPush.mock.calls[1]?.[0] as string;
    const finalParams = new URLSearchParams(finalUrl.split("?")[1] ?? "");
    expect(finalParams.get("class")).toBe("opus");
    expect(finalParams.get("harness")).toBe("claude-code");
  });
});
