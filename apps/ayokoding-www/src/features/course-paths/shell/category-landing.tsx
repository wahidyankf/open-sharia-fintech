import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Badge, Card, CardDescription, CardHeader, CardTitle } from "@open-sharia-enterprise/web-ui";
import { contentUrl } from "@/features/content/core/content-url";
import type { Locale } from "@/features/i18n/core/config";
import type { PathManifest } from "../core/schemas";
import { PathCard } from "./path-card";
import { EmptyPathListState } from "./empty-path-list-state";
import { RampMilestoneStrip } from "./ramp-milestone-strip";
import { groupCareersManifestsByArc, skillsManifests, LEARN_PATHS_PREFIX } from "./paths-route";

export type PathCategory = "careers" | "skills";

export interface CategoryLandingProps {
  locale: string;
  category: PathCategory;
  manifests: readonly PathManifest[];
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
export function CategoryLanding({ locale, category, manifests }: CategoryLandingProps) {
  if (category === "careers") {
    return <CareersCategoryLanding locale={locale} manifests={manifests} />;
  }

  return <SkillsCategoryLanding locale={locale} manifests={manifests} />;
}

function CareersCategoryLanding({ locale, manifests }: { locale: string; manifests: readonly PathManifest[] }) {
  const arcGroups = groupCareersManifestsByArc(manifests);

  if (arcGroups.length === 0) {
    return (
      <EmptyPathListState
        fallbackHref={contentUrl(locale as Locale, `${LEARN_PATHS_PREFIX}/skills`)}
        fallbackLabel="Skills"
      />
    );
  }

  return (
    <nav aria-label="Careers arcs">
      <ul className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {arcGroups.map(({ arc, manifests: arcManifests }) => (
          <li key={arc}>
            <ArcCard locale={locale} arc={arc} manifests={arcManifests} />
          </li>
        ))}
      </ul>
    </nav>
  );
}

function ArcCard({ locale, arc, manifests }: { locale: string; arc: string; manifests: PathManifest[] }) {
  const href = contentUrl(locale as Locale, `${LEARN_PATHS_PREFIX}/careers/${arc}`);
  const roleNames = manifests.map((manifest) => roleFromPathId(manifest.pathId));

  return (
    <Link
      href={href}
      aria-label={`Explore the ${arc} arc — ${roleNames.join(", ")}`}
      className="group block focus-visible:outline-none"
    >
      <Card className="h-full rounded-xl border-l-4 transition-colors group-focus-visible:ring-2 group-focus-visible:ring-ring hover:bg-accent hover:shadow-md">
        <CardHeader>
          <CardTitle className="text-lg font-semibold">{arc}</CardTitle>
          <CardDescription className="text-sm text-muted-foreground">Explore this arc&apos;s roles</CardDescription>
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
            Explore arc
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
