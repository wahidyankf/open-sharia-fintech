import { notFound } from "next/navigation";
import Link from "next/link";
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
import {
  courseIdFromSlug,
  resolveCoursePathRenderData,
  coursePositionInManifest,
  buildCourseTitleIndex,
  buildArcTitleIndex,
  type PrerequisiteLink,
} from "@/features/course-paths/shell/course-path-nav";
import { loadRoutePathData } from "@/features/course-paths/shell/route-path-data";
import { PrerequisiteList } from "@/features/course-paths/shell/prerequisite-list";
import { PathCourseLinks } from "@/features/course-paths/shell/path-course-links";
import { PathBanner } from "@/features/course-paths/shell/path-banner";
import {
  isLearnPathsSlug,
  resolvePathsRoute,
  groupCareersManifestsByArc,
  skillsManifests,
  manifestsForArc,
  LEARN_PATHS_PREFIX,
} from "@/features/course-paths/shell/paths-route";
import { PathCard, CategorySection, ArcGroup } from "@/features/course-paths/shell/path-card";
import { CategoryLanding } from "@/features/course-paths/shell/category-landing";
import { ArcLanding } from "@/features/course-paths/shell/arc-landing";
import { PathLanding } from "@/features/course-paths/shell/path-landing";
import { EmptyPathListState } from "@/features/course-paths/shell/empty-path-list-state";

/**
 * Widened from `false` (Phase 3, course-paths plan) — the `learn/paths/**` namespace (hub,
 * category, arc, and terminal path landings) is deliberately **excluded** from
 * `generateStaticParams` below and rendered on demand instead, because its render depends on
 * `manifest-repository.ts`'s `AYOKODING_WEB_MANIFESTS_DIR`-driven data, which must be read **fresh
 * per request** rather than baked in once at build time (the e2e suite proves this against a
 * fixture manifest set without a second, specially-configured production build). Every
 * already-enumerated content slug (every course, every loose page) is completely unaffected: it
 * stays exactly as static as before — `dynamicParams` only changes what happens for a slug
 * `generateStaticParams` does NOT return, which previously hard-404'd and now renders on demand
 * (still 404ing correctly when nothing resolves, e.g. a truly nonexistent course URL).
 */
export const dynamicParams = true;

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
    // Course-paths plan (Phase 3): the `learn/paths/**` namespace is rendered on demand (see this
    // file's `dynamicParams` doc comment above), never statically enumerated — even though real
    // `_index.md` structural files already exist for the hub/category/arc roots, their render
    // depends on freshly-loaded manifest data that a one-time static build cannot keep current.
    if (isLearnPathsSlug(meta.slug)) continue;
    slugs.push({ slug: meta.slug.split("/") });
  }

  return slugs;
}

interface Props {
  params: Promise<{ locale: string; slug: string[] }>;
  // Only `page.tsx` receives `searchParams` in the App Router (never `layout.tsx`, at any nesting
  // depth) — course-paths plan, Cycle 2.2. `generateMetadata` below does not use it.
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}

/**
 * Adapt Next.js's `searchParams` object shape (a value can be absent, a single string, or a
 * string[] for a repeated key) to the plain `URLSearchParams` the upstream `parsePathContext`
 * expects. Repeated keys append in order; `undefined` values are skipped.
 */
function urlSearchParamsFrom(raw: { [key: string]: string | string[] | undefined }): URLSearchParams {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(raw)) {
    if (value === undefined) continue;
    for (const v of Array.isArray(value) ? value : [value]) {
      params.append(key, v);
    }
  }
  return params;
}

/**
 * True when the slug's first segment under a locale's "learn" bucket is
 * "legacy" — i.e. one of the six relocated subject domains (DD-42). Used to
 * apply the Screen-4 design funnel's Option C treatment: noindex the whole
 * legacy bucket rather than an in-page landing-notice component, so search
 * engines stop ranking the older subject-organized material above the
 * course library while still crawling its internal links (follow: true).
 */
function isLegacySlug(slug: string[]): boolean {
  return slug[0] === "learn" && slug[1] === "legacy";
}

export async function generateMetadata({ params }: { params: Props["params"] }): Promise<Metadata> {
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
      ...(isLegacySlug(slug) ? { robots: { index: false, follow: true } } : {}),
    };
  } catch {
    // A terminal path landing (e.g. `careers/<arc>/<role>`) has no `_index.md` of its own — its
    // title comes from the loaded manifest instead, best-effort, rather than a bare "Not Found".
    if (isLearnPathsSlug(slugStr)) {
      const pathData = await loadRoutePathData(locale);
      const resolution = resolvePathsRoute(slugStr, pathData.manifests);
      if (resolution.kind === "path") {
        return { title: resolution.manifest.title, description: resolution.manifest.description };
      }
      // A careers arc (`learn/paths/careers/<arc>`) has no `_index.md` of its own — it is a
      // synthetic grouping derived from manifest data, not a real content page — so `getBySlug`
      // always rejects for it, including the deliberately-empty "no manifests published yet" arc
      // state. That render is a normal 200 page (`ArcLanding`'s empty-state branch), so its title
      // must not read as an error; mirror the page body's own `resolution.arc` fallback (Cycle
      // 3.1a's `<h1>{seoPage?.title ?? resolution.arc}</h1>`) rather than falling through to a bare
      // "Not Found" (a real defect found live via Playwright MCP at phase-5 manual verification).
      if (resolution.kind === "arc") {
        return { title: resolution.arc };
      }
    }
    return { title: "Not Found" };
  }
}

