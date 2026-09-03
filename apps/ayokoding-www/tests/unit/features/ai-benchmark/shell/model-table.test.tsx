// AI BENCHMARK — ModelTable responsive parity test (Phase 5/6, W-26/W-27, DD-27/DD-28).
//
// Asserts the two representations the component emits — a semantic <table> for md+ (primary
// columns plus a per-row detail disclosure) and `model-card.tsx`'s stacked summary cards below md —
// render the IDENTICAL set of figures for every model. CSS toggles which is visible at a given
// viewport; jsdom applies no CSS, so both are in the DOM and the test can assert parity without a
// real browser viewport.
//
// This is a direct component test (not a Gherkin step): the responsive behaviour is a structural
// invariant of the table, exercised here rather than via a feature scenario.

import { describe, it, expect, afterEach } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { dataset, type Dataset } from "../../../../../src/features/ai-benchmark/core/data/models";
import { ModelTable } from "../../../../../src/features/ai-benchmark/shell/model-table";

/** A model's primary row and its adjacent detail row (cycle 6.3: two <tr>s per model). */
function rowsFor(desktop: Element, modelId: string): { primary: Element | null; detail: Element | null } {
  return {
    primary: desktop.querySelector(`tbody tr[data-model-id="${modelId}"]`),
    detail: desktop.querySelector(`tbody tr[data-model-detail-id="${modelId}"]`),
  };
}

/** The class-column text (td index 1: after vendor(0)) for one model's desktop primary row. */
function classCellText(desktop: Element, modelId: string): string | undefined {
  const { primary } = rowsFor(desktop, modelId);
  return primary?.querySelectorAll("td")[1]?.textContent?.trim();
}

/** The set of formatted figure values rendered inside one model's representation. */
function figureValues(container: Element | null | undefined): Set<string> {
  if (!container) return new Set();
  return new Set(
    Array.from(container.querySelectorAll('[data-slot="figure-cell-value"]')).map((el) => el.textContent?.trim() ?? ""),
  );
}

/** Every figure value across a model's primary row AND its adjacent detail row, combined. */
function desktopFigureValues(desktop: Element, modelId: string): Set<string> {
  const { primary, detail } = rowsFor(desktop, modelId);
  return new Set([...figureValues(primary), ...figureValues(detail)]);
}

describe("ModelTable responsive parity", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders a stacked-card mobile variant and a semantic table desktop variant", () => {
    render(<ModelTable dataset={dataset} fullDataset={dataset} locale="en" />);
    const desktop = screen.getByTestId("model-table-desktop");
    const mobile = screen.getByTestId("model-table-mobile");

    // Desktop: a real <table> with a caption and one primary row + one detail row per model.
    expect(desktop.querySelector("table")).not.toBeNull();
    expect(desktop.querySelector("caption")).not.toBeNull();
    expect(desktop.querySelectorAll("tbody tr[data-model-id]").length).toBe(dataset.models.length);
    expect(desktop.querySelectorAll("tbody tr[data-model-detail-id]").length).toBe(dataset.models.length);

    // Mobile: stacked definition cards — one <li> per model. Each card's disclosure now groups its
    // fields under two labelled <section>s (DD-34 Treatment 3, cycle 6.6), so each model carries
    // TWO <dl>s, not one.
    expect(mobile.querySelectorAll("li[data-model-id]").length).toBe(dataset.models.length);
    expect(mobile.querySelectorAll("dl").length).toBe(dataset.models.length * 2);
  });

  it("renders the same figures in the mobile card and the desktop table for every model", () => {
    render(<ModelTable dataset={dataset} fullDataset={dataset} locale="en" />);
    const desktop = screen.getByTestId("model-table-desktop");
    const mobile = screen.getByTestId("model-table-mobile");

    for (const model of dataset.models) {
      const { primary: desktopRow, detail: detailRow } = rowsFor(desktop, model.id);
      const mobileCard = mobile.querySelector(`li[data-model-id="${model.id}"]`);
      expect(desktopRow, `desktop row for ${model.id}`).not.toBeNull();
      expect(detailRow, `desktop detail row for ${model.id}`).not.toBeNull();
      expect(mobileCard, `mobile card for ${model.id}`).not.toBeNull();
      // The figure sets must match exactly — no figure may appear in one variant but not the
      // other. Desktop now splits its figures across TWO rows (primary + detail, cycle 6.3), so
      // the comparison combines both before checking against the mobile card's own summary+detail.
      expect(figureValues(mobileCard)).toEqual(desktopFigureValues(desktop, model.id));
    }
  });

  it("renders the identical figure set in both locales for a model with a conflicted figure", () => {
    // Localized formatting could in principle diverge between variants; assert it does not, for id too.
    render(<ModelTable dataset={dataset} fullDataset={dataset} locale="id" />);
    const desktop = screen.getByTestId("model-table-desktop");
    const mobile = screen.getByTestId("model-table-mobile");
    const mobileCard = mobile.querySelector('li[data-model-id="claude-opus-5"]');
    const { primary: desktopRow, detail: detailRow } = rowsFor(desktop, "claude-opus-5");
    expect(desktopRow).not.toBeNull();
    expect(detailRow).not.toBeNull();
    expect(mobileCard).not.toBeNull();
    expect(figureValues(mobileCard)).toEqual(desktopFigureValues(desktop, "claude-opus-5"));
  });
});

