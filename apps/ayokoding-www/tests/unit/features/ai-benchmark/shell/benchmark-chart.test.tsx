// AI BENCHMARK — merged chart structural invariants (Phase 2).
//
// Direct component tests (not Gherkin-bound), mirroring the two now-retired chart test files'
// pattern: fixture models built inline, rendered, asserted via `data-testid`. See tech-docs.md
// DD-1/DD-2/DD-8 for the decisions these tests bind.

import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import {
  dataset as fullRosterDataset,
  OPUS_ANCHOR_ID,
  SONNET_ANCHOR_ID,
  type Dataset,
  type HarnessId,
  type MeteredPrice,
  type Model,
  type SubscriptionPrice,
} from "../../../../../src/features/ai-benchmark/core/data/models";
import { computeGroups } from "../../../../../src/features/ai-benchmark/core/bands";
import { t } from "@/features/i18n/core/translations";
import { formatPriceUsd } from "../../../../../src/features/ai-benchmark/shell/format";
import { bandLabel } from "../../../../../src/features/ai-benchmark/shell/chart-primitives";
import { ModelTable } from "../../../../../src/features/ai-benchmark/shell/model-table";
import { BenchmarkChart } from "../../../../../src/features/ai-benchmark/shell/benchmark-chart";

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

/**
 * A model scored across all four composite benchmarks at the SAME value (full coverage), so
 * `assignBand` can place it against a real anchor threshold rather than falling through to
 * `haiku` for want of one (mirrors `ai-benchmark.steps.tsx`'s own `bandFixtureModel` helper, used
 * for the identical anchor-threshold need there).
 */
