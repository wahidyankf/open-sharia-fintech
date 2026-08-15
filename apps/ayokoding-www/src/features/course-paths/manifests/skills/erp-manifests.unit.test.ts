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
const expected = [
  "erp-foundations-and-history",
  "erp-conceptual-data-model",
  "erp-module-map-and-architecture",
  "erp-document-lifecycle-and-state-machines",
  "erp-posting-rules-and-account-determination",
  "erp-subledger-to-gl-architecture",
  "erp-fiscal-calendar-and-period-close",
  "erp-numbering-sequences-and-uom-conversion",
  "erp-audit-trail-and-change-tracking",
  "procure-to-pay-systems",
  "order-to-cash-systems",
  "erp-procurement-and-fulfillment-exceptions",
  "erp-bom-and-routing-architecture",
  "erp-extension-and-customization",
  "erp-integration-patterns",
];

describe("Stage-A ERP manifests", () => {
  for (const name of ["conventional-erp", "sharia-erp"]) {
    it(`${name} publishes the identical ordered fifteen-course foundation`, () => {
      const manifest = PathManifestSchema.parse(
        JSON.parse(
          fs.readFileSync(path.join(appRoot, "src/features/course-paths/manifests/skills", `${name}.json`), "utf8"),
        ),
      );
      expect(manifest.pathId).toBe(`skills/${name}`);
      expect(manifest.courseOrder).toEqual(expected);
      expect(checkManifestIntegrity(manifest, courseIds)).toEqual({ unresolvedIds: [], duplicateIds: [] });
      expect(checkPrerequisiteConsistency(manifest, prerequisites, courseIds).violations).toEqual([]);
    });
  }
});
