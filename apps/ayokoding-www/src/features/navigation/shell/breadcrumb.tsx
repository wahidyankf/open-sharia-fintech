import Link from "next/link";
import { ChevronRight } from "lucide-react";
import { contentUrl } from "@/features/content/core/content-url";
import type { Locale } from "@/features/i18n/core/config";

interface BreadcrumbProps {
  locale: string;
  slug: string;
  segments: { label: string; slug: string; href?: string }[];
  // When true, the final (current-page) segment is rendered as a non-link
  // aria-current="page" crumb instead of being dropped. Callers that already
  // surface the current page in an <h1> leave this absent (default behaviour).
  showCurrent?: boolean;
}

// Always resolves through contentUrl() — once contentUrl() is a uniform bare
// join (DD-48 de-namespacing removed its /c/-prefix branch), this is
// identical to a plain `/{locale}/{slug}` join for every content href, so
// there is no longer a distinct "content" vs "non-content" href mode.
function hrefFor(locale: string, segment: { slug: string; href?: string }): string {
  if (segment.href !== undefined) return segment.href;
  if (!segment.slug) return `/${locale}`;
  return contentUrl(locale as Locale, segment.slug);
}

export function Breadcrumb({ locale, segments, showCurrent = false }: BreadcrumbProps) {
  // Default: exclude the last segment — the current page title is shown in the h1.
  // showCurrent: keep every segment; render the last one as a non-link crumb.
  const visibleSegments = showCurrent ? segments : segments.slice(0, -1);
  if (visibleSegments.length === 0) return null;

  const lastIndex = visibleSegments.length - 1;
  // DWT-001: beyond 3 crumbs, the middle ones collapse behind one ellipsis at
  // mobile widths — see the mobile-collapse doc comment above the <ol> below.
  const hasMobileCollapse = visibleSegments.length > 3;

  return (
    <nav aria-label="Breadcrumb" className="mb-4 text-sm text-muted-foreground">
      {/*
       * DWT-001: the base class is non-wrapping (no bare `flex-wrap`) so a deep
       * breadcrumb never wraps to multiple rows at 375px — prd.md's Screen 4
       * acceptance requires "no multi-line breadcrumb wrap at 375 px", and the
       * committed legacy-landing mobile mockups (`plans/in-progress/
       * ayokoding-learning-path-01-url-restructure/assets/
       * legacy-landing-option-{a,b}-mobile.png`) show a single-line, middle-
       * truncated `Home / … / Legacy`. When there are more than 3 visible
       * crumbs, the middle ones (`hidden sm:flex` below) drop out at mobile
       * widths and one collapsed ellipsis crumb (`sm:hidden` below) stands in
       * for them, keeping the first and last crumbs always visible. At `sm:`
       * and up every crumb reappears and the ellipsis disappears — full
       * desktop behaviour is unchanged.
       */}
      <ol className="flex items-center gap-1">
        {visibleSegments.flatMap((segment, i) => {
          const isCurrent = showCurrent && i === lastIndex;
          const isMobileCollapsedMiddle = hasMobileCollapse && i > 0 && i < lastIndex;
          const crumb = (
            <li
              key={segment.slug}
              className={isMobileCollapsedMiddle ? "hidden items-center gap-1 sm:flex" : "flex items-center gap-1"}
            >
              {i > 0 && <ChevronRight className="h-3 w-3 shrink-0" />}
              {isCurrent ? (
                <span aria-current="page" className="font-medium text-foreground">
                  {segment.label}
                </span>
              ) : (
                <Link href={hrefFor(locale, segment)} className="hover:text-foreground">
                  {segment.label}
                </Link>
              )}
            </li>
          );

          // Insert the collapsed ellipsis crumb right after the first crumb —
          // it stands in for the mobile-hidden middle crumbs above, mobile-only.
          if (hasMobileCollapse && i === 0) {
            return [
              crumb,
              <li
                key="breadcrumb-ellipsis"
                data-testid="breadcrumb-ellipsis"
                className="flex items-center gap-1 sm:hidden"
              >
                <ChevronRight className="h-3 w-3 shrink-0" />
                <span aria-hidden="true">…</span>
                <span className="sr-only">More breadcrumb items</span>
              </li>,
            ];
          }
          return [crumb];
        })}
      </ol>
    </nav>
  );
}
