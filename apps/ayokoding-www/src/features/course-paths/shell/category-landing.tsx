import type { CSSProperties } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Badge, Card, CardDescription, CardHeader, CardTitle } from "@open-sharia-enterprise/web-ui";
import { cn } from "@/lib/utils";
import { contentUrl } from "@/features/content/core/content-url";
import type { Locale } from "@/features/i18n/core/config";
import { t } from "@/features/i18n/core/translations";
import type { ContentMeta } from "@/features/content/core/types";
import type { PathManifest } from "../core/schemas";
import { hueCssVars, hueForCareersArc } from "../core/path-hue";
import { PathCard } from "./path-card";
import { EmptyPathListState } from "./empty-path-list-state";
import { RampMilestoneStrip } from "./ramp-milestone-strip";
import { groupCareersManifestsByArc, skillsManifests, LEARN_PATHS_PREFIX } from "./paths-route";
import { buildArcTitleIndex, humanizeKebabSlug } from "./course-path-nav";

export type PathCategory = "careers" | "skills";

export interface CategoryLandingProps {
  locale: string;
  category: PathCategory;
  manifests: readonly PathManifest[];
  /**
   * The loaded content index's `contentMap` — resolves each arc's humanized title from its own
   * `_index.md` (UWT-001 fix, phase-5 rule-15 retest), rather than rendering the raw arc slug.
   * Optional/defaulted to an empty map so existing callers/tests unaware of it still render (via
   * `buildArcTitleIndex`'s own humanized-slug fallback), just without a real authored title.
   */
  contentMap?: ReadonlyMap<string, ContentMeta>;
}

/** The role (last pathId segment) of a `careers/<arc>/<role>` manifest. */
function roleFromPathId(pathId: string): string {
  return pathId.split("/").at(-1) ?? pathId;
}

/**
 * Category landing (Cycle 3.1b-i/3.1b-ii, R7) — `/en/learn/paths/careers/` and
 * `/en/learn/paths/skills/`. **Two distinct instances, not one template with swapped data (R8)**:
 * the careers instance renders an `ArcCard` grid (an arc chooser); the skills instance renders the
 * shared `PathCard` hub grid plus a `RampMilestoneStrip` per card and states the fixed-arc ramp
 * promise once, with no chooser markup present at all.
 */
export function CategoryLanding({ locale, category, manifests, contentMap = new Map() }: CategoryLandingProps) {
  if (category === "careers") {
    return <CareersCategoryLanding locale={locale} manifests={manifests} contentMap={contentMap} />;
  }

  return <SkillsCategoryLanding locale={locale} manifests={manifests} />;
}

function CareersCategoryLanding({
  locale,
  manifests,
  contentMap,
}: {
  locale: string;
  manifests: readonly PathManifest[];
  contentMap: ReadonlyMap<string, ContentMeta>;
}) {
  const arcGroups = groupCareersManifestsByArc(manifests);

  if (arcGroups.length === 0) {
    return (
      <EmptyPathListState
        fallbackHref={contentUrl(locale as Locale, `${LEARN_PATHS_PREFIX}/skills`)}
        fallbackLabel="Skills"
      />
    );
  }

  const arcTitles = buildArcTitleIndex(
    contentMap,
    locale,
    arcGroups.map(({ arc }) => arc),
  );

  return (
    <nav aria-label="Careers arcs">
      <ul className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {arcGroups.map(({ arc, manifests: arcManifests }) => (
          <li key={arc}>
            <ArcCard locale={locale} arc={arc} arcTitle={arcTitles[arc] ?? arc} manifests={arcManifests} />
          </li>
        ))}
      </ul>
    </nav>
  );
}

function ArcCard({
  locale,
  arc,
  arcTitle,
  manifests,
}: {
  locale: string;
  arc: string;
  /** The arc's humanized/authored display title (UWT-001 fix) — never the raw `arc` slug. */
  arcTitle: string;
  manifests: PathManifest[];
}) {
  const href = contentUrl(locale as Locale, `${LEARN_PATHS_PREFIX}/careers/${arc}`);
  const roleNames = manifests.map((manifest) => humanizeKebabSlug(roleFromPathId(manifest.pathId)));
  // DWT-001 fix (phase-5 rule-15 design-tester retest): the committed category-landing mockup
  // (`../assets/category-landing-option-a-desktop.png`, Selected) shows each `ArcCard` in its arc's
  // hue — the shipped card already carried the `border-l-4` width class but never a colour, so the
  // "wider stripe" rendered in the same neutral border colour as the other three edges.
  const hue = hueForCareersArc(arc);
  const hueStyle = hue ? (hueCssVars(hue) as CSSProperties) : undefined;

  return (
    <Link
      href={href}
      aria-label={`Explore the ${arcTitle} arc — ${roleNames.join(", ")}`}
      className="group block focus-visible:outline-none"
    >
      <Card
        style={hueStyle}
        className={cn(
          "h-full rounded-xl border-l-4 transition-colors group-focus-visible:ring-2 group-focus-visible:ring-ring hover:bg-accent hover:shadow-md",
          hue && "border-l-[var(--hue-current)]",
        )}
      >
        <CardHeader>
          <CardTitle className="text-lg font-semibold">{arcTitle}</CardTitle>
          <CardDescription className="text-sm text-muted-foreground">
            {t(locale as Locale, "pathsExploreArcRoles")}
          </CardDescription>
          <ul className="mt-2 flex flex-wrap gap-1">
            {roleNames.map((name) => (
              <li key={name}>
                <Badge variant="secondary" size="sm">
                  {name}
                </Badge>
              </li>
            ))}
          </ul>
          <span className="mt-2 inline-flex items-center gap-1 text-sm font-medium text-primary">
            {t(locale as Locale, "pathsExploreArc")}
            <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
          </span>
        </CardHeader>
      </Card>
    </Link>
  );
}

function SkillsCategoryLanding({ locale, manifests }: { locale: string; manifests: readonly PathManifest[] }) {
  const skills = skillsManifests(manifests);

  if (skills.length === 0) {
    return (
      <EmptyPathListState
        fallbackHref={contentUrl(locale as Locale, `${LEARN_PATHS_PREFIX}/careers`)}
        fallbackLabel="Careers"
      />
    );
  }

  return (
    <>
      <p className="mt-2 text-muted-foreground">
        Get up and running fast on the ramp — every skills path starts safe, gets you productive quickly, and goes
        deeper from there.
      </p>
      <nav aria-label="Skills paths">
        <ul className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
          {skills.map((manifest) => (
            <li key={manifest.pathId}>
              <PathCard locale={locale} manifest={manifest} context="hub" showCourseCount={false} />
              <RampMilestoneStrip />
            </li>
          ))}
        </ul>
      </nav>
    </>
  );
}
