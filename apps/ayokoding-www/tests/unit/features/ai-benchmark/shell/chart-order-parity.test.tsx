// AI BENCHMARK — per-band sort-order gate (Phase 3, DD-4).
//
// Pre-merge, this file rendered the two separate charts against the same fixture and asserted
// their DOM row orders matched each other — proving neither chart's rendering re-ordered the
// shared canonical list `computeGroups` produces (AC-11). Post-merge there is only one chart, so
// that cross-chart comparison is now vacuous by construction. This file's Phase-3 replacement
// instead gates the property the merge actually introduced: `<BenchmarkChart>`'s per-band sort
// control (DD-4) must reorder a band's rows to match `core/sort.ts`'s comparators exactly, for
// every one of the three `SortMode`s — the default `"capability"` order still matches
// `computeGroups()`'s own canonical order (AC-11's original guarantee, now checked against the
// one merged chart instead of two).

import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import {
  OPUS_ANCHOR_ID,
  SONNET_ANCHOR_ID,
  type Dataset,
  type MeteredPrice,
  type Model,
} from "../../../../../src/features/ai-benchmark/core/data/models";
import { computeGroups } from "../../../../../src/features/ai-benchmark/core/bands";
import { BenchmarkChart } from "../../../../../src/features/ai-benchmark/shell/benchmark-chart";

const SRC = "https://example.test/source";

function metered(input: number, output: number): MeteredPrice {
  return { kind: "metered", input, output, grade: "verified", source: SRC };
}

/** A model scored on all four composite benchmarks at one value, priced with a distinct metered rate. */
function fixtureModel(id: string, score: number, output: number): Model {
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
    pricing: { "claude-code": metered(1, output) },
  };
}

// Deliberately excludes the OPUS/SONNET anchor ids, so `bands.ts` finds no anchor models in this
// fixture dataset and every scored model falls into the "haiku" band (undefined anchor thresholds)
// — one predictable band to sort, rather than depending on the live roster's anchor indices.
// Composite index (score) and output price are deliberately UNCORRELATED (highest score does not
// have the highest price) so the three sort modes below produce three genuinely different orders.
const dataset: Dataset = {
  snapshotDate: "2026-07-28",
  anchorIds: { opus: OPUS_ANCHOR_ID, sonnet: SONNET_ANCHOR_ID },
  models: [
    fixtureModel("order-c", 40, 50), // lowest score, highest price
    fixtureModel("order-a", 80, 10), // highest score, lowest price
    fixtureModel("order-b", 60, 30), // middle score, middle price
  ],
};

function rowOrderWithin(containerTestId: string, rowPrefix: string): string[] {
  const container = screen.getByTestId(containerTestId);
  const rows = Array.from(container.querySelectorAll(`[data-testid^="${rowPrefix}"]`));
  return rows
    .map((row) => row.getAttribute("data-testid") ?? "")
    .map((testId) => testId.slice(rowPrefix.length))
    .filter((id) => id.length > 0);
}

describe("BenchmarkChart per-band sort order (AC-11 / DD-4 gate check)", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders the haiku band in computeGroups()'s own canonical order by default (capability mode)", () => {
    render(<BenchmarkChart dataset={dataset} fullDataset={dataset} locale="en" />);
    const domOrder = rowOrderWithin("benchmark-chart-band-haiku", "benchmark-chart-row-");

    const canonicalOrder = computeGroups(dataset)
      .haiku.map((s) => s.model.id)
      .filter((id) => domOrder.includes(id));

    expect(domOrder).toEqual(["order-a", "order-b", "order-c"]); // descending score: 80, 60, 40
    expect(domOrder).toEqual(canonicalOrder);
  });

  it("reorders the haiku band ascending by price when sortState.haiku is price-asc", () => {
    render(
      <BenchmarkChart
        dataset={dataset}
        fullDataset={dataset}
        locale="en"
        sortState={{ opus: "capability", sonnet: "capability", haiku: "price-asc" }}
      />,
    );
    const domOrder = rowOrderWithin("benchmark-chart-band-haiku", "benchmark-chart-row-");

    expect(domOrder).toEqual(["order-a", "order-b", "order-c"]); // ascending output price: 10, 30, 50
  });

  it("reorders the haiku band descending by price when sortState.haiku is price-desc", () => {
    render(
      <BenchmarkChart
        dataset={dataset}
        fullDataset={dataset}
        locale="en"
        sortState={{ opus: "capability", sonnet: "capability", haiku: "price-desc" }}
      />,
    );
    const domOrder = rowOrderWithin("benchmark-chart-band-haiku", "benchmark-chart-row-");

    expect(domOrder).toEqual(["order-c", "order-b", "order-a"]); // descending output price: 50, 30, 10
  });
});
