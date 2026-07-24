import { normalizeCourseRef } from "./manifest";
import type { PathManifest } from "./schemas";

/** Result of {@link checkManifestIntegrity}. */
export interface ManifestIntegrityResult {
  /** Course IDs listed in `courseOrder` that do not resolve to a real library course. */
  unresolvedIds: readonly string[];
  /** Course IDs that appear more than once in `courseOrder` (reported once each). */
  duplicateIds: readonly string[];
}

/**
 * Check that every `courseOrder` entry in `manifest` resolves to a real course in the library and
 * that no course ID repeats.
 *
 * Pure — no IO, never throws.
 */
export function checkManifestIntegrity(
  manifest: PathManifest,
  libraryCourseIds: readonly string[],
): ManifestIntegrityResult {
  const knownCourseIds = new Set(libraryCourseIds);
  const courseIds = manifest.courseOrder.map((ref) => normalizeCourseRef(ref).id);

  const unresolvedIds = [...new Set(courseIds.filter((id) => !knownCourseIds.has(id)))];

  const seen = new Set<string>();
  const duplicateIds = new Set<string>();
  for (const id of courseIds) {
    if (seen.has(id)) {
      duplicateIds.add(id);
    }
    seen.add(id);
  }

  return { unresolvedIds, duplicateIds: [...duplicateIds] };
}
