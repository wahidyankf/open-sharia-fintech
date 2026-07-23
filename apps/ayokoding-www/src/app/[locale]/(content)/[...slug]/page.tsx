import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { serverCaller } from "@/lib/trpc/server";
import { isValidLocale, type Locale } from "@/features/i18n/core/config";
import { t } from "@/features/i18n/core/translations";
import { contentUrl } from "@/features/content/core/content-url";
import { slugFromSegments } from "@/features/content/core/slug";
import { Breadcrumb } from "@/features/navigation/shell/breadcrumb";
import { TableOfContents } from "@/features/navigation/shell/toc";
import { PrevNext } from "@/features/navigation/shell/prev-next";
import { MarkdownRenderer } from "@/features/content/shell/markdown-renderer";
import { TRPCError } from "@trpc/server";
import { createTRPCContext } from "@/features/app-shell/shell/trpc-init";

export const dynamicParams = false;

export async function generateStaticParams({ params }: { params: { locale: string } }) {
  // Widened (DD-48 de-namespacing): this catch-all now serves the ENTIRE
  // content tree, not just the per-locale loose top-level pages — the merged
  // route absorbed this generateStaticParams from the retired c/[...slug]
  // route. Every content-tree slug, including the two loose pages
  // (about-ayokoding/terms-and-conditions for en, tentang-ayokoding/
  // syarat-dan-ketentuan for id), is already a member of index.contentMap
  // (readAllContent globs every .md under the locale's content dir with no
  // loose-page exclusion — verified at delivery time, apps/ayokoding-www/src/
  // features/content/shell/reader.ts + service.ts's buildContentIndex), so
  // one enumeration covers both without a separate LOOSE_PAGE_ALLOWLIST
  // union. LOOSE_PAGE_ALLOWLIST and isLoosePage() are therefore removed
  // entirely (content-url.ts) rather than kept for this call site.
  // (The locale root "" / "_index" is served by app/[locale]/page.tsx, not
  // this catch-all.)
  if (!isValidLocale(params.locale)) return [];

  const { contentService } = createTRPCContext();
  const index = await contentService.getIndex();
  const slugs: { slug: string[] }[] = [];

  for (const [key, meta] of index.contentMap) {
    if (!key.startsWith(`${params.locale}:`)) continue;
    if (meta.slug === "") continue;
    slugs.push({ slug: meta.slug.split("/") });
  }

  return slugs;
}

interface Props {
  params: Promise<{ locale: string; slug: string[] }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale, slug } = await params;
  const slugStr = slugFromSegments(slug);

  try {
    const page = await serverCaller.content.getBySlug({
      locale: locale as Locale,
      slug: slugStr,
    });

    return {
      title: page.title,
      description: page.description ?? undefined,
      alternates: {
        canonical: contentUrl(locale as Locale, slugStr),
        languages: {
          en: contentUrl("en", slugStr),
          "x-default": contentUrl("en", slugStr),
        },
      },
      openGraph: {
        title: page.title,
        description: page.description ?? undefined,
        type: "article",
        locale: locale === "id" ? "id_ID" : "en_US",
      },
    };
  } catch {
    return { title: "Not Found" };
  }
}

export default async function ContentPage({ params }: Props) {
  const { locale, slug } = await params;
  const slugStr = slugFromSegments(slug);

  let page;
  try {
    page = await serverCaller.content.getBySlug({
      locale: locale as Locale,
      slug: slugStr,
    });
  } catch (err) {
    if (err instanceof TRPCError && err.code === "NOT_FOUND") {
      notFound();
    }
    throw err;
  }

  const breadcrumbSegments = buildBreadcrumbs(locale, slugStr, page.title);

  return (
    <>
      <article className="min-w-0 flex-1 px-6 py-8 lg:px-8">
        <Breadcrumb locale={locale} slug={slugStr} segments={breadcrumbSegments} />

        <h1 className="mb-6 text-4xl font-extrabold tracking-tight">{page.title}</h1>

        <MarkdownRenderer html={page.html} locale={locale} />

        {page.date && (
          <p className="mt-8 text-sm text-muted-foreground">
            {t(locale as Locale, "lastUpdated")}{" "}
            {new Date(page.date).toLocaleDateString(locale === "id" ? "id-ID" : "en-US", {
              year: "numeric",
              month: "long",
              day: "numeric",
            })}
          </p>
        )}

        <PrevNext locale={locale} prev={page.prev} next={page.next} />
      </article>

      <aside className="hidden w-[200px] shrink-0 xl:block">
        <div className="sticky top-20 p-4">
          <TableOfContents headings={page.headings} label={t(locale as Locale, "onThisPage")} />
        </div>
      </aside>
    </>
  );
}

function buildBreadcrumbs(
  locale: string,
  slug: string,
  currentTitle: string,
): { label: string; slug: string; href?: string }[] {
  const parts = slug.split("/");
  // Home -> /{locale}; Browse -> /{locale}/browse. The "Browse" segment,
  // carried over from the retired c/[...slug] route (DD-48), used to point
  // at /{locale}/c; it now points at the relocated browse/ route.
  const segments: { label: string; slug: string; href?: string }[] = [
    { label: t(locale as Locale, "breadcrumbHome"), slug: "" },
    { label: t(locale as Locale, "browseTitle"), slug: "browse", href: `/${locale}/browse` },
  ];

  for (let i = 0; i < parts.length - 1; i++) {
    const part = parts[i];
    if (!part) continue;
    segments.push({
      label: part.charAt(0).toUpperCase() + part.slice(1).replace(/-/g, " "),
      slug: parts.slice(0, i + 1).join("/"),
    });
  }

  segments.push({ label: currentTitle, slug });
  return segments;
}
