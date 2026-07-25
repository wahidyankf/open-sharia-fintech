"use client";

import { createContext, useContext } from "react";

interface MobileNavOpenState {
  open: boolean;
  setOpen: (open: boolean) => void;
}

/**
 * Shared open/close state for the mobile navigation drawer (course-paths plan, Cycle 2.9).
 *
 * Lifted out of `header.tsx`'s local `useState` into a shared context so a second, structurally
 * disconnected trigger — `PathBanner`'s "open path course list" disclosure button, rendered
 * inside the course page's `<article>`, a cousin of `Header` in the tree — can open the exact
 * same `Sheet` the header's hamburger-menu button opens, rather than a second overlay.
 */
export const MobileNavOpenContext = createContext<MobileNavOpenState>({
  open: false,
  setOpen: () => {},
});

export function useMobileNavOpen() {
  return useContext(MobileNavOpenContext);
}
