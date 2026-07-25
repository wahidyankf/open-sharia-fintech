"use client";

import { usePathname, useSearchParams } from "next/navigation";
import type { ReactNode } from "react";
import type { PathManifest } from "../core/schemas";
import { resolveActiveCourseFromLocation } from "./course-path-nav";
import { PathRail } from "./path-rail";

export interface SidebarHostProps {
  locale: string;
  manifests: readonly PathManifest[];
  /** courseId -> title, covering every ID that appears in any of `manifests`. */
  courseTitles: Readonly<Record<string, string>>;
  /** The pre-rendered fallback (today's `<Sidebar>`) — a Server Component's output, passed as `children`. */
  children: ReactNode;
}

/**
 * Content-swap host for `ResizableSidebar`'s `children` (course-paths plan, Cycle 2.8 — the
 * selected Screen 3 Option B).
 *
 * `ResizableSidebar` itself is never forked: its `<aside>`, `hidden … md:block` gate,
 * `ResizablePanel` 15%-35% band, resize handle, and persisted-width `localStorage` key are all
 * untouched (tech-docs.md §Screen 3) — only this one host's `children` decision changes.
 *
 * A layout receives neither `searchParams` nor a descendant route's `[...slug]` params (the App
 * Router constraint tech-docs.md documents), so this Client Component detects the active path
 * context itself via `usePathname()` + `useSearchParams()`, given `manifests` passed down as
 * props from the nearest Server ancestor that CAN do IO ((content)/layout.tsx).
 *
 * Renders the passed-through `children` (today's generic `<Sidebar>`) unchanged when there is no
 * active path context — the Cycle 2.10 invariant this component must never regress.
 */
export function SidebarHost({ locale, manifests, courseTitles, children }: SidebarHostProps) {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const active = resolveActiveCourseFromLocation(pathname, searchParams, locale, manifests);

  if (!active) {
    return <>{children}</>;
  }

  return (
    <PathRail
      locale={locale}
      manifest={active.context.manifest}
      currentCourseId={active.courseId}
      courseTitles={courseTitles}
    />
  );
}
