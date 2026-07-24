import { describe, expect, it } from "vitest";
import { checkPrerequisiteConsistency, resolvePrerequisites } from "./prerequisites";
import type { PathManifest } from "./schemas";

const prerequisitesByCourse: Record<string, readonly string[]> = {
  "advanced-algorithms": ["data-structures-and-algorithms-essentials", "discrete-math-foundations"],
  "just-enough-python": [],
};

const libraryCourseIds: readonly string[] = [
  "just-enough-python",
  "data-structures-and-algorithms-essentials",
  "discrete-math-foundations",
  "advanced-algorithms",
];

// Clean: every in-manifest prerequisite of advanced-algorithms precedes it.
const cleanManifest: PathManifest = {
  pathId: "skills/algorithms",
  arc: "algorithms",
  title: "Algorithms",
  description: "Algorithms path",
  courseOrder: ["data-structures-and-algorithms-essentials", "discrete-math-foundations", "advanced-algorithms"],
};

// Violating: advanced-algorithms precedes its declared prerequisite
// data-structures-and-algorithms-essentials. discrete-math-foundations is deliberately absent
// from this manifest so it can never count toward the violation total (only in-manifest
// prerequisites are checked) — keeping the violation count at exactly one.
// Link-don't-walk (OI-4): advanced-algorithms is included but its declared, in-library
// prerequisite discrete-math-foundations is omitted from the manifest entirely — permitted by
// design, never an ordering violation, only informational.
const omittedPrerequisiteManifest: PathManifest = {
  pathId: "skills/algorithms",
  arc: "algorithms",
  title: "Algorithms",
  description: "Algorithms path",
  courseOrder: ["data-structures-and-algorithms-essentials", "advanced-algorithms"],
};

const violatingManifest: PathManifest = {
  pathId: "skills/algorithms",
  arc: "algorithms",
  title: "Algorithms",
  description: "Algorithms path",
  courseOrder: ["advanced-algorithms", "data-structures-and-algorithms-essentials"],
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

describe("checkPrerequisiteConsistency", () => {
  it("reports zero violations for a manifest whose courseOrder respects every in-manifest prerequisite", () => {
    const result = checkPrerequisiteConsistency(cleanManifest, prerequisitesByCourse, libraryCourseIds);

    expect(result.violations).toEqual([]);
    expect(result.linkedPrerequisites).toEqual([]);
  });

  it("reports zero violations and one linked prerequisite for a manifest that omits a declared, in-library prerequisite (OI-4)", () => {
    const result = checkPrerequisiteConsistency(omittedPrerequisiteManifest, prerequisitesByCourse, libraryCourseIds);

    expect(result.violations).toEqual([]);
    expect(result.linkedPrerequisites).toHaveLength(1);
    expect(result.linkedPrerequisites[0]).toEqual({
      courseId: "advanced-algorithms",
      missingPrerequisiteId: "discrete-math-foundations",
    });
  });

  it("reports exactly one violation naming the course placed before its declared prerequisite", () => {
    const result = checkPrerequisiteConsistency(violatingManifest, prerequisitesByCourse, libraryCourseIds);

    expect(result.violations).toHaveLength(1);
    expect(result.violations[0]).toEqual({
      courseId: "advanced-algorithms",
      missingPrerequisiteId: "data-structures-and-algorithms-essentials",
      courseIndex: 0,
      prerequisiteIndex: 1,
    });
  });
});
