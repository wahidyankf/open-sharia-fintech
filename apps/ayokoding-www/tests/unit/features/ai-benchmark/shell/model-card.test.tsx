// AI BENCHMARK — ModelCard collapsed-summary + disclosure tests (Phase 6, DD-28, AC-53/AC-54).
//
// AC-53: the card's summary (name, class, composite index, price) is always visible; the remaining
// figures sit inside a closed `<details>`. AC-54 (cycle 6.2): the summary and the expanded content
// together carry every figure the desktop table's row carries for the same model (W-26/W-30).

import { describe, it, expect, afterEach } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { dataset, type Model } from "../../../../../src/features/ai-benchmark/core/data/models";
import { computeScoreViews } from "../../../../../src/features/ai-benchmark/shell/model-figures";
import { ModelCard } from "../../../../../src/features/ai-benchmark/shell/model-card";
import { ModelTable } from "../../../../../src/features/ai-benchmark/shell/model-table";

const MODEL_ID = "claude-opus-5";
const model = dataset.models.find((m) => m.id === MODEL_ID)!;
const view = computeScoreViews(dataset, dataset).get(MODEL_ID)!;

const SRC = "https://example.test/source";

/** A model reporting only `swe-bench-verified` — `swe-bench-pro`, `terminal-bench-2-1`, and
 * `gpqa-diamond` are all unpublished (AC-64 needs MORE THAN ONE unpublished figure). */
function unpublishedFixtureModel(): Model {
  return {
    id: "ac64-unpublished-model",
    name: "ac64-unpublished-model",
    vendor: "Test",
    harnesses: ["claude-code"],
    figures: [{ benchmark: "swe-bench-verified", value: 80, grade: "verified", source: SRC }],
    pricing: {},
  };
}

describe("ModelCard — collapsed summary until expanded (AC-53)", () => {
  afterEach(() => {
    cleanup();
  });

  it("shows the model name, its class, its composite index, and its price without interaction", () => {
    render(<ModelCard model={model} view={view} locale="en" />);
    expect(screen.getByTestId(`model-card-name-${MODEL_ID}`).textContent?.trim()).toBe(model.name);
    expect(screen.getByTestId(`model-card-class-${MODEL_ID}`).textContent?.trim().length).toBeGreaterThan(0);
    expect(screen.getByTestId(`model-card-index-${MODEL_ID}`).textContent?.trim().length).toBeGreaterThan(0);
    expect(screen.getByTestId(`model-card-price-${MODEL_ID}`).textContent?.trim().length).toBeGreaterThan(0);
  });

  it("keeps the remaining figures inside a closed disclosure", () => {
    const { container } = render(<ModelCard model={model} view={view} locale="en" />);
    const details = screen.getByTestId(`model-card-details-${MODEL_ID}`);
    expect(details.tagName).toBe("DETAILS");
    expect(details.hasAttribute("open")).toBe(false);
    // The disclosure carries at least one dt/dd pair not present in the always-visible summary.
    expect(details.querySelectorAll("dt").length).toBeGreaterThan(0);
    // The summary region (outside <details>) must NOT itself be inside the details element.
    const summaryRegion = container.querySelector(`[data-testid="model-card-summary-${MODEL_ID}"]`);
    expect(summaryRegion).not.toBeNull();
    expect(details.contains(summaryRegion)).toBe(false);
  });
});

