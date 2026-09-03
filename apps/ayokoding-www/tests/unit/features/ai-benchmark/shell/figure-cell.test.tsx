// AI BENCHMARK — FigureCell layout prop tests (Phase 6, DD-34 Treatment 2, AC-62).
//
// The default MUST stay "stacked" (DD-27's "the table must fit below lg" precondition depends on
// it); "inline" is opt-in for the roster card/table detail region's rail rows only.

import { describe, it, expect, afterEach } from "vitest";
import { cleanup, render } from "@testing-library/react";
import { FigureCell } from "../../../../../src/features/ai-benchmark/shell/figure-cell";

const BASE_PROPS = {
  value: "42%",
  grade: "verified" as const,
  source: "https://example.com",
  locale: "en" as const,
};

describe("FigureCell — layout prop (AC-62)", () => {
  afterEach(() => {
    cleanup();
  });

  it("defaults to the stacked layout when layout is omitted", () => {
    render(<FigureCell {...BASE_PROPS} />);
    const el = document.querySelector('[data-slot="figure-cell"]');
    expect(el?.className).toContain("flex-col");
    expect(el?.className).not.toContain("flex-row");
  });

  it('emits flex-row when layout="inline"', () => {
    render(<FigureCell {...BASE_PROPS} layout="inline" />);
    const el = document.querySelector('[data-slot="figure-cell"]');
    expect(el?.className).toContain("flex-row");
    expect(el?.className).not.toContain("flex-col");
  });
});
