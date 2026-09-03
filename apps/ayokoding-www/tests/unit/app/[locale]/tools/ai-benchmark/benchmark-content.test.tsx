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
    const { BenchmarkContent } =
      await import("../../../../../../src/app/[locale]/tools/ai-benchmark/benchmark-content");
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
    const { BenchmarkContent } =
      await import("../../../../../../src/app/[locale]/tools/ai-benchmark/benchmark-content");
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

// AC-56 (Phase 7, cycle 7.2): the chart and roster (the page's primary content) now precede the
// legend and sources (reference material, collapsed into `<details>`) in document order — this
// file carried no `@covers` marker before this cycle, so one is added here directly (per
// delivery.md's instruction to follow cycle 6.1's pattern of binding the scenario at the same
// site as its assertion) alongside the mirrored binding in
// `apps/ayokoding-www/tests/unit/fe-steps/ai-benchmark.steps.tsx`.
// Regression test for Rule-15 UWT-007 (Phase 12 PR review, finding F2): the e2e AC-55/AC-60
// scenarios (retargeted in this same fix to the realistic 320x568/390x664 breakpoints) are the
// pixel-measuring half of this guard — jsdom cannot measure wrapped-text layout, so it cannot
// reproduce the "chart pushed past the fold" defect directly. This unit test is the other half: it
// pins the className-level edits the fix actually made, so reverting any one of them (even if the
// e2e suite were skipped locally) fails immediately here instead of silently reopening the defect.
describe("BenchmarkContent — Rule-15 UWT-007 regression guard (F2, Phase 12 PR review)", () => {
  it("hides the decorative subtitle below `sm` and keeps the trimmed vertical spacing that closes the above-the-fold gap", async () => {
    const { BenchmarkContent } =
      await import("../../../../../../src/app/[locale]/tools/ai-benchmark/benchmark-content");
    render(<BenchmarkContent />);

    const subtitle = screen.getByTestId("ai-bench-subtitle");
    expect(subtitle.className).toContain("hidden");
    expect(subtitle.className).toContain("sm:block");

    const root = screen.getByTestId("ai-bench-page");
    expect(root.className).toContain("py-4");
    expect(root.className).toContain("sm:py-6");

    const howToRead = screen.getByTestId("how-to-read");
    expect(howToRead.className).toContain("space-y-2");
    expect(howToRead.className).toContain("sm:space-y-4");

    const filtersMobile = screen.getByTestId("benchmark-filters-mobile");
    expect(filtersMobile.className).toContain("p-2");
    expect(filtersMobile.className).toContain("sm:p-3");
  });
});

describe("BenchmarkContent — document order (AC-56)", () => {
  it("renders the chart before the roster, and the roster before the legend and sources disclosures", async () => {
    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The chart precedes the roster and both precede the collapsed reference sections
    const { BenchmarkContent } =
      await import("../../../../../../src/app/[locale]/tools/ai-benchmark/benchmark-content");
    render(<BenchmarkContent />);

    const chart = screen.getByTestId("benchmark-chart");
    const roster = screen.getByTestId("model-table");
    const legend = screen.getByTestId("ai-bench-legend");
    const sources = screen.getByTestId("ai-bench-sources");

    // `DOCUMENT_POSITION_FOLLOWING` (4) on `a.compareDocumentPosition(b)` means `b` follows `a` in
    // the document — i.e. `a` precedes `b`.
    expect(chart.compareDocumentPosition(roster) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(roster.compareDocumentPosition(legend) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(roster.compareDocumentPosition(sources) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  });
});
