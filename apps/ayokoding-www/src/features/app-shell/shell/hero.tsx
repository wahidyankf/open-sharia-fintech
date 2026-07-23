import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Button } from "@open-sharia-enterprise/web-ui";
import type { Locale } from "@/features/i18n/core/config";
import { t } from "@/features/i18n/core/translations";

interface HeroProps {
  locale: Locale;
}

/**
 * Landing hero — the page's single H1 plus the intro tagline and the two
 * primary CTAs (Learn → `/{locale}/browse`, Tools → `/{locale}/tools`). All
 * copy resolves through {@link t}; the buttons reuse the shared `Button`
 * token surface (no net-new primitive).
 */
export function Hero({ locale }: HeroProps) {
  return (
    <section className="px-6 pt-12 pb-10 lg:px-8 lg:pt-16">
      <div className="mx-auto max-w-6xl">
        <h1 className="max-w-3xl text-4xl font-extrabold tracking-tight text-balance sm:text-5xl lg:text-6xl">
          {t(locale, "heroHeading")}
        </h1>
        <p className="mt-5 max-w-2xl text-lg text-muted-foreground">{t(locale, "heroIntro")}</p>
        <div className="mt-8 flex flex-col gap-3 sm:flex-row">
          <Button asChild size="lg">
            <Link href={`/${locale}/browse`}>
              {t(locale, "heroCtaLearn")}
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
          </Button>
          <Button asChild size="lg" variant="outline">
            <Link href={`/${locale}/tools`}>{t(locale, "heroCtaTools")}</Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
