import { serverCaller } from "@/lib/trpc/server";
import {
  courseIdFromSlug,
  resolveCoursePathClientRenderData,
  toCoursePathClientData,
} from "@/features/course-paths/shell/course-path-nav";
import { loadRoutePathData } from "@/features/course-paths/shell/route-path-data";
import { CoursePageContent } from "@/features/course-paths/shell/course-page-content";
import type { Locale } from "@/features/i18n/core/config";

interface RenderCoursePathPageInput {
  locale: Locale;
  slug: string[];
  search: Record<string, string | string[] | undefined>;
}

function toUrlSearchParams(search: RenderCoursePathPageInput["search"]): URLSearchParams {
  const result = new URLSearchParams();
  for (const [key, value] of Object.entries(search)) {
    for (const item of Array.isArray(value) ? value : [value]) {
      if (item !== undefined) result.append(key, item);
    }
  }
  return result;
}

/**
 * Test-only renderer for query-aware course chrome. It exercises the exact
 * client resolver used after hydration without making static-route unit tests
 * depend on a server-side query prop.
 */
export async function renderCoursePathPage({ locale, slug, search }: RenderCoursePathPageInput) {
  const slugString = slug.join("/");
  const page = await serverCaller.content.getBySlug({ locale, slug: slugString });
  const courseId = courseIdFromSlug(slugString);
  const breadcrumbSegments = [
    { label: "Home", slug: "" },
    { label: "Browse", slug: "browse", href: `/${locale}/browse` },
    ...slug.slice(0, -1).map((part, index) => ({
      label: part.charAt(0).toUpperCase() + part.slice(1).replace(/-/g, " "),
      slug: slug.slice(0, index + 1).join("/"),
    })),
    { label: page.title, slug: slugString },
  ];

  if (courseId === null) {
    return (
      <CoursePageContent
        locale={locale}
        slug={slugString}
        title={page.title}
        html={page.html}
        headings={page.headings}
        date={page.date ?? undefined}
        breadcrumbSegments={breadcrumbSegments}
        renderData={{ activeContext: null, prerequisiteLinks: [], pathBadges: [], prev: page.prev, next: page.next }}
      />
    );
  }

  const pathData = await loadRoutePathData(locale);
  const renderData = resolveCoursePathClientRenderData(
    toUrlSearchParams(search),
    toCoursePathClientData(pathData, locale),
    courseId,
    page.prev,
    page.next,
  );

  return (
    <CoursePageContent
      locale={locale}
      slug={slugString}
      title={page.title}
      html={page.html}
      headings={page.headings}
      date={page.date ?? undefined}
      breadcrumbSegments={breadcrumbSegments}
      renderData={renderData}
      courseId={courseId}
    />
  );
}
