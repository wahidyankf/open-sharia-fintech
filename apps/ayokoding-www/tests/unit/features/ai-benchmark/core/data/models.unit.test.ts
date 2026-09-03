import { describe, expect, it } from "vitest";
import {
  BENCHMARK_WEIGHTS,
  dataset,
  isConflictedFigure,
  OPUS_ANCHOR_ID,
  SONNET_ANCHOR_ID,
  type ConflictedFigure,
  type EvidenceGrade,
  type HarnessId,
  type MeteredPrice,
  type SubscriptionPrice,
} from "../../../../../../src/features/ai-benchmark/core/data/models";

// Dataset invariant tests for the AI Benchmark feature — the honesty surface that makes the
// dataset enforceable rather than aspirational. The ten invariants are reproduced verbatim from
// `plans/done/2026-07-30__ayokoding-www-tools-ai-benchmark/tech-docs.md` §"Dataset invariant tests".
// Each failure message MUST name the offending model id and field so a broken figure is locatable
// without re-reading the whole dataset.

const VALID_GRADES: readonly EvidenceGrade[] = ["verified", "self-reported", "secondary", "conflicted", "unavailable"];

const VALID_HARNESSES: readonly HarnessId[] = ["claude-code", "codex-cli", "cursor", "opencode-go", "opencode-zen"];

const knownBenchmarkIds = new Set(Object.keys(BENCHMARK_WEIGHTS));

// Flatten every figure and every price across the roster so per-figure / per-price invariants can
// be expressed with `it.each`, which surfaces the offending model id + field in the test name.
const allFigures = dataset.models.flatMap((m) => m.figures.map((f) => ({ modelId: m.id, figure: f })));

type PriceRow = { modelId: string; harness: HarnessId; price: MeteredPrice | SubscriptionPrice };

const allPrices: PriceRow[] = dataset.models.flatMap((m) =>
  Object.entries(m.pricing)
    .filter(([, price]) => price !== undefined)
    .map(([harness, price]) => ({
      modelId: m.id,
      harness: harness as HarnessId,
      price: price as MeteredPrice | SubscriptionPrice,
    })),
);

const conflictedFigures = allFigures.filter((row) => row.figure.grade === "conflicted");
const subscriptionPriceRows = allPrices.filter(
  (row): row is PriceRow & { price: SubscriptionPrice } => row.price.kind === "subscription",
);

// ─── Invariant 1 — every benchmark figure has a non-empty source URL ──────────────────────

describe("invariant 1 — every benchmark figure has a non-empty source URL", () => {
  it.each(allFigures)("$modelId figure[$figure.benchmark].source is a non-empty URL", ({ modelId, figure }) => {
    expect(typeof figure.source, `${modelId}: figure ${figure.benchmark}.source must be a string`).toBe("string");
    expect(
      figure.source.trim().length,
      `${modelId}: figure ${figure.benchmark}.source must be non-empty`,
    ).toBeGreaterThan(0);
  });
});

// ─── Invariant 2 — every price figure has a non-empty source URL ─────────────────────────

describe("invariant 2 — every price figure has a non-empty source URL", () => {
  it.each(allPrices)("$modelId pricing[$harness].source is a non-empty URL", ({ modelId, harness, price }) => {
    expect(typeof price.source, `${modelId}: pricing.${harness}.source must be a string`).toBe("string");
    expect(price.source.trim().length, `${modelId}: pricing.${harness}.source must be non-empty`).toBeGreaterThan(0);
  });
});

// ─── Invariant 3 — every figure carries an evidence grade from the five-value union ───────

describe("invariant 3 — every figure has an evidence grade drawn from the five-value union", () => {
  it.each(allFigures)("$modelId figure[$figure.benchmark].grade is a known EvidenceGrade", ({ modelId, figure }) => {
    expect(
      VALID_GRADES,
      `${modelId}: figure ${figure.benchmark}.grade "${figure.grade}" is not one of ${VALID_GRADES.join(" | ")}`,
    ).toContain(figure.grade);
  });
});

