// AI BENCHMARK — band assignment core (Phase 4, steps B-1..B-13).
//
// Implements the class-band decision from
// `plans/done/2026-07-30__ayokoding-www-tools-ai-benchmark/tech-docs.md` §"Band assignment" (the
// state diagram with anchor pinning) and §"DD-20a". No React, no router, no side effects.
//
// Bands: `opus` | `sonnet` | `light` | `unrated`. The two anchors (Claude Opus 5, Claude Sonnet 5)
// DEFINE the bands and are PINNED by id — they always occupy their own band even if arithmetic
// would place them elsewhere. Every other model is compared against the anchors' own full
// composite indices (DD-20a): at/above opus → opus, at/above sonnet → sonnet, else light. A model
// with no composite index (zero coverage) is unrated.

import { OPUS_ANCHOR_ID, SONNET_ANCHOR_ID, type Dataset, type Model } from "./data/models";
import { computeIndex, computeRosterMaxes, coverage, type RosterMaxes } from "./score";

/** The four capability classes. */
export type Band = "opus" | "sonnet" | "light" | "unrated";

/** Per-model composite index lookup; `undefined` = no index (unrated). */
export type IndexMap = Record<string, number | undefined>;

/** The two anchor indices that define the opus/sonnet thresholds (DD-20a). */
export type AnchorIndices = {
  opus: number | undefined;
  sonnet: number | undefined;
};

/** A model scored and placed in a band — the unit both charts consume. */
export type ModelScore = {
  model: Model;
  /** Composite index; `undefined` for an unrated (zero-coverage) model. */
  index: number | undefined;
  /** Coverage ratio `W(m) / 100`. */
  coverage: number;
  band: Band;
};

/** The four disjoint, canonically ordered capability groups. */
export type BandGroups = {
  opus: ModelScore[];
  sonnet: ModelScore[];
  light: ModelScore[];
  unrated: ModelScore[];
};

/**
 * Assign a model to exactly one band.
 *
 * Order (mirrors the band-assignment state diagram):
 *   1. Anchor pinning — each anchor occupies the band it defines, by id, regardless of arithmetic.
 *   2. No composite index (zero coverage) → `unrated`.
 *   3. `index ≥ opus anchor index` → `opus`.
 *   4. `index ≥ sonnet anchor index` → `sonnet`.
 *   5. otherwise → `light`.
 *
 * Pinning is checked BEFORE the zero-coverage branch so an anchor always lands in its own band
 * even in the degenerate case where an anchor happened to carry no composite figure — the bands
 * are defined by these models, so they cannot fall out of their own band.
 *
 * @param model          The model to place (its `id` selects anchor pinning).
 * @param indices        Per-model composite index map; `indices[model.id]` is this model's index
 *                       (`undefined` or missing = unrated).
 * @param anchorIndices  The two anchor indices (the thresholds).
 */
export function assignBand(model: Model, indices: IndexMap, anchorIndices: AnchorIndices): Band {
  // 1. Anchor pinning by id (B-7 / B-8).
  if (model.id === OPUS_ANCHOR_ID) {
    return "opus";
  }
  if (model.id === SONNET_ANCHOR_ID) {
    return "sonnet";
  }
  // 2. Zero coverage → no composite index → unrated.
  const index = indices[model.id] ?? undefined;
  if (index === undefined) {
    return "unrated";
  }
  // 3-5. Threshold comparison against the anchors' own full indices (DD-20a).
  if (anchorIndices.opus !== undefined && index >= anchorIndices.opus) {
    return "opus";
  }
  if (anchorIndices.sonnet !== undefined && index >= anchorIndices.sonnet) {
    return "sonnet";
  }
  return "light";
}

/**
 * The two anchor composite indices for a dataset — the single place the thresholds are derived
 * (B-13), so no caller re-derives them. Computes the roster-max map once, then each anchor's full
 * index over the benchmarks it actually has (DD-20a: thresholds are the anchors' OWN indices, not
 * a like-for-like subset).
 */
export function anchors(dataset: Dataset): AnchorIndices {
  return anchorIndices(dataset, computeRosterMaxes(dataset));
}

/** Internal: anchor indices from a precomputed roster-max map (reused by {@link computeGroups}). */
function anchorIndices(dataset: Dataset, maxes: RosterMaxes): AnchorIndices {
  const opusModel = dataset.models.find((m) => m.id === OPUS_ANCHOR_ID);
  const sonnetModel = dataset.models.find((m) => m.id === SONNET_ANCHOR_ID);
  return {
    opus: opusModel ? computeIndex(opusModel, maxes) : undefined,
    sonnet: sonnetModel ? computeIndex(sonnetModel, maxes) : undefined,
  };
}

/**
 * Canonical within-band ordering: descending composite index (undefined last), then ascending id.
 * Both charts consume the SAME per-band list produced here, so each band lists its models in the
 * same order in the capability chart and the price chart (AC-11).
 */
function compareForOrder(a: ModelScore, b: ModelScore): number {
  const ai = a.index ?? -Infinity;
  const bi = b.index ?? -Infinity;
  if (bi !== ai) {
    return bi - ai; // descending index
  }
  if (a.model.id < b.model.id) return -1; // ascending id
  if (a.model.id > b.model.id) return 1;
  return 0;
}

/**
 * Score every model in `dataset` and group it into one of the four disjoint, canonically ordered
 * capability bands (B-9..B-12). The four groups are disjoint and together cover exactly the models
 * in `dataset` — but the roster-max map and the two anchor threshold indices are ALWAYS derived
 * from `fullDataset` (defaulting to `dataset` itself when omitted), never from `dataset` alone.
 *
 * This matters whenever a caller passes an already-filtered subset as `dataset` (e.g. a harness
 * filter): a model's band is a property of the FULL roster (DD-5a — the composite index and the
 * anchor thresholds are roster-relative), so filtering must only govern which models are
 * displayed, never which models define the band boundaries. Passing the harness-filtered subset
 * as BOTH `dataset` and (implicitly) `fullDataset` reproduces the anchor-collapse bug: when the
 * filter excludes both `claude-opus-5` and `claude-sonnet-5`, the thresholds silently become
 * `undefined` and every surviving rated model falls through to `light`.
 */
export function computeGroups(dataset: Dataset, fullDataset: Dataset = dataset): BandGroups {
  const maxes = computeRosterMaxes(fullDataset);
  const anchorIdx = anchorIndices(fullDataset, maxes);
  const indices: IndexMap = {};
  for (const m of fullDataset.models) {
    indices[m.id] = computeIndex(m, maxes);
  }
  const scored: ModelScore[] = dataset.models.map((m) => ({
    model: m,
    index: indices[m.id] ?? undefined,
    coverage: coverage(m),
    band: assignBand(m, indices, anchorIdx),
  }));

  const groups: BandGroups = { opus: [], sonnet: [], light: [], unrated: [] };
  for (const s of scored) {
    groups[s.band].push(s);
  }
  groups.opus.sort(compareForOrder);
  groups.sonnet.sort(compareForOrder);
  groups.light.sort(compareForOrder);
  groups.unrated.sort(compareForOrder);
  return groups;
}
