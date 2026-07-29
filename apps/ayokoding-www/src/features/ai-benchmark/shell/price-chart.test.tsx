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
  OPUS_ANCHOR_ID,
  SONNET_ANCHOR_ID,
  type Dataset,
  type MeteredPrice,
  type Model,
  type SubscriptionPrice,
} from "../core/data/models";
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
    render(<PriceChart dataset={fixtureDataset([subOnlyModel, meteredModel])} locale="en" />);

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
    render(<PriceChart dataset={fixtureDataset([subOnlyModel])} locale="en" />);

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
    render(<PriceChart dataset={fixtureDataset([meteredModel])} locale="en" />);

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
    render(<PriceChart dataset={fixtureDataset([meteredModel])} locale="en" />);

    const ticks = screen.getByTestId("price-chart-ticks");
    expect(ticks.querySelectorAll("text").length).toBeGreaterThan(0);
    expect(screen.getByTestId("price-chart-tick-0")).not.toBeNull();
  });
});
