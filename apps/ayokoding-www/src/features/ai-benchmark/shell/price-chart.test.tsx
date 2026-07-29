// AI BENCHMARK — price chart structural invariants (Phase 7, Y-4, Y-9/Y-10).
//
// Direct component tests (not Gherkin-bound), mirroring `capability-chart.test.tsx`'s pattern:
//   1. A subscription-only model never renders a `<rect>` bar anywhere in the chart, and no
//      subscription-group entry ever shows a literal "$0" value.
//   2. The mobile (two-line in/out text block) and md/lg (two bars sharing a row) placements
//      render the SAME rate values — jsdom applies no CSS, so both are present in the DOM and
//      parity can be asserted without a real viewport.

import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import {
  dataset as fullRosterDataset,
  OPUS_ANCHOR_ID,
  SONNET_ANCHOR_ID,
  type Dataset,
  type HarnessId,
  type MeteredPrice,
  type Model,
  type SubscriptionPrice,
} from "../core/data/models";
import { computeGroups } from "../core/bands";
import { lowestRate } from "../core/price";
import { formatPriceUsd } from "./format";
import { PriceChart } from "./price-chart";

const SRC = "https://example.test/source";

function metered(input: number, output: number): MeteredPrice {
  return { kind: "metered", input, output, grade: "verified", source: SRC };
}

function subscription(planCostUsd: number, caps?: string): SubscriptionPrice {
  return { kind: "subscription", planCostUsd, grade: "verified", source: SRC, caps };
}

function fixtureDataset(models: Model[]): Dataset {
  return { snapshotDate: "2026-07-28", anchorIds: { opus: OPUS_ANCHOR_ID, sonnet: SONNET_ANCHOR_ID }, models };
}

describe("PriceChart — subscription group", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders a subscription-only model as a labelled text list entry, never a bar, never $0", () => {
    const subOnlyModel: Model = {
      id: "sub-only-model",
      name: "sub-only-model",
      vendor: "Test",
      harnesses: ["opencode-go"],
      figures: [],
      pricing: { "opencode-go": subscription(10, "First month $5, then $10/month.") },
    };
    const meteredModel: Model = {
      id: "metered-model",
      name: "metered-model",
      vendor: "Test",
      harnesses: ["claude-code"],
      figures: [],
      pricing: { "claude-code": metered(3, 15) },
    };
    const ds1 = fixtureDataset([subOnlyModel, meteredModel]);
    render(<PriceChart dataset={ds1} fullDataset={ds1} locale="en" />);

    const subscriptionSection = screen.getByTestId("price-chart-subscription");
    expect(subscriptionSection.textContent).toContain("sub-only-model");
    expect(subscriptionSection.textContent ?? "").not.toMatch(/\$0\b/);

    // The subscription-only model gets no bar anywhere in the chart.
    expect(screen.queryByTestId("price-chart-bar-in-sub-only-model")).toBeNull();
    expect(screen.queryByTestId("price-chart-bar-out-sub-only-model")).toBeNull();
    // The metered model DOES get bars.
    expect(screen.getByTestId("price-chart-bar-in-metered-model")).not.toBeNull();
    expect(screen.getByTestId("price-chart-bar-out-metered-model")).not.toBeNull();

    // No <rect> in the whole chart carries the subscription-only model's id.
    const svg = screen.getByTestId("price-chart-svg");
    const rects = Array.from(svg.querySelectorAll("rect"));
    for (const rect of rects) {
      expect(rect.getAttribute("data-testid")).not.toMatch(/sub-only-model/);
    }
  });

  it("emits a subscription line naming the plan cost and its caps", () => {
    const subOnlyModel: Model = {
      id: "sub-caps-model",
      name: "sub-caps-model",
      vendor: "Test",
      harnesses: ["opencode-go"],
      figures: [],
      pricing: { "opencode-go": subscription(10, "Usage caps: $12/5hr.") },
    };
    const ds2 = fixtureDataset([subOnlyModel]);
    render(<PriceChart dataset={ds2} fullDataset={ds2} locale="en" />);

    const entry = screen.getByTestId("price-chart-subscription-sub-caps-model");
    expect(entry.textContent ?? "").toContain(formatPriceUsd(10, "en"));
    expect(entry.textContent ?? "").toContain("Usage caps: $12/5hr.");
  });
});

