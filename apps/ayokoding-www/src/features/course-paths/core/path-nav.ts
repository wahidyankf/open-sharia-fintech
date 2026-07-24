import { normalizeCourseRef, type NormalizedCourseRef } from "./manifest";
import type { PathManifest } from "./schemas";

/** The prev/next neighbours of a course within a path's manifest, or `null` at either boundary. */
export interface PathNav {
  prev: NormalizedCourseRef | null;
  next: NormalizedCourseRef | null;
}

/**
 * Resolve the prev/next neighbours of `courseId` within `manifest`'s `courseOrder`.
 *
 * Returns `{ prev: null, next: null }` both when `courseId` is the only course in the manifest
 * (no neighbours exist) and when `courseId` is absent from `courseOrder` entirely — a course a
 * path's manifest omits gets no path nav for that path, per design. Pure — no IO, never throws.
 */
export function resolvePathNav(manifest: PathManifest, courseId: string): PathNav {
  const normalized = manifest.courseOrder.map(normalizeCourseRef);
  const index = normalized.findIndex((ref) => ref.id === courseId);

  if (index === -1) {
    return { prev: null, next: null };
  }

  return {
    prev: index > 0 ? (normalized[index - 1] ?? null) : null,
    next: index < normalized.length - 1 ? (normalized[index + 1] ?? null) : null,
  };
}
