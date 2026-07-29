// AI BENCHMARK — capability chart structural invariants (Phase 6, A-13/A-14, A-15/A-16).
//
// Two invariants exercised as direct component tests (not Gherkin-bound, mirroring
// `model-table.test.tsx`'s responsive-parity pattern):
//   1. The `unrated` group (no composite index) never renders as a zero-length bar — it is a
//      plain, labelled text list, and it emits no `<rect>` for those models.
//   2. The mobile ("label above bar") and `md`/`lg` ("left-gutter label") placements render the
//      SAME text content for every bar — jsdom applies no CSS, so both are present in the DOM and
//      parity can be asserted without a real viewport.

import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import {
  OPUS_ANCHOR_ID,
  SONNET_ANCHOR_ID,
  type BenchmarkId,
  type Dataset,
  type Figure,
  type Model,
} from "../core/data/models";
import { CapabilityChart } from "./capability-chart";

function fig(benchmark: BenchmarkId, value: number): Figure {
  return { benchmark, value, grade: "verified", source: "https://example.test/source" };
}

function fixtureModel(id: string, figures: Figure[] = []): Model {
  return { id, name: id, vendor: "Test", harnesses: ["claude-code"], figures, pricing: {} };
}

function fixtureDataset(models: Model[]): Dataset {
  return { snapshotDate: "2026-07-28", anchorIds: { opus: OPUS_ANCHOR_ID, sonnet: SONNET_ANCHOR_ID }, models };
}

describe("CapabilityChart — unrated group", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders a model with no composite index as a labelled text list entry, never a bar", () => {
    const noFigureModel = fixtureModel("no-figures-model");
    const ratedModel = fixtureModel("rated-model", [
      fig("swe-bench-verified", 80),
      fig("gpqa-diamond", 80),
      fig("swe-bench-pro", 80),
      fig("terminal-bench-2-1", 80),
    ]);
    render(<CapabilityChart dataset={fixtureDataset([noFigureModel, ratedModel])} locale="en" />);

    const unratedSection = screen.getByTestId("capability-chart-unrated");
    expect(unratedSection.textContent).toContain("no-figures-model");

    // The unrated model gets no bar anywhere in the chart.
    expect(screen.queryByTestId("capability-chart-bar-no-figures-model")).toBeNull();
    // The rated model DOES get a bar.
    expect(screen.getByTestId("capability-chart-bar-rated-model")).not.toBeNull();

    // No <rect> in the whole chart carries the unrated model's id.
    const svg = screen.getByTestId("capability-chart-svg");
    const rects = Array.from(svg.querySelectorAll("rect"));
    for (const rect of rects) {
      expect(rect.getAttribute("data-testid")).not.toBe("capability-chart-bar-no-figures-model");
    }
  });
});

describe("CapabilityChart — responsive label placement", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders the same text content in the mobile (above-bar) and md/lg (left-gutter) label placements", () => {
    const ratedModel = fixtureModel("rated-model", [
      fig("swe-bench-verified", 80),
      fig("gpqa-diamond", 80),
      fig("swe-bench-pro", 80),
      fig("terminal-bench-2-1", 80),
    ]);
    render(<CapabilityChart dataset={fixtureDataset([ratedModel])} locale="en" />);

    const mobileLabel = screen.getByTestId("capability-chart-label-mobile-rated-model");
    const desktopLabel = screen.getByTestId("capability-chart-label-desktop-rated-model");

    expect(mobileLabel.textContent).not.toBe("");
    expect(mobileLabel.textContent).toBe(desktopLabel.textContent);
    expect(mobileLabel.textContent).toContain("rated-model");
  });

  it("renders an lg-only axis tick row with the same numeric ticks regardless of viewport", () => {
    const ratedModel = fixtureModel("rated-model", [fig("swe-bench-verified", 80)]);
    render(<CapabilityChart dataset={fixtureDataset([ratedModel])} locale="en" />);

    const ticks = screen.getByTestId("capability-chart-ticks");
    expect(ticks.querySelectorAll("text").length).toBeGreaterThan(0);
    expect(screen.getByTestId("capability-chart-tick-0")).not.toBeNull();
  });
});
