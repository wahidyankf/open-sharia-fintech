"use client";

import { useState, type MouseEvent } from "react";
import { useMobileNavOpen } from "@/features/app-shell/shell/use-mobile-nav-open";

/** Must match the `id` the shipped drawer's content element renders (`mobile-nav.tsx`). */
export const MOBILE_NAV_DRAWER_ID = "mobile-nav-drawer";

export interface PathBannerProps {
  pathTitle: string;
  /** 1-based position of the current course within the path. */
  courseIndex: number;
  totalCourses: number;
}

/**
 * The compact "on path · course k of N" readout and its `md:hidden` disclosure trigger
 * (course-paths plan, Cycle 2.9) — `PathRail`'s mobile form, per DD-46: retained from the
 * originally-selected Option A, demoted to the rail's always-visible compact readout.
 *
 * Activating the trigger opens the **existing** left navigation drawer (`MobileNav`'s shipped
 * `Sheet`, opened via the same shared `open` state the header's hamburger-menu button controls)
 * rather than a second overlay — `aria-controls` names that drawer's content element.
 */
export function PathBanner({ pathTitle, courseIndex, totalCourses }: PathBannerProps) {
  const { setOpen } = useMobileNavOpen();
  const [expanded, setExpanded] = useState(false);

  function handleActivate(event: MouseEvent<HTMLButtonElement>) {
    setExpanded((prev) => !prev);
    // Pass the trigger explicitly — WebKit does not focus a clicked `<button>` by default, unlike
    // Chromium/Firefox, so `document.activeElement` alone is not a reliable stand-in here (see
    // `use-mobile-nav-open.ts`).
    setOpen(true, event.currentTarget);
  }

  return (
    <div className="mt-4 flex items-center justify-between rounded-md border border-border px-3 py-2 text-sm md:hidden">
      <span>
        on path · course {courseIndex} of {totalCourses}
      </span>
      <button
        type="button"
        aria-expanded={expanded}
        aria-controls={MOBILE_NAV_DRAWER_ID}
        aria-label={`Open path course list — ${pathTitle}, course ${courseIndex} of ${totalCourses}`}
        onClick={handleActivate}
        className="font-medium underline underline-offset-2"
      >
        View path
      </button>
    </div>
  );
}
