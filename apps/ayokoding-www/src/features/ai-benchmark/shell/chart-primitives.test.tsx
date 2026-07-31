// AI BENCHMARK — shared chart primitives (Phase 6, A-1/A-2; Phase 7, Y-11).
//
// `scaleLinear` is the one place either chart converts a domain value (a composite index or a
// price) into a pixel offset. This RED anchor pins its contract BEFORE `chart-primitives.tsx`
// exists: `scaleLinear(domainMax, pixelWidth)` returns a function mapping `0 → 0`,
// `domainMax → pixelWidth`, and monotonically increasing in between — so a caller can trust that
// a larger domain value always produces a longer (or equal) bar.
//
// `evenTicks` and `bandLabel` (Y-11 refactor targets, hoisted here from both charts' identical
// local copies) get their own direct tests too.

import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { bandLabel, evenTicks, scaleLinear, TickRow } from "./chart-primitives";

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

describe("evenTicks", () => {
  it("returns count + 1 evenly spaced values from 0 to max, inclusive", () => {
    expect(evenTicks(100, 5)).toEqual([0, 20, 40, 60, 80, 100]);
  });

  it("reproduces the capability chart's fixed-20-unit-interval ticks over its 0-100 domain", () => {
    // Pins the Y-11 refactor's own claim: hoisting the generator changes WHERE it lives, not the
    // tick VALUES either chart renders.
    expect(evenTicks(100, 5)).toEqual([0, 20, 40, 60, 80, 100]);
  });

  it("degenerates to a single zero tick for a non-positive max or count", () => {
    expect(evenTicks(0, 5)).toEqual([0]);
    expect(evenTicks(100, 0)).toEqual([0]);
  });
});

describe("bandLabel", () => {
  it("resolves each known band to its localized class-name label", () => {
    expect(bandLabel("opus", "en")).toBe("Opus");
    expect(bandLabel("sonnet", "en")).toBe("Sonnet");
    expect(bandLabel("haiku", "en")).toBe("Haiku");
    expect(bandLabel("unrated", "en")).toBe("Unrated");
  });

  it("resolves identical copy per locale for haiku, a model-tier proper noun like opus/sonnet", () => {
    // All three rated labels ("Opus"/"Sonnet"/"Haiku") are proper nouns and are therefore
    // identical in both locales — unlike "unrated", which still translates ("Unrated"/"Belum
    // dinilai").
    expect(bandLabel("haiku", "id")).toBe(bandLabel("haiku", "en"));
  });
});

describe("TickRow", () => {
  it("renders one text element per value, each carrying the formatted value as testid and text", () => {
    render(
      <svg>
        <TickRow
          testId="chart-ticks"
          tickTestId="chart-tick"
          values={[0, 50, 100]}
          x={(v) => v * 2}
          y={10}
          format={(v) => `${v}%`}
        />
      </svg>,
    );
    const row = screen.getByTestId("chart-ticks");
    expect(row.querySelectorAll("text").length).toBe(3);
    expect(screen.getByTestId("chart-tick-0").textContent).toBe("0%");
    expect(screen.getByTestId("chart-tick-100").textContent).toBe("100%");
  });
});
