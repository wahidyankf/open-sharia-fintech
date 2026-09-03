import { describe, expect, it } from "vitest";
import {
  BENCHMARK_WEIGHTS,
  dataset,
  type BenchmarkId,
  type ConflictedFigure,
  type Dataset,
  type Figure,
  type Model,
} from "../../../../../src/features/ai-benchmark/core/data/models";
import {
  LOW_COVERAGE_THRESHOLD,
  computeIndex,
  coverage,
  isLowCoverage,
  isIncludedFigure,
  rel,
  rosterMax,
  type RosterMaxes,
} from "../../../../../src/features/ai-benchmark/core/score";

// Pure-function tests for the AI Benchmark scoring core (Phase 4 steps C-1..C-11).
// Arithmetic is specified verbatim by
// `plans/done/2026-07-30__ayokoding-www-tools-ai-benchmark/tech-docs.md` §"Scoring pipeline" and
// §"DD-5a" / §"DD-6". Fixture datasets give known inputs so the assertions are exact.

// ─── Fixture builders ──────────────────────────────────────────────────────────

const SRC = "https://example.test/source";

function figure(benchmark: BenchmarkId, value: number, extra: Partial<Figure> = {}): Figure {
  return { benchmark, value, grade: "verified", source: SRC, ...extra };
}

function conflicted(
  benchmark: BenchmarkId,
  low: number,
  high: number,
  extra: Partial<ConflictedFigure> = {},
): ConflictedFigure {
  return { benchmark, value: low, grade: "conflicted", low, high, source: SRC, ...extra };
}

function model(id: string, figures: Figure[], harnesses: Model["harnesses"] = ["claude-code"]): Model {
  return { id, name: id, vendor: "Test", harnesses, figures, pricing: {} };
}

function datasetOf(models: Model[]): Dataset {
  return { snapshotDate: "2026-07-28", anchorIds: { opus: "opus-anchor", sonnet: "sonnet-anchor" }, models };
}

// A roster-max map fixed at 80 on every axis — keeps rel arithmetic readable.
const MAXES_80: RosterMaxes = {
  "swe-bench-verified": 80,
  "swe-bench-pro": 80,
  "terminal-bench-2-1": 80,
  "gpqa-diamond": 80,
};

// ─── C-1 / C-2 — rosterMax ─────────────────────────────────────────────────────

describe("rosterMax — highest INCLUDED figure for a benchmark", () => {
  it("returns the max figure value over the real roster for each composite benchmark", () => {
    // Hand-computed from core/data/models.ts (low end of every conflicted figure).
    expect(rosterMax(dataset, "swe-bench-verified")).toBe(96.0); // claude-opus-5
    expect(rosterMax(dataset, "swe-bench-pro")).toBe(80.3); // claude-fable-5
    expect(rosterMax(dataset, "terminal-bench-2-1")).toBe(91.9); // gpt-5.6-sol
    expect(rosterMax(dataset, "gpqa-diamond")).toBe(94.1); // gpt-5.6-sol / gemini-3.1-pro (low)
  });

  it("uses the LOW end of a conflicted figure (never the high)", () => {
    const ds = datasetOf([model("a", [conflicted("gpqa-diamond", 70, 85)]), model("b", [figure("gpqa-diamond", 90)])]);
    // a's conflicted range is [70, 85]; the low (70) enters, so the max is max(70, 90) = 90,
    // NOT max(85, 90) = 90 would coincide here — assert the low path explicitly below.
    expect(rosterMax(ds, "gpqa-diamond")).toBe(90);
    const dsLowWins = datasetOf([model("a", [conflicted("gpqa-diamond", 70, 99)])]);
    // If the high (99) were used, rosterMax would be 99; the low (70) is what enters.
    expect(rosterMax(dsLowWins, "gpqa-diamond")).toBe(70);
  });

  it("EXCLUDES a Terminal-Bench 2.0 figure from a terminal-bench-2-1 roster max (version trap)", () => {
    const ds = datasetOf([
      model("tb2", [figure("terminal-bench-2-1", 99, { benchmarkVersion: "2.0" })]),
      model("tb21", [figure("terminal-bench-2-1", 50, { benchmarkVersion: "2.1" })]),
    ]);
    // The 2.0 figure (99) is excluded — counts as absent — so the roster max is the 2.1 figure (50).
    expect(rosterMax(ds, "terminal-bench-2-1")).toBe(50);
  });

  it("EXCLUDES a SWE-bench Multilingual figure from a swe-bench-verified roster max (version trap)", () => {
    const ds = datasetOf([
      model("multi", [figure("swe-bench-verified", 99, { benchmarkVersion: "Verified", conditions: "Multilingual" })]),
      model("ver", [figure("swe-bench-verified", 60, { benchmarkVersion: "Verified" })]),
    ]);
    expect(rosterMax(ds, "swe-bench-verified")).toBe(60);
  });

  it("returns undefined when no included figure exists for a benchmark", () => {
    const ds = datasetOf([model("none", [figure("swe-bench-verified", 50)])]);
    expect(rosterMax(ds, "swe-bench-pro")).toBeUndefined();
  });
});

