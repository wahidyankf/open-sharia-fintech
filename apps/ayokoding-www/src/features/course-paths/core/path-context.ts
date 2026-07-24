import type { PathManifest } from "./schemas";

/**
 * Resolve the active path context from a course URL's `path` search param.
 *
 * Returns the `pathId` only when the param is present **and** names one of the loaded
 * `manifests`; returns `null` for an absent param and for a param naming an unknown or renamed
 * path. Pure — no IO, never throws. Graceful fallback (`null`) is the default outcome, not an
 * error path — three of the four possible branches end here by design.
 */
export function parsePathContext(searchParams: URLSearchParams, manifests: readonly PathManifest[]): string | null {
  const pathId = searchParams.get("path");

  if (pathId === null) {
    return null;
  }

  const knownPathIds = new Set(manifests.map((manifest) => manifest.pathId));

  return knownPathIds.has(pathId) ? pathId : null;
}