function bandFixtureModel(id: string, score: number, outputRate: number): Model {
  return {
    id,
    name: id,
    vendor: "Test",
    harnesses: ["claude-code"],
    figures: (["swe-bench-verified", "swe-bench-pro", "terminal-bench-2-1", "gpqa-diamond"] as const).map((b) => ({
      benchmark: b,
      value: score,
      grade: "verified",
      source: SRC,
    })),
    pricing: { "claude-code": metered(1, outputRate) },
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

  it("labels the input and output price bars with their formatted USD rate, preserving the retired price chart's full detail (DD-2)", () => {
    const model = ratedMeteredModel("labelled-model", 3, 15);
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    const inLabel = screen.getByTestId("benchmark-chart-bar-price-in-labelled-model-label");
    expect(inLabel.textContent ?? "").toContain(formatPriceUsd(3, "en"));
    const outLabel = screen.getByTestId("benchmark-chart-bar-price-out-labelled-model-label");
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

    const lowerOut = screen.getByTestId("benchmark-chart-bar-price-out-lower-model-fill");
    const higherOut = screen.getByTestId("benchmark-chart-bar-price-out-higher-model-fill");
    const lowerWidth = parseFloat(lowerOut.style.width);
    const higherWidth = parseFloat(higherOut.style.width);

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
    const unfilteredOut = parseFloat(
      screen.getByTestId("benchmark-chart-bar-price-out-dual-harness-model-fill").style.width,
    );

    rerender(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" harness="codex-cli" />);
    const filteredOutWidth = parseFloat(
      screen.getByTestId("benchmark-chart-bar-price-out-dual-harness-model-fill").style.width,
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
    // Regression (Rule-15 UWT-009 fix): the fixture previously carried NO anchor models at all, so
    // — per `assignBand`'s own fallback (no opus/sonnet threshold to compare against) — both
    // "sonnet-a"/"sonnet-b" silently landed in the `haiku` band despite their names, and this test
    // only ever exercised an EMPTY Sonnet band's sort control. Before UWT-009's fix, every band's
    // control rendered unconditionally regardless of whether it had rows, so the test passed
    // anyway; UWT-009 now hides an empty band's control, which is the CORRECT behaviour and is
    // exactly what broke this test — the fixture below adds real opus/sonnet anchor models so
    // "sonnet-a"/"sonnet-b" genuinely land in the Sonnet band this test's own name promises.
    const opusAnchor = bandFixtureModel(OPUS_ANCHOR_ID, 100, 1);
    const sonnetAnchor = bandFixtureModel(SONNET_ANCHOR_ID, 60, 1);
    const sonnetA = bandFixtureModel("sonnet-a", 70, 5);
    const sonnetB = bandFixtureModel("sonnet-b", 70, 20);
    const ds = fixtureDataset([opusAnchor, sonnetAnchor, sonnetA, sonnetB]);
    const onSortChange = vi.fn();
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" onSortChange={onSortChange} />);

    const sortLabel = `${t("en", "aiBenchSortLabel")} — ${bandLabel("sonnet", "en")}`;
    const sonnetSelect = screen.getByRole("combobox", { name: sortLabel });
    fireEvent.change(sonnetSelect, { target: { value: "price-asc" } });

    expect(onSortChange).toHaveBeenCalledWith("sonnet", "price-asc");
    expect(onSortChange).toHaveBeenCalledTimes(1);
  });

  it("re-orders only the band whose sortState entry changed", () => {
    // Fixture carries no anchor models, so both models fall through to the `haiku` band (no
    // opus/sonnet threshold to compare against) — this test targets `haiku` accordingly.
    const modelA = ratedMeteredModel("model-a", 1, 5); // cheaper output
    const modelB = ratedMeteredModel("model-b", 1, 20); // pricier output
    const ds = fixtureDataset([modelA, modelB]);

    // Default (capability) order: both share the same composite index (identical figures), so the
    // tie-break is ascending id — model-a before model-b.
    const { rerender } = render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);
    const bandDefault = screen.getByTestId("benchmark-chart-band-haiku");
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
        sortState={{ opus: "capability", sonnet: "capability", haiku: "price-desc" }}
      />,
    );
    const bandSorted = screen.getByTestId("benchmark-chart-band-haiku");
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
    // mirrors the retired capability chart test's AC-12 fixture exactly.
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

  // Rule-15 UWT-014 fix (Phase 11): `flex flex-wrap` let multiple Unrated models share one visual
  // line (wrapping only when a row filled), reading as one dense, unbroken text run — worst with
  // the roster's own ~15 Unrated models — rather than a properly chunked, one-model-per-line list.
  it("lists Unrated models one per line (no flex-wrap sharing a visual line), matching the roster table's own line-per-model layout", () => {
    const unratedA = { ...ratedMeteredModel("unrated-a", 1, 5), figures: [] };
    const unratedB = { ...ratedMeteredModel("unrated-b", 1, 20), figures: [] };
    const ds = fixtureDataset([unratedA, unratedB]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    const list = screen.getByTestId("benchmark-chart-unrated").querySelector("ul");
    expect(list?.className).not.toContain("flex-wrap");
    expect(list?.className).toContain("space-y-1");
  });
});

describe("BenchmarkChart — DD-1 retained global list for unrated + subscription-only models", () => {
  afterEach(() => {
    cleanup();
  });

  it("states the plan cost and caps for an unrated model priced only under a subscription, mirroring the retired price chart's global subscription list", () => {
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

  // Rule-15 UWT-001 fix (2026-07-30, partial fix by user decision): an unrated model priced by
  // METERED per-token rate (not subscription) previously showed ONLY its bare name here, even
  // though the same model's price was visible two sections down in ModelTable — the fix adds that
  // price as TEXT (matching the subscription-only branch's existing pattern), deliberately NOT
  // adding bars or a sort control (that would conflict with DD-1's already-reviewed decision that
  // unrated models render as plain text, since they have no comparable capability score to bar
  // against).
  it("states the input and output price for an unrated model priced by a metered per-token rate", () => {
    const unratedMetered: Model = {
      id: "unrated-metered",
      name: "unrated-metered",
      vendor: "Test",
      harnesses: ["claude-code"],
      figures: [],
      pricing: { "claude-code": metered(3, 15) },
    };
    const ds = fixtureDataset([unratedMetered]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    const item = screen.getByTestId("benchmark-chart-unrated-model-unrated-metered");
    expect(item.textContent ?? "").toContain(formatPriceUsd(3, "en"));
    expect(item.textContent ?? "").toContain(formatPriceUsd(15, "en"));
  });
});

describe("BenchmarkChart — accessible name and text alternative (AC-36/AC-46, reworded)", () => {
  afterEach(() => {
    cleanup();
  });

  // DD-25: the chart no longer emits any SVG (so there is no `role="img"` region left to name) —
  // each rated band's own DOM region instead carries `role="group"` with `aria-labelledby` pointing
  // at its own visible heading, carrying its localized band label as its accessible name (AC-36).
  // UWT-002's per-band split (each band independently reachable to assistive tech) is unchanged —
  // only the "svg role=img" mechanism was reworded to a DOM "group" region (AC-46).
  it("exposes one labelled group region PER rated band, and every model it shows is also reachable via the roster below", () => {
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

    for (const band of ["opus", "sonnet", "haiku"] as const) {
      const group = screen.getByRole("group", { name: bandLabel(band, "en") });
      expect(group).not.toBeNull();
    }

    const table = screen.getByTestId("model-table");
    expect(table.textContent).toContain("access-rated-model");
    expect(table.textContent).toContain("access-unrated-model");
  });
});

describe("BenchmarkChart — renders as DOM, not SVG (DD-25)", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders no <svg> element, keeps every chart label's declared text-size class static, and carries the lg:grid-cols- reflow class exactly once per row", () => {
    const model = ratedMeteredModel("dom-only-model", 2, 10);
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    const container = screen.getByTestId("benchmark-chart");
    expect(container.querySelectorAll("svg").length).toBe(0);

    // Phase 8, AC-49: `text-[10px]` (9.5px under the plan's own 12 CSS px floor) is retired for
    // `text-xs` (12px) — the property this test protects (a STATIC class, no responsive modifier)
    // is unchanged; only the declared size itself moved to clear the new floor.
    const label = screen.getByTestId("benchmark-chart-label-dom-only-model");
    expect(label.className).toContain("text-xs");

    const row = screen.getByTestId("benchmark-chart-row-dom-only-model");
    const reflowMatches = row.className.match(/lg:grid-cols-\S+/g) ?? [];
    expect(reflowMatches.length).toBe(1);
  });
});

// ─── DD-31 (tech-docs.md §DD-31): DWT-001 (right-margin marker clip) and DWT-004 (band-header/
// first-row baseline overlap) are RETIRED as SVG-geometry concerns, not dropped — DOM block flow
// makes both classes of defect structurally impossible (DOM text wraps/overflows rather than
// clipping at a `viewBox` edge; two adjacent block elements cannot overlap without explicit
// negative margin or absolute positioning, neither of which this markup uses). The two tests below
// replace those retired geometry guards with DOM-sibling-structure guards that protect the same
// underlying regressions.
describe("DD-31 — replacements for the retired SVG-geometry guards", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders the low-coverage marker as a sibling of the capability bar, not nested inside its track (replaces DWT-001)", () => {
    const model: Model = {
      id: "dd31-low-coverage-model",
      name: "dd31-low-coverage-model",
      vendor: "Test",
      harnesses: ["claude-code"],
      // swe-bench-verified alone (weight 25) keeps coverage at 0.25, below the 0.5 threshold.
      figures: [{ benchmark: "swe-bench-verified", value: 50, grade: "verified", source: SRC }],
      pricing: { "claude-code": metered(2, 10) },
    };
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    const bar = screen.getByTestId("benchmark-chart-bar-capability-dd31-low-coverage-model");
    const marker = screen.getByTestId("benchmark-chart-low-coverage-dd31-low-coverage-model");
    // The marker must not be clippable BY the bar's own track — it is a sibling, not a descendant.
    expect(bar.contains(marker)).toBe(false);
    expect(marker.parentElement).toBe(bar.parentElement);
  });

  it("keeps the band header and the first model row as separate block-level siblings, never fused into one element (replaces DWT-004)", () => {
    const model = ratedMeteredModel("dd31-first-row-model", 2, 10);
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    // A lone fixture model with no anchor models present always lands in the "haiku" band
    // (bands.ts falls through to "haiku" when both anchor thresholds are undefined).
    const header = screen.getByTestId("benchmark-chart-band-haiku-label");
    const firstRow = screen.getByTestId("benchmark-chart-row-dd31-first-row-model");
    expect(header).not.toBe(firstRow);
    expect(header.contains(firstRow)).toBe(false);
    expect(firstRow.contains(header)).toBe(false);
    expect(header.parentElement).toBe(firstRow.parentElement);
  });
});

