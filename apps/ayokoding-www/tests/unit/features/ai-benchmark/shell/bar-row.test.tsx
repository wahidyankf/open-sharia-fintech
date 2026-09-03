// AI BENCHMARK — DOM proportional-fill bar row (Phase 5, cycle 5.1, DD-25).
//
// RED anchor: `./bar-row` does not exist yet. `BarRow` is the DOM (non-SVG) replacement for the
// retired SVG `<Bar>` primitive — given a `value`/`max` pair and a `band`, it renders a labelled
// track+fill whose fill element's inline `width` style is `scaleLinear(max, 100)(value)` as a `%`
// string (DD-25's percentage-scale contract), coloured via `bandBarBgClass(band)`.

import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { BarRow } from "../../../../../src/features/ai-benchmark/shell/bar-row";

afterEach(() => {
  cleanup();
});

describe("BarRow", () => {
  it("renders the label text", () => {
    render(<BarRow value={50} max={100} band="opus" label="GPT-6 — 85.7" testId="bar-row-a" />);
    expect(screen.getByTestId("bar-row-a-label").textContent).toBe("GPT-6 — 85.7");
  });

  it("sets the fill element's width style to the scaled percentage", () => {
    render(<BarRow value={50} max={100} band="opus" label="half" testId="bar-row-b" />);
    const fill = screen.getByTestId("bar-row-b-fill");
    expect(fill.style.width).toBe("50%");
  });

  it("maps the domain maximum to a full-width (100%) fill", () => {
    render(<BarRow value={100} max={100} band="sonnet" label="full" testId="bar-row-c" />);
    expect(screen.getByTestId("bar-row-c-fill").style.width).toBe("100%");
  });

  it("maps a zero value to a zero-width fill", () => {
    render(<BarRow value={0} max={100} band="haiku" label="empty" testId="bar-row-d" />);
    expect(screen.getByTestId("bar-row-d-fill").style.width).toBe("0%");
  });

  it("colours the fill with the band's DOM bar-background class", () => {
    render(<BarRow value={10} max={100} band="haiku" label="haiku-row" testId="bar-row-e" />);
    expect(screen.getByTestId("bar-row-e-fill").className).toContain("bg-[var(--chart-band-haiku)]");
  });
});
