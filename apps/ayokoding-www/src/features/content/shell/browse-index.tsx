import type { TreeNode } from "@/features/content/core/types";
import { contentUrl } from "@/features/content/core/content-url";
import type { Locale } from "@/features/i18n/core/config";
import { t } from "@/features/i18n/core/translations";
import { Breadcrumb } from "@/features/navigation/shell/breadcrumb";
import { SectionCard } from "./section-card";

interface BrowseIndexProps {
  locale: Locale;
  sections: TreeNode[];
}

/**
 * Presentational browse index — renders one {@link SectionCard} per top-level
 * content section plus a `Home > Browse` breadcrumb. Pure view: it takes the
 * already-fetched `sections` and renders; all IO stays in the server component
 * (`app/[locale]/(content)/browse/page.tsx`).
 */
export function BrowseIndex({ locale, sections }: BrowseIndexProps) {
  const breadcrumbSegments = [
    { label: t(locale, "breadcrumbHome"), slug: "" },
    { label: t(locale, "browseTitle"), slug: "browse" },
  ];

  return (
    <div className="min-w-0 flex-1 px-6 py-8 lg:px-8">
      <Breadcrumb locale={locale} slug="browse" segments={breadcrumbSegments} showCurrent />

      <h1 className="mb-2 text-4xl font-extrabold tracking-tight">{t(locale, "browseTitle")}</h1>
      <p className="mb-8 text-muted-foreground">{t(locale, "browseIntro")}</p>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {sections.map((section) => (
          <SectionCard
            key={section.slug}
            href={contentUrl(locale, section.slug)}
            title={section.title}
            description={t(locale, "sectionBlurbFallback")}
          />
        ))}
      </div>
    </div>
  );
}