// ─── Regression: `computeGroups(dataset, fullDataset)`'s band-collapse guard was deleted with the
// retired `capability-chart.test.tsx` and never re-established here (pr-review-synthesis-maker
// HIGH finding). `benchmark-chart.tsx:computeGroups(dataset, fullDataset)` calls it identically, so
// the class applies unchanged: a harness-filtered `dataset` must still place a surviving model in
// its FULL-ROSTER band, never re-derive band thresholds from the filtered subset alone. Derives
// the filtered roster and the surviving model from the REAL dataset (mirroring
// `bands.unit.test.ts`'s own pattern) rather than hardcoding an id.
describe("BenchmarkChart — fullDataset keeps a harness-filtered survivor in its full-roster band", () => {
  afterEach(() => {
    cleanup();
  });

  const harness: HarnessId = "codex-cli";

  const fullRosterBand = (() => {
    const groups = computeGroups(fullRosterDataset);
    const byId = new Map<string, string>();
    for (const list of [groups.opus, groups.sonnet, groups.haiku, groups.unrated]) {
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
    render(<BenchmarkChart dataset={filteredDataset} fullDataset={fullRosterDataset} locale="en" />);
    const expectedBand = fullRosterBand.get(survivor!.id);
    const bandGroup = screen.getByTestId(`benchmark-chart-band-${expectedBand}`);
    expect(bandGroup.querySelector(`[data-testid="benchmark-chart-row-${survivor!.id}"]`)).not.toBeNull();
  });

  it("WITHOUT fullDataset, the bug would reproduce — the survivor's own band collapses to haiku", () => {
    // Proves the assertion above is not vacuous: the same survivor, scored against ONLY the
    // filtered subset (no full-roster anchors), no longer lands in its full-roster band.
    const collapsedGroups = computeGroups(filteredDataset);
    const collapsedById = new Map<string, string>();
    for (const list of [collapsedGroups.opus, collapsedGroups.sonnet, collapsedGroups.haiku, collapsedGroups.unrated]) {
      for (const s of list) collapsedById.set(s.model.id, s.band);
    }
    expect(collapsedById.get(survivor!.id)).toBe("haiku");
    expect(fullRosterBand.get(survivor!.id)).not.toBe("haiku");
  });
});

// ─── Regression: an ascending/descending price sort must sort by the SAME rate the price bars
// themselves plot under an active harness filter (pr-review-synthesis-maker HIGH finding):
// `sort.ts`'s comparators used `lowestRate` unconditionally, ignoring an active `harness` prop,
// while `benchmark-chart.tsx` rendered each row with `rateForHarness` — so an ascending price sort
// could render a costlier row above a cheaper one whenever a model's cheapest harness was not the
// selected one. No prior test combined a harness filter with a price sort (they lived in separate
// `describe` blocks that never intersected) — this is that missing combination.
describe("BenchmarkChart — price sort honours an active harness filter (DD-8)", () => {
  afterEach(() => {
    cleanup();
  });

  it("sorts ascending by the SELECTED harness's own rate, not each model's lowest-available rate", () => {
    // dual-harness-model's cheapest rate overall is claude-code (10), but codex-cli charges 25 —
    // higher than flat-priced-model's 15. Under a codex-cli filter, an ascending sort must place
    // flat-priced-model (15) before dual-harness-model (25); sorting by `lowestRate` (10) would
    // reverse that.
    const dualHarnessModel: Model = {
      id: "harness-sort-dual",
      name: "harness-sort-dual",
      vendor: "Test",
      harnesses: ["claude-code", "codex-cli"],
      figures: [{ benchmark: "swe-bench-verified", value: 70, grade: "verified", source: SRC }],
      pricing: {
        "claude-code": metered(1, 10), // the LOWEST rate overall — must NOT drive the sort here
        "codex-cli": metered(2, 25), // what codex-cli actually charges — must drive the sort
      },
    };
    // Exposed by codex-cli directly (NOT claude-code) — both models must be exposed by the
    // filtered harness for this comparison to isolate "which rate the comparator picks", rather
    // than also exercising the separate "not exposed at all" fallback case.
    const flatPricedModel: Model = {
      id: "harness-sort-flat",
      name: "harness-sort-flat",
      vendor: "Test",
      harnesses: ["codex-cli"],
      figures: [{ benchmark: "swe-bench-verified", value: 70, grade: "verified", source: SRC }],
      pricing: { "codex-cli": metered(1, 15) },
    };
    const ds = fixtureDataset([dualHarnessModel, flatPricedModel]);

    render(
      <BenchmarkChart
        dataset={ds}
        fullDataset={ds}
        locale="en"
        harness="codex-cli"
        sortState={{ opus: "capability", sonnet: "capability", haiku: "price-asc" }}
      />,
    );

    const bandHaiku = screen.getByTestId("benchmark-chart-band-haiku");
    const domOrder = within(bandHaiku)
      .getAllByTestId(/^benchmark-chart-row-/)
      .map((el) => el.getAttribute("data-testid"));
    expect(domOrder).toEqual(["benchmark-chart-row-harness-sort-flat", "benchmark-chart-row-harness-sort-dual"]);

    // Sanity: the displayed price bar for dual-harness-model really is the codex-cli rate (25),
    // not the lowest (10) — proving the comparator and the render use the SAME number (DD-8).
    const displayedOutWidth = parseFloat(
      screen.getByTestId("benchmark-chart-bar-price-out-harness-sort-dual-fill").style.width,
    );
    const flatOutWidth = parseFloat(
      screen.getByTestId("benchmark-chart-bar-price-out-harness-sort-flat-fill").style.width,
    );
    expect(displayedOutWidth).toBeGreaterThan(flatOutWidth); // 25 > 15
  });
});

// ─── Regression: reusing `FilterSelect` for the sort dropdown rendered a duplicate "Capability"
// option (its own empty `value=""` option PLUS the real `"capability"` option, both labelled
// identically) and cast `""` to `SortMode` on change (pr-review-synthesis-maker HIGH finding).
// `FilterSelect` now omits its empty option whenever the caller passes no `allLabel` (see its own
// docstring) — the sort control's call site does exactly that.
describe("BenchmarkChart — sort dropdown has no duplicate/invalid empty option", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders exactly the three known SortModes as options, with no blank value option", () => {
    const model = ratedMeteredModel("sort-options-model", 2, 10);
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" onSortChange={vi.fn()} />);

    const sortLabel = `${t("en", "aiBenchSortLabel")} — ${bandLabel("haiku", "en")}`;
    const select = screen.getByRole("combobox", { name: sortLabel }) as HTMLSelectElement;
    const values = Array.from(select.options).map((opt) => opt.value);

    expect(values).toEqual(["capability", "price-asc", "price-desc"]);
    expect(values).not.toContain("");
  });
});