describe("PriceChart — responsive label placement", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders the same rate values in the mobile (two-line block) and md/lg (two-bar row) placements", () => {
    const meteredModel: Model = {
      id: "responsive-model",
      name: "responsive-model",
      vendor: "Test",
      harnesses: ["claude-code"],
      figures: [],
      pricing: { "claude-code": metered(3, 15) },
    };
    const ds3 = fixtureDataset([meteredModel]);
    render(<PriceChart dataset={ds3} fullDataset={ds3} locale="en" />);

    const mobileIn = screen.getByTestId("price-chart-mobile-in-responsive-model");
    const mobileOut = screen.getByTestId("price-chart-mobile-out-responsive-model");
    const desktopIn = screen.getByTestId("price-chart-label-in-responsive-model");
    const desktopOut = screen.getByTestId("price-chart-label-out-responsive-model");

    expect(mobileIn.textContent).not.toBe("");
    expect(mobileIn.textContent).toBe(desktopIn.textContent);
    expect(mobileOut.textContent).toBe(desktopOut.textContent);
    expect(mobileIn.textContent).toContain(formatPriceUsd(3, "en"));
    expect(mobileOut.textContent).toContain(formatPriceUsd(15, "en"));

    // The bars themselves only render at md/lg (mobile shows text only, no bars).
    expect(screen.getByTestId("price-chart-bar-in-responsive-model")).not.toBeNull();
    expect(screen.getByTestId("price-chart-bar-out-responsive-model")).not.toBeNull();
  });

  it("renders an lg-only axis tick row with numeric ticks regardless of viewport", () => {
    const meteredModel: Model = {
      id: "tick-model",
      name: "tick-model",
      vendor: "Test",
      harnesses: ["claude-code"],
      figures: [],
      pricing: { "claude-code": metered(4, 20) },
    };
    const ds4 = fixtureDataset([meteredModel]);
    render(<PriceChart dataset={ds4} fullDataset={ds4} locale="en" />);

    const ticks = screen.getByTestId("price-chart-ticks");
    expect(ticks.querySelectorAll("text").length).toBeGreaterThan(0);
    expect(screen.getByTestId("price-chart-tick-0")).not.toBeNull();
  });
});

// ─── Regression: THIS component's own `fullDataset` wiring must not collapse a harness-filtered
// rated model to `light` (pr-review-synthesis-maker HIGH finding, PR #118 cycle 2). `bands.ts` and
// `model-table.tsx` already carry this proof — this component did not, and reverting its fix alone
// passed the whole suite. Derives the filtered roster and the surviving model from the REAL
// dataset, mirroring `bands.unit.test.ts`'s pattern, rather than hardcoding an id — the survivor
// must also carry a METERED rate under the filtering harness, or it renders no bar at all
// (subscription-only models never render as bars — see the "subscription group" describe above).
describe("PriceChart — fullDataset keeps a harness-filtered survivor in its full-roster band", () => {
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
    (m) =>
      (fullRosterBand.get(m.id) === "opus" || fullRosterBand.get(m.id) === "sonnet") &&
      lowestRate(m)?.kind === "metered",
  );

  it(`sanity: ${harness} excludes both anchor models but still exposes a metered opus/sonnet survivor`, () => {
    expect(filteredModels.some((m) => m.id === OPUS_ANCHOR_ID)).toBe(false);
    expect(filteredModels.some((m) => m.id === SONNET_ANCHOR_ID)).toBe(false);
    expect(survivor, `${harness} must expose at least one metered opus/sonnet survivor`).toBeDefined();
  });

  it("renders the surviving model's bars under its correct full-roster band when fullDataset is passed", () => {
    render(<PriceChart dataset={filteredDataset} fullDataset={fullRosterDataset} locale="en" harness={harness} />);
    const expectedBand = fullRosterBand.get(survivor!.id);
    const bandGroup = screen.getByTestId(`price-chart-band-${expectedBand}`);
    expect(bandGroup.querySelector(`[data-testid="price-chart-row-${survivor!.id}"]`)).not.toBeNull();
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
