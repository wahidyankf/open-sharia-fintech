import Link from "next/link";
import { contentUrl } from "@/features/content/core/content-url";
import type { Locale } from "@/features/i18n/core/config";
import { t } from "@/features/i18n/core/translations";
import type { PrerequisiteLink } from "./course-path-nav";

export interface PrerequisiteListProps {
  locale: string;
  /**
   * Already-resolved prerequisite links (Cycle 2.4's REFACTOR note — no lookup of its own). Each
   * link carries its own optional `pathId` (EWT-002 fix) — set only when that specific
   * prerequisite is itself a member of the active manifest, never a single blanket value applied
   * to every prerequisite regardless of manifest membership.
   */
  prerequisites: readonly PrerequisiteLink[];
}

/**
 * A course page's declared-prerequisites list (course-paths plan, Cycle 2.4).
 *
 * Renders in **both** the canonical and the path-aware view — path-independent, since a
 * prerequisite is the body's own honest dependency statement (tech-docs.md §Prerequisite
 * display). Renders nothing at all (not an empty "Prerequisites" heading) when there are no
 * declared prerequisites — advisory, never gated: no lock, no quiz-wall.
 *
 * Functional core / imperative shell: this component takes already-resolved `PrerequisiteLink`s
 * (each already carrying its own per-item `pathId` decision) and performs no lookup of its own.
 */
export function PrerequisiteList({ locale, prerequisites }: PrerequisiteListProps) {
  if (prerequisites.length === 0) {
    return null;
  }

  const label = t(locale as Locale, "pathsPrerequisites");

  return (
    <nav aria-label={label} className="mt-8 text-sm">
      <h2 className="mb-2 font-semibold text-muted-foreground">{label}</h2>
      <ul className="flex flex-col gap-1">
        {prerequisites.map((prerequisite) => (
          <li key={prerequisite.slug}>
            <Link
              href={contentUrl(locale as Locale, prerequisite.slug, prerequisite.pathId)}
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
