import Link from "next/link";
import { cn } from "@/lib/utils";
import { contentUrl } from "@/features/content/core/content-url";
import type { Locale } from "@/features/i18n/core/config";
import type { PathManifest } from "../core/schemas";
import { manifestCourseOrder, slugForCourseId } from "./course-path-nav";

/**
 * Shared base classes for the ordered course-row `Link`s — factored out (rather than duplicated
 * per `isCurrent` branch) so the one focus-visible/min-height/spacing definition edits in a single
 * place. See Finding 2 of the check6 audit (`generated-reports/swe-ui__55d6c6__*__audit.md`): the
 * prior duplicated-string shape was the mechanical root cause of the check3-check5 "one new
 * drifted spot per round" trickle.
 */
const COURSE_LINK_BASE =
  "flex min-h-11 items-center gap-1 truncate px-2 py-2 focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none";

/** Shared, unconditional classes for both footer escape links — identical for each, so no `cn()` branching is needed. */
const FOOTER_LINK_CLASS =
  "flex min-h-11 items-center px-2 text-muted-foreground hover:text-foreground focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none";

export interface PathRailProps {
  locale: string;
  manifest: PathManifest;
  /** The course ID currently being read — marked `aria-current="page"` in the ordered list. */
  currentCourseId: string;
  /** courseId -> title, covering every ID in `manifest.courseOrder` (falls back to the ID itself). */
  courseTitles: Readonly<Record<string, string>>;
}

/**
 * The left path rail (course-paths plan, Cycle 2.8 — the selected Screen 3 Option B).
 *
 * A content swap into the **existing** `ResizableSidebar` host — this component owns no `<aside>`,
 * no `hidden … md:block` gate, and no `localStorage` width key of its own; all three stay exactly
 * where `resizable-sidebar.tsx` already defines them (tech-docs.md §Screen 3).
 */
export function PathRail({ locale, manifest, currentCourseId, courseTitles }: PathRailProps) {
  const courses = manifestCourseOrder(manifest);

  return (
    <nav aria-label={`${manifest.title} course list`} className="flex flex-col gap-3 text-sm">
      <ol className="flex flex-col gap-1">
        {courses.map((course) => {
          const isCurrent = course.id === currentCourseId;
          const title = courseTitles[course.id] ?? course.id;

          return (
            <li key={course.id}>
              <Link
                href={contentUrl(locale as Locale, slugForCourseId(course.id), manifest.pathId)}
                aria-label={title}
                aria-current={isCurrent ? "page" : undefined}
                className={cn(
                  COURSE_LINK_BASE,
                  isCurrent ? "font-semibold text-foreground" : "text-muted-foreground hover:text-foreground",
                )}
              >
                {isCurrent && <span aria-hidden="true">▸</span>}
                <span className="truncate">{title}</span>
              </Link>
            </li>
          );
        })}
      </ol>

      <div className="flex flex-col gap-1 border-t border-border pt-3 text-xs">
        <Link
          href={contentUrl(locale as Locale, `learn/paths/${manifest.pathId}`, manifest.pathId)}
          className={FOOTER_LINK_CLASS}
        >
          View full path
        </Link>
        <Link href={`/${locale}/browse`} className={FOOTER_LINK_CLASS}>
          Browse all courses
        </Link>
      </div>
    </nav>
  );
}
