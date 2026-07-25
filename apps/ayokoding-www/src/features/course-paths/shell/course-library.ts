import type { ContentMeta } from "@/features/content/core/types";
import type { PrerequisitesByCourse } from "../core/prerequisites";
import { courseIdFromSlug } from "./course-path-nav";

/** The course library derived from a loaded content index, scoped to one locale. */
export interface CourseLibrary {
  libraryCourseIds: readonly string[];
  prerequisitesByCourse: PrerequisitesByCourse;
}

/**
 * Derive the course library (known course IDs + their declared prerequisites) for `locale` from a
 * loaded content index's `contentMap`.
 *
 * Pure — no IO. Scopes to entries whose slug is a course page (per {@link courseIdFromSlug} —
 * `learn/courses/<id>`) for the given locale only; every other content page (sections, legacy
 * pages, paths pages) is excluded, matching `resolvePrerequisites`'s and `manifest-repository`'s
 * own "real course in the library" contract.
 */
export function buildCourseLibrary(contentMap: ReadonlyMap<string, ContentMeta>, locale: string): CourseLibrary {
  const libraryCourseIds: string[] = [];
  const prerequisitesByCourse: Record<string, readonly string[]> = {};

  for (const [key, meta] of contentMap) {
    if (!key.startsWith(`${locale}:`)) continue;

    const courseId = courseIdFromSlug(meta.slug);
    if (courseId === null) continue;

    libraryCourseIds.push(courseId);
    prerequisitesByCourse[courseId] = meta.prerequisites ?? [];
  }

  return { libraryCourseIds, prerequisitesByCourse };
}
