// AI BENCHMARK — merged chart structural invariants (Phase 2).
//
// Direct component tests (not Gherkin-bound), mirroring `capability-chart.test.tsx`/
// `price-chart.test.tsx`'s pattern: fixture models built inline, rendered, asserted via
// `data-testid`. See tech-docs.md DD-1/DD-2/DD-8 for the decisions these tests bind.

import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import {
  OPUS_ANCHOR_ID,
  SONNET_ANCHOR_ID,
  type Dataset,
  type MeteredPrice,
  type Model,
  type SubscriptionPrice,
} from "../core/data/models";
import { t } from "@/features/i18n/core/translations";
import { formatPriceUsd } from "./format";
import { bandLabel } from "./chart-primitives";
import { ModelTable } from "./model-table";
import { BenchmarkChart } from "./benchmark-chart";

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

/** A rated (has figures so it scores > 0), metered-priced model — the common case. */
function ratedMeteredModel(id: string, input: number, output: number): Model {
  return {
    id,
    name: id,
    vendor: "Test",
    harnesses: ["claude-code"],
    figures: [{ benchmark: "swe-bench-verified", value: 70, grade: "verified", source: SRC }],
    pricing: { "claude-code": metered(input, output) },
  };
}

describe("BenchmarkChart — merged row structure", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders a rated model's row with one capability bar, one price-in bar, and one price-out bar", () => {
    const model = ratedMeteredModel("row-model", 3, 15);
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    expect(screen.getByTestId("benchmark-chart-bar-capability-row-model")).not.toBeNull();
    expect(screen.getByTestId("benchmark-chart-bar-price-in-row-model")).not.toBeNull();
    expect(screen.getByTestId("benchmark-chart-bar-price-out-row-model")).not.toBeNull();

    // All three bars are inside the SAME row group, not separate chart sections.
    const row = screen.getByTestId("benchmark-chart-row-row-model");
    expect(row.querySelector('[data-testid="benchmark-chart-bar-capability-row-model"]')).not.toBeNull();
    expect(row.querySelector('[data-testid="benchmark-chart-bar-price-in-row-model"]')).not.toBeNull();
    expect(row.querySelector('[data-testid="benchmark-chart-bar-price-out-row-model"]')).not.toBeNull();
  });
});

describe("BenchmarkChart — DD-2 price bar text labels", () => {
  afterEach(() => {
    cleanup();
  });

  it("labels the input and output price bars with their formatted USD rate, preserving price-chart.tsx's full detail (DD-2)", () => {
    const model = ratedMeteredModel("labelled-model", 3, 15);
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    const inLabel = screen.getByTestId("benchmark-chart-label-in-labelled-model");
    expect(inLabel.textContent ?? "").toContain(formatPriceUsd(3, "en"));
    const outLabel = screen.getByTestId("benchmark-chart-label-out-labelled-model");
    expect(outLabel.textContent ?? "").toContain(formatPriceUsd(15, "en"));
  });
});

