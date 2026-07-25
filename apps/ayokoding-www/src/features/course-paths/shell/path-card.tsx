import type { CSSProperties, ReactNode } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Badge, Card, CardDescription, CardHeader, CardTitle } from "@open-sharia-enterprise/web-ui";
import { cn } from "@/lib/utils";
import { contentUrl } from "@/features/content/core/content-url";
import type { Locale } from "@/features/i18n/core/config";
import { t } from "@/features/i18n/core/translations";
import type { PathManifest } from "../core/schemas";
import { hueCssVars, hueForManifest } from "../core/path-hue";
import { LEARN_PATHS_PREFIX } from "./paths-route";
import { humanizeKebabSlug } from "./course-path-nav";

export type PathCardContext = "hero" | "hub";

export interface PathCardProps {
  locale: string;
  manifest: PathManifest;
  /** Screen 0's `hero` variant (goal-framed) vs. Screen 1's `hub` variant (formal name + description). */
  context: PathCardContext;
  /** Careers cards show a course-count badge; skills cards omit it pre-manifest (no meaningful count yet). */
  showCourseCount?: boolean;
  /**
   * The hero variant's humanized/authored arc title (UWT-001 fix, phase-5 rule-15 retest) — used in
   * place of the raw `manifest.arc` slug. Optional/defaulted to `manifest.arc` so a caller unaware
   * of arc-title resolution still renders (just without the humanization).
   */
  arcTitle?: string;
}

/**
 * One path rendered as a card — the **single** `PathCard` implementation shared by the landing
 * hero (Screen 0, `context="hero"`) and the paths hub (Screen 1, `context="hub"`), per prd.md's
 * shared design legend. A single `<Link>` wraps the whole `Card` (the shipped `SectionCard`
 * pattern), so there is no link-in-link.
 */
export function PathCard({ locale, manifest, context, showCourseCount = true, arcTitle }: PathCardProps) {
  const href = contentUrl(locale as Locale, `${LEARN_PATHS_PREFIX}/${manifest.pathId}`);
  const courseCount = manifest.courseOrder.length;
  // One consistent, concise accessible name for BOTH contexts (EWT-001 fix) — the prior hero
  // variant concatenated the full `manifest.description` (a multi-clause sentence, sometimes
  // QA-authoring commentary in fixture data) into `aria-label`, which a sighted hero reader never
  // sees; the hub variant did the opposite (visible description never announced). Neither
  // `manifest.description` nor `manifest.arc` is announced here — the visible `CardDescription`
  // text (shown for both variants below) already carries that content for sighted users, and a
  // longer description belongs behind `aria-describedby`, not concatenated into the name.
  const label = `Start the ${manifest.title} path — ${courseCount} courses`;

  // DWT-001 fix (phase-5 rule-15 design-tester retest): every one of this plan's five committed,
  // Selected hi-fi mockups depicts a per-arc/per-compliance-track hue-coded `border-l-4` and a
  // hue-wash course-count badge (prd.md's Screen 0/1 hi-fi specs) — the shipped card carried
  // neither. `hue` is `undefined` for any arc/subject not yet named in the DD-50 map (this plan's
  // own e2e fixtures, or a real skills subject not yet authored by its owning plan), in which case
  // the card renders exactly as before: a plain neutral border, no wash badge.
  const hue = hueForManifest(manifest);
  const hueStyle = hue ? (hueCssVars(hue) as CSSProperties) : undefined;

  return (
    <Link href={href} aria-label={label} className="group block focus-visible:outline-none">
      <Card
        style={hueStyle}
        className={cn(
          "h-full rounded-xl transition-colors group-focus-visible:ring-2 group-focus-visible:ring-ring hover:bg-accent hover:shadow-md",
          hue && "border-l-4 border-l-[var(--hue-current)]",
        )}
      >
        <CardHeader>
          <CardTitle className="text-lg font-semibold">{manifest.title}</CardTitle>
          {/* `line-clamp-3` (UWT-006 fix, phase-5 rule-15 retest): without a length constraint,
              sibling cards in the same grid row varied by 80-100px in height depending on
              description length, unbounded by any real content-length ceiling — clamping bounds
              that variance to a small, predictable range regardless of copy length. */}
          <CardDescription className="line-clamp-3 text-sm text-muted-foreground">
            {context === "hero" ? (arcTitle ?? manifest.arc) : manifest.description}
          </CardDescription>
          {showCourseCount && (
            <Badge
              variant="secondary"
              size="sm"
              style={hueStyle}
              className={cn(hue && "bg-[var(--hue-current-wash)] text-[var(--hue-current-ink)]")}
            >{`~${courseCount} courses`}</Badge>
          )}
          <span className="mt-2 inline-flex items-center gap-1 text-sm font-medium text-primary">
            {t(locale as Locale, "pathsStart")}
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
  /**
   * The arc's humanized/authored display title (same UWT-001 fix family as `buildArcTitleIndex`) —
   * defaults to {@link humanizeKebabSlug}`(arc)` so a caller unaware of arc-title resolution still
   * renders plain language, never the raw `arc` slug (e.g. `"immediately-effective"`), which the
   * hub's own `<h3>` sub-heading rendered verbatim before this fix.
   */
  arcTitle?: string;
  children: ReactNode;
}

/**
 * One careers arc's role-card row inside the paths hub's Careers section (Screen 1, R6) — an
 * `<h3>` arc sub-heading (correctly nested under the section's `<h2>`) followed by the arc's
 * `PathCard` grid.
 */
export function ArcGroup({ arc, arcTitle, children }: ArcGroupProps) {
  return (
    <div>
      <h3 className="mt-6 text-xs font-medium tracking-wide text-muted-foreground uppercase">
        {arcTitle ?? humanizeKebabSlug(arc)}
      </h3>
      <ul className="mt-2 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">{children}</ul>
    </div>
  );
}
