import Link from "next/link";
import type { Locale } from "@/features/i18n/core/config";
import { t } from "@/features/i18n/core/translations";
import type { PathManifest } from "@/features/course-paths/core/schemas";
import { PathCard } from "@/features/course-paths/shell/path-card";
import { careersManifests, LEARN_PATHS_PREFIX } from "@/features/course-paths/shell/paths-route";

interface HeroProps {
  locale: Locale;
  /**
   * The same loaded-manifest data the paths hub renders from (Cycle 3.2) — never a second,
   * hard-coded list. Optional/defaulted to `[]` so every pre-existing call site that renders no
   * path data stays valid unchanged.
   */
  manifests?: readonly PathManifest[];
}

/** R1: the hero's careers-path grid never shows more than four cards. */
const HERO_CAREERS_CARD_CAP = 4;

/**
 * Landing hero (Screen 0) — the page's single H1, the intro tagline, and the "Choose your path"
 * `PathCard` grid (Cycle 3.2). The previous standalone Learn/Tools CTA buttons are retired: both
 * destinations (`/{locale}/browse`, `/{locale}/tools`) are already reachable from the global nav's
 * `PRIMARY_NAV_LINKS` (`header.tsx`), so the hero's primary visual weight becomes the path
 * decision instead of duplicating navigation the header already provides.
 */
export function Hero({ locale, manifests = [] }: HeroProps) {
  const heroManifests = careersManifests(manifests).slice(0, HERO_CAREERS_CARD_CAP);

  return (
    <section className="px-6 pt-12 pb-10 lg:px-8 lg:pt-16">
      <div className="mx-auto max-w-6xl">
        <h1 className="max-w-3xl text-4xl font-extrabold tracking-tight text-balance sm:text-5xl lg:text-6xl">
          {t(locale, "heroHeading")}
        </h1>
        <p className="mt-5 max-w-2xl text-lg text-muted-foreground">{t(locale, "heroIntro")}</p>

        <p className="mt-8 text-sm font-semibold tracking-wide text-muted-foreground uppercase">Choose your path</p>
        <ul className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
          {heroManifests.map((manifest) => (
            <li key={manifest.pathId}>
              <PathCard locale={locale} manifest={manifest} context="hero" />
            </li>
          ))}
        </ul>

        <div className="mt-6 flex flex-wrap items-center gap-x-5 gap-y-2">
          <Link href={`/${locale}/${LEARN_PATHS_PREFIX}`} className="text-sm font-medium text-[var(--hue-honey-ink)]">
            Compare all paths →
          </Link>
          <Link
            href={`/${locale}/${LEARN_PATHS_PREFIX}/skills`}
            className="text-sm font-medium text-[var(--hue-sky-ink)]"
          >
            Explore skills paths →
          </Link>
          <Link href={`/${locale}/browse`} className="text-sm text-muted-foreground">
            Browse the full course library →
          </Link>
        </div>
      </div>
    </section>
  );
}
