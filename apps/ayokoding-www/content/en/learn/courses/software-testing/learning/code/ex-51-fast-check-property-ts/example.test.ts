// learning/code/ex-51-fast-check-property-ts/example.test.ts
// Example 51: A Round-Trip Property in fast-check (TS).

import { describe, expect, it } from "vitest"; // => Vitest -- verified against 4.1.10 in an isolated scratch env (this repo's own Vitest pin is 4.1.0, compatible)
import fc from "fast-check"; // => fast-check 4.9.0 -- TS's property-based testing library (co-18/co-20 counterpart to Hypothesis); not a dependency of this repo -- run `npm install fast-check` to try this file here

// encode/decode mirror ex-44's Python round-trip pair exactly, using base64 instead of utf-8 bytes
function encode(text: string): string {
  // => converts an arbitrary string to a base64-encoded string
  return Buffer.from(text, "utf-8").toString("base64"); // => a REAL, standard encoding, not a toy transform
} // => encode() is pure -- same input always yields the same base64 output, no side effects

function decode(encoded: string): string {
  // => the INVERSE of encode above
  return Buffer.from(encoded, "base64").toString("utf-8"); // => decodes back to the original text
} // => decode() mirrors encode() exactly -- together they form the round-trip pair under test

describe("round-trip property", () => {
  // => groups the single property test below under a readable suite name
  it("decode(encode(x)) === x for any generated string", () => {
    // => the property under test, stated in plain English
    // fc.assert runs the property below over MANY generated strings (co-18), analogous
    // to Hypothesis's @given -- fc.property() wraps the invariant, fc.string() is the strategy (co-20)
    fc.assert(
      // => runs the property check below (default: 100 generated cases)
      fc.property(fc.string(), (original) => {
        // => fc.string() is the strategy -- generates arbitrary strings
        // => original is a freshly GENERATED string each run, not a hand-picked example
        const roundTripped = decode(encode(original)); // => act: encode then immediately decode
        expect(roundTripped).toBe(original); // => the invariant: nothing lost or corrupted in the round trip
      }),
    ); // => fc.assert throws (and Vitest reports a failure) only if a counterexample is found
  });
});