// ─── C-3 / C-4 — rel ───────────────────────────────────────────────────────────

describe("rel — roster-relative normalized score", () => {
  it("returns 100 × score / rosterMax", () => {
    const m = model("m", [figure("swe-bench-verified", 64)]);
    expect(rel(m, "swe-bench-verified", 80)).toBe(80);
  });

  it("returns exactly 100 for the roster-max holder", () => {
    const m = model("holder", [figure("gpqa-diamond", 80)]);
    expect(rel(m, "gpqa-diamond", 80)).toBe(100);
  });

  it("returns undefined for an absent figure", () => {
    const m = model("m", [figure("swe-bench-verified", 64)]);
    expect(rel(m, "swe-bench-pro", 80)).toBeUndefined();
  });

  it("returns undefined for a figure excluded by the version trap", () => {
    const m = model("m", [figure("terminal-bench-2-1", 99, { benchmarkVersion: "2.0" })]);
    expect(rel(m, "terminal-bench-2-1", 100)).toBeUndefined();
  });
});

// ─── isIncludedFigure (version-trap guard) ─────────────────────────────────────

describe("isIncludedFigure — version-trap guard", () => {
  it("includes a correctly-versioned Terminal-Bench 2.1 figure", () => {
    expect(isIncludedFigure(figure("terminal-bench-2-1", 80, { benchmarkVersion: "2.1" }))).toBe(true);
  });
  it("excludes a Terminal-Bench 2.0 figure from a 2.1 slot", () => {
    expect(isIncludedFigure(figure("terminal-bench-2-1", 80, { benchmarkVersion: "2.0" }))).toBe(false);
    expect(isIncludedFigure(figure("terminal-bench-2-1", 80, { conditions: "Terminal-Bench 2.0 run" }))).toBe(false);
  });
  it("excludes a SWE-bench Multilingual figure from a Verified slot", () => {
    expect(isIncludedFigure(figure("swe-bench-verified", 80, { conditions: "Multilingual eval" }))).toBe(false);
  });
  it("includes a normal SWE-bench Verified figure", () => {
    expect(isIncludedFigure(figure("swe-bench-verified", 80, { benchmarkVersion: "Verified" }))).toBe(true);
  });
});

// ─── C-5 / C-6 — computeIndex + coverage (two of four benchmarks) ──────────────

describe("computeIndex + coverage — weight-renormalized mean over present benchmarks", () => {
  // Fixture: swe-bench-verified=64 (→ rel 80, weight 25) and gpqa-diamond=40 (→ rel 50, weight 30).
  // The other two benchmarks are absent.
  const m = model("two-of-four", [figure("swe-bench-verified", 64), figure("gpqa-diamond", 40)]);

  it("computeIndex returns the weight-renormalized mean of the present normalized scores", () => {
    const expected =
      (BENCHMARK_WEIGHTS["swe-bench-verified"] * 80 + BENCHMARK_WEIGHTS["gpqa-diamond"] * 50) /
      (BENCHMARK_WEIGHTS["swe-bench-verified"] + BENCHMARK_WEIGHTS["gpqa-diamond"]);
    expect(computeIndex(m, MAXES_80)).toBeCloseTo(expected, 10);
    // (25*80 + 30*50) / 55 = 3500/55
    expect(computeIndex(m, MAXES_80)).toBeCloseTo(3500 / 55, 10);
  });

  it("coverage returns the summed present weight ÷ 100", () => {
    expect(coverage(m)).toBe((BENCHMARK_WEIGHTS["swe-bench-verified"] + BENCHMARK_WEIGHTS["gpqa-diamond"]) / 100);
    expect(coverage(m)).toBeCloseTo(0.55, 10);
  });

  it("the roster-max holder scores 100 on its axis (rel feeds the index)", () => {
    const holder = model("holder", [figure("swe-bench-verified", 80), figure("gpqa-diamond", 80)]);
    // Both rels are 100, so the index is 100.
    expect(computeIndex(holder, MAXES_80)).toBeCloseTo(100, 10);
  });
});

