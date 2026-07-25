import Link from "next/link";
import { contentUrl } from "@/features/content/core/content-url";
import type { Locale } from "@/features/i18n/core/config";
import type { PathBadge } from "./course-path-nav";

export interface PathCourseLinksProps {
  locale: string;
  /** Already-derived badges (via {@link import("./course-path-nav").derivePathBadges}) — one per path. */
  paths: readonly PathBadge[];
}

/**
 * The "this course is part of" affordance (course-paths plan, Cycle 2.5) — rendered in the
 * canonical (no active path context) branch of `<ROUTE>` only. Lists every path whose manifest
 * includes the course as a badge link to that path's landing page, preserving that path's own
 * context (via {@link contentUrl}'s optional `pathId` argument — no hand-built query string here).
 *
 * Renders nothing when the course belongs to no path — badges are additive, never a placeholder.
 */
export function PathCourseLinks({ locale, paths }: PathCourseLinksProps) {
  if (paths.length === 0) {
    return null;
  }

  return (
    <nav aria-label="This course is part of" className="mt-8 text-sm">
      <h2 className="mb-2 font-semibold text-muted-foreground">This course is part of</h2>
      <ul className="flex flex-wrap gap-2">
        {paths.map((path) => (
          <li key={path.pathId}>
            <Link
              href={contentUrl(locale as Locale, `learn/paths/${path.pathId}`, path.pathId)}
              className="rounded-full border px-3 py-1 text-xs hover:bg-muted"
            >
              {path.title}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
