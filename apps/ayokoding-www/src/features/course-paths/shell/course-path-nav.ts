import { normalizeCourseRef } from "../core/manifest";
import { parsePathContext } from "../core/path-context";
import { resolvePathNav, type PathNav } from "../core/path-nav";
import { resolvePrerequisites, type PrerequisitesByCourse } from "../core/prerequisites";
import type { PathManifest } from "../core/schemas";
import type { ContentMeta, PageLink } from "@/features/content/core/types";

/** The content-slug prefix every course lives under — the one canonical course URL shape. */
const COURSE_SLUG_PREFIX = "learn/courses/";

/**
 * Extract a course ID from a content slug, or `null` when `slug` is not a course page.
 *
 * Pure — no IO. Path context only ever applies to course pages, so every caller uses this to scope
 * path-aware rendering to the pages where a `courseOrder` entry can possibly match.
 */
export function courseIdFromSlug(slug: string): string | null {
  return slug.startsWith(COURSE_SLUG_PREFIX) ? slug.slice(COURSE_SLUG_PREFIX.length) : null;
}

/** The canonical content slug for a course ID — the inverse of {@link courseIdFromSlug}. */
export function slugForCourseId(courseId: string): string {
  return `${COURSE_SLUG_PREFIX}${courseId}`;
}

/** The resolved path context for a course page: which path, its manifest, and prev/next. */
export interface ActiveCoursePathContext {
  pathId: string;
  manifest: PathManifest;
  nav: PathNav;
}

/**
 * Resolve the active path context for `courseId` given `searchParams` and the loaded `manifests`.
 *
 * Returns `null` — the canonical-view signal — for every one of: no `?path=` present, a `?path=`
 * naming no loaded manifest (Cycle 2.6), and a valid path whose manifest omits `courseId` from its
 * `courseOrder` (Cycle 2.7). All three collapse onto the same branch by design (Cycle 2.6's
 * REFACTOR note): callers need exactly one `null` check, never three separate ones.
 *
 * Pure — no IO, never throws.
 */
export function resolveActiveCoursePathContext(
  searchParams: URLSearchParams,
  manifests: readonly PathManifest[],
  courseId: string,
): ActiveCoursePathContext | null {
  const pathId = parsePathContext(searchParams, manifests);
  if (pathId === null) {
    return null;
  }

  const manifest = manifests.find((candidate) => candidate.pathId === pathId);
  if (!manifest) {
    // Unreachable in practice — parsePathContext only returns a pathId present in `manifests` —
    // kept so this function is total over any (searchParams, manifests) pair, not just the ones
    // parsePathContext's own invariant currently guarantees.
    return null;
  }

  const isCourseInManifest = manifest.courseOrder.some((ref) => normalizeCourseRef(ref).id === courseId);
  if (!isCourseInManifest) {
    return null;
  }

  return { pathId, manifest, nav: resolvePathNav(manifest, courseId) };
}

/**
 * Resolve `courseId`'s canonical `PageLink` (title + slug) from a loaded content index's
 * `contentMap`, or `null` when no content page exists for it in `locale`.
 *
 * Pure — no IO. Shared by prerequisite-link and manifest-neighbour prev/next resolution so
 * neither re-implements the `contentMap` lookup key convention.
 */
export function pageLinkForCourseId(
  contentMap: ReadonlyMap<string, ContentMeta>,
  locale: string,
  courseId: string,
): PageLink | null {
  const meta = contentMap.get(`${locale}:${slugForCourseId(courseId)}`);
  return meta ? { title: meta.title, slug: meta.slug } : null;
}

/** One path a course belongs to, as a renderable badge (Cycle 2.5's "part of paths" affordance). */
export interface PathBadge {
  pathId: string;
  title: string;
}

/**
 * Derive one {@link PathBadge} per loaded manifest whose `courseOrder` lists `courseId`, in
 * `manifests` order.
 *
 * Pure — no IO. Reads `manifests` once (Cycle 2.5's REFACTOR note) rather than being called once
 * per badge. A course ID shared by multiple manifests (the no-forked-body property) still yields
 * one badge per path — the course's canonical body slug ({@link slugForCourseId}) never varies by
 * path, only which paths list it.
 */
export function derivePathBadges(manifests: readonly PathManifest[], courseId: string): PathBadge[] {
  return manifests
    .filter((manifest) => manifest.courseOrder.some((ref) => normalizeCourseRef(ref).id === courseId))
    .map((manifest) => ({ pathId: manifest.pathId, title: manifest.title }));
}

/** The loaded, locale-scoped path data `<ROUTE>` needs to resolve a course page's path-aware render. */
export interface CoursePathData {
  contentMap: ReadonlyMap<string, ContentMeta>;
  manifests: readonly PathManifest[];
  prerequisitesByCourse: PrerequisitesByCourse;
  libraryCourseIds: readonly string[];
}

/** Everything `<ROUTE>` needs to render a course page's path-aware chrome, resolved in one call. */
export interface CoursePathRenderData {
  activeContext: ActiveCoursePathContext | null;
  prerequisiteLinks: readonly PageLink[];
  pathBadges: readonly PathBadge[];
  prev: PageLink | null;
  next: PageLink | null;
}

/**
 * Resolve everything `<ROUTE>` needs to render a course page's path-aware chrome in one call: the
 * active path context (Cycles 2.6/2.7's fallback rules), the resolved prerequisite links (Cycle
 * 2.4 — path-independent, rendered in both views), the "part of paths" badges (Cycle 2.5 —
 * canonical branch only), and prev/next (Cycle 2.2 — manifest neighbours when a path is active,
 * `fallbackPrev`/`fallbackNext` unchanged otherwise).
 *
 * Pure — no IO, never throws. This is the **one place** that decides path-aware vs. canonical
 * (Cycle 2.6's REFACTOR note) — invalid, missing, and omitted-course contexts all converge on
 * `resolveActiveCoursePathContext`'s single `null` branch before this function ever runs its
 * path-aware logic.
 */
