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

/**
 * One declared, in-library prerequisite the manifest omits entirely (OI-4: link-don't-walk).
 * Informational only — never a violation, never affects pass/fail.
 */
export interface LinkedPrerequisite {
  courseId: string;
  missingPrerequisiteId: string;
}

/** Result of {@link checkPrerequisiteConsistency} — ordering-only (OI-4: never completeness). */
export interface PrerequisiteConsistencyResult {
  /** Ordering violations only — never reports a prerequisite the manifest omits entirely. */
  violations: readonly PrerequisiteOrderingViolation[];
  /** Declared, in-library prerequisites the manifest links but does not include. Never a violation. */
  linkedPrerequisites: readonly LinkedPrerequisite[];
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
  // Keep the FIRST index for a duplicated course ID — `new Map(orderedIds.map(...))` would keep
  // the last (a later entry overwrites an earlier one under the same key), which reports a
  // false-positive ordering violation whenever a duplicated ID's first (correctly-ordered)
  // occurrence precedes a course that declares it as a prerequisite.
  const indexById = new Map<string, number>();
  orderedIds.forEach((id, index) => {
    if (!indexById.has(id)) {
      indexById.set(id, index);
    }
  });

  const violations: PrerequisiteOrderingViolation[] = [];
  const linkedPrerequisites: LinkedPrerequisite[] = [];

  orderedIds.forEach((courseId, courseIndex) => {
    for (const prerequisiteId of declaredPrerequisiteIds(courseId, prerequisitesByCourse)) {
      if (!knownCourseIds.has(prerequisiteId)) {
        continue;
      }

      const prerequisiteIndex = indexById.get(prerequisiteId);

      if (prerequisiteIndex === undefined) {
        // OI-4, link-don't-walk: declared and in-library, but the manifest omits it entirely.
        // Permitted by design — informational only, never a violation.
        linkedPrerequisites.push({ courseId, missingPrerequisiteId: prerequisiteId });
        continue;
      }

      if (prerequisiteIndex > courseIndex) {
        violations.push({
          courseId,
          missingPrerequisiteId: prerequisiteId,
          courseIndex,
          prerequisiteIndex,
        });
      }
    }
  });

  return { violations, linkedPrerequisites };
}
