import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { describe, expect, it } from "vitest";
import { checkManifestIntegrity } from "../../../../../../src/features/course-paths/core/manifest-integrity";
import { checkPrerequisiteConsistency } from "../../../../../../src/features/course-paths/core/prerequisites";
import { PathManifestSchema } from "../../../../../../src/features/course-paths/core/schemas";

const appRoot = process.cwd();
const coursesRoot = path.join(appRoot, "content/en/learn/courses");
const manifestsRoot = path.join(appRoot, "src/features/course-paths/manifests/careers");
const manifestPaths = [
  "interview-ready/software-engineer.json",
  "immediately-effective/software-engineer.json",
  "fundamentally-strong/software-engineer.json",
] as const;
const bandNine = [
  "coding-interview",
  "take-home-and-live-coding",
  "system-design-interview",
  "behavioral-and-leadership-interviews",
  "capstone-interview-loop",
] as const;

const courseIds = fs
  .readdirSync(coursesRoot, { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name);
const prerequisitesByCourse = Object.fromEntries(
  courseIds.map((id) => {
    const raw = fs.readFileSync(path.join(coursesRoot, id, "_index.md"), "utf8");
    return [id, (matter(raw).data.prerequisites as string[] | undefined) ?? []];
  }),
);
const manifests = manifestPaths.map((manifestPath) =>
  PathManifestSchema.parse(JSON.parse(fs.readFileSync(path.join(manifestsRoot, manifestPath), "utf8"))),
);

describe("careers software-engineer manifests", () => {
  it("validates each full syllabus transcription against integrity and prerequisite ordering", () => {
    for (const manifest of manifests) {
      expect(checkManifestIntegrity(manifest, courseIds)).toEqual({ unresolvedIds: [], duplicateIds: [] });
      expect(checkPrerequisiteConsistency(manifest, prerequisitesByCourse, courseIds).violations).toEqual([]);
    }
  });

  it("keeps Band 9 in exactly the interview-ready and fundamentals-first routes", () => {
    expect(manifests[0]?.courseOrder).toEqual(expect.arrayContaining([...bandNine]));
    expect(manifests[1]?.courseOrder).toEqual(expect.not.arrayContaining([...bandNine]));
    expect(manifests[2]?.courseOrder).toEqual(expect.arrayContaining([...bandNine]));
  });

  it("preserves the distinct shipping-first and fundamentals-first entry points", () => {
    const immediatelyEffective = manifests[1]?.courseOrder ?? [];
    const fundamentallyStrong = manifests[2]?.courseOrder ?? [];
    expect(immediatelyEffective.indexOf("capstone-full-stack-app")).toBeLessThan(
      immediatelyEffective.indexOf("computer-science-foundations"),
    );
    expect(fundamentallyStrong.indexOf("computer-science-foundations")).toBeLessThan(
      fundamentallyStrong.indexOf("software-architecture"),
    );
  });
});