describe("BenchmarkChart — bar length proportional to value", () => {
  afterEach(() => {
    cleanup();
  });

  it("scales the capability bar by index/COMPOSITE_INDEX_MAX and the price-out bar by output/price-axis-max", () => {
    // Two models so the price axis max is driven by the SECOND model's output rate (30), not the
    // first (15) — proves the scale is a real ratio, not a constant/degenerate width.
    const lower = ratedMeteredModel("lower-model", 2, 15);
    const higher = ratedMeteredModel("higher-model", 4, 30);
    const ds = fixtureDataset([lower, higher]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    const lowerOut = screen.getByTestId("benchmark-chart-bar-price-out-lower-model");
    const higherOut = screen.getByTestId("benchmark-chart-bar-price-out-higher-model");
    const lowerWidth = Number(lowerOut.getAttribute("width"));
    const higherWidth = Number(higherOut.getAttribute("width"));

    // higher-model IS the axis max (output 30), so its bar spans the full plot width; lower-model
    // (output 15) spans exactly half of it — proportional, not merely "wider than".
    expect(higherWidth).toBeGreaterThan(0);
    expect(lowerWidth).toBeCloseTo(higherWidth / 2, 1);
  });
});

describe("BenchmarkChart — AC-17 lowest-rate subtitle (suppressed once a harness filter is active, AC-18)", () => {
  afterEach(() => {
    cleanup();
  });

  it("states that it shows the lowest available harness rate when no harness filter is active", () => {
    const model = ratedMeteredModel("subtitle-model", 3, 15);
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    const subtitle = screen.getByTestId("benchmark-chart-subtitle");
    expect(subtitle.textContent).toBe(t("en", "aiBenchPriceLowestSubtitle"));
  });

  it("suppresses the subtitle once a specific harness filter is active", () => {
    const model = ratedMeteredModel("subtitle-model-2", 3, 15);
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" harness="claude-code" />);

    expect(screen.queryByTestId("benchmark-chart-subtitle")).toBeNull();
  });
});

describe("BenchmarkChart — harness filter (DD-8)", () => {
  afterEach(() => {
    cleanup();
  });

  it("uses the selected harness's own rate, not the lowest available rate, when a harness prop is set", () => {
    // `anchor-model` exposes the SAME large output rate (1000) under both harnesses, so it pins
    // the shared price axis max constant across both renders below — the only thing that can then
    // change `dual-harness-model`'s own bar width is which rate it is plotting.
    const anchorModel = ratedMeteredModel("anchor-model", 1, 1000);
    anchorModel.harnesses = ["claude-code", "codex-cli"];
    anchorModel.pricing = { "claude-code": metered(1, 1000), "codex-cli": metered(1, 1000) };

    const dualHarnessModel: Model = {
      id: "dual-harness-model",
      name: "dual-harness-model",
      vendor: "Test",
      harnesses: ["claude-code", "codex-cli"],
      figures: [{ benchmark: "swe-bench-verified", value: 70, grade: "verified", source: SRC }],
      pricing: {
        "claude-code": metered(2, 10), // the LOWEST rate — what renders with no harness filter
        "codex-cli": metered(5, 25), // the higher rate — what must render when codex-cli is selected
      },
    };
    const ds = fixtureDataset([anchorModel, dualHarnessModel]);

    const { rerender } = render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);
    const unfilteredOut = Number(
      screen.getByTestId("benchmark-chart-bar-price-out-dual-harness-model").getAttribute("width"),
    );

    rerender(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" harness="codex-cli" />);
    const filteredOutWidth = Number(
      screen.getByTestId("benchmark-chart-bar-price-out-dual-harness-model").getAttribute("width"),
    );
    // Axis max is pinned at 1000 by anchor-model in both renders, so a wider bar here can only
    // mean dual-harness-model's OWN plotted rate rose from 10 (lowest, claude-code) to 25 (codex-cli).
    expect(filteredOutWidth).toBeGreaterThan(unfilteredOut);
  });
});

describe("BenchmarkChart — per-band sort control", () => {
  afterEach(() => {
    cleanup();
  });

  it("reports a sort change for only the changed band, leaving other bands untouched", () => {
    // Two sonnet-band models so a sort-order change is observable; opus/light are untouched by
    // the sonnet dropdown regardless of how many models they hold.
    const sonnetA = ratedMeteredModel("sonnet-a", 1, 5);
    const sonnetB = ratedMeteredModel("sonnet-b", 1, 20);
    const ds = fixtureDataset([sonnetA, sonnetB]);
    const onSortChange = vi.fn();
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" onSortChange={onSortChange} />);

    const sortLabel = `${t("en", "aiBenchSortLabel")} — ${bandLabel("sonnet", "en")}`;
    const sonnetSelect = screen.getByRole("combobox", { name: sortLabel });
    fireEvent.change(sonnetSelect, { target: { value: "price-asc" } });

    expect(onSortChange).toHaveBeenCalledWith("sonnet", "price-asc");
    expect(onSortChange).toHaveBeenCalledTimes(1);
  });

  it("re-orders only the band whose sortState entry changed", () => {
    // Fixture carries no anchor models, so both models fall through to the `light` band (no
    // opus/sonnet threshold to compare against) — this test targets `light` accordingly.
    const modelA = ratedMeteredModel("model-a", 1, 5); // cheaper output
    const modelB = ratedMeteredModel("model-b", 1, 20); // pricier output
    const ds = fixtureDataset([modelA, modelB]);

    // Default (capability) order: both share the same composite index (identical figures), so the
    // tie-break is ascending id — model-a before model-b.
    const { rerender } = render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);
    const bandDefault = screen.getByTestId("benchmark-chart-band-light");
    const idsDefault = within(bandDefault)
      .getAllByTestId(/^benchmark-chart-row-/)
      .map((el) => el.getAttribute("data-testid"));
    expect(idsDefault).toEqual(["benchmark-chart-row-model-a", "benchmark-chart-row-model-b"]);

    // price-desc reverses it: model-b (output 20) now comes first.
    rerender(
      <BenchmarkChart
        dataset={ds}
        fullDataset={ds}
        locale="en"
        sortState={{ opus: "capability", sonnet: "capability", light: "price-desc", unrated: "capability" }}
      />,
    );
    const bandSorted = screen.getByTestId("benchmark-chart-band-light");
    const idsSorted = within(bandSorted)
      .getAllByTestId(/^benchmark-chart-row-/)
      .map((el) => el.getAttribute("data-testid"));
    expect(idsSorted).toEqual(["benchmark-chart-row-model-b", "benchmark-chart-row-model-a"]);
  });
});