// ─── Regression: a harness filter excluding both anchors must not collapse rated models to
// `haiku` (pr-review-synthesis-maker CRITICAL finding on PR #118, benchmark-content.tsx:28) ────
//
// `codex-cli` exposes neither `claude-opus-5` nor `claude-sonnet-5`. Before this fix, passing the
// codex-cli-filtered dataset as `<ModelTable dataset={filtered} locale="en" />` (no `fullDataset`)
// re-derived the anchor thresholds from the filtered subset — collapsing `gpt-5.6-sol` (opus on
// the full roster) to `haiku`. The fix threads a `fullDataset` prop so thresholds always come from
// the unfiltered roster while `dataset` still governs which models are displayed. `fullDataset` is
// now a REQUIRED prop (pr-review-synthesis-maker Finding 3, PR #118 cycle 2), so the "omitted"
// half of this regression is a compile-time `TS2741` error rather than a runtime test — a strictly
// stronger guard than the runtime assertion this file used to carry.
describe("ModelTable — fullDataset keeps a harness-filtered model's full-roster class label", () => {
  afterEach(() => {
    cleanup();
  });

  const codexCliModels = dataset.models.filter((m) => m.harnesses.includes("codex-cli"));
  const codexCliDataset: Dataset = { ...dataset, models: codexCliModels };

  it("sanity: codex-cli excludes both anchor models", () => {
    expect(codexCliModels.some((m) => m.id === "claude-opus-5")).toBe(false);
    expect(codexCliModels.some((m) => m.id === "claude-sonnet-5")).toBe(false);
    expect(codexCliModels.some((m) => m.id === "gpt-5.6-sol")).toBe(true);
  });

  it("shows the model's full-roster class (Opus) when fullDataset is passed", () => {
    render(<ModelTable dataset={codexCliDataset} fullDataset={dataset} locale="en" />);
    const desktop = screen.getByTestId("model-table-desktop");
    expect(classCellText(desktop, "gpt-5.6-sol")).toBe("Opus");
  });
});

// ─── R5/AC-59 (tech-docs.md §DD-27) — two-unit fix. Unit 1 (Phase 1) removed the wrapper's
// `lg`-breakpoint overflow override so `overflow-x-auto` held a scroll container at every
// breakpoint, at the cost of the sticky `<thead>` no longer sticking at `lg`. Unit 2 (here, cycle
// 6.3) restores that override — safe now that the table is reduced to its primary columns and fits
// below the `lg` viewport. This guard flips from "the override is absent" (Phase 1) to "the
// override is present AND the table stays within its primary-column budget" (Phase 6) — a table
// that regained the override WITHOUT shedding its secondary columns would still overflow (AC-52).
describe("ModelTable — R5/AC-59 desktop overflow + sticky-header column budget", () => {
  afterEach(() => {
    cleanup();
  });

  it("restores the lg-breakpoint overflow override now that the table fits", () => {
    const { container } = render(<ModelTable dataset={dataset} fullDataset={dataset} locale="en" />);
    const wrapper = container.querySelector('[data-testid="model-table-desktop"] [data-slot="table-wrapper"]');
    expect(wrapper?.className).toContain("lg:overflow-visible");
  });

  it("keeps the desktop primary row within the primary-column budget (model, vendor, class, index, input price, output price)", () => {
    const { container } = render(<ModelTable dataset={dataset} fullDataset={dataset} locale="en" />);
    const headerCells = container.querySelectorAll(
      '[data-testid="model-table-desktop"] thead tr th, [data-testid="model-table-desktop"] thead tr td',
    );
    // 6 primary columns: model, vendor, class, index, input price, output price. Falsifiable both
    // ways: re-adding harnesses/benchmark/coverage columns to the header prints more than 6 and
    // fails; dropping a genuine primary column prints fewer than 6 and fails.
    expect(headerCells.length).toBe(6);
  });
});

