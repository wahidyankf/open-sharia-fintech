import { notFound } from "next/navigation";
import { ThemeProvider } from "next-themes";
import { SUPPORTED_LOCALES, isValidLocale } from "@/features/i18n/core/config";
import { TRPCProvider } from "@/lib/trpc/provider";
import { SearchProvider } from "@/features/search/shell/search-provider";
import { Header } from "@/features/app-shell/shell/header";
import { Footer } from "@/features/app-shell/shell/footer";
import { SkipLink } from "@/features/app-shell/shell/skip-link";

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

  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
      <TRPCProvider>
        <SearchProvider>
          <SkipLink locale={locale} />
          <div className="flex min-h-screen flex-col">
            <Header locale={locale} />
            <main id="main-content" tabIndex={-1} className="flex-1 outline-none">
              {children}
            </main>
            <Footer locale={locale} />
          </div>
        </SearchProvider>
      </TRPCProvider>
    </ThemeProvider>
  );
}
