import { describe, expect, it } from "vitest";
import {
  OPUS_ANCHOR_ID,
  SONNET_ANCHOR_ID,
  dataset,
  type Dataset,
  type HarnessId,
  type Model,
} from "../../../../../src/features/ai-benchmark/core/data/models";
import {
  type AnchorIndices,
  type Band,
  type BandGroups,
  type IndexMap,
  type ModelScore,
  anchors,
  assignBand,
  computeGroups,
} from "../../../../../src/features/ai-benchmark/core/bands";

// Pure-function tests for band assignment (Phase 4 steps B-1..B-13). Band rules are specified by
// `plans/done/2026-07-30__ayokoding-www-tools-ai-benchmark/tech-docs.md` §"Band assignment" (the
// state diagram with anchor pinning) and §"DD-20a". Fixtures give known indices so the rule —
// not the dataset — is what is asserted (a data refresh must not red the suite).

// ─── Fixture builders ──────────────────────────────────────────────────────────

function model(id: string): Model {
  return { id, name: id, vendor: "Test", harnesses: ["claude-code"], figures: [], pricing: {} };
}

// Synthetic anchor thresholds detached from the live dataset.
const SYNTH_ANCHORS: AnchorIndices = { opus: 90, sonnet: 70 };

function withIndex(m: Model, index: number | undefined): IndexMap {
  return { [m.id]: index };
}

// ─── B-1 / B-2 — opus comparison ───────────────────────────────────────────────

describe("assignBand — a model reaching the opus anchor index is opus", () => {
  it("assigns opus when the index equals the opus anchor index", () => {
    const m = model("at-opus");
    expect(assignBand(m, withIndex(m, 90), SYNTH_ANCHORS)).toBe("opus");
  });

  it("assigns opus when the index exceeds the opus anchor index", () => {
    const m = model("above-opus");
    expect(assignBand(m, withIndex(m, 99), SYNTH_ANCHORS)).toBe("opus");
  });
});

// ─── B-3 / B-4 — sonnet comparison ─────────────────────────────────────────────

describe("assignBand — a model between the two anchors is sonnet", () => {
  it("assigns sonnet when above the sonnet anchor and below the opus anchor", () => {
    const m = model("between");
    expect(assignBand(m, withIndex(m, 80), SYNTH_ANCHORS)).toBe("sonnet");
  });

  it("assigns sonnet at exactly the sonnet anchor index", () => {
    const m = model("at-sonnet");
    expect(assignBand(m, withIndex(m, 70), SYNTH_ANCHORS)).toBe("sonnet");
  });
});

// ─── B-5 / B-6 — haiku fallthrough ─────────────────────────────────────────────

describe("assignBand — a model below the sonnet anchor is haiku", () => {
  it("assigns haiku when the index is below the sonnet anchor index", () => {
    const m = model("below-sonnet");
    expect(assignBand(m, withIndex(m, 40), SYNTH_ANCHORS)).toBe("haiku");
  });

  it("assigns haiku at index zero (rated but lowest)", () => {
    const m = model("floor");
    expect(assignBand(m, withIndex(m, 0), SYNTH_ANCHORS)).toBe("haiku");
  });
});

// ─── B-7 / B-8 — anchor pinning by id ──────────────────────────────────────────

describe("assignBand — anchors are pinned by id regardless of arithmetic", () => {
  // Perverse fixture: the opus anchor's own index (50) falls BELOW the sonnet anchor's (90).
  // Pinning must still place each anchor in the band it defines.
  const perverse: AnchorIndices = { opus: 50, sonnet: 90 };
  const opusAnchor = model(OPUS_ANCHOR_ID);
  const sonnetAnchor = model(SONNET_ANCHOR_ID);

  it("the opus anchor belongs to opus even when its index is below the sonnet anchor's", () => {
    const indices: IndexMap = { [OPUS_ANCHOR_ID]: 50, [SONNET_ANCHOR_ID]: 90 };
    expect(assignBand(opusAnchor, indices, perverse)).toBe("opus");
  });

  it("the sonnet anchor belongs to sonnet even when its index is above the opus anchor's", () => {
    const indices: IndexMap = { [OPUS_ANCHOR_ID]: 50, [SONNET_ANCHOR_ID]: 90 };
    expect(assignBand(sonnetAnchor, indices, perverse)).toBe("sonnet");
  });

  it("a non-anchor with no index is unrated", () => {
    const m = model("no-score");
    expect(assignBand(m, { [m.id]: undefined }, SYNTH_ANCHORS)).toBe("unrated");
    expect(assignBand(m, {}, SYNTH_ANCHORS)).toBe("unrated");
  });
});