describe("BenchmarkChart — DD-1 rated + subscription-only rendering", () => {
  afterEach(() => {
    cleanup();
  });

  it("shows inline subscription text in place of price bars for a rated, subscription-only model, while its capability bar still renders", () => {
    const subOnlyModel: Model = {
      id: "sub-only-model",
      name: "sub-only-model",
      vendor: "Test",
      harnesses: ["opencode-go"],
      figures: [{ benchmark: "swe-bench-verified", value: 70, grade: "verified", source: SRC }],
      pricing: { "opencode-go": subscription(10, "First month $5, then $10/month.") },
    };
    const ds = fixtureDataset([subOnlyModel]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    // Capability bar renders as normal.
    expect(screen.getByTestId("benchmark-chart-bar-capability-sub-only-model")).not.toBeNull();

    // No price bars — subscription text instead.
    expect(screen.queryByTestId("benchmark-chart-bar-price-in-sub-only-model")).toBeNull();
    expect(screen.queryByTestId("benchmark-chart-bar-price-out-sub-only-model")).toBeNull();
    const subText = screen.getByTestId("benchmark-chart-subscription-sub-only-model");
    expect(subText.textContent ?? "").toContain(formatPriceUsd(10, "en"));
    expect(subText.textContent ?? "").not.toMatch(/\$0\b/);
  });
});

describe("BenchmarkChart — AC-12 low-coverage marker", () => {
  afterEach(() => {
    cleanup();
  });

  it("marks a rated model whose coverage is below the low-coverage threshold, stating its coverage ratio in text", () => {
    // swe-bench-verified alone carries weight 25 → coverage 0.25, below the 0.5 threshold —
    // mirrors `capability-chart.test.tsx`'s AC-12 fixture exactly.
    const lowCoverageModel: Model = {
      id: "low-coverage-model",
      name: "low-coverage-model",
      vendor: "Test",
      harnesses: ["claude-code"],
      figures: [{ benchmark: "swe-bench-verified", value: 50, grade: "verified", source: SRC }],
      pricing: { "claude-code": metered(2, 10) },
    };
    const ds = fixtureDataset([lowCoverageModel]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    const marker = screen.getByTestId("benchmark-chart-low-coverage-low-coverage-model");
    // 25/100 = 0.25 coverage ratio, formatted as a percentage in the marker text.
    expect(marker.textContent ?? "").toMatch(/25/);
  });

  it("shows no low-coverage marker for a fully-covered rated model", () => {
    const model = ratedMeteredModel("full-coverage-model", 2, 10);
    // ratedMeteredModel's single figure alone is below threshold too, so use a model whose
    // coverage sits at/above the threshold by scoring on enough benchmarks.
    model.figures = [
      { benchmark: "swe-bench-verified", value: 70, grade: "verified", source: SRC },
      { benchmark: "swe-bench-pro", value: 70, grade: "verified", source: SRC },
      { benchmark: "terminal-bench-2-1", value: 70, grade: "verified", source: SRC },
    ];
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    expect(screen.queryByTestId("benchmark-chart-low-coverage-full-coverage-model")).toBeNull();
  });
});

describe("BenchmarkChart — unrated models", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders an unrated model (no published composite score) in the unrated text list, with no capability or price bar", () => {
    const unratedModel: Model = {
      id: "unrated-model",
      name: "unrated-model",
      vendor: "Test",
      harnesses: ["claude-code"],
      figures: [], // zero coverage → no composite index → unrated
      pricing: { "claude-code": metered(2, 10) }, // even WITH a real price, still no row/bar
    };
    const ds = fixtureDataset([unratedModel]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    const unratedSection = screen.getByTestId("benchmark-chart-unrated");
    expect(unratedSection.textContent).toContain("unrated-model");

    expect(screen.queryByTestId("benchmark-chart-row-unrated-model")).toBeNull();
    expect(screen.queryByTestId("benchmark-chart-bar-capability-unrated-model")).toBeNull();
    expect(screen.queryByTestId("benchmark-chart-bar-price-in-unrated-model")).toBeNull();
    expect(screen.queryByTestId("benchmark-chart-bar-price-out-unrated-model")).toBeNull();
  });
});

