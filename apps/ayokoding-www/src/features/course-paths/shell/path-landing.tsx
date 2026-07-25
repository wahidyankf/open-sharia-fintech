import Link from "next/link";
import { contentUrl } from "@/features/content/core/content-url";
import type { Locale } from "@/features/i18n/core/config";
import { MarkdownRenderer } from "@/features/content/shell/markdown-renderer";
import type { PathManifest } from "../core/schemas";
import { manifestCourseOrder, slugForCourseId } from "./course-path-nav";

export interface PathLandingProps {
  locale: string;
  manifest: PathManifest;
  /** courseId -> title, covering every ID in `manifest.courseOrder` (falls back to the ID itself). */
  courseTitles: Readonly<Record<string, string>>;
  /**
   * The path's own `_index.md` markdown body (Cycle 3.1d), when one resolves — `undefined`/`null`
   * for a careers path (which supplies no body) is a silent no-op, not a rendering error.
   */
  bodyHtml?: string | null;
}

/**
 * Path landing (Cycles 3.1/3.1d, Screen 2) — a manifest rendered as a numbered, ordered syllabus.
 * The visible number **is** the `courseOrder` index (semantic `<ol>`); every course link carries
 * `?path=`. For a `skills/` path, `bodyHtml` (the shipped `content.getBySlug` procedure's `html`
 * for this path's own `_index.md`) renders via the shipped `MarkdownRenderer` between the
 * title/arc-summary and the syllabus — the rendering surface for the ramp can/cannot table,
 * runway-justification paragraph, and linked-prerequisite outbound links. A careers path's
 * `_index.md` supplies no body, so `bodyHtml` is omitted and this slot is a silent no-op.
 */
export function PathLanding({ locale, manifest, courseTitles, bodyHtml }: PathLandingProps) {
  const courses = manifestCourseOrder(manifest);

  return (
    <div className="mx-auto max-w-3xl flex-1 px-6 py-8 lg:px-8">
      <div aria-hidden="true" className="mb-4 h-1.5 w-16 rounded-full bg-[var(--hue-honey)]" />
      <h1 className="text-4xl font-extrabold tracking-tight">{manifest.title}</h1>
      <p className="mt-2 text-muted-foreground">{manifest.description}</p>

      {bodyHtml && <MarkdownRenderer html={bodyHtml} locale={locale} />}

      <nav aria-label={`${manifest.title} syllabus`}>
        <section>
          <h2 className="mt-8 text-sm font-semibold tracking-wide text-muted-foreground uppercase">Syllabus</h2>
          <ol className="mt-3 space-y-1">
            {courses.map((course) => {
              const title = courseTitles[course.id] ?? course.id;

              return (
                <li key={course.id}>
                  <Link
                    href={contentUrl(locale as Locale, slugForCourseId(course.id), manifest.pathId)}
                    className="rounded-md px-2 py-1 text-sm hover:bg-accent hover:text-foreground"
                  >
                    {title}
                  </Link>
                </li>
              );
            })}
          </ol>
        </section>
      </nav>
    </div>
  );
}
