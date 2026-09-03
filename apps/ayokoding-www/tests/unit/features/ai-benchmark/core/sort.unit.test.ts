import { describe, expect, it } from "vitest";
import type { HarnessId, MeteredPrice, Model } from "../../../../../src/features/ai-benchmark/core/data/models";
import type { ModelScore } from "../../../../../src/features/ai-benchmark/core/bands";
import { byCapabilityDesc, byPriceAsc, byPriceDesc } from "../../../../../src/features/ai-benchmark/core/sort";

// Pure-function tests for display-order comparators (Phase 1 — new file, sibling to bands.ts /
// price.ts). `byCapabilityDesc` mirrors `bands.ts`'s private `compareForOrder` descending-index
// rule; `byPriceAsc` / `byPriceDesc` sort by output rate (tie-broken by input rate, DD-3) via
// `price.ts`'s `lowestRate`. See
// `plans/in-progress/ayokoding-www-ai-benchmark-merged-chart/tech-docs.md` DD-3/DD-4/DD-5.

const SRC = "https://example.test/pricing";

function met(input: number, output: number): MeteredPrice {
  return { kind: "metered", input, output, grade: "verified", source: SRC };
}

function modelWith(id: string, pricing: Model["pricing"] = {}): Model {
  return { id, name: id, vendor: "Test", harnesses: Object.keys(pricing) as HarnessId[], figures: [], pricing };
}

function score(id: string, index: number | undefined, pricing: Model["pricing"] = {}): ModelScore {
  return { model: modelWith(id, pricing), index, coverage: 1, band: "haiku" };
}

// ─── byCapabilityDesc ───────────────────────────────────────────────────────────

describe("byCapabilityDesc — descending composite index, undefined last", () => {
  it("sorts a three-model fixture descending by index, with undefined index last", () => {
    const low = score("low", 40);
    const high = score("high", 90);
    const none = score("none", undefined);
    const sorted = [low, none, high].sort(byCapabilityDesc);
    expect(sorted.map((s) => s.model.id)).toEqual(["high", "low", "none"]);
  });
});

// ─── byPriceAsc / byPriceDesc ───────────────────────────────────────────────────

describe("byPriceAsc / byPriceDesc — ordered by output rate, input rate as tie-break (DD-3)", () => {
  it("byPriceAsc sorts ascending by output rate", () => {
    const cheap = score("cheap", 50, { cursor: met(1, 5) });
    const mid = score("mid", 60, { cursor: met(2, 10) });
    const pricey = score("pricey", 70, { cursor: met(3, 20) });
    const sorted = [pricey, cheap, mid].sort(byPriceAsc);
    expect(sorted.map((s) => s.model.id)).toEqual(["cheap", "mid", "pricey"]);
  });

  it("byPriceDesc sorts descending by output rate", () => {
    const cheap = score("cheap", 50, { cursor: met(1, 5) });
    const mid = score("mid", 60, { cursor: met(2, 10) });
    const pricey = score("pricey", 70, { cursor: met(3, 20) });
    const sorted = [cheap, pricey, mid].sort(byPriceDesc);
    expect(sorted.map((s) => s.model.id)).toEqual(["pricey", "mid", "cheap"]);
  });

  it("byPriceAsc ties on output rate are broken by ascending input rate", () => {
    const higherInput = score("higher-input", 50, { cursor: met(5, 10) });
    const lowerInput = score("lower-input", 60, { cursor: met(2, 10) });
    const sorted = [higherInput, lowerInput].sort(byPriceAsc);
    expect(sorted.map((s) => s.model.id)).toEqual(["lower-input", "higher-input"]);
  });

  it("byPriceDesc ties on output rate are broken by descending input rate", () => {
    const higherInput = score("higher-input", 50, { cursor: met(5, 10) });
    const lowerInput = score("lower-input", 60, { cursor: met(2, 10) });
    const sorted = [lowerInput, higherInput].sort(byPriceDesc);
    expect(sorted.map((s) => s.model.id)).toEqual(["higher-input", "lower-input"]);
  });

  it("byPriceAsc sorts an unmetered (subscription-only) model last, never as cheapest", () => {
    const priced = score("priced", 50, { cursor: met(3, 15) });
    const subscriptionOnly = score("sub-only", 60, {});
    const sorted = [subscriptionOnly, priced].sort(byPriceAsc);
    expect(sorted.map((s) => s.model.id)).toEqual(["priced", "sub-only"]);
  });

  it("byPriceDesc sorts an unmetered (subscription-only) model last, never as priciest", () => {
    const priced = score("priced", 50, { cursor: met(3, 15) });
    const subscriptionOnly = score("sub-only", 60, {});
    const sorted = [subscriptionOnly, priced].sort(byPriceDesc);
    expect(sorted.map((s) => s.model.id)).toEqual(["priced", "sub-only"]);
  });
});

