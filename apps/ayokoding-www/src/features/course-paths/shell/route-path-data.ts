import { createTRPCContext } from "@/features/app-shell/shell/trpc-init";
import { buildCourseLibrary } from "./course-library";
import { defaultManifestsDir, loadManifests } from "./manifest-repository";
import type { CoursePathData } from "./course-path-nav";

/**
 * Load everything `<ROUTE>` needs to resolve a course page's path-aware chrome: the content
 * index's `contentMap` (for prev/next + prerequisite link title/slug lookups), the derived course
 * library (known course IDs + declared prerequisites, scoped to `locale`), and every loaded
 * manifest, validated against that library.
 *
 * IO lives entirely here (`shell/`) — the returned {@link CoursePathData} feeds the pure
 * `resolveCoursePathRenderData` composer, which performs no IO of its own.
 */
export async function loadRoutePathData(locale: string): Promise<CoursePathData> {
  const { contentService } = createTRPCContext();
  const index = await contentService.getIndex();
  const { libraryCourseIds, prerequisitesByCourse } = buildCourseLibrary(index.contentMap, locale);
  const manifests = await loadManifests(defaultManifestsDir(), libraryCourseIds);

  return { contentMap: index.contentMap, manifests, prerequisitesByCourse, libraryCourseIds };
}
