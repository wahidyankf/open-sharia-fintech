import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { describe, expect, it } from "vitest";
import { checkManifestIntegrity } from "../../core/manifest-integrity";
import { checkPrerequisiteConsistency } from "../../core/prerequisites";
import { PathManifestSchema } from "../../core/schemas";

const appRoot = process.cwd();
const coursesRoot = path.join(appRoot, "content/en/learn/courses");
const courseIds = fs
  .readdirSync(coursesRoot, { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name);
const prerequisites = Object.fromEntries(
  courseIds.map((id) => [
    id,
    (matter(fs.readFileSync(path.join(coursesRoot, id, "_index.md"), "utf8")).data.prerequisites as
      | string[]
      | undefined) ?? [],
  ]),
);
const manifest = PathManifestSchema.parse(
  JSON.parse(
    fs.readFileSync(
      path.join(appRoot, "src/features/course-paths/manifests/skills/conventional-accounting.json"),
      "utf8",
    ),
  ),
);

describe("conventional accounting manifest", () => {
  it("contains the ordered three-course Stage 1 spine", () => {
    expect(manifest.pathId).toBe("skills/conventional-accounting");
    expect(manifest.arc).toBe("immediately-effective");
    expect(manifest.courseOrder).toEqual([
      "accounting-foundations",
      "chart-of-accounts-and-data-modeling",
      "financial-statements-and-close-cycle",
    ]);
    expect(checkManifestIntegrity(manifest, courseIds)).toEqual({ unresolvedIds: [], duplicateIds: [] });
    expect(checkPrerequisiteConsistency(manifest, prerequisites, courseIds).violations).toEqual([]);
  });
});
