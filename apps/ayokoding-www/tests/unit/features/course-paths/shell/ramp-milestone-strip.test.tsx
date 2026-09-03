import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { RampMilestoneStrip } from "../../../../../src/features/course-paths/shell/ramp-milestone-strip";

afterEach(cleanup);

describe("RampMilestoneStrip (Cycle 3.1b-ii — skills fixed-arc compact preview, R7)", () => {
  it("renders a real <ol> of exactly three labelled ticks", () => {
    render(<RampMilestoneStrip />);

    const list = screen.getByRole("list");
    const items = list.querySelectorAll("li");
    expect(items.length).toBe(3);
  });

  it("labels the three ticks dangerous / comfortable / confident", () => {
    render(<RampMilestoneStrip />);

    expect(screen.getByText(/dangerous/i)).toBeTruthy();
    expect(screen.getByText(/comfortable/i)).toBeTruthy();
    expect(screen.getByText(/confident/i)).toBeTruthy();
  });
});
