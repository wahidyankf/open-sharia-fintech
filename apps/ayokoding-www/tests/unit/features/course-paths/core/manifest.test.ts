import { describe, expect, it } from "vitest";
import { normalizeCourseRef } from "../../../../../src/features/course-paths/core/manifest";

describe("normalizeCourseRef", () => {
  it("normalizes a bare course-ID string to { id } with no framing", () => {
    const result = normalizeCourseRef("just-enough-python");

    expect(result).toEqual({ id: "just-enough-python" });
  });

  it("normalizes an object course ref to the same shape, preserving framing", () => {
    const result = normalizeCourseRef({
      id: "capstone-forge-ready",
      framing: { intro: "Before you start the capstone, revisit your interview notes." },
    });

    expect(result).toEqual({
      id: "capstone-forge-ready",
      framing: { intro: "Before you start the capstone, revisit your interview notes." },
    });
  });
});
