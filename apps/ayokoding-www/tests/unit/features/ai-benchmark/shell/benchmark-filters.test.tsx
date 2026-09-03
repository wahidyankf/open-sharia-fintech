// AI BENCHMARK — filter bar responsive layout (Phase 8, N-17/N-18).
//
// The filter bar renders TWO representations simultaneously — jsdom applies no CSS, so both are
// present in the DOM regardless of viewport, mirroring `model-table.tsx`'s own mobile/desktop dual
// -render pattern:
//   - below `md`: a collapsed `<details>` disclosure naming the active-filter count in its summary;
//   - `md`/`lg`: an inline, wrapping bar naming the result count.
// Both variants must expose the SAME accessible control names for the harness and class selectors
// (matching `aria-label`s), so a screen-reader user gets identical semantics regardless of which
// representation their browser happens to display.

import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen, within } from "@testing-library/react";
import { BenchmarkFilters } from "../../../../../src/features/ai-benchmark/shell/benchmark-filters";
import type { FilterState } from "../../../../../src/features/ai-benchmark/core/filter";

const NONE: FilterState = {};

describe("BenchmarkFilters — responsive layout", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders a collapsed <details> disclosure (mobile) and an inline bar (desktop) at once", () => {
    render(<BenchmarkFilters state={NONE} resultCount={38} locale="en" onChange={vi.fn()} />);

    const mobile = screen.getByTestId("benchmark-filters-mobile");
    expect(mobile.tagName).toBe("DETAILS");

    const desktop = screen.getByTestId("benchmark-filters-desktop");
    expect(desktop).not.toBeNull();
  });

  it("the mobile disclosure summary states the active-filter count", () => {
    render(
      <BenchmarkFilters state={{ harness: "cursor", class: "opus" }} resultCount={2} locale="en" onChange={vi.fn()} />,
    );

    const summary = screen.getByTestId("benchmark-filters-mobile-summary");
    expect(summary.textContent ?? "").toContain("2");
  });

  it("with no active filter, the mobile disclosure summary states a zero active-filter count", () => {
    render(<BenchmarkFilters state={NONE} resultCount={38} locale="en" onChange={vi.fn()} />);

    const summary = screen.getByTestId("benchmark-filters-mobile-summary");
    expect(summary.textContent ?? "").toContain("0");
  });

  it("the desktop bar states the result count", () => {
    render(<BenchmarkFilters state={NONE} resultCount={17} locale="en" onChange={vi.fn()} />);

    const resultCount = screen.getByTestId("benchmark-filters-result-count");
    expect(resultCount.textContent ?? "").toContain("17");
  });

  // Rule-15 EWT-001 fix: the pre-fix result-count `role="status"` span lived ONLY inside the
  // `hidden md:flex` desktop-only div — below `md`, that div (and everything inside it) is removed
  // from the accessibility tree by `display: none`, so a mobile/screen-reader user who filtered got
  // no result-count announcement at all (only the mobile `<details>` summary's own, DIFFERENT
  // active-filter-count text updates). The fix hoists the span OUT of that div entirely, so it
  // stays in the a11y tree at every breakpoint (`sr-only md:not-sr-only` keeps it visually
  // unchanged at `md`+ while only its screen-reader announcement survives below `md`).
  it("keeps the result-count status span OUT of the desktop-only hidden-below-md container, so it survives at every breakpoint", () => {
    render(<BenchmarkFilters state={NONE} resultCount={17} locale="en" onChange={vi.fn()} />);

    const desktop = screen.getByTestId("benchmark-filters-desktop");
    expect(desktop.querySelector('[data-testid="benchmark-filters-result-count"]')).toBeNull();

    const resultCount = screen.getByTestId("benchmark-filters-result-count");
    expect(resultCount.getAttribute("role")).toBe("status");
  });

  it("both variants expose the same accessible control names for the harness and class selectors", () => {
    render(<BenchmarkFilters state={NONE} resultCount={38} locale="en" onChange={vi.fn()} />);

    const harnessLabel = "Harness";
    const classLabel = "Class";

    const mobile = within(screen.getByTestId("benchmark-filters-mobile"));
    const desktop = within(screen.getByTestId("benchmark-filters-desktop"));

    const mobileHarness = mobile.getByRole("combobox", { name: harnessLabel });
    const desktopHarness = desktop.getByRole("combobox", { name: harnessLabel });
    expect(mobileHarness).not.toBeNull();
    expect(desktopHarness).not.toBeNull();
    expect(mobileHarness).not.toBe(desktopHarness);

    const mobileClass = mobile.getByRole("combobox", { name: classLabel });
    const desktopClass = desktop.getByRole("combobox", { name: classLabel });
    expect(mobileClass).not.toBeNull();
    expect(desktopClass).not.toBeNull();
    expect(mobileClass).not.toBe(desktopClass);
  });

  // Rule-15 EWT-003 fix: `onChange` now reports only the changed axis as a PATCH — the caller
  // (`benchmark-content.tsx`) owns merging it onto its own always-current state, rather than this
  // component pre-merging against its (potentially stale, across rapid successive changes) `state`
  // prop. See that file's own regression test for the actual race this prevents.
  it("changing the harness select calls onChange with only the harness patch", () => {
    const onChange = vi.fn();
    render(<BenchmarkFilters state={{ class: "opus" }} resultCount={2} locale="en" onChange={onChange} />);

    const select = within(screen.getByTestId("benchmark-filters-desktop")).getByRole("combobox", { name: "Harness" });
    (select as HTMLSelectElement).value = "cursor";
    select.dispatchEvent(new Event("change", { bubbles: true }));

    expect(onChange).toHaveBeenCalledWith({ harness: "cursor" });
  });

  it("changing the class select calls onChange with only the class patch", () => {
    const onChange = vi.fn();
    render(<BenchmarkFilters state={{ harness: "cursor" }} resultCount={5} locale="en" onChange={onChange} />);

    const select = within(screen.getByTestId("benchmark-filters-desktop")).getByRole("combobox", { name: "Class" });
    (select as HTMLSelectElement).value = "sonnet";
    select.dispatchEvent(new Event("change", { bubbles: true }));

    expect(onChange).toHaveBeenCalledWith({ class: "sonnet" });
  });
});