// ─── B-9 / B-10 — totality over the real roster ────────────────────────────────

describe("computeGroups — every roster model belongs to exactly one capability group", () => {
  const groups = computeGroups(dataset);
  const allGroups: Array<[Band, ModelScore[]]> = [
    ["opus", groups.opus],
    ["sonnet", groups.sonnet],
    ["haiku", groups.haiku],
    ["unrated", groups.unrated],
  ];
  const everyone = allGroups.flatMap(([, ms]) => ms);

  it("the four groups are disjoint and cover the whole roster with no omissions or duplicates", () => {
    const ids = everyone.map((s) => s.model.id);
    expect(new Set(ids).size, "no duplicate model across the four bands").toBe(ids.length);
    expect(ids.length, "every roster model is placed").toBe(dataset.models.length);
    const rosterIds = new Set(dataset.models.map((m) => m.id));
    for (const id of ids) {
      expect(rosterIds.has(id), `placed id "${id}" must be a real roster model`).toBe(true);
    }
  });

  it("each ModelScore carries the band it was grouped under", () => {
    for (const [band, ms] of allGroups) {
      for (const s of ms) {
        expect(s.band).toBe(band);
      }
    }
  });

  it("sanity — the two anchors pin to their bands and a zero-figure model is unrated", () => {
    const byId = new Map(everyone.map((s) => [s.model.id, s.band]));
    expect(byId.get(OPUS_ANCHOR_ID)).toBe("opus");
    expect(byId.get(SONNET_ANCHOR_ID)).toBe("sonnet");
    expect(byId.get("cursor-composer-2.5")).toBe("unrated");
  });
});

// ─── B-11 / B-12 — canonical per-band ordering ─────────────────────────────────

describe("computeGroups — models are ordered identically within a band (descending index, then id)", () => {
  const groups: BandGroups = computeGroups(dataset);

  // The canonical comparator: descending index (undefined last), then ascending id. The merged
  // chart consumes this same per-band list, so this property IS the "canonical order" guarantee (AC-11).
  function assertCanonical(band: ModelScore[], allowUndefinedIndex: boolean) {
    for (let i = 1; i < band.length; i++) {
      const prev = band[i - 1];
      const curr = band[i];
      if (prev === undefined || curr === undefined) continue; // unreachable: i within bounds
      const pi = prev.index ?? -Infinity;
      const ci = curr.index ?? -Infinity;
      if (pi !== ci) {
        expect(pi, `${prev.model.id} should outrank ${curr.model.id} by index`).toBeGreaterThan(ci);
      } else {
        expect(
          prev.model.id <= curr.model.id,
          `tie on index: ${prev.model.id} should sort at-or-before ${curr.model.id} by id`,
        ).toBe(true);
        if (!allowUndefinedIndex) {
          expect(prev.index).toBeDefined();
          expect(curr.index).toBeDefined();
        }
      }
    }
  }

  it("opus / sonnet / haiku bands are ordered by descending index then ascending id", () => {
    assertCanonical(groups.opus, false);
    assertCanonical(groups.sonnet, false);
    assertCanonical(groups.haiku, false);
  });

  it("the unrated band (all undefined index) is ordered by ascending id", () => {
    for (const s of groups.unrated) {
      expect(s.index, "unrated models carry no composite index").toBeUndefined();
    }
    assertCanonical(groups.unrated, true);
  });

  it("the per-band order is stable across repeated calls (one canonical list)", () => {
    const again = computeGroups(dataset);
    expect(again.opus.map((s) => s.model.id)).toEqual(groups.opus.map((s) => s.model.id));
    expect(again.haiku.map((s) => s.model.id)).toEqual(groups.haiku.map((s) => s.model.id));
    expect(again.unrated.map((s) => s.model.id)).toEqual(groups.unrated.map((s) => s.model.id));
  });
});

// ─── B-13 — anchors(dataset) helper ────────────────────────────────────────────

describe("anchors — single helper deriving the anchor ids + threshold indices", () => {
  it("returns the opus and sonnet anchor composite indices for the live dataset", () => {
    const a = anchors(dataset);
    expect(a.opus).not.toBeUndefined();
    expect(a.sonnet).not.toBeUndefined();
    // Opus 5 (swe-v 96 roster-max → rel 100 @ weight 25; gpqa 93.2/94.1 → rel ~99.04 @ weight 30)
    // sits above Sonnet 5 (three sub-100 rels) — the opus threshold is the higher one.
    expect(a.opus as number).toBeGreaterThan(a.sonnet as number);
  });

  it("is finite (never NaN) — anchors are rated models with full indices", () => {
    const a = anchors(dataset);
    expect(Number.isFinite(a.opus)).toBe(true);
    expect(Number.isFinite(a.sonnet)).toBe(true);
  });
});

