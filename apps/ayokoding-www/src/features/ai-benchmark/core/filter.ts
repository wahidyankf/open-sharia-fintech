// AI BENCHMARK — roster filtering core (Phase 4, steps F-1/F-2).
//
// Narrows the roster by an optional harness filter and an optional class (band) filter, combined
// as an intersection. A model's band is a property of the FULL roster (the composite index is
// roster-relative per DD-5a), so the class filter is computed over the whole dataset, not the
// already-filtered subset. Unknown filter values never reach this module — they are sanitized to
// "unfiltered" by `url-state.ts` (F-5/F-6), so this selector only ever sees known values. No
// React, no router, no side effects. See prd.md AC-23/AC-24/AC-25/AC-26.

import type { Dataset, HarnessId, Model } from "./data/models";
import { computeGroups, type Band } from "./bands";

/**
 * The canonical known-value lists for the two filter axes (F-9). These are the SINGLE source of
 * truth — `url-state.ts` imports them for validation, and a future filter UI would import them
 * for its dropdown options — so a new harness id or band is added in exactly one place.
 */
export const HARNESS_IDS: readonly HarnessId[] = ["claude-code", "codex-cli", "cursor", "opencode-go", "opencode-zen"];

export const BANDS: readonly Band[] = ["opus", "sonnet", "haiku", "unrated"];

/** Type guard: is `v` one of the known harness ids? */
export function isKnownHarness(v: string): v is HarnessId {
  return (HARNESS_IDS as readonly string[]).includes(v);
}

/** Type guard: is `v` one of the known capability bands? */
export function isKnownBand(v: string): v is Band {
  return (BANDS as readonly string[]).includes(v);
}

/**
 * Filter state for the roster. Either field may be omitted (= that axis is unfiltered). The two
 * axes intersect: a model must satisfy BOTH to be kept.
 */
export type FilterState = {
  /** Keep only models this harness exposes; `undefined` = no harness filter. */
  harness?: HarnessId;
  /** Keep only models in this capability band; `undefined` = no class filter. */
  class?: Band;
};

/**
 * Narrow `dataset.models` by the harness and class filters (intersection). With neither filter
 * set, every roster model is returned. A filter combination matching no model returns `[]` (the
 * caller renders the explicit empty state — never an error).
 *
 * The class filter is derived from {@link computeGroups} over the full dataset so a model's band
 * is roster-relative regardless of what the harness filter removed.
 */
export function filterModels(dataset: Dataset, state: FilterState): Model[] {
  const harness = state.harness;
  const classFilter = state.class;

  // Build the model→band lookup only when a class filter is actually set.
  let bandById: Map<string, Band> | undefined;
  if (classFilter !== undefined) {
    bandById = new Map();
    for (const group of Object.values(computeGroups(dataset))) {
      for (const s of group) {
        bandById.set(s.model.id, s.band);
      }
    }
  }

  return dataset.models.filter((m) => {
    if (harness !== undefined && !m.harnesses.includes(harness)) {
      return false;
    }
    if (classFilter !== undefined && bandById?.get(m.id) !== classFilter) {
      return false;
    }
    return true;
  });
}
