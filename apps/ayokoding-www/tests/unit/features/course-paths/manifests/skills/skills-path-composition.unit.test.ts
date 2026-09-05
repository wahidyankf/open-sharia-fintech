import path from "node:path";
import { describeFeature, loadFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import conventionalAccountingSource from "../../../../../../src/features/course-paths/manifests/skills/conventional-accounting.json";
import shariaAccountingSource from "../../../../../../src/features/course-paths/manifests/skills/sharia-accounting.json";
import { PathManifestSchema, type PathManifest } from "../../../../../../src/features/course-paths/core/schemas";
import { normalizeCourseRef } from "../../../../../../src/features/course-paths/core/manifest";
import { checkManifestIntegrity } from "../../../../../../src/features/course-paths/core/manifest-integrity";
import {
  resolvePathsRoute,
  type PathsRouteResolution,
} from "../../../../../../src/features/course-paths/shell/paths-route";

const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/ayokoding/www/behaviours/frontend/course-paths/skills-path-composition.feature",
  ),
);

const conventionalAccounting = PathManifestSchema.parse(conventionalAccountingSource);
const shariaAccounting = PathManifestSchema.parse(shariaAccountingSource);
const publishedManifests = [conventionalAccounting, shariaAccounting] as const;

describeFeature(feature, ({ ScenarioOutline }) => {
  ScenarioOutline(
    "A two-segment skills path ID resolves to its full shared accounting slice",
    ({ Given, When, Then, And }, examples) => {
      const pathId = String(examples["path-id"]);
      let manifest: PathManifest;
      let resolution: PathsRouteResolution;

      Given('the published accounting manifest for "<path-id>"', () => {
        manifest = publishedManifests.find((candidate) => candidate.pathId === pathId)!;
        expect(manifest).toBeDefined();
      });

      When("its ordered course context is inspected", () => {
        resolution = resolvePathsRoute(`learn/paths/${manifest.pathId}`, publishedManifests);
      });

      Then("it contains its published accounting order", () => {
        expect(resolution).toMatchObject({ kind: "path", manifest: { pathId } });
        expect(manifest.courseOrder.length).toBeGreaterThan(0);
        if (pathId === "skills/sharia-accounting") {
          expect(manifest.courseOrder.slice(0, conventionalAccounting.courseOrder.length)).toEqual(
            conventionalAccounting.courseOrder,
          );
          expect(manifest.courseOrder.length).toBeGreaterThan(conventionalAccounting.courseOrder.length);
        }
      });

      And("every course context is represented by one course directory", () => {
        const injectedCourseDirectoryIds = publishedManifests.flatMap((published) =>
          published.courseOrder.map((reference) => normalizeCourseRef(reference).id),
        );
        expect(checkManifestIntegrity(manifest, injectedCourseDirectoryIds).unresolvedIds).toEqual([]);
      });

      And("an over-segmented path ID is not a published accounting path", () => {
        expect(manifest.pathId.split("/")).toHaveLength(2);
      });
    },
  );
});
