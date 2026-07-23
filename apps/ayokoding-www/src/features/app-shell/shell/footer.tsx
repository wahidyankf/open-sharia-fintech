import Link from "next/link";
import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import { contentUrl } from "@/features/content/core/content-url";
import { PRIMARY_NAV_LINKS } from "@/features/app-shell/core/nav-links";

interface FooterProps {
  locale: string;
}

export function Footer({ locale }: FooterProps) {
  const year = new Date().getFullYear();
  const loc = locale as Locale;

  // Shared primary destinations — kept in lockstep with the header + mobile nav.
  const learnLink = PRIMARY_NAV_LINKS.find((l) => l.labelKey === "navLearn");
  const learnHref = learnLink ? learnLink.hrefFor(loc) : `/${locale}/browse`;

  // Loose top-level pages resolve to bare `/{locale}/{slug}` via contentUrl.
  const aboutHref = contentUrl(loc, loc === "id" ? "tentang-ayokoding" : "about-ayokoding");
  const termsHref = contentUrl(loc, loc === "id" ? "syarat-dan-ketentuan" : "terms-and-conditions");

  const columnHeading = "mb-3 text-sm font-semibold text-foreground";
  const columnLink = "block py-1 text-sm text-muted-foreground transition-colors hover:text-foreground";

  return (
    <footer className="border-t border-border py-10">
      <div className="mx-auto max-w-screen-2xl px-4">
        <nav aria-label="Footer" className="grid grid-cols-2 gap-8 text-sm sm:grid-cols-3 lg:grid-cols-4">
          <div>
            <h2 className={columnHeading}>{t(loc, "footerLearn")}</h2>
            <Link href={learnHref} className={columnLink}>
              {t(loc, "footerBrowseAll")}
            </Link>
          </div>

          <div>
            <h2 className={columnHeading}>{t(loc, "footerTools")}</h2>
            <Link href={`/${locale}/tools/cost-of-living-calculator`} className={columnLink}>
              {t(loc, "footerCalculator")}
            </Link>
          </div>

          <div>
            <h2 className={columnHeading}>{t(loc, "footerAbout")}</h2>
            <Link href={aboutHref} className={columnLink}>
              {t(loc, "footerAboutAyokoding")}
            </Link>
            <Link href={termsHref} className={columnLink}>
              {t(loc, "footerTerms")}
            </Link>
          </div>

          <div>
            <h2 className={columnHeading}>{t(loc, "footerProject")}</h2>
            <a
              href="https://github.com/wahidyankf/ose-public"
              target="_blank"
              rel="noopener noreferrer"
              className={columnLink}
            >
              {t(loc, "openSourceProject")}
            </a>
          </div>
        </nav>

        <p className="mt-10 border-t border-border pt-6 text-sm text-muted-foreground">
          &copy; {year} AyoKoding &middot;{" "}
          <a
            href="https://github.com/wahidyankf/ose-public/blob/main/LICENSE"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-foreground"
          >
            MIT
          </a>{" "}
          &middot; {t(loc, "openSourceProject")}
        </p>
      </div>
    </footer>
  );
}
