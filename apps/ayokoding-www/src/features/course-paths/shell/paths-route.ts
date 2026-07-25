import type { PathManifest } from "../core/schemas";

/**
 * The two path categories this plan's URL grammar recognizes. Duplicated from (not imported from)
 * `core/schemas.ts`'s own `PATH_ID_CATEGORIES` — `course-paths/core` is owned by the archived
 * `ayokoding-learning-path-02-schema-and-prerequisite-dag` and this plan does not edit it.
 */
const PATH_CATEGORIES = ["careers", "skills"] as const;
type PathCategory = (typeof PATH_CATEGORIES)[number];

function isPathCategory(value: string): value is PathCategory {
  return (PATH_CATEGORIES as readonly string[]).includes(value);
}

/** The content slug every paths-hub/category/arc/path-landing route lives under. */
export const LEARN_PATHS_PREFIX = "learn/paths";

/**
 * True for the bare `learn/paths` slug and every slug nested under it — `<ROUTE>`'s gate for
 * dispatching to {@link resolvePathsRoute} instead of the standard canonical content-page render.
 * A same-prefix sibling slug (e.g. `learn/paths-unrelated`) is deliberately excluded — this checks
 * a real path segment boundary, not a string prefix.
 */
export function isLearnPathsSlug(slug: string): boolean {
  return slug === LEARN_PATHS_PREFIX || slug.startsWith(`${LEARN_PATHS_PREFIX}/`);
}

/** Which Screen (hub / category / arc / path landing) a `learn/paths/**` slug resolves to. */
export type PathsRouteResolution =
  | { kind: "hub" }
  | { kind: "category"; category: PathCategory }
  | { kind: "arc"; category: "careers"; arc: string }
  | { kind: "path"; manifest: PathManifest }
  | { kind: "not-found" };

/**
 * Dispatch a content slug to the `learn/paths` render kind it should get — hub (Screen 1),
 * category landing (Screen 1a), arc landing (careers-only, Screen 1b), or path landing (Screen 2,
 * the terminal segment) — purely from **segment count** and the loaded manifests (R2: `pathId` is
 * variable-depth — `careers/<arc>/<role>` is 3 segments, `skills/<subject>` is 2 — so this function
 * never hardcodes a per-category depth expectation).
 *
 * A terminal segment is recognized as `kind: "path"` only when it names a **loaded** manifest —
 * this is what lets a 2-segment `skills/<subject>` terminal path and a 2-segment
 * `careers/<arc>` arc root share a segment count without ambiguity: a matching manifest always
 * wins over the careers-arc interpretation.
 *
 * Returns `{ kind: "not-found" }` for a slug outside this namespace, an unrecognized category
 * segment, or a terminal segment naming no loaded manifest — every caller falls back to the
 * standard canonical content-page render for all three, matching Cycle 2.6's graceful-fallback
 * precedent (invalid/missing context is never an error).
 *
 * Pure — no IO, never throws.
 */
export function resolvePathsRoute(slug: string, manifests: readonly PathManifest[]): PathsRouteResolution {
  if (slug !== LEARN_PATHS_PREFIX && !slug.startsWith(`${LEARN_PATHS_PREFIX}/`)) {
    return { kind: "not-found" };
  }

  const rest = slug === LEARN_PATHS_PREFIX ? "" : slug.slice(LEARN_PATHS_PREFIX.length + 1);
  const segments = rest === "" ? [] : rest.split("/");

  if (segments.length === 0) {
    return { kind: "hub" };
  }

  const category = segments[0] ?? "";
  if (!isPathCategory(category)) {
    return { kind: "not-found" };
  }

  if (segments.length === 1) {
    return { kind: "category", category };
  }

  const candidatePathId = segments.join("/");
  const manifest = manifests.find((candidate) => candidate.pathId === candidatePathId);
  if (manifest) {
    return { kind: "path", manifest };
  }

  if (segments.length === 2 && category === "careers") {
    return { kind: "arc", category: "careers", arc: segments[1] ?? "" };
  }

  return { kind: "not-found" };
}

/** One careers arc's loaded manifests, grouped in first-seen arc order (Screen 1's `ArcGroup`). */
export interface CareersArcGroup {
  arc: string;
  manifests: PathManifest[];
}

/**
 * Group every `careers/`-prefixed manifest by its declared `arc`, preserving first-seen arc order.
 * Skills manifests are excluded — callers combine this with {@link skillsManifests} for the hub's
 * two sections. Pure — no IO.
 */
export function groupCareersManifestsByArc(manifests: readonly PathManifest[]): CareersArcGroup[] {
  const groups: CareersArcGroup[] = [];
  const indexByArc = new Map<string, number>();

  for (const manifest of manifests) {
    if (!manifest.pathId.startsWith("careers/")) continue;

    const existingIndex = indexByArc.get(manifest.arc);
    if (existingIndex === undefined) {
      indexByArc.set(manifest.arc, groups.length);
      groups.push({ arc: manifest.arc, manifests: [manifest] });
    } else {
      groups[existingIndex]?.manifests.push(manifest);
    }
  }

  return groups;
}

/** Every `skills/`-prefixed manifest, in load order (the hub's flat Skills section, R8: no arc grouping). */
export function skillsManifests(manifests: readonly PathManifest[]): PathManifest[] {
  return manifests.filter((manifest) => manifest.pathId.startsWith("skills/"));
}

/**
 * Every `careers/`-prefixed manifest, flat and in load order — Screen 0's landing-hero grid
 * (Cycle 3.2), which shows one card per careers role (not grouped by arc, unlike the hub) and
 * caps the count itself (R1). Shares this one prefix check with {@link skillsManifests} and
 * {@link groupCareersManifestsByArc} rather than re-testing `pathId.startsWith("careers/")` at
 * the call site.
 */
export function careersManifests(manifests: readonly PathManifest[]): PathManifest[] {
  return manifests.filter((manifest) => manifest.pathId.startsWith("careers/"));
}

/** Every `careers/`-prefixed manifest belonging to `arc`, in load order (`arc-landing.tsx`'s role grid). */
export function manifestsForArc(manifests: readonly PathManifest[], arc: string): PathManifest[] {
  return manifests.filter((manifest) => manifest.pathId.startsWith("careers/") && manifest.arc === arc);
}
