import Link from "next/link";
import { ChevronLeft, ChevronRight } from "lucide-react";
import type { PageLink } from "@/features/content/core/types";
import type { Locale } from "@/features/i18n/core/config";
import { t } from "@/features/i18n/core/translations";
import { contentUrl } from "@/features/content/core/content-url";

interface PrevNextProps {
  locale: string;
  prev: PageLink | null;
  next: PageLink | null;
  /**
   * The active path context (course-paths plan, cycle 2.2). When present, carried through to
   * both links via {@link contentUrl}'s optional third argument, so a reader following prev/next
   * inside a path never falls out of that path's context. Omitted entirely (not just `undefined`)
   * for the no-path case — markup is otherwise byte-identical, only the href construction differs.
   */
  pathId?: string;
}

export function PrevNext({ locale, prev, next, pathId }: PrevNextProps) {
  if (!prev && !next) return null;

  return (
    <nav
      aria-label="Page navigation"
      className="mt-12 flex flex-col gap-4 border-t border-border pt-6 sm:flex-row sm:justify-between"
    >
      {prev ? (
        <Link
          href={contentUrl(locale as Locale, prev.slug, pathId)}
          className="group flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"
        >
          <ChevronLeft className="h-4 w-4" />
          <div>
            <div className="text-xs">{t(locale as Locale, "previous")}</div>
            <div className="font-medium text-foreground group-hover:text-primary">{prev.title}</div>
          </div>
        </Link>
      ) : (
        <div />
      )}
      {next ? (
        <Link
          href={contentUrl(locale as Locale, next.slug, pathId)}
          className="group flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground sm:text-right"
        >
          <div>
            <div className="text-xs">{t(locale as Locale, "next")}</div>
            <div className="font-medium text-foreground group-hover:text-primary">{next.title}</div>
          </div>
          <ChevronRight className="h-4 w-4" />
        </Link>
      ) : (
        <div />
      )}
    </nav>
  );
}
