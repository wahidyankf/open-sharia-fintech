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
