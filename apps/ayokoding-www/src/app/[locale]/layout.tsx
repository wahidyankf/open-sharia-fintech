import { notFound } from "next/navigation";
import { ThemeProvider } from "next-themes";
import { SUPPORTED_LOCALES, isValidLocale } from "@/features/i18n/core/config";
import { TRPCProvider } from "@/lib/trpc/provider";
import { SearchProvider } from "@/features/search/shell/search-provider";
import { Header } from "@/features/app-shell/shell/header";
import { Footer } from "@/features/app-shell/shell/footer";
import { SkipLink } from "@/features/app-shell/shell/skip-link";
import { MobileNavOpenProvider } from "@/features/app-shell/shell/mobile-nav-open-provider";
import { loadRoutePathData } from "@/features/course-paths/shell/route-path-data";
import { buildCourseTitleIndex } from "@/features/course-paths/shell/course-path-nav";

export function generateStaticParams() {
  return SUPPORTED_LOCALES.map((locale) => ({ locale }));
}

interface Props {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}

export default async function LocaleLayout({ children, params }: Props) {
  const { locale } = await params;

  if (!isValidLocale(locale)) {
    notFound();
  }

  // Course-paths plan (Cycle 2.9) — loaded here (not per-page) so the header's mobile nav drawer
  // can detect an active path context on every route, not just under (content)/.
  const pathData = await loadRoutePathData(locale);
  const courseTitles = buildCourseTitleIndex(pathData.contentMap, locale, pathData.manifests);

  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
      <TRPCProvider>
        <SearchProvider>
          <MobileNavOpenProvider>
            <SkipLink locale={locale} />
            <div className="flex min-h-screen flex-col">
              <Header locale={locale} manifests={pathData.manifests} courseTitles={courseTitles} />
              <main id="main-content" tabIndex={-1} className="flex-1 outline-none">
                {children}
              </main>
              <Footer locale={locale} />
            </div>
          </MobileNavOpenProvider>
        </SearchProvider>
      </TRPCProvider>
    </ThemeProvider>
  );
}
