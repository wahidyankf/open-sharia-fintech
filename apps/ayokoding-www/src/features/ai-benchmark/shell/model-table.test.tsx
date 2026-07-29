// AI BENCHMARK — ModelTable responsive parity test (Phase 5, W-26/W-27).
//
// Asserts the two representations the component emits — a semantic <table> for md+ and stacked
// definition cards below md — render the IDENTICAL set of figures for every model. CSS toggles
// which is visible at a given viewport; jsdom applies no CSS, so both are in the DOM and the test
// can assert parity without a real browser viewport.
//
// This is a direct component test (not a Gherkin step): the responsive behaviour is a structural
// invariant of the table, exercised here rather than via a feature scenario.

import { describe, it, expect, afterEach } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { dataset, type Dataset } from "../core/data/models";
import { ModelTable } from "./model-table";

/** The class-column text (td index 2: after vendor(0) and harnesses(1)) for one model's desktop row. */
function classCellText(container: Element, modelId: string): string | undefined {
  const row = container.querySelector(`tbody tr[data-model-id="${modelId}"]`);
  return row?.querySelectorAll("td")[2]?.textContent?.trim();
}

/** The set of formatted figure values rendered inside one model's representation. */
function figureValues(container: Element | null | undefined): Set<string> {
  if (!container) return new Set();
  return new Set(
    Array.from(container.querySelectorAll('[data-slot="figure-cell-value"]')).map((el) => el.textContent?.trim() ?? ""),
  );
}

describe("ModelTable responsive parity", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders a stacked-card mobile variant and a semantic table desktop variant", () => {
    render(<ModelTable dataset={dataset} locale="en" />);
    const desktop = screen.getByTestId("model-table-desktop");
    const mobile = screen.getByTestId("model-table-mobile");

    // Desktop: a real <table> with a caption and a row per model.
    expect(desktop.querySelector("table")).not.toBeNull();
    expect(desktop.querySelector("caption")).not.toBeNull();
    expect(desktop.querySelectorAll("tbody tr[data-model-id]").length).toBe(dataset.models.length);

    // Mobile: stacked definition cards — one <li> per model, each carrying a <dl>.
    expect(mobile.querySelectorAll("li[data-model-id]").length).toBe(dataset.models.length);
    expect(mobile.querySelectorAll("dl").length).toBe(dataset.models.length);
  });

  it("renders the same figures in the mobile card and the desktop table for every model", () => {
    render(<ModelTable dataset={dataset} locale="en" />);
    const desktop = screen.getByTestId("model-table-desktop");
    const mobile = screen.getByTestId("model-table-mobile");

    for (const model of dataset.models) {
      const desktopRow = desktop.querySelector(`tbody tr[data-model-id="${model.id}"]`);
      const mobileCard = mobile.querySelector(`li[data-model-id="${model.id}"]`);
      expect(desktopRow, `desktop row for ${model.id}`).not.toBeNull();
      expect(mobileCard, `mobile card for ${model.id}`).not.toBeNull();
      // The figure sets must match exactly — no figure may appear in one variant but not the other.
      expect(figureValues(mobileCard)).toEqual(figureValues(desktopRow));
    }
  });

  it("renders the identical figure set in both locales for a model with a conflicted figure", () => {
    // Localized formatting could in principle diverge between variants; assert it does not, for id too.
    render(<ModelTable dataset={dataset} locale="id" />);
    const desktop = screen.getByTestId("model-table-desktop");
    const mobile = screen.getByTestId("model-table-mobile");
    const desktopRow = desktop.querySelector('tbody tr[data-model-id="claude-opus-5"]');
    const mobileCard = mobile.querySelector('li[data-model-id="claude-opus-5"]');
    expect(desktopRow).not.toBeNull();
    expect(mobileCard).not.toBeNull();
    expect(figureValues(mobileCard)).toEqual(figureValues(desktopRow));
  });
});

// ─── Regression: a harness filter excluding both anchors must not collapse rated models to
// `light` (pr-review-synthesis-maker CRITICAL finding on PR #118, benchmark-content.tsx:28) ────
//
// `codex-cli` exposes neither `claude-opus-5` nor `claude-sonnet-5`. Before this fix, passing the
// codex-cli-filtered dataset as `<ModelTable dataset={filtered} locale="en" />` (no `fullDataset`)
// re-derived the anchor thresholds from the filtered subset — collapsing `gpt-5.6-sol` (opus on
// the full roster) to `light`. The fix threads a `fullDataset` prop so thresholds always come from
// the unfiltered roster while `dataset` still governs which models are displayed.
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

  it("reproduces the bug when fullDataset is omitted — the model collapses to Light", () => {
    render(<ModelTable dataset={codexCliDataset} locale="en" />);
    const desktop = screen.getByTestId("model-table-desktop");
    expect(classCellText(desktop, "gpt-5.6-sol")).toBe("Light");
  });
});
