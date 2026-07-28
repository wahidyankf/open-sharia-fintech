// AI BENCHMARK — pure scoring core (Phase 4, steps C-1..C-11).
//
// Implements the composite-capability index from
// `plans/in-progress/ayokoding-www-tools-ai-benchmark/tech-docs.md` §"Scoring pipeline" and
// §"DD-5a" / §"DD-6". No React, no router, no side effects — every function is pure over the
// dataset, mirroring `src/features/cost-of-living-calculator/core/`.
//
// Arithmetic:
//   rosterMax(b) = max over all INCLUDED models m of score(m, b)
//   rel(m, b)    = 100 × score(m, b) / rosterMax(b)            — undefined when m has no included figure
//   W(m)         = Σ weight(b) for b ∈ present(m)
//   index(m)     = Σ weight(b) × rel(m, b) / W(m)              — undefined when W(m) = 0
//   coverage(m)  = W(m) / 100
//
// "Included" excludes the version-trap figures (Terminal-Bench 2.0 in a 2.1 slot, SWE-bench
// Multilingual in a Verified slot) — they count as absent. For a CONFLICTED figure the LOW
// published value enters the composite (the dataset already stores `value === low`).

import {
  BENCHMARK_WEIGHTS,
  isConflictedFigure,
  type BenchmarkId,
  type Dataset,
  type Figure,
  type Model,
} from "./data/models";

/** A roster-max value per benchmark; `undefined` when no included figure exists for it. */
export type RosterMaxes = Record<BenchmarkId, number | undefined>;

/** Coverage ratio below which a rated model is marked low-coverage (DD-6). */
export const LOW_COVERAGE_THRESHOLD = 0.5;

/**
 * May a figure enter the composite? This is the defensive mirror of dataset invariant 9: a
 * Terminal-Bench 2.0 figure must never enter a `terminal-bench-2-1` slot, and a SWE-bench
 * Multilingual figure must never enter a `swe-bench-verified` slot. Such figures are recorded
 * in the dataset for honesty but EXCLUDED from the composite (they count as absent).
 *
 * The dataset is curated clean, so this guard is a safety net: if a wrongly-versioned figure
 * ever lands, it is scored as absent rather than silently corrupting the index.
 */
export function isIncludedFigure(f: Figure): boolean {
  const trail = `${f.benchmarkVersion ?? ""} ${f.conditions ?? ""}`.toLowerCase();
  if (f.benchmark === "terminal-bench-2-1" && trail.includes("2.0")) {
    return false;
  }
  if (f.benchmark === "swe-bench-verified" && trail.includes("multilingual")) {
    return false;
  }
  return true;
}

/**
 * The roster-max for a benchmark: the highest INCLUDED figure value across the roster. For a
 * conflicted figure the LOW published value is the composite input (the dataset stores
 * `value === low`), so the low is what is compared here. Returns `undefined` when no included
 * figure exists for the benchmark.
 */
export function rosterMax(dataset: Dataset, benchmark: BenchmarkId): number | undefined {
  let max: number | undefined;
  for (const m of dataset.models) {
    for (const f of m.figures) {
      if (f.benchmark !== benchmark) continue;
      if (!isIncludedFigure(f)) continue;
      // `value` is the composite input — for a conflicted figure it is already the low end.
      const v = f.value;
      if (max === undefined || v > max) {
        max = v;
      }
    }
  }
  return max;
}

/**
 * The per-benchmark roster-max map for the whole roster. Convenience over calling
 * {@link rosterMax} once per benchmark.
 */
export function computeRosterMaxes(dataset: Dataset): RosterMaxes {
  const out = {} as RosterMaxes;
  for (const b of Object.keys(BENCHMARK_WEIGHTS) as BenchmarkId[]) {
    out[b] = rosterMax(dataset, b);
  }
  return out;
}

/**
 * Relative normalized score: `100 × score(m, b) / rosterMax`. The roster-max holder scores
 * exactly 100. Returns `undefined` when the model has no included figure for the benchmark
 * (absent — never imputed, never zero).
 */
export function rel(model: Model, benchmark: BenchmarkId, max: number): number | undefined {
  const f = model.figures.find((fig) => fig.benchmark === benchmark && isIncludedFigure(fig));
  if (f === undefined) {
    return undefined;
  }
  return (100 * f.value) / max;
}

/**
 * Σ weight(b) over the benchmarks the model has an included figure for (DD-6 `W(m)`). Shared by
 * {@link computeIndex} (as its denominator) and {@link coverage} (as `W(m) / 100`) so the two
 * never disagree on what "present" means (C-11 refactor).
 */
function presentWeight(model: Model): number {
  let w = 0;
  for (const f of model.figures) {
    if (!isIncludedFigure(f)) continue;
    w += BENCHMARK_WEIGHTS[f.benchmark];
  }
  return w;
}

/**
 * The composite index: the weight-renormalized mean of the present normalized scores
 * (`Σ weight × rel ÷ W`). Returns `undefined` when `W = 0` (no included figure on any composite
 * benchmark) — never `0`, never `NaN`. The model is then unrated.
 *
 * A present benchmark always has a roster max (the model's own figure contributes to it), so the
 * `max === undefined` guard is unreachable for valid data; it keeps the function total.
 */
export function computeIndex(model: Model, rosterMaxes: RosterMaxes): number | undefined {
  const w = presentWeight(model);
  if (w === 0) {
    return undefined;
  }
  let weighted = 0;
  for (const f of model.figures) {
    if (!isIncludedFigure(f)) continue;
    const max = rosterMaxes[f.benchmark];
    if (max === undefined || max <= 0) {
      continue;
    }
    weighted += BENCHMARK_WEIGHTS[f.benchmark] * ((100 * f.value) / max);
  }
  return weighted / w;
}

/**
 * Coverage ratio: `W(m) / 100` — the fraction of the composite weight the model covers. `0`
 * means the model has no included figure on any composite benchmark (unrated).
 */
export function coverage(model: Model): number {
  return presentWeight(model) / 100;
}

/**
 * True for a RATED model whose coverage is below {@link LOW_COVERAGE_THRESHOLD}. An unrated
 * (zero-coverage) model is its own state and is NOT low-coverage — the marker describes "this
 * index exists but rests on sparse data", which an absent index cannot (scoring-pipeline
 * branches Y and K).
 */
export function isLowCoverage(model: Model): boolean {
  const c = coverage(model);
  return c > 0 && c < LOW_COVERAGE_THRESHOLD;
}

// Re-export the conflicted-figure guard for callers that compose this core (e.g. the data table
// rendering a range instead of a single number). Kept here so the scoring core is the one place
// that knows a conflicted figure carries a range.
export { isConflictedFigure };
