// AI BENCHMARK — cross-chart band-order parity (Phase 7 Gate, AC-11).
//
// AC-11's Gherkin scenario ("Models are ordered identically in both charts within a band") is
// bound at the `core/bands.ts` level (Phase 4's `ai-benchmark.steps.tsx` binding) — it proves the
// CANONICAL per-band list `computeGroups` produces has the right order property, which both charts
// read verbatim. This file is the Phase 7 Gate's own separate check: it renders BOTH chart
// components against the same fixture roster and asserts the ACTUAL DOM row order matches, one
// band at a time — not just that the shared canonical list they both read from is correctly
// ordered, but that neither chart's rendering re-orders it.

import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { OPUS_ANCHOR_ID, SONNET_ANCHOR_ID, type Dataset, type MeteredPrice, type Model } from "../core/data/models";
import { CapabilityChart } from "./capability-chart";
import { PriceChart } from "./price-chart";

const SRC = "https://example.test/source";

function metered(input: number, output: number): MeteredPrice {
  return { kind: "metered", input, output, grade: "verified", source: SRC };
}

/** A model scored on all four composite benchmarks at one value, priced with a metered rate — so
 * it renders a row in BOTH charts (a metered rate never gets routed to the price chart's
 * subscription-only list). */
function fixtureModel(id: string, score: number): Model {
  return {
    id,
    name: id,
    vendor: "Test",
    harnesses: ["claude-code"],
    figures: [
      { benchmark: "swe-bench-verified", value: score, grade: "verified", source: SRC },
      { benchmark: "swe-bench-pro", value: score, grade: "verified", source: SRC },
      { benchmark: "terminal-bench-2-1", value: score, grade: "verified", source: SRC },
      { benchmark: "gpqa-diamond", value: score, grade: "verified", source: SRC },
    ],
    pricing: { "claude-code": metered(1 + score / 10, 5 + score / 2) },
  };
}

// Deliberately excludes the OPUS/SONNET anchor ids, so `bands.ts` finds no anchor models in this
// fixture dataset and every scored model falls into the "light" band (undefined anchor thresholds)
// — one predictable band to compare, rather than depending on the live roster's anchor indices.
const dataset: Dataset = {
  snapshotDate: "2026-07-28",
  anchorIds: { opus: OPUS_ANCHOR_ID, sonnet: SONNET_ANCHOR_ID },
  models: [fixtureModel("order-c", 40), fixtureModel("order-a", 80), fixtureModel("order-b", 60)],
};

function rowOrderWithin(containerTestId: string, rowPrefix: string): string[] {
  const container = screen.getByTestId(containerTestId);
  const rows = Array.from(container.querySelectorAll(`[data-testid^="${rowPrefix}"]`));
  return rows
    .map((row) => row.getAttribute("data-testid") ?? "")
    .map((testId) => testId.slice(rowPrefix.length))
    .filter((id) => id.length > 0);
}

describe("Chart band-order parity (AC-11 gate check)", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders the light band's models in the same order in the capability chart and the price chart", () => {
    render(<CapabilityChart dataset={dataset} fullDataset={dataset} locale="en" />);
    const capabilityOrder = rowOrderWithin("capability-chart-band-light", "capability-chart-row-");
    cleanup();

    render(<PriceChart dataset={dataset} fullDataset={dataset} locale="en" />);
    const priceOrder = rowOrderWithin("price-chart-band-light", "price-chart-row-");

    // All three fixture models carry a metered price, so both charts render all three — the
    // membership AND the order must match exactly (highest score first: order-a, order-b, order-c).
    expect(capabilityOrder).toEqual(["order-a", "order-b", "order-c"]);
    expect(priceOrder).toEqual(capabilityOrder);
  });
});
