import type { Metadata } from "next";
import { GoogleAnalytics } from "@next/third-parties/google";
import { notFound } from "next/navigation";
import { ThemeProvider } from "next-themes";
import "katex/dist/katex.min.css";
import "../globals.css";
import { SUPPORTED_LOCALES, isValidLocale } from "@/features/i18n/core/config";
import { TRPCProvider } from "@/lib/trpc/provider";
import { SearchProvider } from "@/features/search/shell/search-provider";
import { Header } from "@/features/app-shell/shell/header";
import { Footer } from "@/features/app-shell/shell/footer";
import { SkipLink } from "@/features/app-shell/shell/skip-link";
import { MobileNavOpenProvider } from "@/features/app-shell/shell/mobile-nav-open-provider";
import { loadRoutePathData } from "@/features/course-paths/shell/route-path-data";
import { toCoursePathClientData } from "@/features/course-paths/shell/course-path-nav";

export const metadata: Metadata = {
  title: {
    default: "AyoKoding",
    template: "%s | AyoKoding",
  },
  description:
    "Bilingual educational platform for software engineering - helping the Indonesian tech community learn and grow",
  metadataBase: new URL("https://ayokoding.com"),
};

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
  const clientPathData = toCoursePathClientData(pathData, locale);

  return (
    <html lang={(await params).locale} suppressHydrationWarning>
      <body className="min-h-screen antialiased">
        <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
          <TRPCProvider>
            <SearchProvider>
              <MobileNavOpenProvider>
                <SkipLink locale={locale} />
                <div className="flex min-h-screen flex-col">
                  <Header locale={locale} pathData={clientPathData} />
                  <main id="main-content" tabIndex={-1} className="flex-1 outline-none">
                    {children}
                  </main>
                  <Footer locale={locale} />
                </div>
              </MobileNavOpenProvider>
            </SearchProvider>
          </TRPCProvider>
        </ThemeProvider>
        <GoogleAnalytics gaId="G-1NHDR7S3GV" />
      </body>
    </html>
  );
}
