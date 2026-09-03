import { describe, expect, it } from "vitest";
import { resolvePathNav } from "../../../../../src/features/course-paths/core/path-nav";
import type { PathManifest } from "../../../../../src/features/course-paths/core/schemas";

const manifest: PathManifest = {
  pathId: "careers/interview-ready/software-engineer",
  arc: "interview-ready",
  title: "Interview-Ready Software Engineer",
  description: "Interview-first track for an experienced engineer re-entering the market.",
  courseOrder: ["just-enough-python", "data-structures-and-algorithms-essentials", "capstone-forge-ready"],
};

describe("resolvePathNav", () => {
  it("returns both neighbours for a middle course", () => {
    const result = resolvePathNav(manifest, "data-structures-and-algorithms-essentials");

    expect(result).toEqual({
      prev: { id: "just-enough-python" },
      next: { id: "capstone-forge-ready" },
    });
  });

  it("returns prev: null for the first course", () => {
    const result = resolvePathNav(manifest, "just-enough-python");

    expect(result).toEqual({
      prev: null,
      next: { id: "data-structures-and-algorithms-essentials" },
    });
  });

  it("returns next: null for the last course", () => {
    const result = resolvePathNav(manifest, "capstone-forge-ready");

    expect(result).toEqual({
      prev: { id: "data-structures-and-algorithms-essentials" },
      next: null,
    });
  });

  it("returns { prev: null, next: null } for a course absent from courseOrder", () => {
    const result = resolvePathNav(manifest, "not-in-this-path");

    expect(result).toEqual({ prev: null, next: null });
  });
});
