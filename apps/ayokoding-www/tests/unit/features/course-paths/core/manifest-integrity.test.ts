import { describe, expect, it } from "vitest";
import { checkManifestIntegrity } from "../../../../../src/features/course-paths/core/manifest-integrity";
import type { PathManifest } from "../../../../../src/features/course-paths/core/schemas";

const libraryCourseIds: readonly string[] = [
  "just-enough-python",
  "data-structures-and-algorithms-essentials",
  "advanced-algorithms",
];

const cleanManifest: PathManifest = {
  pathId: "skills/algorithms",
  arc: "algorithms",
  title: "Algorithms",
  description: "Algorithms path",
  courseOrder: ["just-enough-python", "data-structures-and-algorithms-essentials", "advanced-algorithms"],
};

const unresolvedManifest: PathManifest = {
  pathId: "skills/algorithms",
  arc: "algorithms",
  title: "Algorithms",
  description: "Algorithms path",
  courseOrder: ["just-enough-python", "does-not-exist-in-the-library"],
};

const duplicateManifest: PathManifest = {
  pathId: "skills/algorithms",
  arc: "algorithms",
  title: "Algorithms",
  description: "Algorithms path",
  courseOrder: ["just-enough-python", "advanced-algorithms", "just-enough-python"],
};

// Object-form courseOrder entries must be handled identically to bare strings (2.7 REFACTOR).
const objectFormManifest: PathManifest = {
  pathId: "skills/algorithms",
  arc: "algorithms",
  title: "Algorithms",
  description: "Algorithms path",
  courseOrder: [{ id: "just-enough-python" }, { id: "does-not-exist-in-the-library" }],
};

describe("checkManifestIntegrity", () => {
  it("reports no unresolved and no duplicate IDs for a clean manifest", () => {
    const result = checkManifestIntegrity(cleanManifest, libraryCourseIds);

    expect(result.unresolvedIds).toEqual([]);
    expect(result.duplicateIds).toEqual([]);
  });

  it("reports exactly the course ID absent from the library as unresolved", () => {
    const result = checkManifestIntegrity(unresolvedManifest, libraryCourseIds);

    expect(result.unresolvedIds).toEqual(["does-not-exist-in-the-library"]);
    expect(result.duplicateIds).toEqual([]);
  });

  it("reports exactly the repeated course ID as duplicated", () => {
    const result = checkManifestIntegrity(duplicateManifest, libraryCourseIds);

    expect(result.unresolvedIds).toEqual([]);
    expect(result.duplicateIds).toEqual(["just-enough-python"]);
  });

  it("handles object-form courseOrder entries identically to bare strings", () => {
    const result = checkManifestIntegrity(objectFormManifest, libraryCourseIds);

    expect(result.unresolvedIds).toEqual(["does-not-exist-in-the-library"]);
    expect(result.duplicateIds).toEqual([]);
  });
});
