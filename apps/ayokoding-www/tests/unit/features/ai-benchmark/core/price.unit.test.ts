import { describe, expect, it } from "vitest";
import {
  dataset,
  type HarnessId,
  type MeteredPrice,
  type Model,
  type SubscriptionPrice,
} from "../../../../../src/features/ai-benchmark/core/data/models";
import { lowestRate, rateForHarness } from "../../../../../src/features/ai-benchmark/core/price";

// Pure-function tests for harness price selection (Phase 4 steps P-1..P-7). The price chart shows
// a single rate per model: the selected harness's rate, or — with no harness filter — the lowest
// available harness rate (compare input, then output). A subscription-only model is never shown as
// a numeric zero; it carries its subscription kind. See
// `plans/done/2026-07-30__ayokoding-www-tools-ai-benchmark/prd.md` AC-16/AC-17/AC-18.

const SRC = "https://example.test/pricing";

function met(input: number, output: number, conditions?: string): MeteredPrice {
  return { kind: "metered", input, output, grade: "verified", source: SRC, conditions };
}

function sub(planCostUsd = 10): SubscriptionPrice {
  return { kind: "subscription", planCostUsd, grade: "verified", source: SRC };
}

function modelWith(id: string, pricing: Model["pricing"]): Model {
  return { id, name: id, vendor: "Test", harnesses: Object.keys(pricing) as HarnessId[], figures: [], pricing };
}

// ─── P-1 / P-2 — lowestRate ────────────────────────────────────────────────────

describe("lowestRate — the cheapest harness rate when no harness filter is applied", () => {
  it("returns the cheaper of two metered harness rates (by input)", () => {
    const m = modelWith("m", {
      "claude-code": met(5, 25),
      cursor: met(3, 15),
    });
    expect(lowestRate(m)).toEqual(met(3, 15));
  });

  it("breaks ties on input by the lower output rate", () => {
    const m = modelWith("m", {
      cursor: met(3, 30),
      "opencode-zen": met(3, 15),
    });
    expect(lowestRate(m)).toEqual(met(3, 15));
  });

  it("prefers a metered rate over a subscription when both are present", () => {
    const m = modelWith("m", {
      cursor: met(2, 6),
      "opencode-go": sub(10),
      "opencode-zen": met(4, 12),
    });
    expect(lowestRate(m)?.kind).toBe("metered");
    expect(lowestRate(m)).toEqual(met(2, 6));
  });

  it("returns undefined when a model has no pricing at all", () => {
    const m = modelWith("none", {});
    expect(lowestRate(m)).toBeUndefined();
  });
});

// ─── P-3 / P-4 — rateForHarness ────────────────────────────────────────────────

describe("rateForHarness — a specific harness's rate set", () => {
  const m = modelWith("m", {
    "claude-code": met(5, 25),
    cursor: met(3, 15),
  });

  it("returns that harness's rate set", () => {
    expect(rateForHarness(m, "cursor")).toEqual(met(3, 15));
    expect(rateForHarness(m, "claude-code")).toEqual(met(5, 25));
  });

  it("returns undefined when the model is not exposed by that harness", () => {
    expect(rateForHarness(m, "opencode-zen")).toBeUndefined();
    expect(rateForHarness(m, "opencode-go")).toBeUndefined();
  });
});

// ─── P-5 / P-6 — subscription-only models ──────────────────────────────────────

describe("subscription-only models — both selectors return the subscription, never a zero", () => {
  const subOnly = modelWith("sub-only", { "opencode-go": sub(10) });

  it("lowestRate returns the subscription (kind 'subscription')", () => {
    const r = lowestRate(subOnly);
    expect(r).toBeDefined();
    expect(r?.kind).toBe("subscription");
    expect((r as SubscriptionPrice).planCostUsd).toBe(10);
  });

  it("rateForHarness returns the subscription for the exposing harness", () => {
    const r = rateForHarness(subOnly, "opencode-go");
    expect(r?.kind).toBe("subscription");
  });

  it("neither selector returns a numeric zero or an undefined-with-zero", () => {
    expect(typeof lowestRate(subOnly)).not.toBe("number");
    expect(lowestRate(subOnly)).not.toBe(0);
    expect(lowestRate(subOnly)).not.toBeUndefined();
    // rateForHarness on the exposed harness is the subscription (not zero / not undefined).
    expect(rateForHarness(subOnly, "opencode-go")).not.toBe(0);
    expect(rateForHarness(subOnly, "opencode-go")).not.toBeUndefined();
  });
});

// ─── Real-dataset sanity ───────────────────────────────────────────────────────

describe("lowestRate / rateForHarness against the live roster", () => {
  const byId = new Map(dataset.models.map((m) => [m.id, m]));

  it("claude-opus-5's lowest rate is its metered $5/$25 (three harnesses, identical)", () => {
    const r = lowestRate(byId.get("claude-opus-5")!);
    expect(r?.kind).toBe("metered");
    expect((r as MeteredPrice).input).toBe(5);
    expect((r as MeteredPrice).output).toBe(25);
  });

  it("grok-4.5's lowest rate is its metered cursor/zen rate, not its opencode-go subscription", () => {
    const r = lowestRate(byId.get("grok-4.5")!);
    expect(r?.kind).toBe("metered");
    expect((r as MeteredPrice).input).toBe(2);
  });

  it("a subscription-only roster model (mimo-v2.5) selects the subscription from both selectors", () => {
    const mimo = byId.get("mimo-v2.5")!;
    expect(lowestRate(mimo)?.kind).toBe("subscription");
    expect(rateForHarness(mimo, "opencode-go")?.kind).toBe("subscription");
  });

  it("a model with empty pricing (gemini-3.1-pro) yields undefined from both selectors", () => {
    const g = byId.get("gemini-3.1-pro")!;
    expect(lowestRate(g)).toBeUndefined();
    expect(rateForHarness(g, "cursor")).toBeUndefined();
  });
});
