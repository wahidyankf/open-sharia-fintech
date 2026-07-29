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
import { CapabilityChart, MARKER_MIN_MARGIN, PLOT_WIDTH, PLOT_X, SVG_WIDTH } from "./capability-chart";

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

// ─── Regression: DWT-001's right-margin fix (pr-review-synthesis-maker HIGH finding, PR #122
// cycle 1) had zero automated coverage — verification was live-screenshot-only. This is a pure
// computed-geometry assertion (no browser needed): the right margin the low-coverage marker text
// renders into (`SVG_WIDTH - (PLOT_X + PLOT_WIDTH)`) must stay at least `MARKER_MIN_MARGIN` — the
// documented, locale-derived minimum the marker needs at `text-[9px]` to avoid the SVG clipping it
// past its own `viewBox`.
//
// NOTE (PR #122 cycle 2 fix): `PLOT_WIDTH = SVG_WIDTH - PLOT_X - MARKER_MIN_MARGIN` by definition
// (capability-chart.tsx:77), so `actualMargin` below is ALGEBRAICALLY IDENTICAL to
// `MARKER_MIN_MARGIN` for any value of the constants that compose it — comparing it back against
// `MARKER_MIN_MARGIN` can never fail. The `toBe(164)` assertion is the real regression guard: it
// locks the *current* computed value of `MARKER_MIN_MARGIN` (derived from `MARKER_GAP`,
// `MARKER_SAFETY_BUFFER`, `MARKER_CHAR_WIDTH_RATIO`, `WORST_CASE_MARKER_LENGTH`, and
// `MARKER_FONT_SIZE`) to a literal, so any future edit to those inputs shows up as a failing diff
// requiring deliberate justification, rather than silently passing regardless of margin sign. The
// `toBeGreaterThanOrEqual(140)` assertion independently floors it above the empirically measured
// clip threshold. Historically, pre-fix geometry (`SVG_WIDTH=600`, `PLOT_WIDTH=380` hardcoded
// literal) gave a margin of 60 — well under both guards here.
describe("CapabilityChart — DWT-001 right-margin regression", () => {
  it("reserves at least the documented minimum margin for the longest localized low-coverage marker", () => {
    const actualMargin = SVG_WIDTH - (PLOT_X + PLOT_WIDTH);
    // Locks the computed margin to a literal: any change to MARKER_GAP, MARKER_SAFETY_BUFFER,
    // MARKER_CHAR_WIDTH_RATIO, WORST_CASE_MARKER_LENGTH, or MARKER_FONT_SIZE now shows up as a
    // diff requiring deliberate re-justification, instead of comparing MARKER_MIN_MARGIN to itself.
    expect(MARKER_MIN_MARGIN).toBe(164);
    // ...and independently floors it above the empirically-measured clip threshold.
    expect(MARKER_MIN_MARGIN).toBeGreaterThanOrEqual(140);
    // Sanity: actualMargin still equals MARKER_MIN_MARGIN by construction (see NOTE above) — kept
    // to document that relationship, not as the regression guard itself.
    expect(actualMargin).toBe(MARKER_MIN_MARGIN);
  });

  it("keeps SVG_WIDTH at its pre-regression value — the margin comes from PLOT_WIDTH, not an SVG_WIDTH inflation that would downscale the whole chart", () => {
    // Locks in the root-cause-correct fix: widening SVG_WIDTH scales EVERY user-unit quantity
    // uniformly (SVG 1.1 §Coordinate Systems — CSS `px` inside an SVG is a user unit), so it is
    // not a valid way to buy margin without also shrinking bars/labels/ticks by the same factor.
    expect(SVG_WIDTH).toBe(600);
  });
});
