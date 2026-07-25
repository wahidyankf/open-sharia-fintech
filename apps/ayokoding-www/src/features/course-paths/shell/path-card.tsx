import type { ReactNode } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Badge, Card, CardDescription, CardHeader, CardTitle } from "@open-sharia-enterprise/web-ui";
import { contentUrl } from "@/features/content/core/content-url";
import type { Locale } from "@/features/i18n/core/config";
import type { PathManifest } from "../core/schemas";
import { LEARN_PATHS_PREFIX } from "./paths-route";

export type PathCardContext = "hero" | "hub";

export interface PathCardProps {
  locale: string;
  manifest: PathManifest;
  /** Screen 0's `hero` variant (goal-framed) vs. Screen 1's `hub` variant (formal name + description). */
  context: PathCardContext;
  /** Careers cards show a course-count badge; skills cards omit it pre-manifest (no meaningful count yet). */
  showCourseCount?: boolean;
}

/**
 * One path rendered as a card — the **single** `PathCard` implementation shared by the landing
 * hero (Screen 0, `context="hero"`) and the paths hub (Screen 1, `context="hub"`), per prd.md's
 * shared design legend. A single `<Link>` wraps the whole `Card` (the shipped `SectionCard`
 * pattern), so there is no link-in-link.
 */
export function PathCard({ locale, manifest, context, showCourseCount = true }: PathCardProps) {
  const href = contentUrl(locale as Locale, `${LEARN_PATHS_PREFIX}/${manifest.pathId}`);
  const courseCount = manifest.courseOrder.length;
  const label =
    context === "hero"
      ? `Start the ${manifest.title} path — ${manifest.description}, ~${courseCount} courses`
      : `Start the ${manifest.title} path — ${courseCount} courses`;

  return (
    <Link href={href} aria-label={label} className="group block focus-visible:outline-none">
      <Card className="h-full rounded-xl transition-colors group-focus-visible:ring-2 group-focus-visible:ring-ring hover:bg-accent hover:shadow-md">
        <CardHeader>
          <CardTitle className="text-lg font-semibold">{manifest.title}</CardTitle>
          <CardDescription className="text-sm text-muted-foreground">
            {context === "hero" ? manifest.arc : manifest.description}
          </CardDescription>
          {showCourseCount && <Badge variant="secondary" size="sm">{`~${courseCount} courses`}</Badge>}
          <span className="mt-2 inline-flex items-center gap-1 text-sm font-medium text-primary">
            Start
            <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
          </span>
        </CardHeader>
      </Card>
    </Link>
  );
}

export interface CategorySectionProps {
  /** Used to derive the section's `aria-labelledby` heading id — e.g. `"careers"` -> `"careers-heading"`. */
  id: string;
  heading: string;
  strapline: string;
  children: ReactNode;
}

/**
 * The paths hub's per-category wrapper (Screen 1, R6) — a `<section aria-labelledby>` with a real
 * `<h2>` heading, so the Careers/Skills grouping signal is a landmark, not styled text alone.
 */
export function CategorySection({ id, heading, strapline, children }: CategorySectionProps) {
  const headingId = `${id}-heading`;

  return (
    <section aria-labelledby={headingId}>
      <h2 id={headingId} className="text-sm font-semibold tracking-wide text-muted-foreground uppercase">
        {heading}
      </h2>
      <p className="sr-only">{strapline}</p>
      {children}
    </section>
  );
}

export interface ArcGroupProps {
  arc: string;
  children: ReactNode;
}

/**
 * One careers arc's role-card row inside the paths hub's Careers section (Screen 1, R6) — an
 * `<h3>` arc sub-heading (correctly nested under the section's `<h2>`) followed by the arc's
 * `PathCard` grid.
 */
export function ArcGroup({ arc, children }: ArcGroupProps) {
  return (
    <div>
      <h3 className="mt-6 text-xs font-medium tracking-wide text-muted-foreground uppercase">{arc}</h3>
      <ul className="mt-2 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">{children}</ul>
    </div>
  );
}