// ─── Invariant 4 — every conflicted figure carries low ≤ high (and low is the composite input)

describe("invariant 4 — every conflicted figure carries both a low and a high value, and low ≤ high", () => {
  // Guard: if there are no conflicted figures the invariant is vacuous, but the dataset is
  // EXPECTED to carry several (Opus 5 GPQA, GLM-5.2 TB, Sonnet 4.6 GPQA, Haiku 4.5 GPQA,
  // Gemini 3 Flash SWE-V, Gemini 3.1 Pro GPQA). Assert the set is non-empty so a future edit
  // that silently flattens a range to an average is caught.
  it("the dataset carries at least one conflicted figure (the range-encoding path is exercised)", () => {
    expect(conflictedFigures.length).toBeGreaterThan(0);
  });

  it.each(conflictedFigures)(
    "$modelId figure[$figure.benchmark] (conflicted) has low ≤ high and value === low",
    ({ modelId, figure }) => {
      expect(
        isConflictedFigure(figure),
        `${modelId}: figure ${figure.benchmark} grade is "conflicted" but isConflictedFigure narrows it — low/high must be present`,
      ).toBe(true);
      const c = figure as ConflictedFigure;
      expect(typeof c.low, `${modelId}: figure ${figure.benchmark}.low must be a number`).toBe("number");
      expect(typeof c.high, `${modelId}: figure ${figure.benchmark}.high must be a number`).toBe("number");
      expect(
        c.low,
        `${modelId}: figure ${figure.benchmark} low (${c.low}) must be ≤ high (${c.high})`,
      ).toBeLessThanOrEqual(c.high);
      // The LOW value enters the composite (scoring pipeline line 117); `value` must equal `low`.
      expect(
        c.value,
        `${modelId}: figure ${figure.benchmark}.value (${c.value}) must equal low (${c.low}) — the low enters the composite`,
      ).toBe(c.low);
    },
  );
});

// ─── Invariant 5 — harness ids are non-empty and drawn from the known five ────────────────

describe("invariant 5 — every model names at least one harness, and every named harness is one of the five known ids", () => {
  it.each(dataset.models)("$id names ≥1 harness", (model) => {
    expect(model.harnesses.length, `${model.id}: must name at least one harness`).toBeGreaterThan(0);
  });

  it.each(dataset.models)("$id harnesses are all known ids", (model) => {
    for (const h of model.harnesses) {
      expect(VALID_HARNESSES, `${model.id}: harness "${h}" is not one of ${VALID_HARNESSES.join(" | ")}`).toContain(h);
    }
  });
});

// ─── Invariant 6 — model ids are unique ──────────────────────────────────────────────────

describe("invariant 6 — model ids are unique", () => {
  it("no two models share an id", () => {
    const ids = dataset.models.map((m) => m.id);
    const dupes = ids.filter((id, idx) => ids.indexOf(id) !== idx);
    expect(dupes, `duplicate model ids: ${dupes.join(", ")}`).toHaveLength(0);
  });
});

// ─── Invariant 7 — snapshotDate parses as an ISO date ────────────────────────────────────

describe("invariant 7 — snapshotDate parses as an ISO date", () => {
  it("dataset.snapshotDate matches YYYY-MM-DD and constructs a valid Date", () => {
    expect(dataset.snapshotDate, "snapshotDate must match ^\\d{4}-\\d{2}-\\d{2}$").toMatch(/^\d{4}-\d{2}-\d{2}$/);
    const parsed = new Date(`${dataset.snapshotDate}T00:00:00Z`);
    expect(Number.isNaN(parsed.getTime()), `snapshotDate "${dataset.snapshotDate}" must construct a valid Date`).toBe(
      false,
    );
  });
});

// ─── Invariant 8 — both anchor ids resolve to a model in the roster ───────────────────────

