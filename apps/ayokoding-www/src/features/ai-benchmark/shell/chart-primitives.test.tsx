// AI BENCHMARK — shared chart primitives (Phase 6, A-1/A-2).
//
// `scaleLinear` is the one place either chart converts a domain value (a composite index or a
// price) into a pixel offset. This RED anchor pins its contract BEFORE `chart-primitives.tsx`
// exists: `scaleLinear(domainMax, pixelWidth)` returns a function mapping `0 → 0`,
// `domainMax → pixelWidth`, and monotonically increasing in between — so a caller can trust that
// a larger domain value always produces a longer (or equal) bar.

import { describe, expect, it } from "vitest";
import { scaleLinear } from "./chart-primitives";

describe("scaleLinear", () => {
  it("maps 0 to 0", () => {
    const scale = scaleLinear(100, 400);
    expect(scale(0)).toBe(0);
  });

  it("maps the domain maximum to the pixel width", () => {
    const scale = scaleLinear(100, 400);
    expect(scale(100)).toBe(400);
  });

  it("is monotonic in between", () => {
    const scale = scaleLinear(100, 400);
    const samples = [0, 10, 25, 50, 75, 99, 100];
    for (let i = 1; i < samples.length; i++) {
      const prev = samples[i - 1]!;
      const curr = samples[i]!;
      expect(scale(curr)).toBeGreaterThanOrEqual(scale(prev));
    }
  });

  it("scales proportionally for an arbitrary domain and width", () => {
    const scale = scaleLinear(50, 200);
    expect(scale(25)).toBe(100); // half the domain → half the pixel width
  });

  it("degenerates to always-zero when the domain maximum is zero or negative", () => {
    const scale = scaleLinear(0, 400);
    expect(scale(0)).toBe(0);
    expect(scale(10)).toBe(0);
  });
});