/**
 * The `learn/paths/**` namespace's render dispatch (course-paths plan, Phase 3) — hub (Screen 1),
 * category landing (Screen 1a), arc landing (Screen 1b, careers-only), or terminal path landing
 * (Screen 2). Returns `null` for `{ kind: "not-found" }` so the caller falls through to the
 * standard canonical content-page render (which itself 404s for a genuinely nonexistent slug).
 */
async function renderPathsRoute(locale: string, slugStr: string) {
  const pathData = await loadRoutePathData(locale);
  const resolution = resolvePathsRoute(slugStr, pathData.manifests);

  if (resolution.kind === "not-found") {
    return null;
  }

  const courseTitles = buildCourseTitleIndex(pathData.contentMap, locale, pathData.manifests);

  // Best-effort SEO/body content from this route's own `_index.md`, when one exists — every
  // careers `_index.md` (hub/category/arc roots) already exists; a terminal path's `_index.md` may
  // not (Cycle 3.1d's careers no-regression clause: silent no-op when absent).
  let seoPage: { title: string; description?: string | null; html: string } | null = null;
  try {
    seoPage = await serverCaller.content.getBySlug({ locale: locale as Locale, slug: slugStr });
  } catch (err) {
    if (!(err instanceof TRPCError && err.code === "NOT_FOUND")) {
      throw err;
    }
  }

  if (resolution.kind === "hub") {
    const careersArcGroups = groupCareersManifestsByArc(pathData.manifests);
    const skills = skillsManifests(pathData.manifests);
    // Reuses the same humanized-arc-title resolution the careers category landing already uses
    // (UWT-001 fix) — closes the adjacent gap where this hub's own `<h3>` arc sub-heading still
    // rendered the raw kebab-case `arc` slug (e.g. `"immediately-effective"`) verbatim.
    const arcTitles = buildArcTitleIndex(
      pathData.contentMap,
      locale,
      careersArcGroups.map(({ arc }) => arc),
    );

    return (
      <section className="mx-auto max-w-6xl flex-1 px-6 py-8 lg:px-8">
        <h1 className="text-4xl font-extrabold tracking-tight">{seoPage?.title ?? "Paths"}</h1>
        <p className="mt-2 text-muted-foreground">{seoPage?.description ?? "Choose your path."}</p>

        <CategorySection id="careers" heading="Careers" strapline="Converging within your role">
          {careersArcGroups.length === 0 ? (
            <EmptyPathListState
              fallbackHref={contentUrl(locale as Locale, `${LEARN_PATHS_PREFIX}/skills`)}
              fallbackLabel="Skills"
            />
          ) : (
            careersArcGroups.map(({ arc, manifests: arcManifests }) => (
              <ArcGroup key={arc} arc={arc} arcTitle={arcTitles[arc]}>
                {arcManifests.map((manifest) => (
                  <li key={manifest.pathId}>
                    <PathCard locale={locale} manifest={manifest} context="hub" />
                  </li>
                ))}
              </ArcGroup>
            ))
          )}
        </CategorySection>

        <CategorySection id="skills" heading="Skills" strapline="Up and running fast, then deeper and deeper">
          {skills.length === 0 ? (
            <EmptyPathListState
              fallbackHref={contentUrl(locale as Locale, `${LEARN_PATHS_PREFIX}/careers`)}
              fallbackLabel="Careers"
            />
          ) : (
            <ul className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
              {skills.map((manifest) => (
                <li key={manifest.pathId}>
                  <PathCard locale={locale} manifest={manifest} context="hub" showCourseCount={false} />
                </li>
              ))}
            </ul>
          )}
        </CategorySection>

        <Link
          href={`/${locale}/browse`}
          className="mt-6 inline-flex text-sm text-muted-foreground hover:text-foreground"
        >
          {t(locale as Locale, "pathsBrowseCourseLibrary")} →
        </Link>
      </section>
    );
  }

  if (resolution.kind === "category") {
    return (
      <section className="mx-auto max-w-6xl flex-1 px-6 py-8 lg:px-8">
        <h1 className="text-4xl font-extrabold tracking-tight">
          {seoPage?.title ?? (resolution.category === "careers" ? "Careers" : "Skills")}
        </h1>
        <p className="mt-2 text-muted-foreground">{seoPage?.description ?? ""}</p>
        <CategoryLanding
          locale={locale}
          category={resolution.category}
          manifests={pathData.manifests}
          contentMap={pathData.contentMap}
        />
      </section>
    );
  }

  if (resolution.kind === "arc") {
    const arcManifests = manifestsForArc(pathData.manifests, resolution.arc);
    return (
      <section className="mx-auto max-w-6xl flex-1 px-6 py-8 lg:px-8">
        <h1 className="text-4xl font-extrabold tracking-tight">{seoPage?.title ?? resolution.arc}</h1>
        <p className="mt-2 text-muted-foreground">{seoPage?.description ?? ""}</p>
        <ArcLanding locale={locale} arc={resolution.arc} manifests={arcManifests} courseTitles={courseTitles} />
      </section>
    );
  }

  return (
    <PathLanding locale={locale} manifest={resolution.manifest} courseTitles={courseTitles} bodyHtml={seoPage?.html} />
  );
}

