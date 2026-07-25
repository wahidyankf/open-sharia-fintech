import Link from "next/link";
import { contentUrl } from "@/features/content/core/content-url";
import type { Locale } from "@/features/i18n/core/config";
import type { PageLink } from "@/features/content/core/types";

export interface PrerequisiteListProps {
  locale: string;
  /** Already-resolved prerequisite links (Cycle 2.4's REFACTOR note — no lookup of its own). */
  prerequisites: readonly PageLink[];
  /** When set, every prerequisite link preserves the path context so the reader stays in-path. */
  pathId?: string;
}

/**
 * A course page's declared-prerequisites list (course-paths plan, Cycle 2.4).
 *
 * Renders in **both** the canonical and the path-aware view — path-independent, since a
 * prerequisite is the body's own honest dependency statement (tech-docs.md §Prerequisite
 * display). Renders nothing at all (not an empty "Prerequisites" heading) when there are no
 * declared prerequisites — advisory, never gated: no lock, no quiz-wall.
 *
 * Functional core / imperative shell: this component takes already-resolved `PageLink`s and
 * performs no lookup of its own.
 */
export function PrerequisiteList({ locale, prerequisites, pathId }: PrerequisiteListProps) {
  if (prerequisites.length === 0) {
    return null;
  }

  return (
    <nav aria-label="Prerequisites" className="mt-8 text-sm">
      <h2 className="mb-2 font-semibold text-muted-foreground">Prerequisites</h2>
      <ul className="flex flex-col gap-1">
        {prerequisites.map((prerequisite) => (
          <li key={prerequisite.slug}>
            <Link
              href={contentUrl(locale as Locale, prerequisite.slug, pathId)}
              className="underline hover:text-foreground"
            >
              {prerequisite.title}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
