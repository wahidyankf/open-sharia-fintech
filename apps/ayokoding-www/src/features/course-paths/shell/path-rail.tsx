import Link from "next/link";
import { contentUrl } from "@/features/content/core/content-url";
import type { Locale } from "@/features/i18n/core/config";
import { normalizeCourseRef } from "../core/manifest";
import type { PathManifest } from "../core/schemas";
import { slugForCourseId } from "./course-path-nav";

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
  const courses = manifest.courseOrder.map(normalizeCourseRef);

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
                className={
                  isCurrent
                    ? "flex items-center gap-1 truncate font-semibold text-foreground"
                    : "flex items-center gap-1 truncate text-muted-foreground hover:text-foreground"
                }
              >
                {isCurrent && <span aria-hidden="true">▸</span>}
                <span className="truncate">{title}</span>
              </Link>
            </li>
          );
        })}
      </ol>

      <div className="flex flex-col gap-1 border-t border-border pt-3 text-xs">
        <Link href={contentUrl(locale as Locale, `learn/paths/${manifest.pathId}`, manifest.pathId)}>
          View full path
        </Link>
        <Link href={`/${locale}/browse`}>Browse all courses</Link>
      </div>
    </nav>
  );
}