export function resolveCoursePathRenderData(
  searchParams: URLSearchParams,
  data: CoursePathData,
  courseId: string,
  locale: string,
  fallbackPrev: PageLink | null,
  fallbackNext: PageLink | null,
): CoursePathRenderData {
  const activeContext = resolveActiveCoursePathContext(searchParams, data.manifests, courseId);

  const prerequisiteLinks = resolvePrerequisites(courseId, data.prerequisitesByCourse, data.libraryCourseIds)
    .map((id) => pageLinkForCourseId(data.contentMap, locale, id))
    .filter((link): link is PageLink => link !== null);

  const pathBadges = activeContext === null ? derivePathBadges(data.manifests, courseId) : [];

  const prev = activeContext
    ? activeContext.nav.prev
      ? pageLinkForCourseId(data.contentMap, locale, activeContext.nav.prev.id)
      : null
    : fallbackPrev;

  const next = activeContext
    ? activeContext.nav.next
      ? pageLinkForCourseId(data.contentMap, locale, activeContext.nav.next.id)
      : null
    : fallbackNext;

  return { activeContext, prerequisiteLinks, pathBadges, prev, next };
}

/**
 * Build a plain `courseId -> title` record covering every course ID that appears in any of
 * `manifests`' `courseOrder` — a course ID with no resolvable content page is omitted.
 *
 * Pure — no IO. Deliberately a plain `Record`, not a `Map`: `<APPSHELL>` server layouts pass this
 * to the client-side `SidebarHost`/`MobileNav` (Cycles 2.8/2.9), and a `Map` is not a safe RSC
 * prop shape, whereas a plain object always serializes across the server/client boundary.
 */
export function buildCourseTitleIndex(
  contentMap: ReadonlyMap<string, ContentMeta>,
  locale: string,
  manifests: readonly PathManifest[],
): Record<string, string> {
  const ids = new Set<string>();
  for (const manifest of manifests) {
    for (const ref of manifest.courseOrder) {
      ids.add(normalizeCourseRef(ref).id);
    }
  }

  const titles: Record<string, string> = {};
  for (const id of ids) {
    const link = pageLinkForCourseId(contentMap, locale, id);
    if (link) {
      titles[id] = link.title;
    }
  }
  return titles;
}

/**
 * Strip a `/{locale}` prefix from a Next.js `usePathname()` value, yielding the bare content slug
 * `courseIdFromSlug` expects — or `null` when `pathname` does not start with that locale.
 *
 * Pure — no IO. Exists because two hosts structurally disconnected from `<ROUTE>` (`SidebarHost`,
 * `MobileNav` — Cycles 2.8/2.9) must independently derive "which course page am I on" client-side
 * via `usePathname()`, since a layout receives neither `searchParams` nor a descendant route's
 * `[...slug]` params.
 */
export function slugFromPathname(pathname: string, locale: string): string | null {
  const prefix = `/${locale}`;
  if (pathname === prefix) {
    return "";
  }
  if (!pathname.startsWith(`${prefix}/`)) {
    return null;
  }
  return pathname.slice(prefix.length + 1);
}

/** The course + active path context resolved from the current client-side location. */
export interface ActiveCourseLocation {
  courseId: string;
  context: ActiveCoursePathContext;
}

/**
 * Resolve "which course is the reader on, and is a path context active" purely from client-side
 * location primitives (`usePathname()` + `useSearchParams()`) — the composer `SidebarHost` and
 * `MobileNav` (Cycles 2.8/2.9) share, since both are structurally disconnected from `<ROUTE>`
 * (a layout receives neither `searchParams` nor a descendant route's `[...slug]` params).
 *
 * Returns `null` for a non-course pathname, a course with no active `?path=`, and every case
 * {@link resolveActiveCoursePathContext} itself returns `null` for (invalid path, omitted course).
 *
 * Pure — no IO, never throws.
 */
export function resolveActiveCourseFromLocation(
  pathname: string,
  searchParams: URLSearchParams,
  locale: string,
  manifests: readonly PathManifest[],
): ActiveCourseLocation | null {
  const slug = slugFromPathname(pathname, locale);
  if (slug === null) {
    return null;
  }

  const courseId = courseIdFromSlug(slug);
  if (courseId === null) {
    return null;
  }

  const context = resolveActiveCoursePathContext(searchParams, manifests, courseId);
  return context === null ? null : { courseId, context };
}

/** A course's 1-based position within a manifest's ordered arc, and the arc's total length. */
export interface CoursePosition {
  index: number;
  total: number;
}

/**
 * Resolve `courseId`'s 1-based position within `manifest.courseOrder`, and the manifest's total
 * course count — `PathBanner`'s "course k of N" readout (Cycle 2.9).
 *
 * Pure — no IO. Assumes `courseId` is a member of `manifest.courseOrder` (every caller reaches
 * this only after {@link resolveActiveCoursePathContext} has already confirmed membership);
 * returns `{ index: 0, total }` for a non-member rather than throwing, since this function's own
 * contract stays total even if a caller's invariant is ever violated.
 */
export function coursePositionInManifest(manifest: PathManifest, courseId: string): CoursePosition {
  const normalized = manifest.courseOrder.map(normalizeCourseRef);
  const index = normalized.findIndex((ref) => ref.id === courseId);
  return { index: index + 1, total: normalized.length };
}
