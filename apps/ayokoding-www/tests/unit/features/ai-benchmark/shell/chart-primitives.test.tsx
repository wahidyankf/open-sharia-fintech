// AI BENCHMARK — shared chart primitives (Phase 6, A-1/A-2; Phase 7, Y-11).
//
// `scaleLinear` is the one place either chart converts a domain value (a composite index or a
// price) into a pixel offset. This RED anchor pins its contract BEFORE `chart-primitives.tsx`
// exists: `scaleLinear(domainMax, pixelWidth)` returns a function mapping `0 → 0`,
// `domainMax → pixelWidth`, and monotonically increasing in between — so a caller can trust that
// a larger domain value always produces a longer (or equal) bar.
//
// `bandLabel` (a Y-11 refactor target, hoisted here from both retired charts' identical local
// copies) gets its own direct tests too. `Axis`, `Bar`, `BandGroup`, `TickRow`, and `evenTicks`
// (the SVG-only primitives this file used to export) were deleted in Phase 5 (DD-32) once the DOM
// rewrite left them with zero consumers; their own tests were deleted with them.

import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import {
  Legend,
  bandBarBgClass,
  bandInkTextClass,
  bandLabel,
  bandSwatchClass,
  scaleLinear,
} from "../../../../../src/features/ai-benchmark/shell/chart-primitives";
import { COMPOSITE_INDEX_MAX } from "../../../../../src/features/ai-benchmark/core/score";
import type { ChartBand } from "../../../../../src/features/ai-benchmark/shell/chart-primitives";

const ALL_BANDS: readonly ChartBand[] = ["opus", "sonnet", "haiku", "unrated"];

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

// Characterization (cycle 4.1, DD-25) — pins the specific `scaleLinear(COMPOSITE_INDEX_MAX, 100)`
// call Phase 5's DOM bar rendering will make: with a pixel width of exactly 100, `scaleLinear`
// degenerates into a PERCENTAGE scale (a bar's inline `width` style becomes a `${n}%` string). This
// is a characterization test, not a RED — `scaleLinear`'s existing contract already satisfies it,
// so these assertions are expected to PASS immediately, confirming `tech-docs.md` DD-25's assumption
// rather than driving new production code.
describe("scaleLinear — percentage contract (DD-25)", () => {
  it("maps the domain maximum to 100", () => {
    const scale = scaleLinear(COMPOSITE_INDEX_MAX, 100);
    expect(scale(COMPOSITE_INDEX_MAX)).toBe(100);
  });

  it("maps the midpoint to 50", () => {
    const scale = scaleLinear(COMPOSITE_INDEX_MAX, 100);
    expect(scale(COMPOSITE_INDEX_MAX / 2)).toBe(50);
  });

  it("maps 0 to 0", () => {
    const scale = scaleLinear(COMPOSITE_INDEX_MAX, 100);
    expect(scale(0)).toBe(0);
  });

  it("maps every value to 0 when domainMax is non-positive", () => {
    const scale = scaleLinear(0, 100);
    expect(scale(0)).toBe(0);
    expect(scale(COMPOSITE_INDEX_MAX)).toBe(0);
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

// Cycle 4.2 — DOM band class-map helpers. Exempt from Gherkin tagging (pure plumbing, no
// user-observable behaviour of its own); consumed by cycle 5.1's behaviour-bound `BarRow`.
describe("bandBarBgClass", () => {
  it("returns the bg-[var(--chart-band-ID)] class string for every band", () => {
    for (const band of ALL_BANDS) {
      expect(bandBarBgClass(band)).toBe(`bg-[var(--chart-band-${band})]`);
    }
  });
});

describe("bandInkTextClass", () => {
  it("returns the text-[var(--chart-band-ID-ink)] class string for every band", () => {
    for (const band of ALL_BANDS) {
      expect(bandInkTextClass(band)).toBe(`text-[var(--chart-band-${band}-ink)]`);
    }
  });
});

// `Legend` (used by `how-to-read.tsx`) is the one consumer of `bandSwatchClass` — neither had a
// direct render test.
describe("Legend", () => {
  it("renders each item's label and colours its swatch via bandSwatchClass", () => {
    render(
      <Legend
        items={[
          { band: "opus", label: "Opus" },
          { band: "sonnet", label: "Sonnet" },
        ]}
      />,
    );

    expect(screen.getByText("Opus")).toBeDefined();
    expect(screen.getByText("Sonnet")).toBeDefined();

    const swatches = document.querySelectorAll('[data-slot="chart-legend-item"] span[aria-hidden="true"]');
    expect(swatches).toHaveLength(2);
    expect(swatches[0]?.className).toContain(bandSwatchClass("opus"));
    expect(swatches[1]?.className).toContain(bandSwatchClass("sonnet"));
  });
});