// ─── Regression: a harness filter excluding both anchors must not collapse rated models to `haiku`
// (pr-review-synthesis-maker CRITICAL finding on PR #118, benchmark-content.tsx:28) ───────────────
//
// `codex-cli` and `opencode-go` are the two harnesses that expose neither `claude-opus-5` nor
// `claude-sonnet-5` (see `core/data/models.ts`). Before this fix, `computeGroups` re-derived the
// anchor thresholds from whatever `dataset` it was handed — so a harness-filtered `Dataset` with
// both anchors excluded made `anchorIndices.opus`/`.sonnet` both `undefined`, and every surviving
// rated model silently fell through to `haiku`. The fix is the `fullDataset` parameter: thresholds
// are ALWAYS derived from it (defaulting to `dataset` itself), independent of what subset is being
// displayed.

function bandById(groups: BandGroups): Map<string, Band> {
  const byId = new Map<string, Band>();
  for (const list of [groups.opus, groups.sonnet, groups.haiku, groups.unrated]) {
    for (const s of list) {
      byId.set(s.model.id, s.band);
    }
  }
  return byId;
}

describe("computeGroups — a harness filter that excludes both anchors keeps every rated model's full-roster band", () => {
  const fullRosterBand = bandById(computeGroups(dataset));

  function assertHarnessPreservesRatedBands(harness: HarnessId) {
    const filteredModels = dataset.models.filter((m) => m.harnesses.includes(harness));

    // Sanity: this harness really does reproduce the bug's precondition — it excludes BOTH
    // anchors, which is exactly what made the pre-fix `anchorIndices` collapse to `undefined`.
    expect(
      filteredModels.some((m) => m.id === OPUS_ANCHOR_ID),
      `${harness} must exclude the opus anchor`,
    ).toBe(false);
    expect(
      filteredModels.some((m) => m.id === SONNET_ANCHOR_ID),
      `${harness} must exclude the sonnet anchor`,
    ).toBe(false);

    const ratedSurvivors = filteredModels.filter(
      (m) => fullRosterBand.get(m.id) === "opus" || fullRosterBand.get(m.id) === "sonnet",
    );
    expect(ratedSurvivors.length, `${harness} must still expose at least one opus/sonnet model`).toBeGreaterThan(0);

    const filteredDataset: Dataset = { ...dataset, models: filteredModels };
    // THE FIX: pass the full unfiltered dataset as the second argument so thresholds never shift.
    const filteredBand = bandById(computeGroups(filteredDataset, dataset));

    for (const m of ratedSurvivors) {
      expect(
        filteredBand.get(m.id),
        `${m.id} must keep its full-roster band ("${fullRosterBand.get(m.id)}") under the ${harness} filter`,
      ).toBe(fullRosterBand.get(m.id));
    }
  }

  it("codex-cli: gpt-5.6-sol/terra/luna keep their opus/sonnet bands instead of collapsing to haiku", () => {
    assertHarnessPreservesRatedBands("codex-cli");
  });

  it("opencode-go: the harness's rated survivors keep their opus/sonnet bands instead of collapsing to haiku", () => {
    assertHarnessPreservesRatedBands("opencode-go");
  });

  it("WITHOUT the fullDataset override, the bug reproduces — the same rated models collapse to haiku", () => {
    const filteredModels = dataset.models.filter((m) => m.harnesses.includes("codex-cli"));
    const filteredDataset: Dataset = { ...dataset, models: filteredModels };
    // No second argument — the pre-fix call shape. Documents the bug this fix closes; must stay
    // red if a future change reintroduces a same-dataset default that silently "fixes" this
    // assertion instead of the real call sites.
    const collapsedBand = bandById(computeGroups(filteredDataset));
    const ratedSurvivorIds = filteredModels
      .map((m) => m.id)
      .filter((id) => fullRosterBand.get(id) === "opus" || fullRosterBand.get(id) === "sonnet");
    expect(ratedSurvivorIds.length).toBeGreaterThan(0);
    for (const id of ratedSurvivorIds) {
      expect(collapsedBand.get(id), `${id} collapses to haiku when no fullDataset is supplied`).toBe("haiku");
    }
  });
});