export default async function ContentPage({ params, searchParams }: Props) {
  const { locale, slug } = await params;
  const slugStr = slugFromSegments(slug);

  // The `learn/paths/**` namespace (hub, category, arc, terminal path landings) dispatches to its
  // own renderers before the standard content-page fetch below — `renderPathsRoute` returns `null`
  // for `{ kind: "not-found" }` (an unrecognized segment, or a terminal segment naming no loaded
  // manifest), in which case this falls through to the standard render unchanged.
  if (isLearnPathsSlug(slugStr)) {
    const rendered = await renderPathsRoute(locale, slugStr);
    if (rendered !== null) {
      return rendered;
    }
  }

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

  // Path context only ever applies to course pages (courseIdFromSlug returns null for every
  // other content page) — this is the one place ROUTE decides path-aware vs. canonical
  // (Cycle 2.6's REFACTOR note); invalid, missing, and omitted-course contexts all converge on
  // resolveCoursePathRenderData's single `activeContext === null` branch below.
  const courseId = courseIdFromSlug(slugStr);
  let prev = page.prev;
  let next = page.next;
  let prerequisiteLinks: readonly PrerequisiteLink[] = [];
  let pathBadges: readonly { pathId: string; title: string }[] = [];
  let activePathId: string | undefined;
  let activePathTitle: string | undefined;
  let activeCoursePosition: { index: number; total: number } | undefined;

  if (courseId !== null) {
    const pathData = await loadRoutePathData(locale);
    const usp = urlSearchParamsFrom(await searchParams);
    const renderData = resolveCoursePathRenderData(usp, pathData, courseId, locale, page.prev, page.next);

    prev = renderData.prev;
    next = renderData.next;
    prerequisiteLinks = renderData.prerequisiteLinks;
    pathBadges = renderData.pathBadges;
    activePathId = renderData.activeContext?.pathId;
    activePathTitle = renderData.activeContext?.manifest.title;
    if (renderData.activeContext) {
      activeCoursePosition = coursePositionInManifest(renderData.activeContext.manifest, courseId);
    }
  }

  const breadcrumbSegments = buildBreadcrumbs(locale, slugStr, page.title);
  const pathContext =
    activePathId !== undefined && activePathTitle !== undefined
      ? {
          pathId: activePathId,
          pathTitle: activePathTitle,
          learnLabel: t(locale as Locale, "navLearn"),
          learnHref: `/${locale}/browse`,
        }
      : undefined;

  return (
    <>
      <article className="min-w-0 flex-1 px-6 py-8 lg:px-8">
        <Breadcrumb
          locale={locale}
          slug={slugStr}
          segments={breadcrumbSegments}
          showCurrent={Boolean(pathContext)}
          pathContext={pathContext}
        />

        <h1 className="mb-6 text-4xl font-extrabold tracking-tight">{page.title}</h1>

        {/* Rendered immediately below the H1, above the body/syllabus (UWT-004 fix, phase-5
            rule-15 retest) — the prior position (after the prerequisites, near the bottom) meant a
            mobile reader had to scroll past the entire course body before learning they were even
            inside a path, several page-heights after desktop/tablet readers see the equivalent
            rail in the very first paint (Heuristic 1: Visibility of System Status). */}
        {pathContext !== undefined && activeCoursePosition !== undefined && (
          <PathBanner
            locale={locale}
            pathTitle={pathContext.pathTitle}
            courseIndex={activeCoursePosition.index}
            totalCourses={activeCoursePosition.total}
          />
        )}

        <MarkdownRenderer html={page.html} locale={locale} />

        <PrerequisiteList locale={locale} prerequisites={prerequisiteLinks} />

        {pathContext === undefined && <PathCourseLinks locale={locale} paths={pathBadges} />}

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

        <PrevNext locale={locale} prev={prev} next={next} pathId={activePathId} />
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
