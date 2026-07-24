import { describe, expect, it } from "vitest";
import { resolvePrerequisites } from "./prerequisites";

const prerequisitesByCourse: Record<string, readonly string[]> = {
  "advanced-algorithms": ["data-structures-and-algorithms-essentials", "discrete-math-foundations"],
  "just-enough-python": [],
};

describe("resolvePrerequisites", () => {
  it("returns both declared prerequisites in declaration order", () => {
    const result = resolvePrerequisites("advanced-algorithms", prerequisitesByCourse);

    expect(result).toEqual(["data-structures-and-algorithms-essentials", "discrete-math-foundations"]);
  });

  it("returns an empty array for a course declaring no prerequisites", () => {
    const result = resolvePrerequisites("just-enough-python", prerequisitesByCourse);

    expect(result).toEqual([]);
  });

  it("returns an empty array (not undefined, not a throw) for a course absent from the index", () => {
    const result = resolvePrerequisites("not-in-the-index", prerequisitesByCourse);

    expect(result).toEqual([]);
    expect(result).not.toBeUndefined();
  });
});