describe("ModelCard — figure parity with the desktop table row (AC-54, W-30)", () => {
  afterEach(() => {
    cleanup();
  });

  /** Every formatted figure value rendered anywhere inside `root` (summary + expanded content). */
  function figureValues(root: Element | null): Set<string> {
    if (!root) return new Set();
    return new Set(
      Array.from(root.querySelectorAll('[data-slot="figure-cell-value"]')).map((el) => el.textContent?.trim() ?? ""),
    );
  }

  it("carries every figure the desktop table row carries once the disclosure is expanded", () => {
    const { container: cardContainer } = render(<ModelCard model={model} view={view} locale="en" />);
    const { container: tableContainer } = render(<ModelTable dataset={dataset} fullDataset={dataset} locale="en" />);
    const cardRoot = cardContainer.querySelector(`[data-testid="model-card-${MODEL_ID}"]`);
    // Desktop splits its figures across TWO rows (primary + a sibling detail row, cycle 6.3) — the
    // comparison combines both before checking against the card's own summary+details total.
    const primaryRow = tableContainer.querySelector(
      `[data-testid="model-table-desktop"] tbody tr[data-model-id="${MODEL_ID}"]`,
    );
    const detailRow = tableContainer.querySelector(
      `[data-testid="model-table-desktop"] tbody tr[data-model-detail-id="${MODEL_ID}"]`,
    );
    const tableValues = new Set([...figureValues(primaryRow), ...figureValues(detailRow)]);
    // jsdom has no CSS/layout engine, so a closed <details> still exposes its content to
    // querySelectorAll — the parity comparison does not depend on the disclosure's open state.
    expect(figureValues(cardRoot)).toEqual(tableValues);
    expect(figureValues(cardRoot).size).toBeGreaterThan(0);
  });
});

describe("ModelCard — disclosure content is grouped under labelled headings (AC-63, DD-34 Treatment 3)", () => {
  afterEach(() => {
    cleanup();
  });

  it("splits the expanded content into exactly two <section>s, each headed by an <h4>, covering every field exactly once", () => {
    render(<ModelCard model={model} view={view} locale="en" />);
    const details = screen.getByTestId(`model-card-details-${MODEL_ID}`);
    const sections = Array.from(details.querySelectorAll("section"));
    expect(sections.length).toBe(2);
    expect(sections.every((section) => section.querySelector("h4") !== null)).toBe(true);

    const labelsOf = (section: Element): Set<string> =>
      new Set(Array.from(section.querySelectorAll("dt")).map((dt) => dt.textContent?.trim() ?? ""));
    const [groupA, groupB] = sections.map(labelsOf);
    const allLabels = new Set(Array.from(details.querySelectorAll("dt")).map((dt) => dt.textContent?.trim() ?? ""));

    // Union of the two groups' labels equals every field's label (nothing left ungrouped)...
    expect(new Set([...groupA!, ...groupB!])).toEqual(allLabels);
    // ...and the two groups' label sets are disjoint (nothing belongs to more than one group).
    expect([...groupA!].some((label) => groupB!.has(label))).toBe(false);
  });

  it("nests each group heading one level below the card's own model-name heading", () => {
    render(<ModelCard model={model} view={view} locale="en" />);
    expect(screen.getByTestId(`model-card-name-${MODEL_ID}`).tagName).toBe("H3");
    const details = screen.getByTestId(`model-card-details-${MODEL_ID}`);
    const headings = Array.from(details.querySelectorAll("h4"));
    expect(headings.length).toBe(2);
  });
});

describe("ModelCard — unpublished figures share one value (AC-64, DD-34 Treatment 4)", () => {
  afterEach(() => {
    cleanup();
  });

  it("carries all unpublished labels as terms in ONE shared name-value group, never one dd per absent figure", () => {
    const unpublishedModel = unpublishedFixtureModel();
    const unpublishedView = computeScoreViews(
      { snapshotDate: "2026-07-28", anchorIds: dataset.anchorIds, models: [unpublishedModel] },
      { snapshotDate: "2026-07-28", anchorIds: dataset.anchorIds, models: [unpublishedModel] },
    ).get(unpublishedModel.id)!;
    render(<ModelCard model={unpublishedModel} view={unpublishedView} locale="en" />);
    const details = screen.getByTestId(`model-card-details-${unpublishedModel.id}`);

    // Exactly one <dd> anywhere in the disclosure carries the "not reported" text.
    const notReportedDds = Array.from(details.querySelectorAll("dd")).filter(
      (dd) => dd.textContent?.trim() === "Not reported",
    );
    expect(notReportedDds.length).toBe(1);

    // That one <dd>'s own name-value group carries TWO (or more) <dt> siblings — one per
    // unpublished label — never one <dt>/<dd> pair per absent figure.
    const sharedDd = notReportedDds[0]!;
    const sharedGroup = sharedDd.closest("div") ?? sharedDd.parentElement!;
    expect(sharedGroup.querySelectorAll("dt").length).toBeGreaterThanOrEqual(2);
    expect(sharedGroup.querySelectorAll("dd").length).toBe(1);
  });
});
