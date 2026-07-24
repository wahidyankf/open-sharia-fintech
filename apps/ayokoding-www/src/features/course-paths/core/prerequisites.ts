import { normalizeCourseRef } from "./manifest";
import type { PathManifest } from "./schemas";

/** Maps a course ID to its declared `prerequisites:` frontmatter list. */
export type PrerequisitesByCourse = Record<string, readonly string[]>;

/**
 * Look up the declared prerequisite IDs for `courseId` in `prerequisitesByCourse`, in
 * declaration order.
 *
 * Total (never throws): a course absent from the index and a course declaring an empty list are
 * treated identically, both returning `[]`. Shared by {@link resolvePrerequisites} and
 * `checkPrerequisiteConsistency` so neither re-implements this traversal.
 */
function declaredPrerequisiteIds(courseId: string, prerequisitesByCourse: PrerequisitesByCourse): readonly string[] {
  return prerequisitesByCourse[courseId] ?? [];
}

/**
 * Resolve the declared prerequisite course IDs for `courseId`, in declaration order.
 *
 * Pure — no IO, never throws. A course absent from `prerequisitesByCourse` and a course
 * declaring `[]` are indistinguishable from the caller's perspective: both yield `[]`.
 */
export function resolvePrerequisites(
  courseId: string,
  prerequisitesByCourse: PrerequisitesByCourse,
): readonly string[] {
  return declaredPrerequisiteIds(courseId, prerequisitesByCourse);
}

/** One course placed before a declared, in-manifest prerequisite — an ordering violation. */
export interface PrerequisiteOrderingViolation {
  courseId: string;
  missingPrerequisiteId: string;
  courseIndex: number;
  prerequisiteIndex: number;
}

/** Result of {@link checkPrerequisiteConsistency} — ordering-only (OI-4: never completeness). */
export interface PrerequisiteConsistencyResult {
  /** Ordering violations only — never reports a prerequisite the manifest omits entirely. */
  violations: readonly PrerequisiteOrderingViolation[];
}

/**
 * Check that `manifest.courseOrder` never places a course before a declared prerequisite that is
 * also present in the manifest.
 *
 * Ordering-only by design (OI-4, tech-docs.md §Link-don't-walk): a declared prerequisite the
 * manifest omits entirely is never a violation here — that link-don't-walk case is reported
 * separately (cycle 2.6b's `linkedPrerequisites`). `libraryCourseIds` scopes prerequisite lookups
 * to courses that actually exist in the library.
 *
 * Pure — no IO, never throws.
 */
export function checkPrerequisiteConsistency(
  manifest: PathManifest,
  prerequisitesByCourse: PrerequisitesByCourse,
  libraryCourseIds: readonly string[],
): PrerequisiteConsistencyResult {
  const knownCourseIds = new Set(libraryCourseIds);
  const orderedIds = manifest.courseOrder.map((ref) => normalizeCourseRef(ref).id);
  const indexById = new Map(orderedIds.map((id, index) => [id, index]));

  const violations: PrerequisiteOrderingViolation[] = [];

  orderedIds.forEach((courseId, courseIndex) => {
    for (const prerequisiteId of declaredPrerequisiteIds(courseId, prerequisitesByCourse)) {
      if (!knownCourseIds.has(prerequisiteId)) {
        continue;
      }

      const prerequisiteIndex = indexById.get(prerequisiteId);

      if (prerequisiteIndex !== undefined && prerequisiteIndex > courseIndex) {
        violations.push({
          courseId,
          missingPrerequisiteId: prerequisiteId,
          courseIndex,
          prerequisiteIndex,
        });
      }
    }
  });

  return { violations };
}
