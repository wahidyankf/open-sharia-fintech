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

/**
 * Derive every course ID known to the content index across **all** locales, deduplicated.
 *
 * Pure — no IO. A `PathManifest`'s `courseOrder` is locale-independent navigational metadata, but a
 * course's translation into any one locale routinely lags behind its English original —
 * `buildCourseLibrary`'s `libraryCourseIds` is deliberately scoped to one locale (for
 * prerequisite-link rendering, where a link must only appear when the target page truly exists in
 * the locale being rendered) and must stay that way; this function exists so manifest-integrity
 * checking (`loadManifests`) can ask "does this course exist anywhere in the catalog" without that
 * locale scoping — otherwise a manifest naming a not-yet-translated course would make every content
 * page in that locale fail to render, not just pages related to that course or path.
 */
export function deriveAllCourseIds(contentMap: ReadonlyMap<string, ContentMeta>): string[] {
  const allCourseIds = new Set<string>();

  for (const meta of contentMap.values()) {
    const courseId = courseIdFromSlug(meta.slug);
    if (courseId === null) continue;

    allCourseIds.add(courseId);
  }

  return [...allCourseIds];
}
