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
} from "../core/data/models";
import { computeGroups } from "../core/bands";
import { t } from "@/features/i18n/core/translations";
import { formatPriceUsd } from "./format";
import { bandLabel } from "./chart-primitives";
import { ModelTable } from "./model-table";
import { BenchmarkChart, MARKER_MIN_MARGIN, PLOT_WIDTH, PLOT_X, SVG_WIDTH } from "./benchmark-chart";

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

  it("labels the input and output price bars with their formatted USD rate, preserving the retired price chart's full detail (DD-2)", () => {
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
        sortState={{ opus: "capability", sonnet: "capability", light: "price-desc" }}
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

describe("BenchmarkChart — accessible name and ModelTable reachability", () => {
  afterEach(() => {
    cleanup();
  });

  // UWT-002 fix (Rule-15 web-usability-tester retest, 2026-07-30): the chart is now one svg PER
  // rated band (three: opus/sonnet/light), each with its own role=img and its own localized title
  // built from the shared `aiBenchMergedChartTitle` prefix — not one svg shared across every band.
  it("renders one svg with role img and a localized title PER rated band, and every model it shows is also reachable via ModelTable", () => {
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

    const chartTitlePrefix = t("en", "aiBenchMergedChartTitle");
    const svgs = screen.getAllByRole("img", { name: new RegExp(`^${chartTitlePrefix} — `) });
    expect(svgs).toHaveLength(3); // opus, sonnet, light
    for (const svg of svgs) {
      expect(svg.tagName.toLowerCase()).toBe("svg");
      expect(svg.querySelectorAll("title")).toHaveLength(1);
    }

    const table = screen.getByTestId("model-table");
    expect(table.textContent).toContain("access-rated-model");
    expect(table.textContent).toContain("access-unrated-model");
  });
});

// ─── Regression: DWT-001's right-margin fix REGRESSED in this PR (pr-review-synthesis-maker
// CRITICAL finding, confirmed live in the PR's own committed evidence screenshot
// `phase-6-benchmark-chart-id-1280px.png` — a low-coverage marker's trailing "%)" clipped off the
// SVG's right edge). `capability-chart.tsx` (retired) derived `PLOT_WIDTH` FROM a reserved margin,
// making clipping structurally impossible; this file's merge inverted that dependency and
// hardcoded `PLOT_WIDTH = 380`, which let the right margin fall out to 80 — under the 140-unit
// clip floor this defect's original live investigation found. This is a pure computed-geometry
// assertion (no browser needed): the right margin the low-coverage marker text renders into
// (`SVG_WIDTH - (PLOT_X + PLOT_WIDTH)`) must stay at least `MARKER_MIN_MARGIN` — the documented,
// locale-derived minimum the marker needs at `text-[9px]` to avoid the SVG clipping it past its
// own `viewBox`.
//
// `PLOT_WIDTH = SVG_WIDTH - PLOT_X - MARKER_MIN_MARGIN` by definition (benchmark-chart.tsx), so
// `actualMargin` below is ALGEBRAICALLY IDENTICAL to `MARKER_MIN_MARGIN` for any value of the
// constants that compose it — comparing it back against `MARKER_MIN_MARGIN` can never fail. The
// `toBe(164)` assertion is the real regression guard: it locks the *current* computed value of
// `MARKER_MIN_MARGIN` to a literal, so any future edit to its inputs shows up as a failing diff
// requiring deliberate re-justification, instead of silently passing regardless of margin sign.
// The `toBeGreaterThanOrEqual(140)` assertion independently floors it above the empirically
// measured clip threshold. The pre-fix regression (`SVG_WIDTH=640`, `PLOT_WIDTH=380` hardcoded
// literal) gave a margin of 80 — well under both guards here.
describe("BenchmarkChart — DWT-001 right-margin regression", () => {
  afterEach(() => {
    cleanup();
  });

  it("reserves at least the documented minimum margin for the longest localized low-coverage marker", () => {
    const actualMargin = SVG_WIDTH - (PLOT_X + PLOT_WIDTH);
    expect(MARKER_MIN_MARGIN).toBe(164);
    expect(MARKER_MIN_MARGIN).toBeGreaterThanOrEqual(140);
    // Sanity: actualMargin still equals MARKER_MIN_MARGIN by construction (see NOTE above) — kept
    // to document that relationship, not as the regression guard itself.
    expect(actualMargin).toBe(MARKER_MIN_MARGIN);
  });

  it("would clip the longest low-coverage marker at the pre-fix hardcoded geometry — proving this guard is not vacuous", () => {
    // The exact pre-regression literal this PR shipped (SVG_WIDTH=640, PLOT_WIDTH=380 hardcoded)
    // gave a margin of only 80 units — reproducing why the marker clipped in the committed
    // evidence screenshot. This is a negative control: it proves the guard above would actually
    // fail against the regressed geometry, not merely pass by construction.
    const preFixPlotWidth = 380;
    const preFixMargin = SVG_WIDTH - (PLOT_X + preFixPlotWidth);
    expect(preFixMargin).toBeLessThan(MARKER_MIN_MARGIN);
    expect(preFixMargin).toBeLessThan(140);
  });

  it("renders the longest low-coverage marker text with no characters past the SVG's own viewBox width", () => {
    // GPT-5.6-Terra-style reproduction from the CRITICAL finding: a high-index model (95.1) in the
    // `id` locale (the longer of the two marker strings) — the exact case the committed evidence
    // screenshot showed clipping. Confirms end-to-end (not just the algebraic margin guard above)
    // that the marker's own rendered text never crosses SVG_WIDTH.
    const model: Model = {
      id: "dwt001-high-index-low-coverage",
      name: "dwt001-high-index-low-coverage",
      vendor: "Test",
      harnesses: ["claude-code"],
      // swe-bench-verified alone (weight 25) keeps coverage at 0.25 (< the 0.5 low-coverage
      // threshold) while still scoring a high composite index via a near-maximal figure value.
      figures: [{ benchmark: "swe-bench-verified", value: 95.1, grade: "verified", source: SRC }],
      pricing: { "claude-code": metered(2, 10) },
    };
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="id" />);

    const marker = screen.getByTestId("benchmark-chart-low-coverage-dwt001-high-index-low-coverage");
    const markerX = Number(marker.getAttribute("x"));
    const markerText = marker.textContent ?? "";
    // Conservative estimate of the marker's own rendered width, mirroring the same
    // char-width-ratio/font-size constants the margin itself is derived from.
    const estimatedMarkerWidth = markerText.length * 9 * 0.62;
    expect(markerX + estimatedMarkerWidth).toBeLessThanOrEqual(SVG_WIDTH);
  });
});

// ─── Regression: DWT-004 (Rule-15 web-design-tester retest, 2026-07-30) — the band header's own
// label text baseline sat only 6 SVG user-units above the first row's own label baseline
// (`headerY = cursor + BAND_HEADER_HEIGHT - 8` vs. the first row's `y={rowTop - 2}` where
// `rowTop = cursor + BAND_HEADER_HEIGHT`), which is less than either text run's own ascent+descent
// at their respective font sizes — so the header word rendered fused into the first model's own
// name/index text at every breakpoint (measured overlaps of -2.9px/-7.1px/-10.5px at
// 375/768/1280px live in Chromium). A distinct layout-constant defect from DWT-001 (that one was
// the plot's right margin; this one is the header-to-first-row vertical gap).
describe("BenchmarkChart — DWT-004 band-header/first-row label overlap regression", () => {
  afterEach(() => {
    cleanup();
  });

  it("keeps the band header's label baseline clear of the first row's own label baseline by at least the documented minimum", () => {
    const model = ratedMeteredModel("dwt004-first-row-model", 2, 10);
    const ds = fixtureDataset([model]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    // A lone fixture model with no anchor models present always lands in the "light" band
    // (bands.ts falls through to "light" when both anchor thresholds are undefined) — the "opus"
    // and "sonnet" band headers still render (every RATED_BAND always renders, even with zero
    // rows), but at unrelated cursor offsets, so this must reference "light", the band this
    // model's own row actually belongs to.
    const headerLabel = screen.getByTestId("benchmark-chart-band-light-label");
    const rowLabel = screen.getByTestId("benchmark-chart-label-dwt004-first-row-model");
    const headerY = Number(headerLabel.getAttribute("y"));
    const rowLabelY = Number(rowLabel.getAttribute("y"));

    // MIN_HEADER_TO_ROW_LABEL_GAP: the header's own descent (text-xs/12px, ~4 units) plus the row
    // label's own ascent (text-[10px], ~8 units) plus a safety buffer (~8 units) — same
    // documented-constant discipline DWT-001's MARKER_MIN_MARGIN already established for this file.
    const MIN_HEADER_TO_ROW_LABEL_GAP = 20;
    expect(rowLabelY - headerY).toBeGreaterThanOrEqual(MIN_HEADER_TO_ROW_LABEL_GAP);
  });

  it("would collide at the pre-fix hardcoded geometry — proving this guard is not vacuous", () => {
    // The exact pre-fix offsets this PR shipped (`headerY = cursor + 22 - 8`, first row `y = cursor
    // + 22 - 2`) gave a gap of only 6 units — reproducing the measured live overlap.
    const preFixBandHeaderHeight = 22;
    const preFixHeaderY = preFixBandHeaderHeight - 8;
    const preFixRowLabelY = preFixBandHeaderHeight - 2;
    expect(preFixRowLabelY - preFixHeaderY).toBeLessThan(20);
  });
});

// ─── Regression: the axis-maximum label must right-align to the plot's TRUE right edge
// (`PLOT_X + PLOT_WIDTH`), not to `SVG_WIDTH` (pr-review-synthesis-maker HIGH finding: this guard
// was deleted with the retired `capability-chart.test.tsx` and never re-established here).
// `chart-primitives.tsx`'s own `AxisProps.width` JSDoc documents it as "Right edge of the plot
// area, in pixels — the axis-maximum label right-aligns to this." Reverting
// `benchmark-chart.tsx`'s `<Axis width={...}>` call back to `SVG_WIDTH` fails this test.
describe("BenchmarkChart — axis-maximum label right-alignment", () => {
  afterEach(() => {
    cleanup();
  });

  it("right-aligns the axis-maximum label to the plot's true right edge (PLOT_X + PLOT_WIDTH), not SVG_WIDTH", () => {
    const ratedModel = ratedMeteredModel("axis-align-model", 2, 10);
    const ds = fixtureDataset([ratedModel]);
    render(<BenchmarkChart dataset={ds} fullDataset={ds} locale="en" />);

    // UWT-002 fix (Rule-15, 2026-07-30): every RATED_BAND now renders its own svg (and its own
    // axis-maximum label) regardless of whether it holds any rows — this fixture's lone,
    // anchor-less model lands in "light" alone, so "opus"/"sonnet" render empty but still carry
    // their own (identically positioned) axis-maximum label.
    const axisMaxLabels = screen.getAllByTestId("chart-axis-max");
    expect(axisMaxLabels.length).toBeGreaterThan(0);
    for (const axisMax of axisMaxLabels) {
      expect(axisMax.getAttribute("x")).toBe(String(PLOT_X + PLOT_WIDTH));
    }
    // Sanity: this is NOT the same value as SVG_WIDTH, so the assertion above cannot be
    // accidentally satisfied by the pre-fix (defective) call site.
    expect(PLOT_X + PLOT_WIDTH).not.toBe(SVG_WIDTH);
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
    render(<BenchmarkChart dataset={filteredDataset} fullDataset={fullRosterDataset} locale="en" />);
    const expectedBand = fullRosterBand.get(survivor!.id);
    const bandGroup = screen.getByTestId(`benchmark-chart-band-${expectedBand}`);
    expect(bandGroup.querySelector(`[data-testid="benchmark-chart-row-${survivor!.id}"]`)).not.toBeNull();
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
        sortState={{ opus: "capability", sonnet: "capability", light: "price-asc" }}
      />,
    );

    const bandLight = screen.getByTestId("benchmark-chart-band-light");
    const domOrder = within(bandLight)
      .getAllByTestId(/^benchmark-chart-row-/)
      .map((el) => el.getAttribute("data-testid"));
    expect(domOrder).toEqual(["benchmark-chart-row-harness-sort-flat", "benchmark-chart-row-harness-sort-dual"]);

    // Sanity: the displayed price bar for dual-harness-model really is the codex-cli rate (25),
    // not the lowest (10) — proving the comparator and the render use the SAME number (DD-8).
    const displayedOutWidth = Number(
      screen.getByTestId("benchmark-chart-bar-price-out-harness-sort-dual").getAttribute("width"),
    );
    const flatOutWidth = Number(
      screen.getByTestId("benchmark-chart-bar-price-out-harness-sort-flat").getAttribute("width"),
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

    const sortLabel = `${t("en", "aiBenchSortLabel")} — ${bandLabel("light", "en")}`;
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
// itself lives at `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`.
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