// ─── Regression (pr-review-synthesis-maker HIGH finding): the comparators used `lowestRate`
// unconditionally, ignoring an active harness filter, while the chart plots `rateForHarness` under
// one — so an ascending price sort could render a costlier row above a cheaper one whenever a
// model's cheapest harness was not the selected one. `harness`, when passed, must sort by THAT
// harness's own rate instead.
describe("byPriceAsc / byPriceDesc — an optional `harness` sorts by that harness's own rate, not the lowest", () => {
  it("byPriceAsc sorts by the SELECTED harness's rate: a model whose lowest rate overall is cheaper can still sort AFTER one whose lowest is pricier, once the harness filter picks its costlier rate", () => {
    // Both models are exposed by codex-cli (the fixture's filtered harness) — "dual" ALSO exposes
    // a cheaper claude-code rate (10), which is its lowestRate() but must NOT drive the sort here.
    const dualHarness = score("dual", 50, { "claude-code": met(1, 10), "codex-cli": met(2, 25) });
    const flatPriced = score("flat", 60, { "codex-cli": met(1, 15) });
    // Sorting by lowestRate (10 vs 15) would put "dual" first; sorting by codex-cli's own rate
    // (25 vs 15) must put "flat" first instead.
    const sorted = [dualHarness, flatPriced].sort((a, b) => byPriceAsc(a, b, "codex-cli"));
    expect(sorted.map((s) => s.model.id)).toEqual(["flat", "dual"]);
  });

  it("byPriceDesc sorts by the SELECTED harness's rate the same way, reversed", () => {
    const dualHarness = score("dual", 50, { "claude-code": met(1, 10), "codex-cli": met(2, 25) });
    const flatPriced = score("flat", 60, { "codex-cli": met(1, 15) });
    const sorted = [flatPriced, dualHarness].sort((a, b) => byPriceDesc(a, b, "codex-cli"));
    expect(sorted.map((s) => s.model.id)).toEqual(["dual", "flat"]);
  });

  it("a model not exposed by the selected harness at all sorts last, never as cheapest, under byPriceAsc", () => {
    const exposedElsewhereOnly = score("elsewhere-only", 50, { "claude-code": met(1, 5) });
    const exposedHere = score("exposed-here", 60, { "codex-cli": met(1, 15) });
    const sorted = [exposedElsewhereOnly, exposedHere].sort((a, b) => byPriceAsc(a, b, "codex-cli"));
    expect(sorted.map((s) => s.model.id)).toEqual(["exposed-here", "elsewhere-only"]);
  });

  it("with no harness argument, behaviour is unchanged from the existing lowestRate-based sort", () => {
    const cheap = score("cheap", 50, { cursor: met(1, 5) });
    const pricey = score("pricey", 60, { cursor: met(1, 20) });
    const sorted = [pricey, cheap].sort((a, b) => byPriceAsc(a, b));
    expect(sorted.map((s) => s.model.id)).toEqual(["cheap", "pricey"]);
  });
});
