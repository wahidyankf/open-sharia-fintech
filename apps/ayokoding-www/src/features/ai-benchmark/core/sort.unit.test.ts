import { describe, expect, it } from "vitest";
import type { HarnessId, MeteredPrice, Model } from "./data/models";
import type { ModelScore } from "./bands";
import { byCapabilityDesc, byPriceAsc, byPriceDesc } from "./sort";

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
  return { model: modelWith(id, pricing), index, coverage: 1, band: "light" };
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
