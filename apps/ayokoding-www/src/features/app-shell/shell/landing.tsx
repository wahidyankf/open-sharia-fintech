import type { Locale } from "@/features/i18n/core/config";
import { t } from "@/features/i18n/core/translations";
import type { LandingSectionDescriptor } from "@/features/content/core/landing-sections";
import { contentUrl } from "@/features/content/core/content-url";
import { SectionCard } from "@/features/content/shell/section-card";
import type { PathManifest } from "@/features/course-paths/core/schemas";
import { Hero } from "./hero";
import { ToolsTeaser } from "./tools-teaser";

interface LandingProps {
  locale: Locale;
  /** Resolved, ordered, visible landing-section descriptors (from `mergeLandingSections`). */
  sections: LandingSectionDescriptor[];
  /** Threaded straight through to {@link Hero}'s `PathCard` grid (Cycle 3.2) — see its own doc comment. */
  manifests?: readonly PathManifest[];
}

/**
 * Presentational landing homepage — composes the {@link Hero}, an "Explore"
 * grid of section cards, and the {@link ToolsTeaser}. Pure view: it takes the
 * already-merged `sections` and renders; all IO (`getTree` + merge) stays in
 * the server component (`app/[locale]/page.tsx`).
 *
 * Single H1 lives in the hero; the section grid is an `aria-labelled` H2
 * landmark. Single-column stack on mobile, multi-column grid on desktop, per
 * the Option-A `landing-*.png` mockups.
 */
export function Landing({ locale, sections, manifests }: LandingProps) {
  return (
    <div>
      <Hero locale={locale} manifests={manifests} />

      <section aria-labelledby="explore-heading" className="px-6 py-4 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <h2 id="explore-heading" className="mb-6 text-2xl font-bold tracking-tight">
            {t(locale, "sectionExploreHeading")}
          </h2>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {sections.map((section) => (
              <SectionCard
                key={section.slug}
                href={contentUrl(locale, section.slug)}
                title={section.title}
                description={section.blurb}
              />
            ))}
          </div>
        </div>
      </section>

      <ToolsTeaser locale={locale} />
    </div>
  );
}
