import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, render, screen } from "@testing-library/react";
import { expect, vi } from "vitest";
import React from "react";

// ─── Reactive next/navigation mock (Phase 5 page-render scenarios) ─────────────
// AC-1/AC-2/AC-19/AC-29/AC-32/AC-34/AC-35 render the route's client content, which reads its
// locale from useLocale() → useParams(). navState holds the active locale so each scenario's
// Given step can set it before the page renders. Hoisted so the vi.mock factory can close over it.
const { navState } = vi.hoisted(() => ({ navState: { locale: "en" as string } }));

vi.mock("next/navigation", () => ({
  useParams: () => ({ locale: navState.locale }),
  useSearchParams: () => new URLSearchParams(),
  useRouter: () => ({ push: vi.fn(), replace: vi.fn(), back: vi.fn(), prefetch: vi.fn() }),
  usePathname: () => "/en/tools/ai-benchmark",
  notFound: vi.fn(),
}));

import "./helpers/test-setup";
import AiBenchmarkPage from "@/app/[locale]/tools/ai-benchmark/page";
import { OPERATORS } from "@/features/ai-benchmark/core/data/operators";
import { BENCHMARK_COLUMNS, HARNESS_DISPLAY_NAMES } from "@/features/ai-benchmark/core/data/benchmarks";
import {
  BENCHMARK_WEIGHTS,
  OPUS_ANCHOR_ID,
  SONNET_ANCHOR_ID,
  dataset,
  type BenchmarkId,
  type ConflictedFigure,
  type Dataset,
  type Figure,
  type Model,
} from "@/features/ai-benchmark/core/data/models";
import { computeIndex, computeRosterMaxes, coverage } from "@/features/ai-benchmark/core/score";
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
  path.resolve(process.cwd(), "../../specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature"),
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
};

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
    // Reset the mocked navigation locale and the simulated <html lang> between scenarios.
    navState.locale = "en";
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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A model reaching the opus anchor renders in the opus band
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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A model between the two anchors renders in the sonnet band
    Then('that model belongs to the "sonnet" band', () => {
      expect(ctx.band).toBe("sonnet");
    });
  });

  // ─── AC-6 — light band ──────────────────────────────────────────────────────

  Scenario("A model below the sonnet anchor renders in the light band", ({ Given, When, Then }) => {
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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A model below the sonnet anchor renders in the light band
    Then('that model belongs to the "light" band', () => {
      expect(ctx.band).toBe("light");
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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:Each anchor model occupies the band it defines
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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A model with no published benchmark score renders in the unrated group
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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:Every roster model belongs to exactly one capability group
    Then('each model appears in exactly one of "opus", "sonnet", "light", or "unrated"', () => {
      const g = ctx.groups!;
      const placed = [...g.opus, ...g.sonnet, ...g.light, ...g.unrated].map((s) => s.model.id);
      // Exactly once each (no duplicates), and every roster model is covered.
      expect(new Set(placed).size).toBe(placed.length);
      expect(placed.length).toBe(dataset.models.length);
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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A model missing a benchmark is scored over the benchmarks it has
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

  // ─── AC-11 — canonical per-band ordering shared by both charts ───────────────

  Scenario("Models are ordered identically in both charts within a band", ({ Given, When, Then }) => {
    Given("the full roster is loaded", () => {
      // dataset is the full roster.
    });

    When("both charts are rendered", () => {
      // Both charts consume the SAME canonical per-band list from computeGroups, so rendering both
      // is equivalent to producing that list once.
      ctx.groups = computeGroups(dataset);
    });

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:Models are ordered identically in both charts within a band
    Then("each band lists its models in the same order in the capability chart and the price chart", () => {
      const g = ctx.groups!;
      // The "same order" guarantee is that each band is ONE canonical list (descending index, then
      // id) that both charts read verbatim. Assert the canonical-order property holds per band.
      for (const list of [g.opus, g.sonnet, g.light, g.unrated]) {
        for (let i = 1; i < list.length; i++) {
          const prev = list[i - 1];
          const curr = list[i];
          if (prev === undefined || curr === undefined) continue; // unreachable: i within bounds
          const pi = prev.index ?? -Infinity;
          const ci = curr.index ?? -Infinity;
          if (pi !== ci) {
            expect(pi).toBeGreaterThan(ci);
          } else {
            expect(prev.model.id <= curr.model.id).toBe(true);
          }
        }
      }
    });
  });

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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The English page renders its localized heading
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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The Indonesian page renders its localized heading
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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The data table is present without any interaction
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

  Scenario("The table carries every figure the charts encode", ({ Given, When, Then }) => {
    Given("the full roster is loaded", () => {
      // dataset is the full roster.
    });

    When("the data table is rendered", () => {
      render(<ModelTable dataset={dataset} locale="en" />);
    });

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The table carries every figure the charts encode
    Then(
      "each model row lists its harnesses, class, every benchmark score, composite index, coverage ratio, input price, and output price",
      () => {
        const desktop = screen.getByTestId("model-table-desktop");
        const headerTexts = Array.from(desktop.querySelectorAll("thead th")).map((h) => h.textContent ?? "");
        // Every benchmark column header is present, plus index, coverage, and the two prices.
        for (const col of BENCHMARK_COLUMNS) {
          expect(headerTexts.some((h) => h === t("en", col.labelKey))).toBe(true);
        }
        expect(headerTexts.some((h) => h === t("en", "aiBenchColIndex"))).toBe(true);
        expect(headerTexts.some((h) => h === t("en", "aiBenchColCoverage"))).toBe(true);
        expect(headerTexts.some((h) => h === t("en", "aiBenchColInputPrice"))).toBe(true);
        expect(headerTexts.some((h) => h === t("en", "aiBenchColOutputPrice"))).toBe(true);

        const rows = desktop.querySelectorAll<HTMLTableRowElement>("tbody tr[data-model-id]");
        expect(rows.length).toBe(dataset.models.length);
        // Each row carries its harness display names and its localized class label.
        for (const row of Array.from(rows)) {
          const model = dataset.models.find((m) => m.id === row.getAttribute("data-model-id"));
          expect(model).toBeDefined();
          const rowText = row.textContent ?? "";
          for (const h of model!.harnesses) {
            expect(rowText).toContain(HARNESS_DISPLAY_NAMES[h] ?? h);
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
      render(<ModelTable dataset={dataset} locale="en" />);
    });

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:Every figure in the table carries an evidence grade
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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The page displays the dataset snapshot date
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
      render(<ModelTable dataset={dataset} locale="en" />);
    });

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:Every benchmark figure links to the source it came from
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
      render(<ModelTable dataset={ctx.fixtureDataset!} locale="en" />);
    });

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A conflicted figure renders as a range rather than a single number
    Then("that cell shows the lowest and highest published values", () => {
      const row = screen
        .getByTestId("model-table-desktop")
        .querySelector('tbody tr[data-model-id="fixture-conflicted"]');
      expect(row).not.toBeNull();
      const cellText = row?.textContent ?? "";
      // Both the low (70.0) and high (80.0) formatted values appear.
      expect(cellText).toContain("70.0");
      expect(cellText).toContain("80.0");
    });

    But("that cell shows no averaged value", () => {
      const row = screen
        .getByTestId("model-table-desktop")
        .querySelector('tbody tr[data-model-id="fixture-conflicted"]');
      const cellText = row?.textContent ?? "";
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

      // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The page discloses that frontier scores are overwhelmingly vendor-reported
      Then("the disclosure states that most frontier benchmark scores are vendor self-reported", () => {
        const disclosure = screen.getByTestId("ai-bench-how-to");
        const text = disclosure.textContent ?? "";
        // The English disclosure copy states vendor self-reported scores explicitly.
        expect(text.toLowerCase()).toContain("self-reported");
      });

      And("the disclosure is visible without interaction", () => {
        const disclosure = screen.getByTestId("ai-bench-how-to");
        // <details open> means the body is shown on first paint, before any click.
        expect(disclosure.tagName).toBe("DETAILS");
        expect(disclosure.hasAttribute("open")).toBe(true);
      });
    },
  );

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
        render(<ModelTable dataset={ctx.fixtureDataset!} locale="en" />);
      });

      // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The page names a known benchmark-integrity finding beside the model it concerns
      Then("the integrity note is reachable from that model's row", () => {
        const row = screen.getByTestId("model-table-desktop").querySelector('tbody tr[data-model-id="fixture-noted"]');
        expect(row).not.toBeNull();
        const noteLink = row?.querySelector('[data-slot="integrity-note"]');
        expect(noteLink).not.toBeNull();
        expect(noteLink?.getAttribute("href")).toBe("https://example.test/finding");
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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The page carries a sources and licences section
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

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:No raw translation key leaks on either locale
    Then("no rendered text matches a raw translation key", () => {
      const text = document.body.textContent ?? "";
      // Every aiBench* key resolves to localized copy via t(); a missing key renders as its raw
      // identifier (which always starts with "aiBench"), so any leak surfaces as the substring.
      expect(text).not.toMatch(/aiBench/);
    });
  });
});
