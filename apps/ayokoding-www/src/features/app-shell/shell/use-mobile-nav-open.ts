"use client";

import { createContext, useContext, type RefObject } from "react";

interface MobileNavOpenState {
  open: boolean;
  /**
   * Opens or closes the drawer. `trigger` should be the exact element that was activated to open
   * it — pass `event.currentTarget` from the triggering `onClick` handler.
   *
   * `trigger` is preferred over reading `document.activeElement` at call time because mouse-click
   * default-focus behaviour differs by browser engine: Chromium and Firefox focus a clicked
   * `<button>` by default, but WebKit (Safari) does not — so `document.activeElement` is only a
   * reliable stand-in for "the element the reader just activated" on some engines, never all of
   * them (course-paths plan, Cycle 3.4 — found via the `path-order-nav.feature` phone-drawer e2e
   * scenario's `webkit` project). When `trigger` is omitted (e.g. a caller that only ever expects
   * keyboard activation, where focus-follows-keyboard is universal), `document.activeElement` is
   * still used as a fallback.
   */
  setOpen: (open: boolean, trigger?: HTMLElement | null) => void;
  /**
   * The element that opened the drawer most recently — either the explicit `trigger` passed to
   * `setOpen`, or `document.activeElement` when no explicit trigger was given.
   *
   * Radix's `Dialog` restores focus on close to its own `Dialog.Trigger` ref by default — but this
   * drawer is opened from more than one plain, context-driven control (the header's menu button,
   * `PathBanner`'s "View path" button), neither wrapping a `Dialog.Trigger`, so Radix's built-in
   * restoration never fires (course-paths plan, Cycle 3.4 — found via the
   * `path-order-nav.feature` phone-drawer e2e scenario). `MobileNav` restores focus itself using
   * this ref (see its `onCloseAutoFocus`).
   */
  lastTriggerRef: RefObject<HTMLElement | null>;
}

const noopRef: RefObject<HTMLElement | null> = { current: null };

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
  lastTriggerRef: noopRef,
});

export function useMobileNavOpen() {
  return useContext(MobileNavOpenContext);
}