// ─── Rule-15 DWT-005 fix (Phase 11): the detail row must not inherit the primary row's hover tint ─

describe("ModelTable — Rule-15 DWT-005 fix (detail row does not inherit the primary row's hover tint)", () => {
  afterEach(() => {
    cleanup();
  });

  it("gives the detail TableRow its own hover:bg-transparent override, leaving the primary row's hover class untouched", () => {
    const { container } = render(<ModelTable dataset={dataset} fullDataset={dataset} locale="en" />);
    const anyModelId = dataset.models[0]!.id;
    const { primary, detail } = rowsFor(container.querySelector('[data-testid="model-table-desktop"]')!, anyModelId);
    expect(detail?.className).toContain("hover:bg-transparent");
    // Falsifiable both ways: a regression that also strips the primary row's own shared hover
    // treatment (rather than overriding only the detail row) would make this fail too.
    expect(primary?.className).not.toContain("hover:bg-transparent");
  });
});

// ─── Rule-15 DWT-006 fix (Phase 11): the collapsed absent-figure run shares the reported-figure rail ─

describe("ModelTable — Rule-15 DWT-006 fix (collapsed absent-figure run shares the reported-figure grid rail)", () => {
  afterEach(() => {
    cleanup();
  });

  it("wraps the collapsed absent-figure run in the same grid-rail class reported figures use", () => {
    // gpt-5.6-terra reports only one of the four composite benchmarks (see core/data/models.ts),
    // so its detail region has a genuine collapsed multi-label run to check alignment against.
    const partialModel = dataset.models.find((m) => m.id === "gpt-5.6-terra");
    expect(partialModel).toBeDefined();
    const { container } = render(<ModelTable dataset={dataset} fullDataset={dataset} locale="en" />);
    const { detail } = rowsFor(container.querySelector('[data-testid="model-table-desktop"]')!, "gpt-5.6-terra");
    expect(detail).not.toBeNull();
    const notReportedValue = Array.from(detail!.querySelectorAll('[data-slot="figure-cell-value"]')).find(
      (el) => el.textContent?.trim() === "Not reported",
    );
    expect(notReportedValue).toBeDefined();
    // The rail wrapper is the value's own grandparent (dd's parent `<div>` carrying the grid class) —
    // same `grid-cols-[6.5rem_1fr]` template Treatment 2 already applies to every REPORTED figure's
    // own row, so this row's `<dd>` starts at the identical rail position.
    const railWrapper = notReportedValue!.closest('div[class*="grid-cols-[6.5rem_1fr]"]');
    expect(railWrapper).not.toBeNull();
  });
});

// ─── Rule-15 UWT-016 fix (Phase 11): a subscription's usage-cap detail reaches the model's own row ─

describe("ModelTable — Rule-15 UWT-016 fix (subscription usage-cap detail on the model's own row)", () => {
  afterEach(() => {
    cleanup();
  });

  it("surfaces mimo-v2.5's usage-cap text in its own detail region, not only in the chart's Unrated list", () => {
    const model = dataset.models.find((m) => m.id === "mimo-v2.5");
    expect(model?.pricing["opencode-go"]?.kind).toBe("subscription");
    const caps = (model!.pricing["opencode-go"] as { caps?: string }).caps;
    expect(caps).toBeTruthy();

    const { container } = render(<ModelTable dataset={dataset} fullDataset={dataset} locale="en" />);
    const { detail } = rowsFor(container.querySelector('[data-testid="model-table-desktop"]')!, "mimo-v2.5");
    expect(detail).not.toBeNull();
    expect(detail!.textContent ?? "").toContain(caps);
  });
});