describe("invariant 8 — both anchor ids resolve to a model in the roster", () => {
  it("OPUS_ANCHOR_ID and SONNET_ANCHOR_ID each resolve to a roster model", () => {
    const ids = new Set(dataset.models.map((m) => m.id));
    expect(ids.has(OPUS_ANCHOR_ID), `anchor opus id "${OPUS_ANCHOR_ID}" not in roster`).toBe(true);
    expect(ids.has(SONNET_ANCHOR_ID), `anchor sonnet id "${SONNET_ANCHOR_ID}" not in roster`).toBe(true);
    expect(dataset.anchorIds.opus, "dataset.anchorIds.opus must equal OPUS_ANCHOR_ID").toBe(OPUS_ANCHOR_ID);
    expect(dataset.anchorIds.sonnet, "dataset.anchorIds.sonnet must equal SONNET_ANCHOR_ID").toBe(SONNET_ANCHOR_ID);
  });
});

// ─── Invariant 9 — the benchmark-version trap ─────────────────────────────────────────────
// No model may carry a Terminal-Bench 2.0 figure in a terminal-bench-2-1 slot, nor a SWE-bench
// Multilingual figure in a swe-bench-verified slot. Such figures are excluded from the composite
// (scoring pipeline line 115) and must therefore be absent from these fields.

describe("invariant 9 — no model carries a Terminal-Bench 2.0 or SWE-bench Multilingual figure in a 2.1 or Verified field", () => {
  it.each(allFigures)(
    "$modelId figure[$figure.benchmark] is on the correct benchmark version",
    ({ modelId, figure }) => {
      const versionTrail = `${figure.benchmarkVersion ?? ""} ${figure.conditions ?? ""}`.toLowerCase();
      if (figure.benchmark === "terminal-bench-2-1") {
        expect(
          versionTrail,
          `${modelId}: terminal-bench-2-1 figure must not describe the 2.0 scale (found "${figure.benchmarkVersion ?? ""} / ${figure.conditions ?? ""}")`,
        ).not.toContain("2.0");
      }
      if (figure.benchmark === "swe-bench-verified") {
        expect(
          versionTrail,
          `${modelId}: swe-bench-verified figure must not describe the Multilingual benchmark (found "${figure.benchmarkVersion ?? ""} / ${figure.conditions ?? ""}")`,
        ).not.toContain("multilingual");
      }
      // Sanity: every figure's benchmark is one the composite recognises.
      expect(knownBenchmarkIds, `${modelId}: unknown benchmark id "${figure.benchmark}"`).toContain(figure.benchmark);
    },
  );
});

// ─── Invariant 10 — subscription prices carry a plan cost and omit per-token rates ────────

describe("invariant 10 — every subscription-kind price carries a plan cost, a known evidence grade, and omits per-token rates", () => {
  it.each(subscriptionPriceRows)(
    "$modelId pricing[$harness] (subscription) has planCostUsd, a valid grade, and no per-token rate",
    ({ modelId, harness, price }) => {
      expect(typeof price.planCostUsd, `${modelId}: pricing.${harness}.planCostUsd must be a number`).toBe("number");
      expect(price.planCostUsd, `${modelId}: pricing.${harness}.planCostUsd must be > 0`).toBeGreaterThan(0);
      // AC-21 requires every price cell to carry an evidence grade marker — a subscription price
      // is unsatisfiable-by-construction if its type carries no grade at all (F1a).
      expect(
        VALID_GRADES,
        `${modelId}: pricing.${harness} (subscription) grade "${price.grade}" is not one of ${VALID_GRADES.join(" | ")}`,
      ).toContain(price.grade);
      // A subscription must NEVER carry per-token rates — structural guard against a wrongly-
      // shaped entry that smuggles in input/output fields.
      const stray = price as unknown as Record<string, unknown>;
      expect(
        stray["input"],
        `${modelId}: pricing.${harness} (subscription) must not carry an input rate`,
      ).toBeUndefined();
      expect(
        stray["output"],
        `${modelId}: pricing.${harness} (subscription) must not carry an output rate`,
      ).toBeUndefined();
    },
  );
});
