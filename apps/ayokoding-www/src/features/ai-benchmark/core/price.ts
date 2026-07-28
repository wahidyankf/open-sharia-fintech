// AI BENCHMARK — harness price selection core (Phase 4, steps P-1..P-7).
//
// The price chart shows ONE rate per model: the selected harness's rate, or — with no harness
// filter — the lowest available harness rate. This module is the pure selector; it owns no UI.
// See `plans/in-progress/ayokoding-www-tools-ai-benchmark/prd.md` AC-16/AC-17/AC-18.
//
// Rules:
//   - With no harness filter, the lowest METERED rate wins (compare input, then output).
//   - A subscription-only model (no metered rate anywhere) returns its subscription — NEVER a
//     numeric zero and NEVER undefined-posing-as-zero (invariant 10).
//   - A model exposed by neither a metered nor a subscription rate returns undefined.
//   - With a harness filter, that harness's exact rate set is returned (metered or subscription),
//     or undefined when the model is not exposed by that harness.

import type { HarnessId, MeteredPrice, Model, SubscriptionPrice } from "./data/models";

/** A selected rate set: a metered per-token rate, a flat-rate subscription, or nothing. */
export type SelectedRate = MeteredPrice | SubscriptionPrice | undefined;

/** All metered rates a model exposes, paired with the harness that charges them. */
function meteredRates(model: Model): { harness: HarnessId; rate: MeteredPrice }[] {
  const out: { harness: HarnessId; rate: MeteredPrice }[] = [];
  for (const h of Object.keys(model.pricing) as HarnessId[]) {
    const p = model.pricing[h];
    if (p !== undefined && p.kind === "metered") {
      out.push({ harness: h, rate: p });
    }
  }
  return out;
}

/** The first subscription a model exposes (if any), paired with its harness. */
function firstSubscription(model: Model): { harness: HarnessId; rate: SubscriptionPrice } | undefined {
  for (const h of Object.keys(model.pricing) as HarnessId[]) {
    const p = model.pricing[h];
    if (p !== undefined && p.kind === "subscription") {
      return { harness: h, rate: p };
    }
  }
  return undefined;
}

/**
 * The lowest available rate for a model: the cheapest metered rate (by input, then output); if no
 * metered rate exists, a subscription; otherwise undefined. A subscription-only model therefore
 * resolves to its subscription — never a numeric zero.
 */
function pickLowest(model: Model): SelectedRate {
  const metered = meteredRates(model);
  if (metered.length > 0) {
    metered.sort((a, b) => a.rate.input - b.rate.input || a.rate.output - b.rate.output);
    // length > 0 guarantees a first element; the guard keeps the function total under
    // `noUncheckedIndexedAccess`.
    const lowest = metered[0];
    return lowest === undefined ? undefined : lowest.rate;
  }
  return firstSubscription(model)?.rate;
}

/**
 * The single internal selector both public functions delegate to (P-7 refactor). With a harness,
 * returns that harness's exact rate set (or undefined); without one, the lowest available rate.
 */
function selectRateSet(model: Model, harness?: HarnessId): SelectedRate {
  if (harness !== undefined) {
    return model.pricing[harness];
  }
  return pickLowest(model);
}

/**
 * The model's rate when no harness filter is applied — the lowest available harness rate
 * (cheapest metered by input then output, else its subscription). Undefined when the model has no
 * pricing at all.
 */
export function lowestRate(model: Model): SelectedRate {
  return selectRateSet(model);
}

/**
 * The rate a specific harness charges for the model, or undefined when the model is not exposed by
 * that harness. Returns the subscription when the harness carries the model on a flat-rate plan.
 */
export function rateForHarness(model: Model, harness: HarnessId): SelectedRate {
  return selectRateSet(model, harness);
}
