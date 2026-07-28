import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import "./helpers/test-setup";
import {
  BENCHMARK_WEIGHTS,
  OPUS_ANCHOR_ID,
  SONNET_ANCHOR_ID,
  dataset,
  type BenchmarkId,
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
};

let ctx: Ctx = {};

// The live anchor indices, used as the threshold reference for the rule scenarios.
const liveAnchors: AnchorIndices = anchors(dataset);

describeFeature(feature, ({ Background, Scenario, AfterEachScenario }) => {
  Background(({ Given }) => {
    Given("the AI benchmark dataset is loaded", () => {
      // The `dataset` import is the loaded roster; nothing to set up.
      expect(dataset.models.length).toBeGreaterThan(0);
    });
  });

  AfterEachScenario(() => {
    ctx = {};
  });

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
});
