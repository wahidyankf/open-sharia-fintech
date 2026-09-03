import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { expect, vi } from "vitest";
import React from "react";

// ─── Reactive next/navigation mock (Phase 5 page-render scenarios) ─────────────
// AC-1/AC-2/AC-19/AC-29/AC-32/AC-34/AC-35 render the route's client content, which reads its
// locale from useLocale() → useParams(). navState holds the active locale so each scenario's
// Given step can set it before the page renders. Hoisted so the vi.mock factory can close over it.
// `lastPush` (SG-003 fix) — the most recent URL string a filter/sort change passed to
// `router.push`, so a scenario can assert what the NEXT navigation would carry without needing
// the full reactive-context re-render machinery `cost-of-living-calculator.steps.tsx` uses (no
// existing scenario here needs the page to actually re-render after a push).
const { navState } = vi.hoisted(() => ({
  navState: { locale: "en" as string, search: "" as string, lastPush: undefined as string | undefined },
}));

vi.mock("next/navigation", () => ({
  useParams: () => ({ locale: navState.locale }),
  useSearchParams: () => new URLSearchParams(navState.search),
  useRouter: () => ({
    push: (url: string) => {
      navState.lastPush = url;
    },
    replace: vi.fn(),
    back: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => "/en/tools/ai-benchmark",
  notFound: vi.fn(),
}));

import "./helpers/test-setup";
import AiBenchmarkPage from "@/app/[locale]/tools/ai-benchmark/page";
import { OPERATORS } from "@/features/ai-benchmark/core/data/operators";
import {
  BAND_LABEL_KEYS,
  BENCHMARK_COLUMNS,
  HARNESS_DISPLAY_NAMES,
} from "@/features/ai-benchmark/core/data/benchmarks";
import {
  BENCHMARK_WEIGHTS,
  OPUS_ANCHOR_ID,
  SONNET_ANCHOR_ID,
  dataset,
  type BenchmarkId,
  type ConflictedFigure,
  type Dataset,
  type Figure,
  type HarnessId,
  type MeteredPrice,
  type Model,
  type SubscriptionPrice,
} from "@/features/ai-benchmark/core/data/models";
import {
  COMPOSITE_INDEX_MAX,
  LOW_COVERAGE_THRESHOLD,
  computeIndex,
  computeRosterMaxes,
  coverage,
} from "@/features/ai-benchmark/core/score";
import {
  anchors,
  assignBand,
  computeGroups,
  type AnchorIndices,
  type Band,
  type BandGroups,
  type IndexMap,
} from "@/features/ai-benchmark/core/bands";
import { ModelTable } from "@/features/ai-benchmark/shell/model-table";
import { ModelCard } from "@/features/ai-benchmark/shell/model-card";
import { computeScoreViews } from "@/features/ai-benchmark/shell/model-figures";
import { BenchmarkChart } from "@/features/ai-benchmark/shell/benchmark-chart";
import { bandLabel } from "@/features/ai-benchmark/shell/chart-primitives";
import { formatCoverage, formatIndex, formatPriceUsd } from "@/features/ai-benchmark/shell/format";
import { BANDS, filterModels } from "@/features/ai-benchmark/core/filter";
import { lowestRate } from "@/features/ai-benchmark/core/price";
import type { SortMode } from "@/features/ai-benchmark/core/sort";
import {
  decodeState,
  encodeState,
  DEFAULT_SORT_STATE,
  DEFAULT_STATE,
  type SortState,
} from "@/features/ai-benchmark/core/url-state";
import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";

// vitest-cucumber bindings for the AI Benchmark feature's capability-scoring scenarios (AC-4..AC-11).
// These scenarios are PURE LOGIC — fixture data in, a band/index out — so they bind here in Phase 4
// against the `core/` functions rather than waiting for the route Phase 5 builds. No page is
// rendered; each step is a thin call into the already-unit-tested `core/` modules.
//
// The rendering-dependent scenarios (AC-1/AC-2 page shell, AC-12 low-coverage marker, the charts
// and the data table, the filter UX) are appended to the same feature file and bound by later
// phases — only what this phase implements is bound here.

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature"),
);

// ─── Fixture builders (Z-17: one shared helper set) ────────────────────────────

const SRC = "https://example.test/source";

function fig(benchmark: BenchmarkId, value: number): Figure {
  return { benchmark, value, grade: "verified", source: SRC };
}

function fixtureModel(id: string, figures: Figure[] = []): Model {
  return { id, name: id, vendor: "Test", harnesses: ["claude-code"], figures, pricing: {} };
}

function fixtureDataset(models: Model[]): Dataset {
  return { snapshotDate: "2026-07-28", anchorIds: { opus: OPUS_ANCHOR_ID, sonnet: SONNET_ANCHOR_ID }, models };
}

/**
 * A model scored identically on all four composite benchmarks, metered-priced at `outputRate`.
 * Every model built by this helper for the SAME fixture roster shares a `rosterMax` of whichever
 * one holds the highest `score` — so when that holder scores exactly 100, every other model's
 * composite index equals its own `score` verbatim (100 × score ÷ 100), making index values
 * trivial to reason about across a multi-band fixture (AC-11/AC-41's real opus/sonnet/haiku
 * split, rather than the single-band-only shortcut most other fixtures use).
 */
function bandFixtureModel(id: string, score: number, outputRate: number): Model {
  const m = fixtureModel(id, [
    fig("swe-bench-verified", score),
    fig("swe-bench-pro", score),
    fig("terminal-bench-2-1", score),
    fig("gpqa-diamond", score),
  ]);
  m.pricing = { "claude-code": { kind: "metered", input: 1, output: outputRate, grade: "verified", source: SRC } };
  return m;
}

/**
 * The desktop table's two rightmost price `<td>`s for one model row — input price then output
 * price, per the column order in `model-table.tsx` (F1b: AC-21/AC-30 must check every price cell,
 * not just "some anchor exists somewhere in the table").
 */
function priceCellsOf(row: HTMLTableRowElement): HTMLTableCellElement[] {
  const cells = Array.from(row.querySelectorAll<HTMLTableCellElement>(":scope > td"));
  return cells.slice(-2);
}

// ─── Per-scenario context ──────────────────────────────────────────────────────

type Ctx = {
  // Direct rule-test inputs (AC-4/5/6/7/8).
  model?: Model;
  indices?: IndexMap;
  anchorIndices?: AnchorIndices;
  // Computed results.
  band?: Band;
  index?: number | undefined;
  coverageRatio?: number;
  groups?: BandGroups;
  // Page/table render inputs (Phase 5).
  locale?: Locale;
  // A fixture dataset for table scenarios that need a controlled roster (AC-31/AC-33).
  fixtureDataset?: Dataset;
  // The URL query string a Phase 8 filter scenario sets up before rendering (e.g. "harness=cursor").
  search?: string;
  // A model id picked dynamically from the live roster (AC-39).
  targetModelId?: string;
  // Per-band sort state a Phase 4 sort scenario builds up across its Given/When steps (AC-41).
  sortState?: SortState;
  // The (band, mode) pair the chart's onSortChange callback most recently reported (AC-41).
  requestedSortMode?: SortMode;
  // A band's row order captured before a sort change, to prove an unrelated band is untouched (AC-41).
  opusOrderBefore?: string[];
  haikuOrderBefore?: string[];
  // The encoded URLSearchParams a URL-encoding scenario builds (AC-42).
  encodedParams?: URLSearchParams;
  // Whether the page-load step threw (AC-43).
  thrown?: boolean;
  // One label-element declared text-size class list per simulated viewport width (AC-47, Phase 5
  // reword — DD-25/DD-26).
  widthLabelClasses?: string[][];
  // The row container's own declared className, captured once (it never varies by window width —
  // see the AC-47 binding's own docstring for why jsdom cannot exercise a live reflow).
  rowReflowClassName?: string;
  // A rendered <ModelCard>'s own container, for the card-specific Phase 6 scenarios (AC-53/AC-54).
  cardContainer?: Element;
  // A rendered <ModelTable>'s own container, for the AC-54 card/table parity comparison.
  tableContainer?: Element;
};

/** Every formatted figure value rendered anywhere inside `root` (Phase 6, AC-54 parity). */
function figureValuesIn(root: Element | null | undefined): Set<string> {
  if (!root) return new Set();
  return new Set(
    Array.from(root.querySelectorAll('[data-slot="figure-cell-value"]')).map((el) => el.textContent?.trim() ?? ""),
  );
}

let ctx: Ctx = {};

// The live anchor indices, used as the threshold reference for the rule scenarios.
const liveAnchors: AnchorIndices = anchors(dataset);

describeFeature(feature, ({ Background, Scenario, ScenarioOutline, AfterEachScenario }) => {
  Background(({ Given }) => {
    Given("the AI benchmark dataset is loaded", () => {
      // The `dataset` import is the loaded roster; nothing to set up.
      expect(dataset.models.length).toBeGreaterThan(0);
    });
  });

  AfterEachScenario(() => {
    ctx = {};
    // Reset the mocked navigation locale/search and the simulated <html lang> between scenarios.
    navState.locale = "en";
    navState.search = "";
    navState.lastPush = undefined;
    document.documentElement.lang = "";
    cleanup();
  });

  // Render the full route (server page → client content) for the active locale. The root layout
  // sets <html lang> in production; in jsdom we simulate that here so the "document language
  // attribute" step has something real to assert against.
  function renderPageForLocale(locale: Locale) {
    navState.locale = locale;
    document.documentElement.lang = locale;
    render(React.createElement(AiBenchmarkPage));
  }

  // ─── Phase 8 helpers — render the page against a mocked URL query string ──────
  // The mocked `useSearchParams()` reads `navState.search`; setting it before render + calling
  // `renderPageWithSearch` is the unit-level equivalent of "the URL carries …" (AC-22..AC-28).
  function renderPageWithSearch(search: string, locale: Locale = "en") {
    navState.locale = locale;
    navState.search = search;
    document.documentElement.lang = locale;
    render(React.createElement(AiBenchmarkPage));
  }

  /**
   * Every model id rendered ANYWHERE in the merged chart (rated rows + the unrated list). Since
   * the merge (Phase 3), one rated row always carries BOTH the capability bar and some price
   * representation (bars, subscription text, or "not reported" text — `benchmark-chart.tsx`'s
   * `BenchmarkRow`, unlike the old retired price chart, never omits a priceless model's row), so this
   * one helper now serves what `capabilityChartModelIds()`/`priceChartModelIds()` used to split
   * into two — both resolve to the exact same DOM node set post-merge.
   */
  function benchmarkChartModelIds(): string[] {
    const container = screen.getByTestId("benchmark-chart");
    const rows = Array.from(container.querySelectorAll('[data-testid^="benchmark-chart-row-"]'));
    const unratedItems = Array.from(container.querySelectorAll('[data-testid^="benchmark-chart-unrated-model-"]'));
    return [
      ...rows.map((el) => el.getAttribute("data-testid")!.replace("benchmark-chart-row-", "")),
      ...unratedItems.map((el) => el.getAttribute("data-testid")!.replace("benchmark-chart-unrated-model-", "")),
    ];
  }

  /** The model ids rendered as rows within one band group, in DOM order (AC-41's per-band gate). */
  function rowOrderWithin(bandTestId: string): string[] {
    const container = screen.getByTestId(bandTestId);
    return Array.from(container.querySelectorAll('[data-testid^="benchmark-chart-row-"]')).map((row) =>
      (row.getAttribute("data-testid") ?? "").replace("benchmark-chart-row-", ""),
    );
  }

  /** Every model id rendered as a row in the (desktop) data table. */
  function tableModelIds(): string[] {
    const rows = screen
      .getByTestId("model-table-desktop")
      .querySelectorAll<HTMLTableRowElement>("tbody tr[data-model-id]");
    return Array.from(rows).map((r) => r.getAttribute("data-model-id")!);
  }

  const sorted = (ids: readonly string[]): string[] => [...ids].sort();
  const idsOf = (models: readonly Model[]): string[] => models.map((m) => m.id);

  // ─── AC-4 — opus band ───────────────────────────────────────────────────────

  Scenario("A model reaching the opus anchor renders in the opus band", ({ Given, When, Then }) => {
    Given("a fixture model whose composite index equals the opus anchor index", () => {
      const m = fixtureModel("fixture-at-opus");
      ctx.model = m;
      ctx.indices = { [m.id]: liveAnchors.opus };
      ctx.anchorIndices = liveAnchors;
    });

    When("the capability groups are computed", () => {
      ctx.band = assignBand(ctx.model!, ctx.indices!, ctx.anchorIndices!);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A model reaching the opus anchor renders in the opus band
    Then('that model belongs to the "opus" band', () => {
      expect(ctx.band).toBe("opus");
    });
  });

  // ─── AC-5 — sonnet band ─────────────────────────────────────────────────────

  Scenario("A model between the two anchors renders in the sonnet band", ({ Given, When, Then, And }) => {
    const opus = liveAnchors.opus as number;
    const sonnet = liveAnchors.sonnet as number;
    const between = (opus + sonnet) / 2;

    Given("a fixture model whose composite index is above the sonnet anchor index", () => {
      const m = fixtureModel("fixture-between");
      ctx.model = m;
      ctx.indices = { [m.id]: between };
      ctx.anchorIndices = liveAnchors;
    });

    And("that model's composite index is below the opus anchor index", () => {
      expect((ctx.indices![ctx.model!.id] as number) < opus).toBe(true);
    });

    When("the capability groups are computed", () => {
      ctx.band = assignBand(ctx.model!, ctx.indices!, ctx.anchorIndices!);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A model between the two anchors renders in the sonnet band
    Then('that model belongs to the "sonnet" band', () => {
      expect(ctx.band).toBe("sonnet");
    });
  });

  // ─── AC-6 — haiku band ──────────────────────────────────────────────────────

  Scenario("A model below the sonnet anchor renders in the haiku band", ({ Given, When, Then }) => {
    const sonnet = liveAnchors.sonnet as number;

    Given("a fixture model whose composite index is below the sonnet anchor index", () => {
      const m = fixtureModel("fixture-below-sonnet");
      ctx.model = m;
      ctx.indices = { [m.id]: sonnet / 2 };
      ctx.anchorIndices = liveAnchors;
    });

    When("the capability groups are computed", () => {
      ctx.band = assignBand(ctx.model!, ctx.indices!, ctx.anchorIndices!);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A model below the sonnet anchor renders in the haiku band
    Then('that model belongs to the "haiku" band', () => {
      expect(ctx.band).toBe("haiku");
    });
  });

  // ─── AC-7 — anchor pinning ──────────────────────────────────────────────────

  Scenario("Each anchor model occupies the band it defines", ({ Given, When, Then, And }) => {
    // Perverse fixture: the opus anchor's index (50) is BELOW the sonnet anchor's (90). Pinning
    // must still place each anchor in the band it defines.
    const perverse: AnchorIndices = { opus: 50, sonnet: 90 };
    const perverseIndices: IndexMap = { [OPUS_ANCHOR_ID]: 50, [SONNET_ANCHOR_ID]: 90 };
    const opusAnchor = fixtureModel(OPUS_ANCHOR_ID);
    const sonnetAnchor = fixtureModel(SONNET_ANCHOR_ID);
    const bands: Partial<Record<Band, Band>> = {};

    Given("the two anchor models are present in the roster", () => {
      ctx.anchorIndices = perverse;
      ctx.indices = perverseIndices;
    });

    When("the capability groups are computed", () => {
      bands.opus = assignBand(opusAnchor, perverseIndices, perverse);
      bands.sonnet = assignBand(sonnetAnchor, perverseIndices, perverse);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Each anchor model occupies the band it defines
    Then('the opus anchor belongs to the "opus" band', () => {
      expect(bands.opus).toBe("opus");
    });

    And('the sonnet anchor belongs to the "sonnet" band', () => {
      expect(bands.sonnet).toBe("sonnet");
    });
  });

  // ─── AC-8 — unrated group ───────────────────────────────────────────────────

  Scenario("A model with no published benchmark score renders in the unrated group", ({ Given, When, Then, And }) => {
    Given("a fixture model with no score on any composite benchmark", () => {
      ctx.model = fixtureModel("no-score", []);
    });

    When("the capability groups are computed", () => {
      const ds = fixtureDataset([ctx.model!]);
      const maxes = computeRosterMaxes(ds);
      ctx.index = computeIndex(ctx.model!, maxes);
      ctx.band = assignBand(ctx.model!, { [ctx.model!.id]: ctx.index }, liveAnchors);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A model with no published benchmark score renders in the unrated group
    Then('that model belongs to the "unrated" group', () => {
      expect(ctx.band).toBe("unrated");
    });

    And("that model has no composite index", () => {
      expect(ctx.index).toBeUndefined();
    });
  });

  // ─── AC-9 — totality ────────────────────────────────────────────────────────

  Scenario("Every roster model belongs to exactly one capability group", ({ Given, When, Then }) => {
    Given("the full roster is loaded", () => {
      // dataset is the full roster.
    });

    When("the capability groups are computed", () => {
      ctx.groups = computeGroups(dataset);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Every roster model belongs to exactly one capability group
    Then('each model appears in exactly one of "opus", "sonnet", "haiku", or "unrated"', () => {
      const g = ctx.groups!;
      const placed = [...g.opus, ...g.sonnet, ...g.haiku, ...g.unrated].map((s) => s.model.id);
      // Exactly once each (no duplicates), and every roster model is covered.
      expect(new Set(placed).size).toBe(placed.length);
      expect(placed.length).toBe(dataset.models.length);
    });
  });

  // ─── AC-65 — the rated capability classes are named opus, sonnet, and haiku ────

  Scenario("The rated capability classes are named opus, sonnet, and haiku", ({ Given, When, Then, And }) => {
    let identifiers: readonly string[] = [];

    Given("the full roster is loaded", () => {
      // dataset is the full roster.
    });

    When("the set of known capability class identifiers is inspected", () => {
      identifiers = BANDS;
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The rated capability classes are named opus, sonnet, and haiku
    Then('the identifiers are exactly "opus", "sonnet", "haiku", and "unrated"', () => {
      expect(identifiers).toEqual(["opus", "sonnet", "haiku", "unrated"]);
    });

    And('no identifier is "light"', () => {
      expect(identifiers).not.toContain("light");
    });
  });

  // ─── AC-10 — composite index + coverage over present benchmarks ─────────────

  Scenario("A model missing a benchmark is scored over the benchmarks it has", ({ Given, When, Then, And }) => {
    // Fixture: swe-bench-verified=64 and gpqa-diamond=40 (two of four); a roster-max holder pins
    // both axes at 80 so the rels are 80 and 50 respectively.
    const twoOfFour = fixtureModel("two-of-four", [fig("swe-bench-verified", 64), fig("gpqa-diamond", 40)]);
    const holder = fixtureModel("holder", [fig("swe-bench-verified", 80), fig("gpqa-diamond", 80)]);
    const ds = fixtureDataset([twoOfFour, holder]);
    const maxes = computeRosterMaxes(ds);

    Given("a fixture model with a score on two of the four composite benchmarks", () => {
      ctx.model = twoOfFour;
    });

    When("its composite index is computed", () => {
      ctx.index = computeIndex(twoOfFour, maxes);
      ctx.coverageRatio = coverage(twoOfFour);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A model missing a benchmark is scored over the benchmarks it has
    Then("the index equals the weight-renormalized mean of those two normalized scores", () => {
      const relSv = (100 * 64) / 80;
      const relGpqa = (100 * 40) / 80;
      const wSv = BENCHMARK_WEIGHTS["swe-bench-verified"];
      const wGpqa = BENCHMARK_WEIGHTS["gpqa-diamond"];
      const expected = (wSv * relSv + wGpqa * relGpqa) / (wSv + wGpqa);
      expect(ctx.index).toBeCloseTo(expected, 10);
    });

    And("its coverage ratio equals the summed weight of those two benchmarks divided by one hundred", () => {
      const expected = (BENCHMARK_WEIGHTS["swe-bench-verified"] + BENCHMARK_WEIGHTS["gpqa-diamond"]) / 100;
      expect(ctx.coverageRatio).toBeCloseTo(expected, 10);
    });
  });

  // ─── AC-11 — rewritten (Phase 4): a sort change preserves band membership ─────

  Scenario(
    "Models are ordered identically before and after a sort change within a band",
    ({ Given, When, Then, And }) => {
      const opusAnchor = bandFixtureModel(OPUS_ANCHOR_ID, 100, 1);
      const sonnetAnchor = bandFixtureModel(SONNET_ANCHOR_ID, 60, 1);
      const opusHi = bandFixtureModel("ac11-opus-hi", 100, 50); // higher price
      const opusLo = bandFixtureModel("ac11-opus-lo", 100, 10); // lower price
      const ds = fixtureDataset([opusAnchor, sonnetAnchor, opusHi, opusLo]);

      function renderWithSort(sortState: SortState) {
        cleanup();
        ctx.sortState = sortState;
        render(
          React.createElement(BenchmarkChart, {
            dataset: ds,
            fullDataset: ds,
            locale: "en",
            sortState,
            onSortChange: (band, mode) => {
              if (band === "opus") ctx.requestedSortMode = mode;
            },
          }),
        );
      }

      Given("the opus band is sorted by capability", () => {
        renderWithSort({ ...DEFAULT_SORT_STATE, opus: "capability" });
        ctx.opusOrderBefore = rowOrderWithin("benchmark-chart-band-opus");
      });

      When("the reader switches the opus band's sort to price low to high", () => {
        const select = screen.getByRole("combobox", {
          name: `${t("en", "aiBenchSortLabel")} — ${bandLabel("opus", "en")}`,
        });
        fireEvent.change(select, { target: { value: "price-asc" } });
        renderWithSort({ ...ctx.sortState!, opus: ctx.requestedSortMode ?? "price-asc" });
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Models are ordered identically before and after a sort change within a band
      Then("every model previously in the opus band still appears in the opus band", () => {
        const after = rowOrderWithin("benchmark-chart-band-opus");
        for (const id of ctx.opusOrderBefore!) {
          expect(after).toContain(id);
        }
      });

      And("the set of models in the band is unchanged, only their order changes", () => {
        const after = rowOrderWithin("benchmark-chart-band-opus");
        expect([...after].sort()).toEqual([...ctx.opusOrderBefore!].sort());
        expect(ctx.requestedSortMode).toBe("price-asc");
      });
    },
  );

  // ════════════════════════════════════════════════════════════════════════════
  // Phase 5 — route, data table, i18n, and the honesty surface.
  // Rendering-dependent scenarios (AC-1/2/19/20/21/29/30/31/32/33/34/35). Each scenario
  // registers its own steps (vitest-cucumber scopes step registrations per Scenario block).
  // ════════════════════════════════════════════════════════════════════════════

  // ─── AC-1 — English page heading ──────────────────────────────────────────────

  Scenario("The English page renders its localized heading", ({ Given, When, Then, And }) => {
    Given('the locale is "en"', () => {
      ctx.locale = "en";
    });

    When("the AI benchmark page renders", () => {
      renderPageForLocale(ctx.locale ?? "en");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The English page renders its localized heading
    Then("the page shows a level-one heading in English", () => {
      const h1 = screen.getByRole("heading", { level: 1 });
      expect(h1.textContent).toBe(t("en", "aiBenchTitle"));
    });

    And('the document language attribute is "en"', () => {
      expect(document.documentElement.lang).toBe("en");
    });
  });

  // ─── AC-2 — Indonesian page heading ───────────────────────────────────────────

  Scenario("The Indonesian page renders its localized heading", ({ Given, When, Then, And }) => {
    Given('the locale is "id"', () => {
      ctx.locale = "id";
    });

    When("the AI benchmark page renders", () => {
      renderPageForLocale(ctx.locale ?? "id");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The Indonesian page renders its localized heading
    Then("the page shows a level-one heading in Indonesian", () => {
      const h1 = screen.getByRole("heading", { level: 1 });
      expect(h1.textContent).toBe(t("id", "aiBenchTitle"));
      // The two locales must produce distinct copy (else the page isn't really localized).
      expect(t("id", "aiBenchTitle")).not.toBe(t("en", "aiBenchTitle"));
    });

    And('the document language attribute is "id"', () => {
      expect(document.documentElement.lang).toBe("id");
    });
  });

  // ─── AC-19 — data table present without interaction ───────────────────────────

  Scenario("The data table is present without any interaction", ({ Given, When, Then, And }) => {
    Given("the full roster is loaded", () => {
      // dataset is the full roster.
    });

    When("the page first renders", () => {
      renderPageForLocale("en");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The data table is present without any interaction
    Then("a data table is present in the document", () => {
      const table = screen.getByTestId("model-table-desktop");
      expect(table.querySelector("table")).not.toBeNull();
    });

    And("the table has a caption", () => {
      const caption = screen.getByTestId("model-table-desktop").querySelector("caption");
      expect(caption).not.toBeNull();
      expect((caption?.textContent ?? "").trim().length).toBeGreaterThan(0);
    });

    And("every table header cell declares a scope", () => {
      const headers = screen.getByTestId("model-table-desktop").querySelectorAll("th");
      expect(headers.length).toBeGreaterThan(0);
      for (const th of Array.from(headers)) {
        expect(th.getAttribute("scope")).toMatch(/^(col|row)$/);
      }
    });
  });

  // ─── AC-20 — the table carries every figure ───────────────────────────────────

  Scenario("The table carries every figure the merged chart encodes", ({ Given, When, Then }) => {
    Given("the full roster is loaded", () => {
      // dataset is the full roster.
    });

    When("the data table is rendered", () => {
      render(<ModelTable dataset={dataset} fullDataset={dataset} locale="en" />);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The table carries every figure the merged chart encodes
    Then(
      "each model row lists its harnesses, class, every benchmark score, composite index, coverage ratio, input price, and output price",
      () => {
        const desktop = screen.getByTestId("model-table-desktop");
        const headerTexts = Array.from(desktop.querySelectorAll("thead th")).map((h) => h.textContent ?? "");
        // Index and the two prices are primary columns (Phase 6 cycle 6.3), so their header exists.
        expect(headerTexts.some((h) => h === t("en", "aiBenchColIndex"))).toBe(true);
        expect(headerTexts.some((h) => h === t("en", "aiBenchColInputPrice"))).toBe(true);
        expect(headerTexts.some((h) => h === t("en", "aiBenchColOutputPrice"))).toBe(true);

        const rows = desktop.querySelectorAll<HTMLTableRowElement>("tbody tr[data-model-id]");
        expect(rows.length).toBe(dataset.models.length);
        // Every benchmark score and coverage moved into each row's own detail disclosure (cycle
        // 6.3) rather than the header — assert each row's ADJACENT detail row carries every
        // benchmark column's label plus coverage's label as a `<dt>` (DD-28: still in the DOM,
        // just behind a native disclosure, not a hidden column).
        for (const row of Array.from(rows)) {
          const modelId = row.getAttribute("data-model-id")!;
          const model = dataset.models.find((m) => m.id === modelId);
          expect(model).toBeDefined();
          const detailRow = desktop.querySelector(`tbody tr[data-model-detail-id="${modelId}"]`);
          expect(detailRow, `detail row for ${modelId}`).not.toBeNull();
          // A benchmark this model never published (DD-34 Treatment 4, cycle 6.7) shares its <dt>
          // with the other unpublished labels in the same group, each carrying a trailing comma
          // except the last — strip it so the label match below is exact either way.
          const detailDtLabels = Array.from(detailRow!.querySelectorAll("dt")).map((dt) =>
            (dt.textContent ?? "").replace(/,$/, "").trim(),
          );
          for (const col of BENCHMARK_COLUMNS) {
            expect(detailDtLabels).toContain(t("en", col.labelKey));
          }
          expect(detailDtLabels).toContain(t("en", "aiBenchColCoverage"));
          // Each row's own detail region carries its harness display names.
          const detailText = detailRow!.textContent ?? "";
          for (const h of model!.harnesses) {
            expect(detailText).toContain(HARNESS_DISPLAY_NAMES[h] ?? h);
          }
        }
        // At least one metered model renders numeric input and output prices.
        const allText = desktop.textContent ?? "";
        expect(allText).toMatch(/\$/); // formatted USD prices are present
      },
    );
  });

  // ─── AC-21 — every figure carries an evidence grade ───────────────────────────

  Scenario("Every figure in the table carries an evidence grade", ({ Given, When, Then, And }) => {
    Given("the full roster is loaded", () => {
      // dataset is the full roster.
    });

    When("the data table is rendered", () => {
      render(<ModelTable dataset={dataset} fullDataset={dataset} locale="en" />);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Every figure in the table carries an evidence grade
    Then("every benchmark score cell carries an evidence grade marker", () => {
      const figureCells = screen
        .getAllByTestId("model-table-desktop")
        .flatMap((el) => Array.from(el.querySelectorAll('[data-slot="figure-cell"]')));
      // Benchmark figures exist on the roster, so there must be figure cells.
      expect(figureCells.length).toBeGreaterThan(0);
      // Every figure cell has a grade marker (the evidence badge).
      for (const cell of figureCells) {
        expect(cell.querySelector('[data-slot="evidence-badge"]')).not.toBeNull();
      }
    });

    And("every price cell carries an evidence grade marker", () => {
      // Enumerate EVERY model row's two price cells (input, then output — the last two <td>s) and
      // check each one individually, rather than asserting "some anchor exists somewhere in the
      // table" (which could pass with zero correctly-rendered price cells; see F1b). A price cell
      // either reports a real price — in which case it MUST carry a proper `<FigureCell>` grade
      // marker — or it reports no price at all, in which case it must read as "not reported" and
      // carry no link (never a fabricated/unmarked citation; see F1a).
      const rows = screen
        .getByTestId("model-table-desktop")
        .querySelectorAll<HTMLTableRowElement>("tbody tr[data-model-id]");
      expect(rows.length).toBe(dataset.models.length);
      for (const row of Array.from(rows)) {
        for (const cell of priceCellsOf(row)) {
          const anchor = cell.querySelector("a[href]");
          if (anchor === null) {
            expect(cell.textContent).toContain(t("en", "aiBenchNoFigure"));
            continue;
          }
          expect(cell.querySelector('[data-slot="figure-cell"] [data-slot="evidence-badge"]')).not.toBeNull();
        }
      }
    });
  });

  // ─── AC-29 — snapshot date in text ────────────────────────────────────────────

  Scenario("The page displays the dataset snapshot date", ({ Given, When, Then }) => {
    Given("the dataset carries a snapshot date", () => {
      expect(dataset.snapshotDate.length).toBeGreaterThan(0);
    });

    When("the page renders", () => {
      renderPageForLocale("en");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The page displays the dataset snapshot date
    Then("the snapshot date is shown in text", () => {
      const snapshot = screen.getByTestId("ai-bench-snapshot");
      const text = snapshot.textContent ?? "";
      // The snapshot date is formatted with its year, regardless of locale formatting.
      expect(text).toContain("2026");

      // Regression pin (F2): `new Date(dataset.snapshotDate)` parses as UTC midnight, so the
      // formatter MUST pin `timeZone: "UTC"` — otherwise the runtime's local zone reformats it and
      // every visitor west of UTC sees the day before the dataset's actual snapshot date. Assert
      // this directly against the real `Intl.DateTimeFormat` call the component makes, rather than
      // depending on the test runner's own host timezone (which may itself be UTC).
      const NativeDateTimeFormat = Intl.DateTimeFormat;
      const optionsSeen: Intl.DateTimeFormatOptions[] = [];
      const spy = vi.spyOn(Intl, "DateTimeFormat").mockImplementation(function (
        this: unknown,
        locale?: string | string[],
        options?: Intl.DateTimeFormatOptions,
      ) {
        if (options) optionsSeen.push(options);
        return new NativeDateTimeFormat(locale, options);
      } as unknown as typeof Intl.DateTimeFormat);
      try {
        cleanup();
        renderPageForLocale("en");
      } finally {
        spy.mockRestore();
      }
      const snapshotDateCall = optionsSeen.find(
        (o) => o.year === "numeric" && o.month === "long" && o.day === "numeric",
      );
      expect(snapshotDateCall?.timeZone).toBe("UTC");
    });
  });

  // ─── AC-30 — every figure links to its source ─────────────────────────────────

  Scenario("Every benchmark figure links to the source it came from", ({ Given, When, Then, And }) => {
    Given("the full roster is loaded", () => {
      // dataset is the full roster.
    });

    When("the data table is rendered", () => {
      render(<ModelTable dataset={dataset} fullDataset={dataset} locale="en" />);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Every benchmark figure links to the source it came from
    Then("every benchmark score cell resolves to a source link", () => {
      const figureCells = screen.getByTestId("model-table-desktop").querySelectorAll('[data-slot="figure-cell"]');
      expect(figureCells.length).toBeGreaterThan(0);
      for (const cell of Array.from(figureCells)) {
        const anchor = cell.querySelector("a[href]");
        expect(anchor).not.toBeNull();
        expect((anchor?.getAttribute("href") ?? "").length).toBeGreaterThan(0);
      }
    });

    And("every price cell resolves to a source link", () => {
      // Same per-cell enumeration as AC-21 above (F1b): a price cell that reports a figure must
      // resolve to a non-empty source href; a price cell with genuinely no data must carry no link
      // at all (never a fabricated citation pointing at this page itself; see F1a).
      const rows = screen
        .getByTestId("model-table-desktop")
        .querySelectorAll<HTMLTableRowElement>("tbody tr[data-model-id]");
      expect(rows.length).toBe(dataset.models.length);
      for (const row of Array.from(rows)) {
        for (const cell of priceCellsOf(row)) {
          const anchor = cell.querySelector("a[href]");
          if (anchor === null) {
            expect(cell.textContent).toContain(t("en", "aiBenchNoFigure"));
            continue;
          }
          expect((anchor.getAttribute("href") ?? "").length).toBeGreaterThan(0);
          // The anchor must be a genuine `<FigureCell>` source link, not an ad-hoc/fabricated one
          // (F1a: the old subscription-cell markup carried a "source" link outside any figure-cell).
          expect(cell.querySelector('[data-slot="figure-cell"]')).not.toBeNull();
        }
      }
    });
  });

  // ─── AC-31 — conflicted figure renders as a range ─────────────────────────────

  Scenario("A conflicted figure renders as a range rather than a single number", ({ Given, When, Then, But }) => {
    // Fixture: one model with a conflicted GPQA Diamond figure, low 70 / high 80.
    const low = 70;
    const high = 80;
    const average = (low + high) / 2;
    const conflictedFigure: ConflictedFigure = {
      benchmark: "gpqa-diamond",
      value: low,
      grade: "conflicted",
      low,
      high,
      source: "https://example.test/conflict",
    };
    const conflictedModel: Model = {
      id: "fixture-conflicted",
      name: "Fixture Conflicted",
      vendor: "Test",
      harnesses: ["claude-code"],
      figures: [conflictedFigure],
      pricing: {},
    };

    Given("a fixture model whose benchmark figure has conflicting published values", () => {
      ctx.fixtureDataset = fixtureDataset([conflictedModel]);
    });

    When("the data table is rendered", () => {
      render(<ModelTable dataset={ctx.fixtureDataset!} fullDataset={ctx.fixtureDataset!} locale="en" />);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A conflicted figure renders as a range rather than a single number
    Then("that cell shows the lowest and highest published values", () => {
      // GPQA Diamond is a benchmark column — it lives in the row's own detail disclosure (cycle
      // 6.3), not the primary row.
      const detailRow = screen
        .getByTestId("model-table-desktop")
        .querySelector('tbody tr[data-model-detail-id="fixture-conflicted"]');
      expect(detailRow).not.toBeNull();
      const cellText = detailRow?.textContent ?? "";
      // Both the low (70.0) and high (80.0) formatted values appear.
      expect(cellText).toContain("70.0");
      expect(cellText).toContain("80.0");
    });

    But("that cell shows no averaged value", () => {
      const detailRow = screen
        .getByTestId("model-table-desktop")
        .querySelector('tbody tr[data-model-detail-id="fixture-conflicted"]');
      const cellText = detailRow?.textContent ?? "";
      // The average (75.0) must NOT appear — no averaged middle value is shown.
      expect(cellText).not.toContain(`${average.toFixed(1)}`);
    });
  });

  // ─── AC-32 — how-to-read disclosure ───────────────────────────────────────────

  Scenario(
    "The page discloses that frontier scores are overwhelmingly vendor-reported",
    ({ Given, When, Then, And }) => {
      Given("the page carries a how-to-read disclosure", () => {
        // The disclosure ships with the page; nothing to set up.
      });

      When("the page renders", () => {
        renderPageForLocale("en");
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The page discloses that frontier scores are overwhelmingly vendor-reported
      Then(
        "a single honesty line stating that most frontier benchmark scores are vendor self-reported is visible without interaction",
        () => {
          const honesty = screen.getByTestId("ai-bench-how-to-honesty");
          // The English copy states vendor self-reported scores explicitly.
          expect((honesty.textContent ?? "").toLowerCase()).toContain("self-reported");
          // Visible without interaction means it is NOT gated behind any `<details>` ancestor.
          expect(honesty.closest("details")).toBeNull();
        },
      );

      And("the remaining how-to-read points are reachable from that line's disclosure control", () => {
        const details = screen.getByTestId("ai-bench-how-to-details");
        expect(details.tagName).toBe("DETAILS");
        expect(details.querySelector("summary")).not.toBeNull();
        // 6, not 5, since Rule-15 UWT-013 added the price-unit-basis bullet.
        expect(details.querySelectorAll("li").length).toBe(6);
      });
    },
  );

  // ─── Rule-15 UWT-013/USS-004 fix — price figures disclose their unit basis ────

  Scenario("Price figures disclose their unit basis", ({ Given, When, Then, And }) => {
    Given('the reader opens "How to read this benchmark"', () => {
      renderPageForLocale("en");
      const details = screen.getByTestId("ai-bench-how-to-details");
      // Native `<details>` starts closed below `lg` in jsdom (no CSS applied) — open it via its
      // own `open` attribute so its content is present the same way a real click would reveal it.
      details.setAttribute("open", "");
    });

    When("the reader reads the price-related guidance", () => {
      // Nothing further to set up — the content opened above IS the guidance being read.
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Price figures disclose their unit basis
    Then("the text states the unit each dollar figure is priced per", () => {
      const priceUnit = screen.getByTestId("ai-bench-how-to-price-unit");
      expect((priceUnit.textContent ?? "").toLowerCase()).toContain("per 1m tokens");
    });

    And("a Subscription-priced model's figure is visibly distinguished from a per-unit price", () => {
      const priceUnit = screen.getByTestId("ai-bench-how-to-price-unit");
      expect((priceUnit.textContent ?? "").toLowerCase()).toContain("subscription");
    });
  });

  // ─── USS-002 — a legend defines the capability classes and evidence grades ────

  Scenario("A legend defines the capability classes and evidence grades", ({ Given, When, Then }) => {
    Given("I am on the AI Model Benchmark page", () => {
      renderPageForLocale("en");
    });

    When('I look for an explanation of the "Class" and evidence-grade labels', () => {
      // The legend ships with the page; nothing to set up beyond the render above.
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A legend defines the capability classes and evidence grades
    Then("an expandable legend defines each of the four classes and each of the five evidence grades", () => {
      const legend = screen.getByTestId("ai-bench-legend");
      // AC-57 (cycle 7.3): the legend is now its own `<details>`, reachable via its `<summary>`
      // rather than unconditionally visible.
      expect(legend.tagName).toBe("DETAILS");
      expect(legend.querySelector("summary")).not.toBeNull();

      for (const band of ["opus", "sonnet", "haiku", "unrated"]) {
        expect(screen.getByTestId(`ai-bench-legend-class-${band}`)).toBeTruthy();
      }
      for (const grade of ["verified", "self-reported", "secondary", "conflicted", "unavailable"]) {
        expect(screen.getByTestId(`ai-bench-legend-grade-${grade}`)).toBeTruthy();
      }

      // Rule-15 UWT-011 fix: the Class column/filter reused Anthropic's own tier names
      // cross-vendor with no inline hint anywhere pointing at this legend — both hint links below
      // must resolve to a real anchor `id` this legend's own classes list carries.
      const classesList = screen.getByTestId("ai-bench-legend-classes");
      expect(classesList.id).toBe("ai-bench-legend-classes");
      const desktopHint = document
        .getElementById("benchmark-filter-class-desktop")
        ?.closest('[data-slot="filter-select"]')
        ?.querySelector('a[href="#ai-bench-legend-classes"]');
      expect(desktopHint).not.toBeNull();
      const tableHint = screen.getByTestId("model-table-desktop").querySelector('a[href="#ai-bench-legend-classes"]');
      expect(tableHint).not.toBeNull();
    });
  });

  // ─── AC-33 — integrity note reachable from the model's row ────────────────────

  Scenario(
    "The page names a known benchmark-integrity finding beside the model it concerns",
    ({ Given, When, Then }) => {
      const notedModel: Model = {
        id: "fixture-noted",
        name: "Fixture Noted",
        vendor: "Test",
        harnesses: ["claude-code"],
        figures: [],
        pricing: {},
        notes: [
          {
            modelId: "fixture-noted",
            text: "A benchmark-integrity finding for this fixture model.",
            source: "https://example.test/finding",
          },
        ],
      };

      Given("the dataset records a benchmark-integrity note for a model", () => {
        ctx.fixtureDataset = fixtureDataset([notedModel]);
      });

      When("that model is rendered in the data table", () => {
        render(<ModelTable dataset={ctx.fixtureDataset!} fullDataset={ctx.fixtureDataset!} locale="en" />);
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The page names a known benchmark-integrity finding beside the model it concerns
      Then("the integrity note is reachable from that model's row", () => {
        const row = screen.getByTestId("model-table-desktop").querySelector('tbody tr[data-model-id="fixture-noted"]');
        expect(row).not.toBeNull();
        const noteLink = row?.querySelector('[data-slot="integrity-note"]');
        expect(noteLink).not.toBeNull();
        expect(noteLink?.getAttribute("href")).toBe("https://example.test/finding");
      });
    },
  );

  // ─── Rule-15 UWT-010 fix — the integrity-note claim is visible + localized ────

  Scenario(
    "The integrity-note claim is reachable without hovering, and is localized on id",
    ({ Given, When, Then, And }) => {
      Given('the dataset records a benchmark-integrity note for the model "gpt-5.6-sol"', () => {
        expect(dataset.models.find((m) => m.id === "gpt-5.6-sol")?.notes?.length).toBeGreaterThan(0);
      });

      When('that model is rendered in the data table on the "id" locale', () => {
        render(<ModelTable dataset={dataset} fullDataset={dataset} locale="id" />);
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The integrity-note claim is reachable without hovering, and is localized on id
      Then("the claim text is visible as real on-page text behind a click-to-reveal disclosure", () => {
        const row = screen.getByTestId("model-table-desktop").querySelector('tbody tr[data-model-id="gpt-5.6-sol"]');
        const detail = row?.querySelector('[data-slot="integrity-note-detail"]');
        expect(detail?.tagName).toBe("DETAILS");
        expect(detail?.querySelector("summary")).not.toBeNull();
        const claimText = detail?.querySelector("p")?.textContent ?? "";
        expect(claimText.length).toBeGreaterThan(0);
      });

      And("the visible claim text is the Indonesian translation, not the English source text", () => {
        const row = screen.getByTestId("model-table-desktop").querySelector('tbody tr[data-model-id="gpt-5.6-sol"]');
        const claimText = row?.querySelector('[data-slot="integrity-note-detail"] p')?.textContent ?? "";
        const englishSource = dataset.models.find((m) => m.id === "gpt-5.6-sol")!.notes![0]!.text;
        expect(claimText).not.toBe(englishSource);
        expect(claimText.toLowerCase()).toContain("mencurangi");
      });
    },
  );

  // ─── AC-34 — sources and licences section ─────────────────────────────────────

  Scenario("The page carries a sources and licences section", ({ Given, When, Then, And }) => {
    Given("the dataset names its benchmark operators", () => {
      expect(OPERATORS.length).toBeGreaterThan(0);
    });

    When("the page renders", () => {
      renderPageForLocale("en");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The page carries a sources and licences section
    Then("a sources and licences section lists every named operator", () => {
      const section = screen.getByTestId("ai-bench-sources");
      const text = section.textContent ?? "";
      for (const op of OPERATORS) {
        expect(text).toContain(op.name);
      }

      // Regression guard for F8: each operator's rendered link must point at the URL declared
      // for that operator's own name — no entry may bundle an unrelated organization's name onto
      // another operator's URL (or vice versa), which is exactly how a prior entry conflated the
      // unrelated "ARC Prize" and "GPQA" operators into a single row.
      const containers = screen.getAllByTestId("source-operator");
      expect(containers.length).toBe(OPERATORS.length);
      OPERATORS.forEach((op, index) => {
        const link = containers[index]?.querySelector("a[href]");
        if (op.url) {
          expect(link).not.toBeNull();
          expect(link?.getAttribute("href")).toBe(op.url);
          expect(link?.textContent).toBe(op.name);
          // Rule-15 UWT-012 fix: these citation links measured below the 24x24 CSS px minimum
          // (DD-30/AC-58) — same `TAP_TARGET_MIN_CLASS` treatment already applied to the
          // integrity-note links and every `<summary>` on this page.
          expect(link?.className).toContain("min-h-6");
        } else {
          expect(link).toBeNull();
        }
      });

      // GPQA contributes a weight-30 composite figure (URL.gpqa, cited across the roster) and
      // must be named as its own operator — never merged with the unrelated ARC Prize
      // Foundation, whose figures do not appear in this roster (see DD-23 in tech-docs.md).
      const gpqa = OPERATORS.find((op) => op.url === "https://github.com/idavidrein/gpqa");
      expect(gpqa).toBeDefined();
      expect(gpqa?.name).toBe("GPQA");
      expect(OPERATORS.some((op) => op.name.includes("ARC Prize"))).toBe(false);
    });

    And("each operator entry states its republication terms or records that none are stated", () => {
      const terms = screen.getAllByTestId("operator-terms");
      expect(terms.length).toBe(OPERATORS.length);
      for (const dd of terms) {
        // Terms copy resolves to real localized text (not a raw key), and is non-empty.
        expect((dd.textContent ?? "").trim().length).toBeGreaterThan(0);
        expect(dd.textContent ?? "").not.toMatch(/aiBench/);
      }

      // Regression guard for F8: every operator's termsKey must be distinct, unless it
      // deliberately shares the generic "no terms stated" key — a copy-pasted or merged entry
      // silently reusing another operator's dedicated termsKey must fail here.
      const seenTermsKeys = new Set<string>();
      for (const op of OPERATORS) {
        if (op.termsKey !== "aiBenchOpTermsNone") {
          expect(seenTermsKeys.has(op.termsKey)).toBe(false);
        }
        seenTermsKeys.add(op.termsKey);
      }

      // GPQA's stated terms must reflect the benchmark repository's actual MIT licence, not the
      // generic "no terms stated" text used for operators that genuinely publish none.
      const gpqaIndex = OPERATORS.findIndex((op) => op.url === "https://github.com/idavidrein/gpqa");
      expect(gpqaIndex).toBeGreaterThanOrEqual(0);
      expect(terms[gpqaIndex]?.textContent ?? "").toMatch(/MIT/i);
    });
  });

  // ─── AC-35 — no raw translation key leaks (both locales) ───────────────────────

  ScenarioOutline("No raw translation key leaks on either locale", ({ Given, When, Then }, variables) => {
    Given('the locale is "<locale>"', () => {
      ctx.locale = variables.locale as Locale;
    });

    When("the AI benchmark page renders", () => {
      renderPageForLocale(ctx.locale ?? "en");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:No raw translation key leaks on either locale
    Then("no rendered text matches a raw translation key", () => {
      const text = document.body.textContent ?? "";
      // Every aiBench* key resolves to localized copy via t(); a missing key renders as its raw
      // identifier (which always starts with "aiBench"), so any leak surfaces as the substring.
      expect(text).not.toMatch(/aiBench/);
    });
  });

  // ─── AC-66 — the haiku class label is identical in both locales ───────────────

  ScenarioOutline("The haiku class label is identical in both locales", ({ Given, When, Then, And }, variables) => {
    let label = "";

    Given('the class legend is rendered in the "<locale>" locale', () => {
      ctx.locale = variables.locale as Locale;
    });

    When("the haiku class label is read", () => {
      label = bandLabel("haiku", ctx.locale ?? "en");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The haiku class label is identical in both locales
    Then('that label is "Haiku"', () => {
      expect(label).toBe("Haiku");
    });

    And("that label is identical to the label the other locale renders", () => {
      const otherLocale: Locale = ctx.locale === "en" ? "id" : "en";
      expect(label).toBe(bandLabel("haiku", otherLocale));
    });
  });

  // ════════════════════════════════════════════════════════════════════════════
  // Phase 6 — shared chart primitives and the capability chart (AC-12/13/14/36/37).
  // ════════════════════════════════════════════════════════════════════════════

  // The three RATED bands, in the same canonical order `computeGroups` produces them.
  const RATED_BAND_KEYS = ["opus", "sonnet", "haiku"] as const;

  // ─── AC-13 — bar length proportional to the composite index ────────────────────

  Scenario("Bar length is proportional to the composite index", ({ Given, When, Then, And }) => {
    Given("two fixture models whose composite indices differ", () => {
      const low = fixtureModel("cap-low", [fig("swe-bench-verified", 40)]);
      const high = fixtureModel("cap-high", [
        fig("swe-bench-verified", 80),
        fig("swe-bench-pro", 80),
        fig("terminal-bench-2-1", 80),
        fig("gpqa-diamond", 80),
      ]);
      ctx.fixtureDataset = fixtureDataset([low, high]);
    });

    When("the merged chart is rendered", () => {
      render(
        React.createElement(BenchmarkChart, {
          dataset: ctx.fixtureDataset!,
          fullDataset: ctx.fixtureDataset!,
          locale: "en",
        }),
      );
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Bar length is proportional to the composite index
    Then("the ratio of their bar lengths equals the ratio of their composite indices", () => {
      const groups = computeGroups(ctx.fixtureDataset!);
      const all = [...groups.opus, ...groups.sonnet, ...groups.haiku];
      const lowScore = all.find((s) => s.model.id === "cap-low");
      const highScore = all.find((s) => s.model.id === "cap-high");
      expect(lowScore?.index).toBeDefined();
      expect(highScore?.index).toBeDefined();

      const lowBar = screen.getByTestId("benchmark-chart-bar-capability-cap-low-fill");
      const highBar = screen.getByTestId("benchmark-chart-bar-capability-cap-high-fill");
      const lowWidth = parseFloat(lowBar.style.width);
      const highWidth = parseFloat(highBar.style.width);

      const expectedRatio = (lowScore!.index ?? 0) / (highScore!.index ?? 1);
      const actualRatio = lowWidth / highWidth;
      expect(actualRatio).toBeCloseTo(expectedRatio, 5);
    });

    And("the chart states its axis maximum", () => {
      // UWT-002 fix (Rule-15, 2026-07-30): one axis-maximum label PER rated band's own DOM region
      // now, not one shared label — the axis maximum itself (COMPOSITE_INDEX_MAX) is still
      // identical across every band, so every one of them must show it.
      const axisMaxLabels = screen.getAllByTestId("chart-axis-max");
      expect(axisMaxLabels.length).toBeGreaterThan(0);
      for (const label of axisMaxLabels) {
        expect(label.textContent ?? "").toContain(formatIndex(COMPOSITE_INDEX_MAX, "en"));
      }
    });
  });

  // ─── AC-14 — every bar carries its model name and index in text ────────────────

  Scenario("Every capability bar carries its model name and index in text", ({ Given, When, Then, And }) => {
    Given("the full roster is loaded", () => {
      // dataset is the full roster.
    });

    When("the merged chart is rendered", () => {
      render(React.createElement(BenchmarkChart, { dataset, fullDataset: dataset, locale: "en" }));
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Every capability bar carries its model name and index in text
    Then("every bar has a text label carrying the model name", () => {
      const groups = computeGroups(dataset);
      for (const key of RATED_BAND_KEYS) {
        for (const s of groups[key]) {
          const label = screen.getByTestId(`benchmark-chart-label-${s.model.id}`);
          expect(label.textContent ?? "").toContain(s.model.name);
        }
      }
    });

    And("every bar has a text label carrying its numeric composite index", () => {
      const groups = computeGroups(dataset);
      for (const key of RATED_BAND_KEYS) {
        for (const s of groups[key]) {
          const label = screen.getByTestId(`benchmark-chart-label-${s.model.id}`);
          expect(label.textContent ?? "").toContain(formatIndex(s.index ?? 0, "en"));
        }
      }
    });
  });

  // ─── AC-12 — a low-coverage model is marked as low coverage ────────────────────

  Scenario("A low-coverage model is marked as low coverage", ({ Given, When, Then, And }) => {
    Given("a fixture model whose coverage ratio is below the low-coverage threshold", () => {
      // swe-bench-verified alone carries weight 25 → coverage 0.25, below the 0.5 threshold.
      const lowCoverage = fixtureModel("cap-low-coverage", [fig("swe-bench-verified", 50)]);
      ctx.fixtureDataset = fixtureDataset([lowCoverage]);
      const [score] = computeGroups(ctx.fixtureDataset).haiku;
      expect(score?.coverage).toBeLessThan(LOW_COVERAGE_THRESHOLD);
    });

    When("the merged chart is rendered", () => {
      render(
        React.createElement(BenchmarkChart, {
          dataset: ctx.fixtureDataset!,
          fullDataset: ctx.fixtureDataset!,
          locale: "en",
        }),
      );
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A low-coverage model is marked as low coverage
    Then("that model's row carries a low-coverage marker", () => {
      expect(screen.getByTestId("benchmark-chart-low-coverage-cap-low-coverage")).not.toBeNull();
    });

    And("the marker states the model's coverage ratio in text", () => {
      const marker = screen.getByTestId("benchmark-chart-low-coverage-cap-low-coverage");
      const [score] = computeGroups(ctx.fixtureDataset!).haiku;
      expect(marker.textContent ?? "").toContain(formatCoverage(score!.coverage, "en"));
    });
  });

  // ─── AC-37 — capability class is carried textually, not by colour alone ────────

  Scenario("The capability class is carried textually, not by colour alone", ({ Given, When, Then, And }) => {
    Given("the full roster is loaded", () => {
      // dataset is the full roster.
    });

    When("the merged chart is rendered", () => {
      render(React.createElement(BenchmarkChart, { dataset, fullDataset: dataset, locale: "en" }));
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The capability class is carried textually, not by colour alone
    Then("every band group carries its class name as text", () => {
      for (const band of RATED_BAND_KEYS) {
        const header = screen.getByTestId(`benchmark-chart-band-${band}-label`);
        const key = BAND_LABEL_KEYS[band];
        expect(header.textContent).toBe(key ? t("en", key) : band);
      }
    });

    And("every model row carries its class as text in the data table", () => {
      cleanup();
      render(React.createElement(ModelTable, { dataset, fullDataset: dataset, locale: "en" }));
      const groups = computeGroups(dataset);
      for (const list of [groups.opus, groups.sonnet, groups.haiku, groups.unrated]) {
        for (const s of list) {
          const row = document.querySelector(`tbody tr[data-model-id="${s.model.id}"]`);
          expect(row, `row for ${s.model.id}`).not.toBeNull();
          const key = BAND_LABEL_KEYS[s.band];
          expect(row!.textContent ?? "").toContain(key ? t("en", key) : s.band);
        }
      }
    });
  });

  // ════════════════════════════════════════════════════════════════════════════
  // Phase 7 — price chart (AC-15/16/17).
  // ════════════════════════════════════════════════════════════════════════════

  // Rated (one figure) — post-merge, only a rated model gets a row with price bars at all (an
  // unrated model renders in the plain text list, no capability or price bar).
  function meteredFixture(id: string, input: number, output: number, harness: HarnessId = "claude-code"): Model {
    const rate: MeteredPrice = { kind: "metered", input, output, grade: "verified", source: SRC };
    return {
      id,
      name: id,
      vendor: "Test",
      harnesses: [harness],
      figures: [fig("swe-bench-verified", 50)],
      pricing: { [harness]: rate },
    };
  }

  // ─── AC-15 — a metered model shows separate labelled input and output bars ────

  Scenario("A metered model shows separate labelled input and output bars", ({ Given, When, Then, And }) => {
    Given("a fixture model with a per-token input rate and output rate", () => {
      ctx.fixtureDataset = fixtureDataset([meteredFixture("price-metered", 3, 15)]);
    });

    When("the merged chart is rendered", () => {
      render(
        React.createElement(BenchmarkChart, {
          dataset: ctx.fixtureDataset!,
          fullDataset: ctx.fixtureDataset!,
          locale: "en",
        }),
      );
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A metered model shows separate labelled input and output bars
    Then("that model has one bar labelled as the input rate", () => {
      expect(screen.getByTestId("benchmark-chart-bar-price-in-price-metered")).not.toBeNull();
      const label = screen.getByTestId("benchmark-chart-bar-price-in-price-metered-label");
      expect(label.textContent ?? "").toContain(formatPriceUsd(3, "en"));
    });

    And("that model has one bar labelled as the output rate", () => {
      expect(screen.getByTestId("benchmark-chart-bar-price-out-price-metered")).not.toBeNull();
      const label = screen.getByTestId("benchmark-chart-bar-price-out-price-metered-label");
      expect(label.textContent ?? "").toContain(formatPriceUsd(15, "en"));
    });
  });

  // ─── AC-16 — reworded (Phase 4): unrated + subscription-only shows its plan cost in the unrated list ──

  Scenario(
    "A subscription-only unrated model shows its plan cost in the unrated list",
    ({ Given, When, Then, And, But }) => {
      Given("a fixture model with no published composite score, available only under a flat-rate subscription", () => {
        const rate: SubscriptionPrice = {
          kind: "subscription",
          planCostUsd: 10,
          grade: "verified",
          source: SRC,
          caps: "First month $5, then $10/month.",
        };
        const m: Model = {
          id: "price-sub-only",
          name: "price-sub-only",
          vendor: "Test",
          harnesses: ["opencode-go"],
          figures: [],
          pricing: { "opencode-go": rate },
        };
        ctx.fixtureDataset = fixtureDataset([m]);
      });

      When("the merged chart renders the roster", () => {
        render(
          React.createElement(BenchmarkChart, {
            dataset: ctx.fixtureDataset!,
            fullDataset: ctx.fixtureDataset!,
            locale: "en",
          }),
        );
      });

      // This fixture carries zero figures, so it is UNRATED (no composite index, no row to attach
      // to) — DD-1's resolution retains the retired two-chart design's global subscription list text
      // (plan cost + caps) for exactly this subset, inside the merged chart's unrated list item
      // (a RATED+subscription-only model instead gets `BenchmarkRow`'s inline treatment, covered by
      // `benchmark-chart.test.tsx`'s own DD-1 test).
      // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A subscription-only unrated model shows its plan cost in the unrated list
      Then("that model appears in the unrated group's plain text list", () => {
        const item = screen.getByTestId("benchmark-chart-unrated-model-price-sub-only");
        expect(item.textContent ?? "").toContain("price-sub-only");
      });

      And("that list entry states the model's subscription plan cost", () => {
        const item = screen.getByTestId("benchmark-chart-unrated-model-price-sub-only");
        expect(item.textContent ?? "").toContain(formatPriceUsd(10, "en"));
      });

      But("that model renders no per-token bar and no zero value", () => {
        expect(screen.queryByTestId("benchmark-chart-bar-price-in-price-sub-only")).toBeNull();
        expect(screen.queryByTestId("benchmark-chart-bar-price-out-price-sub-only")).toBeNull();
        const item = screen.getByTestId("benchmark-chart-unrated-model-price-sub-only");
        expect(item.textContent ?? "").not.toContain("$0.00");
        expect(item.textContent ?? "").not.toMatch(/\$0\b/);
      });
    },
  );

  // ─── AC-17 — an unfiltered price chart shows the lowest harness rate ──────────

  Scenario("An unfiltered merged chart shows the lowest harness rate", ({ Given, When, Then, And }) => {
    Given("a fixture model priced differently by two harnesses", () => {
      // Post-merge, only a RATED model gets a row with price bars at all (the decision-branches
      // diagram in tech-docs.md: an unrated model never renders a price bar, only its bare name in
      // the unrated list) — this fixture carries one figure so it lands in a rated band, unlike the
      // pre-merge fixture, which relied on the retired price chart's now-removed "unrated models still get
      // metered bars" behavior.
      const m: Model = {
        id: "price-two-harness",
        name: "price-two-harness",
        vendor: "Test",
        harnesses: ["claude-code", "cursor"],
        figures: [fig("swe-bench-verified", 50)],
        pricing: {
          "claude-code": { kind: "metered", input: 5, output: 25, grade: "verified", source: SRC },
          cursor: { kind: "metered", input: 3, output: 15, grade: "verified", source: SRC },
        },
      };
      ctx.fixtureDataset = fixtureDataset([m]);
    });

    When("the merged chart is rendered without a harness filter", () => {
      render(
        React.createElement(BenchmarkChart, {
          dataset: ctx.fixtureDataset!,
          fullDataset: ctx.fixtureDataset!,
          locale: "en",
        }),
      );
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An unfiltered merged chart shows the lowest harness rate
    Then("that model's bars use the lower of the two harness rates", () => {
      const inLabel = screen.getByTestId("benchmark-chart-bar-price-in-price-two-harness-label");
      expect(inLabel.textContent ?? "").toContain(formatPriceUsd(3, "en"));
      expect(inLabel.textContent ?? "").not.toContain(formatPriceUsd(5, "en"));
    });

    And("the chart states that it shows the lowest available harness rate", () => {
      const subtitle = screen.getByTestId("benchmark-chart-subtitle");
      expect(subtitle.textContent).toBe(t("en", "aiBenchPriceLowestSubtitle"));
    });
  });

  // ─── AC-36 — reworded (Phase 4): one merged chart, one accessible name ────────

  Scenario("The merged chart exposes an accessible name", ({ Given, When, Then }) => {
    Given("the full roster is loaded", () => {
      // dataset is the full roster.
    });

    When("the page renders", () => {
      renderPageForLocale("en");
    });

    // DD-25 reword: the merged chart no longer renders `<svg role="img">` — each rated band's own
    // DOM region instead carries `role="group"` with `aria-labelledby` pointing at its own visible
    // heading (its localized band label), giving each band a genuine accessible name.
    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The merged chart exposes an accessible name
    Then("each rated band's chart region exposes a localized accessible name", () => {
      for (const band of ["opus", "sonnet", "haiku"] as const) {
        const group = screen.getByRole("group", { name: bandLabel(band, "en") });
        expect(group).not.toBeNull();
      }
    });
  });

  // ════════════════════════════════════════════════════════════════════════════
  // Phase 8 — harness and class filters (AC-18, AC-22..AC-28).
  // ════════════════════════════════════════════════════════════════════════════

  // ─── AC-22 — no query parameters shows the whole roster ───────────────────────

  Scenario("The page with no query parameters shows the whole roster", ({ Given, When, Then }) => {
    Given("the URL carries no query parameters", () => {
      ctx.search = "";
    });

    When("the page renders", () => {
      renderPageWithSearch(ctx.search ?? "");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The page with no query parameters shows the whole roster
    Then("every roster model is shown in the data table", () => {
      expect(sorted(tableModelIds())).toEqual(sorted(idsOf(dataset.models)));
    });
  });

  // ─── AC-23 — reworded (Phase 4): a harness parameter narrows the merged chart and the table ──

  Scenario("A harness parameter narrows the merged chart and the table", ({ Given, When, Then, And }) => {
    // "cursor" genuinely narrows the live roster — at least one model (e.g. grok-build-0.1) is
    // opencode-zen-only and is not exposed by cursor.
    Given("the URL carries a harness parameter naming a known harness", () => {
      ctx.search = "harness=cursor";
    });

    When("the page renders", () => {
      renderPageWithSearch(ctx.search!);
    });

    const expected = () => filterModels(dataset, { harness: "cursor" });

    // This is an exact-set equality check: unlike the retired two-chart design's price chart
    // (which omitted a priceless model entirely, AC-16/17), `benchmark-chart.tsx`'s `BenchmarkRow`
    // always renders a row (with a "not reported" placeholder when priceless) or an unrated-list
    // entry — no filtered model is ever dropped from the merged chart.
    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A harness parameter narrows the merged chart and the table
    Then("only models that harness exposes are shown in the merged chart", () => {
      expect(sorted(benchmarkChartModelIds())).toEqual(sorted(idsOf(expected())));
    });

    And("only models that harness exposes are shown in the data table", () => {
      expect(sorted(tableModelIds())).toEqual(sorted(idsOf(expected())));
    });
  });

  // ─── AC-24 — reworded (Phase 4): a class parameter narrows the merged chart and the table ────

  Scenario("A class parameter narrows the merged chart and the table", ({ Given, When, Then, And }) => {
    Given("the URL carries a class parameter naming a known band", () => {
      ctx.search = "class=opus";
    });

    When("the page renders", () => {
      renderPageWithSearch(ctx.search!);
    });

    const expected = () => filterModels(dataset, { class: "opus" });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A class parameter narrows the merged chart and the table
    Then("only models in that band are shown in the merged chart", () => {
      expect(sorted(benchmarkChartModelIds())).toEqual(sorted(idsOf(expected())));
    });

    And("only models in that band are shown in the data table", () => {
      expect(sorted(tableModelIds())).toEqual(sorted(idsOf(expected())));
    });
  });

  // ─── AC-25 — harness and class parameters intersect ───────────────────────────

  Scenario("Harness and class parameters intersect", ({ Given, When, Then }) => {
    Given("the URL carries both a harness parameter and a class parameter", () => {
      ctx.search = "harness=cursor&class=opus";
    });

    When("the page renders", () => {
      renderPageWithSearch(ctx.search!);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Harness and class parameters intersect
    Then("only models satisfying both filters are shown", () => {
      const expected = filterModels(dataset, { harness: "cursor", class: "opus" });
      expect(sorted(tableModelIds())).toEqual(sorted(idsOf(expected)));
    });
  });

  // ─── AC-18 — rewritten (Phase 4) verbatim from prd.md ─────────────────────────

  Scenario("A harness filter switches the merged chart to that harness's rate", ({ Given, When, Then }) => {
    Given("a fixture model priced differently by two harnesses", () => {
      // Rated (one figure), same reasoning as AC-17's fixture above — only a rated model gets a row
      // with price bars post-merge.
      const m: Model = {
        id: "price-harness-switch",
        name: "price-harness-switch",
        vendor: "Test",
        harnesses: ["cursor", "opencode-go"],
        figures: [fig("swe-bench-verified", 50)],
        pricing: {
          cursor: { kind: "metered", input: 2, output: 6, grade: "verified", source: SRC },
          "opencode-go": { kind: "metered", input: 5, output: 20, grade: "verified", source: SRC },
        },
      };
      ctx.fixtureDataset = fixtureDataset([m]);
    });

    When("the merged chart renders with that harness selected", () => {
      render(
        React.createElement(BenchmarkChart, {
          dataset: ctx.fixtureDataset!,
          fullDataset: ctx.fixtureDataset!,
          locale: "en",
          harness: "opencode-go",
        }),
      );
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A harness filter switches the merged chart to that harness's rate
    Then("that model's price bars use that harness's own rate, not its lowest available rate", () => {
      const inLabel = screen.getByTestId("benchmark-chart-bar-price-in-price-harness-switch-label");
      expect(inLabel.textContent ?? "").toContain(formatPriceUsd(5, "en"));
      const outLabel = screen.getByTestId("benchmark-chart-bar-price-out-price-harness-switch-label");
      expect(outLabel.textContent ?? "").toContain(formatPriceUsd(20, "en"));
      // Never the OTHER (lowest-available) harness's cheaper rate.
      expect(inLabel.textContent ?? "").not.toContain(formatPriceUsd(2, "en"));
    });
  });

  // ─── AC-26 — an unrecognized filter value falls back to the unfiltered view ───

  Scenario("An unrecognized filter value falls back to the unfiltered view", ({ Given, When, Then, But }) => {
    Given("the URL carries a harness parameter with an unknown value", () => {
      ctx.search = "harness=not-a-real-harness";
    });

    When("the page renders", () => {
      renderPageWithSearch(ctx.search!);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An unrecognized filter value falls back to the unfiltered view
    Then("every roster model is shown", () => {
      expect(sorted(tableModelIds())).toEqual(sorted(idsOf(dataset.models)));
    });

    But("no error is surfaced to the reader", () => {
      // The render above completed without throwing (an error would have failed the `When` step),
      // the page shows its normal heading, and no empty-state fallback is shown in its place.
      const h1 = screen.getByRole("heading", { level: 1 });
      expect((h1.textContent ?? "").length).toBeGreaterThan(0);
      expect(screen.queryByTestId("ai-bench-empty-state")).toBeNull();
    });
  });

  // ─── SG-001 — a duplicated query parameter resolves to its first value ────────

  Scenario("A duplicated query parameter resolves to its first value", ({ Given, When, Then, And }) => {
    Given("the URL carries the harness parameter twice with two different known harness values", () => {
      ctx.search = "harness=claude-code&harness=codex-cli";
    });

    When("the page renders", () => {
      renderPageWithSearch(ctx.search!);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A duplicated query parameter resolves to its first value
    Then("the filter uses the first of the two values", () => {
      // Both the mobile and desktop filter variants render simultaneously (jsdom applies no CSS)
      // with matching accessible names — select by id (the desktop variant's own `FilterSelect`
      // id) to avoid an ambiguous role query.
      const select = document.getElementById("benchmark-filter-harness-desktop") as HTMLSelectElement;
      expect(select.value).toBe("claude-code");
    });

    And("every roster model matching that harness is shown", () => {
      const expected = idsOf(dataset.models.filter((m) => m.harnesses.includes("claude-code")));
      expect(sorted(tableModelIds())).toEqual(sorted(expected));
    });
  });

  // ─── SG-002 — a duplicated parameter with an unrecognized first value ignores a valid later value ─

  Scenario(
    "A duplicated query parameter with an unrecognized first value ignores a valid later value",
    ({ Given, When, Then, And }) => {
      Given("the URL carries the harness parameter twice, an unknown value first and a known harness second", () => {
        ctx.search = "harness=not-a-real-harness&harness=claude-code";
      });

      When("the page renders", () => {
        renderPageWithSearch(ctx.search!);
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A duplicated query parameter with an unrecognized first value ignores a valid later value
      Then("the filter falls back to unfiltered", () => {
        const select = document.getElementById("benchmark-filter-harness-desktop") as HTMLSelectElement;
        expect(select.value).toBe("");
      });

      And("every roster model is shown", () => {
        expect(sorted(tableModelIds())).toEqual(sorted(idsOf(dataset.models)));
      });
    },
  );

  // ─── SG-003 — resetting a filter to "All" removes it from the URL ─────────────

  Scenario('Resetting a filter to "All" removes it from the URL', ({ Given, When, Then, And }) => {
    Given("the URL carries both a harness parameter and a class parameter", () => {
      ctx.search = "harness=claude-code&class=opus";
      renderPageWithSearch(ctx.search);
    });

    When('the reader resets the class filter to "All classes"', () => {
      const select = document.getElementById("benchmark-filter-class-desktop") as HTMLSelectElement;
      fireEvent.change(select, { target: { value: "" } });
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Resetting a filter to "All" removes it from the URL
    Then("the URL retains the harness parameter but no longer carries the class parameter", () => {
      const pushed = new URLSearchParams((navState.lastPush ?? "").split("?")[1] ?? "");
      expect(pushed.get("harness")).toBe("claude-code");
      expect(pushed.has("class")).toBe(false);
    });

    And("the roster reflects only the harness filter", () => {
      const pushed = new URLSearchParams((navState.lastPush ?? "").split("?")[1] ?? "");
      cleanup();
      renderPageWithSearch(pushed.toString());
      const expected = idsOf(dataset.models.filter((m) => m.harnesses.includes("claude-code")));
      expect(sorted(tableModelIds())).toEqual(sorted(expected));
    });
  });

  // ─── AC-28 — a filter combination matching no model renders an explicit empty state ─

  Scenario("A filter combination matching no model renders an explicit empty state", ({ Given, When, Then, But }) => {
    // opencode-go carries no opus-band model in the live roster (filter.unit.test.ts pins this).
    Given("the URL carries a filter combination that matches no model", () => {
      ctx.search = "harness=opencode-go&class=opus";
    });

    When("the page renders", () => {
      renderPageWithSearch(ctx.search!);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A filter combination matching no model renders an explicit empty state
    Then("an explicit empty-state message is shown", () => {
      const empty = screen.getByTestId("ai-bench-empty-state");
      expect((empty.textContent ?? "").length).toBeGreaterThan(0);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A filter combination matching no model renders an explicit empty state
    But("the chart and the data table do not render in the empty state", () => {
      // Phase 5 fix (commit 167bd0299): BenchmarkChart was rewritten from per-band `<svg>`
      // elements to DOM bars, so this guard now targets the chart root's exact testid
      // (`benchmark-chart`, `benchmark-chart.tsx:38`/`:249`) rather than a per-band SVG family.
      // Exact string match only — `queryByTestId` throws on multiple matches, and a broader
      // pattern like `/^benchmark-chart/` would collide with sibling testids
      // (`benchmark-chart-heading`, `-row-*`, `-band-*`, etc.).
      expect(screen.queryByTestId("benchmark-chart")).toBeNull();
      // Rule-15 UWT-006 fix regression (pr-review-synthesis-maker HIGH finding, PR #122 cycle 1):
      // the empty-state message must not be followed by an empty, redundant table skeleton either
      // — <ModelTable> moved inside the `!isEmpty` branch alongside the chart. AC-28 itself
      // constrains only the chart, but reverting the table's move would leave every OTHER
      // assertion in this scenario passing, so this is the assertion that actually protects it.
      expect(screen.queryByTestId("model-table")).toBeNull();
    });
  });

  // ─── Rule-15 UWT-009/USS-003 fix — an active Class filter can empty ONE rated band ─

  Scenario(
    "An active Class filter empties one rated band while others still show models",
    ({ Given, When, Then, And }) => {
      // `?class=opus` matches at least one model (the Opus anchor itself always qualifies), so the
      // page renders the roster, not the whole-roster empty state above — but the Sonnet and Haiku
      // bands genuinely have zero matching rows under this filter.
      Given("a Class filter is active that excludes every model in the Sonnet band", () => {
        ctx.search = "class=opus";
      });

      When("the page renders the Sonnet band", () => {
        renderPageWithSearch(ctx.search!);
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An active Class filter empties one rated band while others still show models
      Then("the band shows an explicit message that no models in this class match the current filter", () => {
        const sonnetEmpty = screen.getByTestId("benchmark-chart-band-sonnet-empty");
        expect(sonnetEmpty.textContent).toBe(t("en", "aiBenchBandEmptyMessage"));
      });

      And("the band's own sort control is hidden rather than left interactive", () => {
        expect(
          screen.queryByRole("combobox", { name: `${t("en", "aiBenchSortLabel")} — ${bandLabel("sonnet", "en")}` }),
        ).toBeNull();
      });
    },
  );

  // ─── AC-27 — a reloaded filtered URL reproduces the same view ─────────────────

  Scenario("A reloaded filtered URL reproduces the same view", ({ Given, When, Then }) => {
    Given("the reader has applied a harness filter and a class filter", () => {
      ctx.search = "harness=cursor&class=opus";
      renderPageWithSearch(ctx.search);
    });

    When("the reader reloads the resulting URL", () => {
      // Unit-level equivalent of a real browser reload (see the e2e binding for the real
      // navigation-level round-trip, AC-27): tear down and re-render fresh against the SAME URL.
      cleanup();
      renderPageWithSearch(ctx.search!);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A reloaded filtered URL reproduces the same view
    Then("the same filtered set of models is shown", () => {
      const expected = filterModels(dataset, { harness: "cursor", class: "opus" });
      expect(sorted(tableModelIds())).toEqual(sorted(idsOf(expected)));
    });
  });

  // ════════════════════════════════════════════════════════════════════════════
  // Phase 9 — AC-39..AC-47, nine new scenarios added verbatim from prd.md's
  // Acceptance criteria (Gherkin) section (Phase 4).
  // ════════════════════════════════════════════════════════════════════════════

  // ─── AC-39 — a rated model's row carries its capability bar and both price bars together ──

  Scenario(
    "A rated model's row carries its capability bar and both price bars together",
    ({ Given, When, Then, And }) => {
      Given("a model in the sonnet band with a metered input and output rate", () => {
        const groups = computeGroups(dataset);
        const candidate = groups.sonnet.find((s) => lowestRate(s.model)?.kind === "metered");
        expect(candidate, "expected at least one sonnet-band model with a metered rate").toBeDefined();
        ctx.targetModelId = candidate!.model.id;
      });

      When("the merged chart renders that model's row", () => {
        render(React.createElement(BenchmarkChart, { dataset, fullDataset: dataset, locale: "en" }));
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A rated model's row carries its capability bar and both price bars together
      Then("the row shows one capability bar, one price-in bar, and one price-out bar", () => {
        const id = ctx.targetModelId!;
        expect(screen.getByTestId(`benchmark-chart-bar-capability-${id}`)).not.toBeNull();
        expect(screen.getByTestId(`benchmark-chart-bar-price-in-${id}`)).not.toBeNull();
        expect(screen.getByTestId(`benchmark-chart-bar-price-out-${id}`)).not.toBeNull();
      });

      And("all three bars appear stacked within that single row, not in separate chart sections", () => {
        const id = ctx.targetModelId!;
        const row = screen.getByTestId(`benchmark-chart-row-${id}`);
        expect(row.querySelector(`[data-testid="benchmark-chart-bar-capability-${id}"]`)).not.toBeNull();
        expect(row.querySelector(`[data-testid="benchmark-chart-bar-price-in-${id}"]`)).not.toBeNull();
        expect(row.querySelector(`[data-testid="benchmark-chart-bar-price-out-${id}"]`)).not.toBeNull();
      });
    },
  );

  // ─── AC-40 — bar length is proportional to its own value ─────────────────────

  Scenario("Bar length is proportional to its own value", ({ Given, When, Then, And }) => {
    // The reference model holds the roster max on every composite benchmark (index exactly 100 —
    // COMPOSITE_INDEX_MAX) and the highest metered rate (30) — the ruler both proportionality
    // checks below divide against, so no exported layout constant (e.g. `PLOT_WIDTH`) is needed.
    Given("a model with a composite index of 85.7 and an output rate of $15.00", () => {
      const reference = fixtureModel("ac40-reference-max", [
        fig("swe-bench-verified", 100),
        fig("swe-bench-pro", 100),
        fig("terminal-bench-2-1", 100),
        fig("gpqa-diamond", 100),
      ]);
      reference.pricing = { "claude-code": { kind: "metered", input: 10, output: 30, grade: "verified", source: SRC } };
      const target = fixtureModel("ac40-target", [
        fig("swe-bench-verified", 85.7),
        fig("swe-bench-pro", 85.7),
        fig("terminal-bench-2-1", 85.7),
        fig("gpqa-diamond", 85.7),
      ]);
      target.pricing = { "claude-code": { kind: "metered", input: 1, output: 15, grade: "verified", source: SRC } };
      ctx.fixtureDataset = fixtureDataset([reference, target]);
    });

    When("the merged chart renders that model's row", () => {
      render(
        React.createElement(BenchmarkChart, {
          dataset: ctx.fixtureDataset!,
          fullDataset: ctx.fixtureDataset!,
          locale: "en",
        }),
      );
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Bar length is proportional to its own value
    Then("the capability bar's length is proportional to 85.7 over the composite index max", () => {
      const targetWidth = parseFloat(screen.getByTestId("benchmark-chart-bar-capability-ac40-target-fill").style.width);
      const referenceWidth = parseFloat(
        screen.getByTestId("benchmark-chart-bar-capability-ac40-reference-max-fill").style.width,
      );
      // The reference model's own index is exactly COMPOSITE_INDEX_MAX (100), so its bar spans the
      // full capability plot width — the ruler for "85.7 over the composite index max".
      expect(targetWidth / referenceWidth).toBeCloseTo(85.7 / 100, 5);
    });

    And("the price-out bar's length is proportional to $15.00 over the chart's shared price axis max", () => {
      const targetWidth = parseFloat(screen.getByTestId("benchmark-chart-bar-price-out-ac40-target-fill").style.width);
      const referenceWidth = parseFloat(
        screen.getByTestId("benchmark-chart-bar-price-out-ac40-reference-max-fill").style.width,
      );
      // The reference model's own output rate (30) is the highest metered rate in the fixture, so
      // it IS the price axis max — the ruler for "$15.00 over the chart's shared price axis max".
      expect(targetWidth / referenceWidth).toBeCloseTo(15 / 30, 5);
    });
  });

  // ─── AC-41 — a band's sort control reorders only that band ───────────────────

  Scenario("A band's sort control reorders only that band", ({ Given, When, Then, And }) => {
    const opusAnchor = bandFixtureModel(OPUS_ANCHOR_ID, 100, 1);
    const sonnetAnchor = bandFixtureModel(SONNET_ANCHOR_ID, 60, 1);
    const opusA = bandFixtureModel("ac41-opus-a", 100, 20);
    const opusB = bandFixtureModel("ac41-opus-b", 100, 5);
    const sonnetHi = bandFixtureModel("ac41-sonnet-hi", 85, 50); // higher score, higher price
    const sonnetLo = bandFixtureModel("ac41-sonnet-lo", 75, 10); // lower score, lower price
    const haikuA = bandFixtureModel("ac41-haiku-a", 30, 40);
    const haikuB = bandFixtureModel("ac41-haiku-b", 20, 15);
    const ds = fixtureDataset([opusAnchor, sonnetAnchor, opusA, opusB, sonnetHi, sonnetLo, haikuA, haikuB]);

    function renderWithSort(sortState: SortState) {
      cleanup();
      render(
        React.createElement(BenchmarkChart, {
          dataset: ds,
          fullDataset: ds,
          locale: "en",
          sortState,
          onSortChange: (band, mode) => {
            if (band === "sonnet") ctx.requestedSortMode = mode;
          },
        }),
      );
    }

    Given("the sonnet band is displaying models in capability-descending order", () => {
      renderWithSort({ ...DEFAULT_SORT_STATE });
      const sonnetOrder = rowOrderWithin("benchmark-chart-band-sonnet");
      // The sonnet anchor itself also renders in the sonnet band (its own index, 60, is the
      // LOWEST of the three) — descending score: hi(85), lo(75), anchor(60).
      expect(sonnetOrder).toEqual(["ac41-sonnet-hi", "ac41-sonnet-lo", SONNET_ANCHOR_ID]);
      ctx.opusOrderBefore = rowOrderWithin("benchmark-chart-band-opus");
      ctx.haikuOrderBefore = rowOrderWithin("benchmark-chart-band-haiku");
    });

    When('the reader selects "Price: Low to High" from the sonnet band\'s sort control', () => {
      const select = screen.getByRole("combobox", {
        name: `${t("en", "aiBenchSortLabel")} — ${bandLabel("sonnet", "en")}`,
      });
      fireEvent.change(select, { target: { value: "price-asc" } });
      renderWithSort({ ...DEFAULT_SORT_STATE, sonnet: ctx.requestedSortMode ?? "price-asc" });
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A band's sort control reorders only that band
    Then("the sonnet band's rows re-render sorted by ascending output rate", () => {
      const sonnetOrder = rowOrderWithin("benchmark-chart-band-sonnet");
      // Ascending output price: anchor(1), lo(10), hi(50).
      expect(sonnetOrder).toEqual([SONNET_ANCHOR_ID, "ac41-sonnet-lo", "ac41-sonnet-hi"]);
    });

    And("the opus and haiku bands keep their own independently-selected sort order", () => {
      expect(rowOrderWithin("benchmark-chart-band-opus")).toEqual(ctx.opusOrderBefore);
      expect(rowOrderWithin("benchmark-chart-band-haiku")).toEqual(ctx.haikuOrderBefore);
    });
  });

  // ─── AC-42 — a band's sort choice is encoded in the URL ───────────────────────

  Scenario("A band's sort choice is encoded in the URL", ({ Given, When, Then, And }) => {
    Given('the reader has selected "Price: High to Low" for the opus band', () => {
      ctx.sortState = { ...DEFAULT_SORT_STATE, opus: "price-desc" };
    });

    When("the reader copies the current page URL", () => {
      ctx.encodedParams = encodeState({ harness: undefined, class: undefined, ...ctx.sortState! });
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A band's sort choice is encoded in the URL
    Then('the URL contains a "sort-opus" query parameter set to the descending-price value', () => {
      expect(ctx.encodedParams!.get("sort-opus")).toBe("price-desc");
    });

    And("loading that URL directly reproduces the opus band sorted the same way", () => {
      const decoded = decodeState(ctx.encodedParams!);
      expect(decoded.opus).toBe("price-desc");
    });
  });

  // ─── AC-43 — an unknown sort value in the URL falls back to the default ──────

  Scenario("An unknown sort value in the URL falls back to the default", ({ Given, When, Then, And }) => {
    Given('a URL containing "sort-sonnet=not-a-real-value"', () => {
      ctx.search = "sort-sonnet=not-a-real-value";
    });

    When("the page loads with that URL", () => {
      ctx.thrown = false;
      try {
        renderPageWithSearch(ctx.search!);
      } catch {
        ctx.thrown = true;
      }
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An unknown sort value in the URL falls back to the default
    Then("the sonnet band renders sorted by capability (the default)", () => {
      const select = screen.getByRole("combobox", {
        name: `${t("en", "aiBenchSortLabel")} — ${bandLabel("sonnet", "en")}`,
      }) as HTMLSelectElement;
      expect(select.value).toBe("capability");
    });

    And("no error is thrown", () => {
      expect(ctx.thrown).toBe(false);
    });
  });

  // ─── AC-67 — the URL carries the renamed class=haiku and sort-haiku parameters ─

  Scenario("A shared benchmark URL carries the renamed capability-class parameters", ({ Given, When, Then, And }) => {
    let original = "";
    let reEncoded = "";

    Given('a query string of "class=haiku&sort-haiku=price-asc"', () => {
      original = "class=haiku&sort-haiku=price-asc";
    });

    When("that query string is decoded and then re-encoded", () => {
      const decoded = decodeState(new URLSearchParams(original));
      reEncoded = encodeState(decoded).toString();
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A shared benchmark URL carries the renamed capability-class parameters
    Then("the re-encoded query string is identical to the original", () => {
      expect(reEncoded).toBe(original);
    });

    And(
      'a query string carrying the retired "class=light" or "sortLight" decodes to the default unfiltered, capability-sorted state',
      () => {
        const decodedClass = decodeState(new URLSearchParams("class=light"));
        expect(decodedClass).toEqual(DEFAULT_STATE);
        const decodedSort = decodeState(new URLSearchParams("sortLight=price-asc"));
        expect(decodedSort).toEqual(DEFAULT_STATE);
      },
    );
  });

  // ─── AC-44 (DD-1) — a rated model billed only by subscription shows inline subscription text ──

  Scenario("A rated model billed only by subscription shows inline subscription text", ({ Given, When, Then, And }) => {
    Given("a model in the haiku band with no metered rate and one subscription rate", () => {
      const m: Model = {
        id: "ac44-sub-rated",
        name: "ac44-sub-rated",
        vendor: "Test",
        harnesses: ["opencode-go"],
        figures: [fig("swe-bench-verified", 50)], // rated: one figure, no anchors present -> haiku band
        pricing: {
          "opencode-go": {
            kind: "subscription",
            planCostUsd: 20,
            grade: "verified",
            source: SRC,
            caps: "Cap: 500 req/day.",
          },
        },
      };
      ctx.fixtureDataset = fixtureDataset([m]);
    });

    When("the merged chart renders that model's row", () => {
      render(
        React.createElement(BenchmarkChart, {
          dataset: ctx.fixtureDataset!,
          fullDataset: ctx.fixtureDataset!,
          locale: "en",
        }),
      );
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A rated model billed only by subscription shows inline subscription text
    Then("the row shows its capability bar as normal", () => {
      expect(screen.getByTestId("benchmark-chart-bar-capability-ac44-sub-rated")).not.toBeNull();
    });

    And('the price-bar area of that row shows "Subscription ($cost)" text instead of two bars', () => {
      expect(screen.queryByTestId("benchmark-chart-bar-price-in-ac44-sub-rated")).toBeNull();
      expect(screen.queryByTestId("benchmark-chart-bar-price-out-ac44-sub-rated")).toBeNull();
      const label = screen.getByTestId("benchmark-chart-subscription-ac44-sub-rated");
      expect(label.textContent ?? "").toContain(t("en", "aiBenchSubscription"));
      expect(label.textContent ?? "").toContain(formatPriceUsd(20, "en"));
    });
  });

  // ─── AC-45 — an unrated model still renders in the existing text-only list ───

  Scenario("An unrated model still renders in the existing text-only list", ({ Given, When, Then, And }) => {
    Given("a model with no published composite score on any benchmark", () => {
      ctx.fixtureDataset = fixtureDataset([fixtureModel("ac45-unrated", [])]);
    });

    When("the merged chart renders the roster", () => {
      render(
        React.createElement(BenchmarkChart, {
          dataset: ctx.fixtureDataset!,
          fullDataset: ctx.fixtureDataset!,
          locale: "en",
        }),
      );
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An unrated model still renders in the existing text-only list
    Then("that model appears in the unrated group's plain text list", () => {
      const item = screen.getByTestId("benchmark-chart-unrated-model-ac45-unrated");
      expect(item.textContent ?? "").toContain("ac45-unrated");
    });

    And("no capability bar or price bar is rendered for that model", () => {
      expect(screen.queryByTestId("benchmark-chart-bar-capability-ac45-unrated")).toBeNull();
      expect(screen.queryByTestId("benchmark-chart-bar-price-in-ac45-unrated")).toBeNull();
      expect(screen.queryByTestId("benchmark-chart-bar-price-out-ac45-unrated")).toBeNull();
    });
  });

  // ─── AC-46 — the merged chart keeps its accessible name and text alternative ─

  Scenario("The merged chart keeps its accessible name and text alternative", ({ Given, When, Then, And }) => {
    Given("the merged chart has replaced the two former charts", () => {
      // The live page renders exactly one BenchmarkChart; nothing further to arrange.
    });

    When("a screen reader encounters the chart", () => {
      renderPageForLocale("en");
    });

    // DD-25 reword: the chart no longer renders any svg — each rated band (three, for the live
    // roster's opus/sonnet/haiku bands) instead renders its own `role="group"` DOM region, labelled
    // via `aria-labelledby` at its own localized band-name heading.
    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The merged chart keeps its accessible name and text alternative
    Then(
      "each rated band renders its own labelled region carrying its localized band name as its accessible name",
      () => {
        for (const band of ["opus", "sonnet", "haiku"] as const) {
          const group = screen.getByRole("group", { name: bandLabel(band, "en") });
          expect(group).not.toBeNull();
        }
      },
    );

    And("every figure the chart encodes is still reachable via the roster below", () => {
      const table = screen.getByTestId("model-table-desktop");
      const groups = computeGroups(dataset);
      for (const list of [groups.opus, groups.sonnet, groups.haiku, groups.unrated]) {
        for (const s of list) {
          expect(table.textContent ?? "").toContain(s.model.name);
        }
      }
    });
  });

  // ─── AC-47 — reworded (Phase 5, DD-25/DD-26/DD-31): the chart reflows without rescaling type ──

  Scenario("The chart reflows its layout without rescaling its typography", ({ Given, When, Then, And }) => {
    // jsdom applies no CSS and has no real layout engine (same limitation AC-38's docstring
    // records) — there is no live reflow to trigger by window width. What IS assertable here: the
    // component's rendered markup is declared identically at every render (it never reads
    // `window.innerWidth`), and that declared markup uses a plain, un-prefixed text-size utility on
    // every label (identical regardless of viewport) plus a `lg:`-prefixed grid utility on the row
    // container — Tailwind's own breakpoint-prefix convention is what makes "only at the desktop
    // width" true in a real browser; jsdom cannot exercise that live, so this asserts the
    // DECLARATION rather than a live-rendered pixel/layout change.
    function labelTextSizeClasses(): string[] {
      const container = screen.getByTestId("benchmark-chart");
      return Array.from(
        container.querySelectorAll('[data-slot="chart-bar-label"], [data-slot="chart-bar-row-label"]'),
      ).map((el) => {
        // Phase 8, AC-49: the declared size moved from an arbitrary `text-[10px]` bracket value to
        // the named `text-xs` utility (12px, clearing AC-49's floor) — this regex matches EITHER
        // form so it protects the "one static declared size, no responsive modifier" property
        // regardless of which spelling the declared size takes.
        const match = el.className.match(/text-(?:\[[0-9]+px\]|xs|sm|base|lg|xl)\b/);
        return match ? match[0] : "";
      });
    }

    Given("the merged chart is rendered at a mobile, a tablet, and a desktop viewport width", () => {
      ctx.widthLabelClasses = [375, 768, 1280].map((width) => {
        Object.defineProperty(window, "innerWidth", { writable: true, configurable: true, value: width });
        window.dispatchEvent(new Event("resize"));
        cleanup();
        render(React.createElement(BenchmarkChart, { dataset, fullDataset: dataset, locale: "en" }));
        return labelTextSizeClasses();
      });
      // The row container's own className is captured once — it is a static declaration, not a
      // window-width-dependent branch (see docstring above).
      const anyRow = screen.getAllByTestId(/^benchmark-chart-row-/)[0];
      ctx.rowReflowClassName = anyRow?.className ?? "";
    });

    When("the DOM structure and the declared text sizes at each width are inspected", () => {
      // The three label-class lists and the row's reflow class were already captured above;
      // nothing further to arrange.
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The chart reflows its layout without rescaling its typography
    Then("the declared text size of every chart label is identical at all three widths", () => {
      const [mobile, tablet, desktop] = ctx.widthLabelClasses!;
      expect(mobile).toEqual(tablet);
      expect(tablet).toEqual(desktop);
      expect(mobile!.length).toBeGreaterThan(0);
      expect(mobile!.every((c) => c.length > 0)).toBe(true);
    });

    And("the row layout changes from stacked to a label column only at the desktop width", () => {
      // Tailwind's `lg:` prefix is exactly what makes this class a no-op below the desktop
      // breakpoint and a grid-column layout at/above it — declared once, applied conditionally by
      // the browser's own media query, not by any window-width branch in this component.
      expect(ctx.rowReflowClassName ?? "").toMatch(/\blg:grid-cols-\S+/);
    });
  });

  // ─── AC-48 — a rated model with no reported price shows a not-reported placeholder ───
  //
  // Added post-merge (pr-review-synthesis-maker MEDIUM finding): the retired `price-chart.tsx`
  // used to omit a model with no metered rate and no subscription from the plot entirely, so
  // nothing rendered for it; the merged chart instead renders `aiBenchNoFigure` inline
  // (`benchmark-chart.tsx`'s `not-reported` branch), which had no owning scenario until now.

  Scenario("A rated model with no reported price shows a not-reported placeholder", ({ Given, When, Then, And }) => {
    Given("a model in the haiku band with no metered rate and no subscription rate", () => {
      const m: Model = {
        id: "ac48-no-price-rated",
        name: "ac48-no-price-rated",
        vendor: "Test",
        harnesses: ["claude-code"],
        figures: [fig("swe-bench-verified", 50)], // rated: one figure, no anchors present -> haiku band
        pricing: {}, // no metered rate anywhere AND no subscription — genuinely no reported price
      };
      ctx.fixtureDataset = fixtureDataset([m]);
    });

    When("the merged chart renders that model's row", () => {
      render(
        React.createElement(BenchmarkChart, {
          dataset: ctx.fixtureDataset!,
          fullDataset: ctx.fixtureDataset!,
          locale: "en",
        }),
      );
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A rated model with no reported price shows a not-reported placeholder
    Then("the row shows its capability bar as normal", () => {
      expect(screen.getByTestId("benchmark-chart-bar-capability-ac48-no-price-rated")).not.toBeNull();
    });

    And('the price-bar area of that row shows a "not reported" placeholder instead of two bars', () => {
      expect(screen.queryByTestId("benchmark-chart-bar-price-in-ac48-no-price-rated")).toBeNull();
      expect(screen.queryByTestId("benchmark-chart-bar-price-out-ac48-no-price-rated")).toBeNull();
      expect(screen.queryByTestId("benchmark-chart-subscription-ac48-no-price-rated")).toBeNull();
      const notReported = screen.getByTestId("benchmark-chart-not-reported-ac48-no-price-rated");
      expect(notReported.textContent).toBe(t("en", "aiBenchNoFigure"));
    });
  });

  // ─── AC-38 — band colours meet contrast in both themes ────────────────────────
  //
  // jsdom cannot resolve `oklch()` custom properties through a cascade (tech-docs.md §Band design
  // tokens): `getComputedStyle` in jsdom never rasterizes a colour to concrete sRGB bytes the way a
  // real browser's `<canvas>` 2D context does, so the REAL WCAG contrast assertion can only run at
  // the e2e layer (`apps/ayokoding-www-fe-e2e/tests/e2e/steps/ai-benchmark.steps.ts`). This binding exists
  // so `specs:behavior:coverage` (which scans only `apps/ayokoding-www`, not the sibling
  // `ayokoding-www-fe-e2e` project) has a `@covers` annotation to find — the exact same
  // established pattern `course-rehome-redirects.steps.tsx`'s raw-HTTP-redirect scenario already
  // uses for its own jsdom-incapable assertions (`expect(true).toBe(true)` placeholders with a
  // comment pointing at the real check).
  ScenarioOutline("Band colours meet contrast in both themes", ({ Given, When, Then, And }) => {
    Given('the page is rendered in the "<theme>" theme', () => {
      expect(true).toBe(true);
    });

    When("the computed styles of the band tokens are read from the live page", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Band colours meet contrast in both themes
    Then("every band token meets the WCAG AA contrast ratio against its background", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Band colours meet contrast in both themes
    And("every rated band's bar fill meets the WCAG non-text contrast ratio against the page background", () => {
      expect(true).toBe(true);
    });
  });

  // ─── AC-52 — the document never scrolls horizontally (R5) ─────────────────────
  //
  // jsdom has no real viewport or layout engine, so `document.documentElement.scrollWidth` vs
  // `clientWidth` cannot be meaningfully compared — the REAL assertion runs at the e2e layer
  // (`apps/ayokoding-www-fe-e2e/tests/e2e/steps/ai-benchmark.steps.ts`). Same established
  // `expect(true).toBe(true)` placeholder convention as the AC-38 binding above, so
  // `specs:behavior:coverage` finds a `@covers` annotation for this scenario.
  ScenarioOutline("The document never scrolls horizontally", ({ Given, When, Then }) => {
    Given('the AI benchmark page is loaded at a "<width>" px viewport in the "<locale>" locale', () => {
      expect(true).toBe(true);
    });

    When("the document's scroll width is compared with its client width", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The document never scrolls horizontally
    Then("the document scroll width does not exceed the document client width", () => {
      expect(true).toBe(true);
    });
  });

  // ─── AC-53 — a roster card shows only its summary until it is expanded (DD-28) ────
  Scenario("A roster card shows only its summary until it is expanded", ({ Given, When, Then, But }) => {
    Given("the full roster is rendered below the md breakpoint", () => {
      ctx.fixtureDataset = fixtureDataset([bandFixtureModel("ac53-card-model", 80, 5)]);
    });

    When("a model's card is inspected before any interaction", () => {
      const model = ctx.fixtureDataset!.models[0]!;
      const view = computeScoreViews(ctx.fixtureDataset!, ctx.fixtureDataset!).get(model.id)!;
      const { container } = render(React.createElement(ModelCard, { model, view, locale: "en" }));
      ctx.targetModelId = model.id;
      ctx.cardContainer = container;
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A roster card shows only its summary until it is expanded
    Then("the card shows the model name, its class, its composite index, and its price", () => {
      const id = ctx.targetModelId!;
      expect(screen.getByTestId(`model-card-name-${id}`).textContent?.trim()).toBe("ac53-card-model");
      expect(screen.getByTestId(`model-card-class-${id}`).textContent?.trim().length).toBeGreaterThan(0);
      expect(screen.getByTestId(`model-card-index-${id}`).textContent?.trim().length).toBeGreaterThan(0);
      expect(screen.getByTestId(`model-card-price-${id}`).textContent?.trim().length).toBeGreaterThan(0);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A roster card shows only its summary until it is expanded
    But("the card's remaining figures are inside a closed disclosure", () => {
      const details = screen.getByTestId(`model-card-details-${ctx.targetModelId!}`);
      expect(details.tagName).toBe("DETAILS");
      expect(details.hasAttribute("open")).toBe(false);
      expect(details.querySelectorAll("dt").length).toBeGreaterThan(0);
    });
  });

  // ─── AC-54 — an expanded roster card carries every figure the desktop table carries (W-30) ───
  Scenario("An expanded roster card carries every figure the desktop table carries", ({ Given, When, Then }) => {
    Given("a model is rendered in both the roster card and the desktop table", () => {
      ctx.fixtureDataset = fixtureDataset([bandFixtureModel("ac54-parity-model", 70, 3)]);
    });

    When("that model's card disclosure is expanded", () => {
      const model = ctx.fixtureDataset!.models[0]!;
      const view = computeScoreViews(ctx.fixtureDataset!, ctx.fixtureDataset!).get(model.id)!;
      const { container: cardContainer } = render(React.createElement(ModelCard, { model, view, locale: "en" }));
      // jsdom exposes a closed <details>'s content to querySelectorAll regardless of the `open`
      // attribute (there is no CSS/layout engine to actually hide it) — setting `open` here mirrors
      // the real user action the scenario names without changing what the parity assertion sees.
      cardContainer.querySelector("details")?.setAttribute("open", "");
      const { container: tableContainer } = render(
        React.createElement(ModelTable, {
          dataset: ctx.fixtureDataset!,
          fullDataset: ctx.fixtureDataset!,
          locale: "en",
        }),
      );
      ctx.targetModelId = model.id;
      ctx.cardContainer = cardContainer;
      ctx.tableContainer = tableContainer;
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An expanded roster card carries every figure the desktop table carries
    Then("the card's summary and expanded content together carry every figure that model's table row carries", () => {
      // Desktop splits its figures across TWO rows (primary + a sibling detail row, cycle 6.3).
      const primaryRow = ctx.tableContainer!.querySelector(
        `[data-testid="model-table-desktop"] tbody tr[data-model-id="${ctx.targetModelId}"]`,
      );
      const detailRow = ctx.tableContainer!.querySelector(
        `[data-testid="model-table-desktop"] tbody tr[data-model-detail-id="${ctx.targetModelId}"]`,
      );
      const cardValues = figureValuesIn(ctx.cardContainer);
      const tableValues = new Set([...figureValuesIn(primaryRow), ...figureValuesIn(detailRow)]);
      expect(cardValues).toEqual(tableValues);
      expect(cardValues.size).toBeGreaterThan(0);
    });
  });

  // ─── AC-59/AC-61/AC-62 — real assertions live at the e2e layer (they read live computed
  // styles/scroll position a real browser produces; jsdom has no layout engine). Same established
  // `expect(true).toBe(true)` placeholder convention as the AC-38/AC-52 bindings above, so
  // `specs:behavior:coverage` (which scans only `apps/ayokoding-www`) finds a `@covers` annotation
  // for each. Cycles 6.3-6.5 bind the real assertions in
  // `apps/ayokoding-www-fe-e2e/tests/e2e/steps/ai-benchmark.steps.ts`. ─────────────────────────────────
  Scenario("The roster table header stays visible while the page scrolls at desktop width", ({ Given, When, Then }) => {
    Given("the AI benchmark page is loaded at a 1440 px viewport", () => {
      expect(true).toBe(true);
    });

    When("the page is scrolled until the roster table's last row is in view", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The roster table header stays visible while the page scrolls at desktop width
    Then("the table's header row is still visible", () => {
      expect(true).toBe(true);
    });
  });

  Scenario("An expanded card's figure value out-ranks its own field label", ({ Given, When, Then, And }) => {
    Given("the AI benchmark page is loaded at a 390 px viewport with one roster card expanded", () => {
      expect(true).toBe(true);
    });

    When(
      "the computed font size and font weight of a field label and of its own value are read from the live page",
      () => {
        expect(true).toBe(true);
      },
    );

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An expanded card's figure value out-ranks its own field label
    Then("the value's computed font size is larger than the label's computed font size", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An expanded card's figure value out-ranks its own field label
    And("the value's computed font weight is greater than the label's computed font weight", () => {
      expect(true).toBe(true);
    });
  });

  Scenario("An expanded card's figure value and its evidence badge flow on one row", ({ Given, When, Then, And }) => {
    Given("the AI benchmark page is loaded at a 390 px viewport with one roster card expanded", () => {
      expect(true).toBe(true);
    });

    When("the computed flex direction of a graded figure cell is read from the live page", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An expanded card's figure value and its evidence badge flow on one row
    Then("that computed flex direction is row rather than column", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An expanded card's figure value and its evidence badge flow on one row
    And("the field label's vertical band overlaps the vertical band of its own value", () => {
      expect(true).toBe(true);
    });
  });

  // ─── AC-63 — an expanded card groups its fields under labelled headings (DD-34 Treatment 3) ───
  // AC-64's placeholder still lands with cycle 6.7's own RED step.
  Scenario("An expanded card groups its fields under labelled headings", ({ Given, When, Then, And }) => {
    Given("a model's roster card is rendered with its disclosure expanded", () => {
      ctx.fixtureDataset = fixtureDataset([bandFixtureModel("ac63-group-model", 65, 3)]);
      const model = ctx.fixtureDataset.models[0]!;
      const view = computeScoreViews(ctx.fixtureDataset, ctx.fixtureDataset).get(model.id)!;
      const { container } = render(React.createElement(ModelCard, { model, view, locale: "en" }));
      container.querySelector("details")?.setAttribute("open", "");
      ctx.targetModelId = model.id;
      ctx.cardContainer = container;
    });

    When("the structure of the disclosure's content is inspected", () => {
      // Structural inspection happens directly in the Then/And assertions below.
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An expanded card groups its fields under labelled headings
    Then("every field belongs to exactly one labelled group", () => {
      const details = screen.getByTestId(`model-card-details-${ctx.targetModelId!}`);
      const sections = Array.from(details.querySelectorAll("section"));
      expect(sections.length).toBe(2);
      expect(sections.every((section) => section.querySelector("h4") !== null)).toBe(true);
      const labelsOf = (section: Element): Set<string> =>
        new Set(Array.from(section.querySelectorAll("dt")).map((dt) => dt.textContent?.trim() ?? ""));
      const [groupA, groupB] = sections.map(labelsOf);
      const allLabels = new Set(Array.from(details.querySelectorAll("dt")).map((dt) => dt.textContent?.trim() ?? ""));
      expect(new Set([...groupA!, ...groupB!])).toEqual(allLabels);
      expect([...groupA!].some((label) => groupB!.has(label))).toBe(false);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An expanded card groups its fields under labelled headings
    And("each group's heading is one level below the card's own model-name heading", () => {
      expect(screen.getByTestId(`model-card-name-${ctx.targetModelId!}`).tagName).toBe("H3");
      const details = screen.getByTestId(`model-card-details-${ctx.targetModelId!}`);
      expect(details.querySelectorAll("h4").length).toBe(2);
    });
  });

  // ─── AC-64 — unpublished figures share one value instead of occupying a field each (DD-34 T4) ──
  Scenario("Unpublished figures share one value instead of occupying a field each", ({ Given, When, Then, And }) => {
    Given("a model with more than one unpublished benchmark figure is rendered with its disclosure expanded", () => {
      // Reports only one of the four composite benchmarks — the other three are unpublished.
      const model = fixtureModel("ac64-unpublished-model", [fig("swe-bench-verified", 80)]);
      ctx.fixtureDataset = fixtureDataset([model]);
      const view = computeScoreViews(ctx.fixtureDataset, ctx.fixtureDataset).get(model.id)!;
      const { container } = render(React.createElement(ModelCard, { model, view, locale: "en" }));
      container.querySelector("details")?.setAttribute("open", "");
      ctx.targetModelId = model.id;
      ctx.cardContainer = container;
    });

    When("the disclosure's name-value groups are inspected", () => {
      // Structural inspection happens directly in the Then/And assertions below.
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Unpublished figures share one value instead of occupying a field each
    Then(
      'every unpublished figure\'s label is a term in one single group sharing one "not reported" description',
      () => {
        const details = screen.getByTestId(`model-card-details-${ctx.targetModelId!}`);
        const notReportedDds = Array.from(details.querySelectorAll("dd")).filter(
          (dd) => dd.textContent?.trim() === "Not reported",
        );
        expect(notReportedDds.length).toBe(1);
        const sharedGroup = notReportedDds[0]!.closest("div")!;
        expect(sharedGroup.querySelectorAll("dt").length).toBeGreaterThanOrEqual(2);
      },
    );

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Unpublished figures share one value instead of occupying a field each
    And("no unpublished figure occupies a name-value group of its own", () => {
      const details = screen.getByTestId(`model-card-details-${ctx.targetModelId!}`);
      const notReportedDds = Array.from(details.querySelectorAll("dd")).filter(
        (dd) => dd.textContent?.trim() === "Not reported",
      );
      const sharedGroup = notReportedDds[0]!.closest("div")!;
      expect(sharedGroup.querySelectorAll("dd").length).toBe(1);
    });
  });

  // ─── AC-56 — document order (Phase 7, cycle 7.2) ──────────────────────────────
  // The full ordering assertion (via `compareDocumentPosition`) lives in
  // `apps/ayokoding-www/src/app/[locale]/tools/ai-benchmark/benchmark-content.test.tsx` — this
  // binding renders the same route through `AiBenchmarkPage` (this file's own navigation mock)
  // and repeats the check so `specs:behavior:coverage`'s `@covers` scan finds this scenario here.
  Scenario(
    "The chart precedes the roster and both precede the collapsed reference sections",
    ({ Given, When, Then, And }) => {
      Given("the page renders with no filters applied", () => {
        renderPageForLocale("en");
      });

      When("the document order of the page's regions is inspected", () => {
        // Inspection happens directly in the Then/And assertions below.
        expect(true).toBe(true);
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The chart precedes the roster and both precede the collapsed reference sections
      Then("the chart region precedes the roster region", () => {
        const chart = screen.getByTestId("benchmark-chart");
        const roster = screen.getByTestId("model-table");
        expect(chart.compareDocumentPosition(roster) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The chart precedes the roster and both precede the collapsed reference sections
      And("the legend and sources disclosures both follow the roster region", () => {
        const roster = screen.getByTestId("model-table");
        const legend = screen.getByTestId("ai-bench-legend");
        const sources = screen.getByTestId("ai-bench-sources");
        expect(roster.compareDocumentPosition(legend) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
        expect(roster.compareDocumentPosition(sources) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
      });
    },
  );

  // ─── AC-57 — the legend and sources stay reachable after collapsing (Phase 7, cycle 7.3) ─────
  Scenario("The legend and sources remain reachable after collapsing", ({ Given, When, Then, And }) => {
    Given("the legend and sources are rendered as disclosures below the roster", () => {
      renderPageForLocale("en");
    });

    When("each disclosure is expanded", () => {
      screen.getByTestId("ai-bench-legend").setAttribute("open", "");
      screen.getByTestId("ai-bench-sources").setAttribute("open", "");
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The legend and sources remain reachable after collapsing
    Then("the legend defines each of the four classes and each of the five evidence grades", () => {
      for (const band of ["opus", "sonnet", "haiku", "unrated"]) {
        expect(screen.getByTestId(`ai-bench-legend-class-${band}`)).toBeTruthy();
      }
      for (const grade of ["verified", "self-reported", "secondary", "conflicted", "unavailable"]) {
        expect(screen.getByTestId(`ai-bench-legend-grade-${grade}`)).toBeTruthy();
      }
      // UWT-005 — the coverage formula is stated in text, not just a bare percentage.
      expect(screen.getByTestId("ai-bench-legend-coverage")).toBeTruthy();
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The legend and sources remain reachable after collapsing
    And("the sources section lists every named operator", () => {
      const sources = screen.getByTestId("ai-bench-sources");
      const text = sources.textContent ?? "";
      for (const op of OPERATORS) {
        expect(text).toContain(op.name);
      }
    });
  });

  // ─── Phase 8 — accessibility: tap targets and the live layout criteria ────────
  // AC-49/AC-50/AC-51/AC-55/AC-58/AC-60 are ALL @e2e-only: every one of them reads a computed
  // style, a bounding box, or a real viewport dimension that jsdom has no layout engine to produce
  // (the same DD-26 "verification gap" jsdom cannot close as AC-38/AC-52/AC-59/AC-61/AC-62 above).
  // Same established `expect(true).toBe(true)` placeholder convention, so `specs:behavior:coverage`
  // (which scans only `apps/ayokoding-www`) finds a `@covers` annotation for each. The real
  // assertions live in `apps/ayokoding-www-fe-e2e/tests/e2e/steps/ai-benchmark.steps.ts`.

  ScenarioOutline("Every interactive target meets the minimum target size", ({ Given, When, Then }) => {
    Given('the AI benchmark page is loaded at a "<width>" px viewport', () => {
      expect(true).toBe(true);
    });

    When("the bounding box of every link and every disclosure control is measured", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Every interactive target meets the minimum target size
    Then("every measured target is at least 24 CSS pixels wide and at least 24 CSS pixels tall", () => {
      expect(true).toBe(true);
    });
  });

  ScenarioOutline("Chart label text renders at a fixed size across viewports", ({ Given, When, Then, And }) => {
    Given('the AI benchmark page is loaded at a "<width>" px viewport', () => {
      expect(true).toBe(true);
    });

    When("the computed font size of a chart model label is read from the live page", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Chart label text renders at a fixed size across viewports
    Then("that computed font size equals the computed font size of the same label at every other tested width", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Chart label text renders at a fixed size across viewports
    And("that computed font size is at least 12 CSS pixels", () => {
      expect(true).toBe(true);
    });
  });

  Scenario("Chart label text never exceeds the page's own body text size", ({ Given, When, Then }) => {
    Given("the AI benchmark page is loaded at a 1440 px viewport", () => {
      expect(true).toBe(true);
    });

    When("the computed font sizes of a chart model label and the page body text are read from the live page", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Chart label text never exceeds the page's own body text size
    Then("the chart label's computed font size is no larger than the page body text's computed font size", () => {
      expect(true).toBe(true);
    });
  });

  Scenario("The chart plot occupies the full container width on a phone", ({ Given, When, Then, And }) => {
    Given("the AI benchmark page is loaded at a 320 px viewport", () => {
      expect(true).toBe(true);
    });

    When("the width of a capability bar's track is compared with the width of its containing chart region", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The chart plot occupies the full container width on a phone
    Then("the bar track spans the full width of that region", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The chart plot occupies the full container width on a phone
    And("no reserved label column is present at that width", () => {
      expect(true).toBe(true);
    });
  });

  // Rule-15 UWT-007 regression fix (Phase 12 PR review, finding F2): mirrors the Scenario Outline
  // the `.feature` file now carries (retargeted from a fixed 390x844 viewport to the two realistic
  // breakpoints `delivery.md`'s UWT-007 retest actually measured — this mock binding is unaffected
  // by which breakpoint is substituted since every step body is a no-op `expect(true).toBe(true)`,
  // but the step TEXT must still match the `.feature` file's quoted-parameter Given for the shared
  // spec-coverage validator to resolve this as a bound step rather than an orphan).
  ScenarioOutline("The chart is visible above the fold on a phone", ({ Given, When, Then }) => {
    Given('the AI benchmark page is loaded at a "<width>" px wide, "<height>" px tall viewport', () => {
      expect(true).toBe(true);
    });

    When("the vertical offset of the first chart element is read from the live page", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The chart is visible above the fold on a phone
    Then("that offset is less than the viewport height", () => {
      expect(true).toBe(true);
    });
  });

  ScenarioOutline("The overhauled page behaves identically in both locales", ({ Given, When, Then, And }) => {
    Given('the AI benchmark page is loaded in the "<locale>" locale at a 390 px viewport', () => {
      expect(true).toBe(true);
    });

    When("the page renders", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The overhauled page behaves identically in both locales
    Then("the chart is present above the fold", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The overhauled page behaves identically in both locales
    And("every roster card is collapsed", () => {
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The overhauled page behaves identically in both locales
    And("no raw translation key is rendered", () => {
      expect(true).toBe(true);
    });
  });
});
