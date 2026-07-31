// AI BENCHMARK — ModelCard collapsed-summary + disclosure tests (Phase 6, DD-28, AC-53/AC-54).
//
// AC-53: the card's summary (name, class, composite index, price) is always visible; the remaining
// figures sit inside a closed `<details>`. AC-54 (cycle 6.2): the summary and the expanded content
// together carry every figure the desktop table's row carries for the same model (W-26/W-30).

import { describe, it, expect, afterEach } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { dataset } from "../core/data/models";
import { computeScoreViews } from "./model-figures";
import { ModelCard } from "./model-card";
import { ModelTable } from "./model-table";

const MODEL_ID = "claude-opus-5";
const model = dataset.models.find((m) => m.id === MODEL_ID)!;
const view = computeScoreViews(dataset, dataset).get(MODEL_ID)!;

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
    const { container: tableContainer } = render(
      <table>
        <tbody>
          <ModelTable dataset={dataset} fullDataset={dataset} locale="en" />
        </tbody>
      </table>,
    );
    const cardRoot = cardContainer.querySelector(`[data-testid="model-card-${MODEL_ID}"]`);
    const tableRow = tableContainer.querySelector(
      `[data-testid="model-table-desktop"] tbody tr[data-model-id="${MODEL_ID}"]`,
    );
    // jsdom has no CSS/layout engine, so a closed <details> still exposes its content to
    // querySelectorAll — the parity comparison does not depend on the disclosure's open state.
    expect(figureValues(cardRoot)).toEqual(figureValues(tableRow));
    expect(figureValues(cardRoot).size).toBeGreaterThan(0);
  });
});