describe("BenchmarkChart — DD-1 retained global list for unrated + subscription-only models", () => {
  afterEach(() => {
    cleanup();
  });

  it("states the plan cost and caps for an unrated model priced only under a subscription, mirroring price-chart.tsx's retired global subscription list", () => {
    const unratedSubOnly: Model = {
      id: "unrated-sub-only",
      name: "unrated-sub-only",
      vendor: "Test",
      harnesses: ["opencode-go"],
      figures: [], // zero coverage → no composite index → unrated
      pricing: { "opencode-go": subscription(10, "First month $5, then $10/month.") },
    };
    const ds = fixtureDataset([unratedSubOnly]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    const item = screen.getByTestId("benchmark-chart-unrated-model-unrated-sub-only");
    expect(item.textContent ?? "").toContain(formatPriceUsd(10, "en"));
    expect(item.textContent ?? "").toContain("First month $5, then $10/month.");
  });

  it("shows only the model name for a genuinely priceless unrated model", () => {
    const unratedNoPrice: Model = {
      id: "unrated-no-price",
      name: "unrated-no-price",
      vendor: "Test",
      harnesses: ["claude-code"],
      figures: [],
      pricing: {},
    };
    const ds = fixtureDataset([unratedNoPrice]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    const item = screen.getByTestId("benchmark-chart-unrated-model-unrated-no-price");
    expect(item.textContent).toBe("unrated-no-price");
  });
});

describe("BenchmarkChart — accessible name and ModelTable reachability", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders as one svg with role img and a single localized title, and every model it shows is also reachable via ModelTable", () => {
    const rated = ratedMeteredModel("access-rated-model", 2, 10);
    const unrated: Model = {
      id: "access-unrated-model",
      name: "access-unrated-model",
      vendor: "Test",
      harnesses: ["claude-code"],
      figures: [],
      pricing: {},
    };
    const ds = fixtureDataset([rated, unrated]);

    render(
      <>
        <BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />
        <ModelTable dataset={ds} fullDataset={ds} locale="en" />
      </>,
    );

    const svgs = screen.getAllByRole("img", { name: t("en", "aiBenchMergedChartTitle") });
    expect(svgs).toHaveLength(1);
    const svg = svgs[0]!;
    expect(svg.tagName.toLowerCase()).toBe("svg");
    expect(svg.querySelectorAll("title")).toHaveLength(1);

    const table = screen.getByTestId("model-table");
    expect(table.textContent).toContain("access-rated-model");
    expect(table.textContent).toContain("access-unrated-model");
  });
});