// ─── AC-48: a rated model with no reported price (no metered rate, no subscription, under any
// harness) shows a "not reported" placeholder — new user-facing behaviour introduced by the merge
// (the retired `price-chart.tsx` used to omit such models from the plot entirely) that had no unit
// test or owning Gherkin scenario (pr-review-synthesis-maker MEDIUM finding); the Gherkin scenario
// itself lives at `specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature`.
describe("BenchmarkChart — AC-48 rated model with no reported price", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders the not-reported placeholder for a rated model with no metered rate and no subscription anywhere", () => {
    const noPriceRatedModel: Model = {
      id: "no-price-rated-model",
      name: "no-price-rated-model",
      vendor: "Test",
      harnesses: ["claude-code"],
      figures: [{ benchmark: "swe-bench-verified", value: 70, grade: "verified", source: SRC }],
      pricing: {}, // rated (has figures) but genuinely no reported price anywhere
    };
    const ds = fixtureDataset([noPriceRatedModel]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    // Capability bar still renders — only the price presentation is affected.
    expect(screen.getByTestId("benchmark-chart-bar-capability-no-price-rated-model")).not.toBeNull();
    expect(screen.queryByTestId("benchmark-chart-bar-price-in-no-price-rated-model")).toBeNull();
    expect(screen.queryByTestId("benchmark-chart-subscription-no-price-rated-model")).toBeNull();
    const notReported = screen.getByTestId("benchmark-chart-not-reported-no-price-rated-model");
    expect(notReported.textContent).toBe(t("en", "aiBenchNoFigure"));
  });
});

