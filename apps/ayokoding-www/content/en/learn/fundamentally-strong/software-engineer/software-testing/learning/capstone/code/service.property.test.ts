// Capstone Step 3 (TS half): the SAME order-independence invariant, checked with fast-check.
//
// Mirrors test_service_property.py's Hypothesis test -- computeSubtotal() must return the
// SAME total regardless of the price list's order, checked over MANY fast-check-generated
// lists rather than a few hand-picked ones. Run standalone with `npx vitest run` (verified
// against fast-check 4.9.0 + Vitest 4.1.10 in an isolated scratch env, not this repo's own
// dependency pins -- run `npm install fast-check` first to try this file here).

import { describe, expect, it } from "vitest";
import fc from "fast-check";

function computeSubtotal(prices: number[]): number {
  // => the SAME correct logic as service.py's compute_subtotal() -- order-independent by construction
  const total = prices.reduce((sum, price) => sum + price, 0);
  return Math.round(total * 100) / 100; // => rounds to cents, matching Python's round(x, 2) behavior
}

describe("computeSubtotal order independence", () => {
  it("returns the same total regardless of price order", () => {
    fc.assert(
      // => co-18/co-20 (TS side): fast-check GENERATES many price arrays, not hand-picked ones
      fc.property(fc.array(fc.float({ min: 0, max: 1000, noNaN: true }), { maxLength: 10 }), (prices) => {
        const forward = computeSubtotal(prices); // => the ORIGINAL order
        const reversedTotal = computeSubtotal([...prices].reverse()); // => the SAME items, REVERSED
        expect(forward).toBeCloseTo(reversedTotal, 2); // => co-18: the invariant, checked every run
      }),
    );
  });
});
