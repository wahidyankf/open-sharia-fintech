import { describe, expect, it } from "vitest";
import {
  dataset,
  type Dataset,
  type HarnessId,
  type Model,
} from "../../../../../src/features/ai-benchmark/core/data/models";
import { computeGroups } from "../../../../../src/features/ai-benchmark/core/bands";
import { filterModels, type FilterState } from "../../../../../src/features/ai-benchmark/core/filter";

// Pure-function tests for roster filtering (Phase 4 steps F-1/F-2). The harness filter keeps only
// models a harness exposes; the class filter keeps only models in a capability band; together they
// intersect. A model's band is a property of the FULL roster (roster-relative normalization), so
// the class filter is computed over the whole dataset, not the already-filtered subset. See
// `plans/done/2026-07-30__ayokoding-www-tools-ai-benchmark/prd.md` AC-23/AC-24/AC-25.

// ─── Fixture builders ──────────────────────────────────────────────────────────

function modelWith(id: string, harnesses: HarnessId[]): Model {
  return { id, name: id, vendor: "Test", harnesses, figures: [], pricing: {} };
}

function datasetOf(models: Model[]): Dataset {
  return { snapshotDate: "2026-07-28", anchorIds: { opus: "opus-anchor", sonnet: "sonnet-anchor" }, models };
}

const NONE: FilterState = {};

// ─── Harness filter (no band computation needed) ───────────────────────────────

describe("filterModels — harness filter narrows to models that harness exposes", () => {
  const ds = datasetOf([
    modelWith("a", ["claude-code", "cursor"]),
    modelWith("b", ["cursor", "opencode-zen"]),
    modelWith("c", ["opencode-go", "opencode-zen"]),
  ]);

  it("keeps only models whose harnesses include the selected harness", () => {
    expect(filterModels(ds, { harness: "cursor" }).map((m) => m.id)).toEqual(["a", "b"]);
    expect(filterModels(ds, { harness: "opencode-go" }).map((m) => m.id)).toEqual(["c"]);
  });

  it("an empty filter state returns every model", () => {
    expect(filterModels(ds, NONE).map((m) => m.id)).toEqual(["a", "b", "c"]);
  });
});

// ─── Class filter + intersection (cross-checked against computeGroups) ─────────

describe("filterModels — class filter narrows to a capability band over the full roster", () => {
  const groups = computeGroups(dataset);
  const bandIds = (band: keyof ReturnType<typeof computeGroups>) => groups[band].map((s) => s.model.id);

  it("a class filter returns exactly the models computeGroups placed in that band", () => {
    for (const band of ["opus", "sonnet", "haiku", "unrated"] as const) {
      const got = filterModels(dataset, { class: band })
        .map((m) => m.id)
        .sort();
      const want = [...bandIds(band)].sort();
      expect(got, `class=${band}`).toEqual(want);
    }
  });
});

describe("filterModels — harness and class parameters intersect", () => {
  const groups = computeGroups(dataset);
  const opusIds = new Set(groups.opus.map((s) => s.model.id));

  it("both filters together keep only opus-band models that the harness exposes", () => {
    const got = filterModels(dataset, { harness: "cursor", class: "opus" });
    for (const m of got) {
      expect(m.harnesses, `${m.id} must be exposed by cursor`).toContain("cursor");
      expect(opusIds.has(m.id), `${m.id} must be in the opus band`).toBe(true);
    }
    // And it is exactly the intersection (no omissions).
    const expected = dataset.models
      .filter((m) => m.harnesses.includes("cursor") && opusIds.has(m.id))
      .map((m) => m.id)
      .sort();
    expect(got.map((m) => m.id).sort()).toEqual(expected);
  });

  it("a filter combination matching no model returns an empty list (no error)", () => {
    // opencode-go carries no opus-band model in the live roster (cursor/zen carry the frontier).
    const got = filterModels(dataset, { harness: "opencode-go", class: "opus" });
    expect(got).toEqual([]);
  });
});