// ─── Rule-15 UWT-008 fix (Phase 11): the sort scope note ───────────────────────

describe("BenchmarkChart — Rule-15 UWT-008 fix (sort scope note)", () => {
  afterEach(() => {
    cleanup();
  });

  it("states the per-band sort applies to the chart only, when a sort handler is passed", () => {
    const model = ratedMeteredModel("scope-note-model", 1, 5);
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" onSortChange={vi.fn()} />);
    const note = screen.getByTestId("benchmark-chart-sort-scope-note");
    expect(note.textContent).toBe(t("en", "aiBenchSortScopeNote"));
  });

  it("omits the sort scope note when no sort handler is passed (read-only rendering)", () => {
    const model = ratedMeteredModel("scope-note-readonly-model", 1, 5);
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);
    expect(screen.queryByTestId("benchmark-chart-sort-scope-note")).toBeNull();
  });
});

// ─── Rule-15 UWT-009 fix (Phase 11): an active Class filter can empty one rated band ───

describe("BenchmarkChart — Rule-15 UWT-009 fix (a rated band emptied by the active Class filter)", () => {
  afterEach(() => {
    cleanup();
  });

  it("shows an explicit empty-band message and hides that band's sort control, leaving other bands untouched", () => {
    // Only an opus-anchor model in the (already filtered) `dataset` prop — but `fullDataset` still
    // carries both anchors, so the sonnet band genuinely exists (AC-40-style roster-relative
    // thresholds) yet has zero matching rows in THIS filtered view.
    const opusAnchor = bandFixtureModel(OPUS_ANCHOR_ID, 100, 1);
    const sonnetAnchor = bandFixtureModel(SONNET_ANCHOR_ID, 60, 1);
    const fullDs = fixtureDataset([opusAnchor, sonnetAnchor]);
    const filteredDs = fixtureDataset([opusAnchor]); // sonnet anchor filtered out of THIS view
    render(<BenchmarkChart dataset={filteredDs} fullDataset={fullDs} locale="en" onSortChange={vi.fn()} />);

    // Opus (still populated) keeps its normal axis-max line and sort control.
    expect(screen.getByTestId(`benchmark-chart-band-opus-label`).textContent).toBe(bandLabel("opus", "en"));
    expect(screen.queryByTestId("benchmark-chart-band-opus-empty")).toBeNull();
    expect(
      screen.getByRole("combobox", { name: `${t("en", "aiBenchSortLabel")} — ${bandLabel("opus", "en")}` }),
    ).not.toBeNull();

    // Sonnet (emptied by the filter) shows the explicit message, not a bare axis-max line, and its
    // OWN sort control does not render at all (rather than rendering disabled-but-present).
    const sonnetEmpty = screen.getByTestId("benchmark-chart-band-sonnet-empty");
    expect(sonnetEmpty.textContent).toBe(t("en", "aiBenchBandEmptyMessage"));
    expect(
      screen.queryByRole("combobox", { name: `${t("en", "aiBenchSortLabel")} — ${bandLabel("sonnet", "en")}` }),
    ).toBeNull();
  });
});
