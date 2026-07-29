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
  dataset as fullRosterDataset,
  OPUS_ANCHOR_ID,
  SONNET_ANCHOR_ID,
  type BenchmarkId,
  type Dataset,
  type Figure,
  type HarnessId,
  type Model,
} from "../core/data/models";
import { computeGroups } from "../core/bands";
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
    const ds = fixtureDataset([noFigureModel, ratedModel]);
    render(<CapabilityChart dataset={ds} fullDataset={ds} locale="en" />);

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
    const ds = fixtureDataset([ratedModel]);
    render(<CapabilityChart dataset={ds} fullDataset={ds} locale="en" />);

    const mobileLabel = screen.getByTestId("capability-chart-label-mobile-rated-model");
    const desktopLabel = screen.getByTestId("capability-chart-label-desktop-rated-model");

    expect(mobileLabel.textContent).not.toBe("");
    expect(mobileLabel.textContent).toBe(desktopLabel.textContent);
    expect(mobileLabel.textContent).toContain("rated-model");
  });

  it("renders an lg-only axis tick row with the same numeric ticks regardless of viewport", () => {
    const ratedModel = fixtureModel("rated-model", [fig("swe-bench-verified", 80)]);
    const ds = fixtureDataset([ratedModel]);
    render(<CapabilityChart dataset={ds} fullDataset={ds} locale="en" />);

    const ticks = screen.getByTestId("capability-chart-ticks");
    expect(ticks.querySelectorAll("text").length).toBeGreaterThan(0);
    expect(screen.getByTestId("capability-chart-tick-0")).not.toBeNull();
  });
});

// ─── Regression: THIS component's own `fullDataset` wiring must not collapse a harness-filtered
// rated model to `light` (pr-review-synthesis-maker HIGH finding, PR #118 cycle 2). `bands.ts` and
// `model-table.tsx` already carry this proof — this component did not, and reverting its fix alone
// passed the whole suite. Derives the filtered roster and the surviving model from the REAL
// dataset, mirroring `bands.unit.test.ts`'s pattern, rather than hardcoding an id.
describe("CapabilityChart — fullDataset keeps a harness-filtered survivor in its full-roster band", () => {
  afterEach(() => {
    cleanup();
  });

  const harness: HarnessId = "codex-cli";

  const fullRosterBand = (() => {
    const groups = computeGroups(fullRosterDataset);
    const byId = new Map<string, string>();
    for (const list of [groups.opus, groups.sonnet, groups.light, groups.unrated]) {
      for (const s of list) byId.set(s.model.id, s.band);
    }
    return byId;
  })();

  const filteredModels = fullRosterDataset.models.filter((m) => m.harnesses.includes(harness));
  const filteredDataset: Dataset = { ...fullRosterDataset, models: filteredModels };
  const survivor = filteredModels.find(
    (m) => fullRosterBand.get(m.id) === "opus" || fullRosterBand.get(m.id) === "sonnet",
  );

  it(`sanity: ${harness} excludes both anchor models but still exposes an opus/sonnet survivor`, () => {
    expect(filteredModels.some((m) => m.id === OPUS_ANCHOR_ID)).toBe(false);
    expect(filteredModels.some((m) => m.id === SONNET_ANCHOR_ID)).toBe(false);
    expect(survivor, `${harness} must expose at least one opus/sonnet survivor`).toBeDefined();
  });

  it("renders the surviving model under its correct full-roster band when fullDataset is passed", () => {
    render(<CapabilityChart dataset={filteredDataset} fullDataset={fullRosterDataset} locale="en" />);
    const expectedBand = fullRosterBand.get(survivor!.id);
    const bandGroup = screen.getByTestId(`capability-chart-band-${expectedBand}`);
    expect(bandGroup.querySelector(`[data-testid="capability-chart-row-${survivor!.id}"]`)).not.toBeNull();
  });

  it("WITHOUT fullDataset, the bug would reproduce — the survivor's own band collapses to light", () => {
    // Proves the assertion above is not vacuous: the same survivor, scored against ONLY the
    // filtered subset (no full-roster anchors), no longer lands in its full-roster band.
    const collapsedGroups = computeGroups(filteredDataset);
    const collapsedById = new Map<string, string>();
    for (const list of [collapsedGroups.opus, collapsedGroups.sonnet, collapsedGroups.light, collapsedGroups.unrated]) {
      for (const s of list) collapsedById.set(s.model.id, s.band);
    }
    expect(collapsedById.get(survivor!.id)).toBe("light");
    expect(fullRosterBand.get(survivor!.id)).not.toBe("light");
  });
});
