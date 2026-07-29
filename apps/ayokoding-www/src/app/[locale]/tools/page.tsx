import Link from "next/link";
import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";

export default async function ToolsIndexPage({ params }: { params: Promise<{ locale: Locale }> }) {
  const { locale } = await params;
  return (
    // A plain `<div>`, not `<main>` — `layout.tsx`'s `<main id="main-content">` is already the
    // page's one landmark; a second nested `<main>` here produced two `role="main"` landmarks on
    // this page, invalid HTML5 and a WCAG 4.1.2/1.3.1 defect (Rule-15 EWT-001 fix).
    <div className="mx-auto max-w-6xl space-y-4 px-4 py-6">
      <h1 className="text-2xl font-bold tracking-tight">{t(locale, "toolsPageTitle")}</h1>
      <ul className="space-y-2">
        <li>
          <Link href="./tools/cost-of-living-calculator" className="text-primary underline">
            {t(locale, "toolsPageCalcLink")}
          </Link>
          <p data-testid="tool-desc-calculator" className="text-sm text-muted-foreground">
            {t(locale, "toolsPageCalcDesc")}
          </p>
        </li>
        <li>
          <Link href="./tools/ai-benchmark" className="text-primary underline">
            {t(locale, "toolsPageAiBenchLink")}
          </Link>
          <p data-testid="tool-desc-ai-benchmark" className="text-sm text-muted-foreground">
            {t(locale, "toolsPageAiBenchDesc")}
          </p>
        </li>
      </ul>
    </div>
  );
}