// ─── C-7 / C-8 — zero present benchmarks ───────────────────────────────────────

describe("zero present benchmarks — coverage 0, index undefined (never 0, never NaN)", () => {
  const empty = model("empty", []);

  it("coverage is exactly 0", () => {
    expect(coverage(empty)).toBe(0);
  });

  it("computeIndex is undefined (NOT 0, NOT NaN)", () => {
    const idx = computeIndex(empty, MAXES_80);
    expect(idx).toBeUndefined();
    expect(idx).not.toBe(0);
    expect(Number.isNaN(idx)).toBe(false);
  });

  it("a model whose only figure is version-trap-excluded also has coverage 0 and undefined index", () => {
    const trap = model("trap", [figure("terminal-bench-2-1", 99, { benchmarkVersion: "2.0" })]);
    expect(coverage(trap)).toBe(0);
    expect(computeIndex(trap, MAXES_80)).toBeUndefined();
  });
});

// ─── C-9 / C-10 — isLowCoverage + LOW_COVERAGE_THRESHOLD ───────────────────────

describe("isLowCoverage — true only for rated models below the threshold", () => {
  it("exports the 0.50 threshold as a named constant", () => {
    expect(LOW_COVERAGE_THRESHOLD).toBe(0.5);
  });

  it("is true below the threshold", () => {
    // swe-bench-pro (25) + terminal-bench-2-1 (20) = 45 → 0.45 coverage.
    const low = model("low", [figure("swe-bench-pro", 50), figure("terminal-bench-2-1", 50)]);
    expect(coverage(low)).toBeCloseTo(0.45, 10);
    expect(isLowCoverage(low)).toBe(true);
  });

  it("is false at the threshold", () => {
    // swe-bench-verified (25) + swe-bench-pro (25) = 50 → 0.50 coverage.
    const at = model("at", [figure("swe-bench-verified", 50), figure("swe-bench-pro", 50)]);
    expect(coverage(at)).toBeCloseTo(0.5, 10);
    expect(isLowCoverage(at)).toBe(false);
  });

  it("is false above the threshold", () => {
    // swe-bench-verified (25) + gpqa-diamond (30) = 55 → 0.55 coverage.
    const above = model("above", [figure("swe-bench-verified", 50), figure("gpqa-diamond", 50)]);
    expect(coverage(above)).toBeCloseTo(0.55, 10);
    expect(isLowCoverage(above)).toBe(false);
  });

  it("is false for a zero-coverage (unrated) model — unrated is its own state, not low-coverage", () => {
    const empty = model("empty", []);
    expect(isLowCoverage(empty)).toBe(false);
  });
});

// ─── C-11 — shared weight-table helper (computeIndex and coverage agree on W) ──

describe("computeIndex and coverage share the present-weight table", () => {
  it("coverage × 100 equals the weight sum that computeIndex divides by", () => {
    const m = model("three", [
      figure("swe-bench-verified", 60),
      figure("terminal-bench-2-1", 60),
      figure("gpqa-diamond", 60),
    ]);
    const w =
      BENCHMARK_WEIGHTS["swe-bench-verified"] +
      BENCHMARK_WEIGHTS["terminal-bench-2-1"] +
      BENCHMARK_WEIGHTS["gpqa-diamond"];
    // coverage = W/100, so W = coverage*100 — the same W computeIndex divides by.
    expect(coverage(m) * 100).toBe(w);
    // All three rels are 75 (60/80*100), so index = 75 regardless of weights.
    expect(computeIndex(m, MAXES_80)).toBeCloseTo(75, 10);
  });
});
