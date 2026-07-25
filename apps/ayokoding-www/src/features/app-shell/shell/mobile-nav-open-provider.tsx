"use client";

import { useCallback, useRef, useState, type ReactNode } from "react";
import { MobileNavOpenContext } from "./use-mobile-nav-open";

export function MobileNavOpenProvider({ children }: { children: ReactNode }) {
  const [open, setOpenState] = useState(false);
  const lastTriggerRef = useRef<HTMLElement | null>(null);

  // Capture the element that opened the drawer — see `use-mobile-nav-open.ts` for why an explicit
  // `trigger` (preferred) or a `document.activeElement` fallback is used, instead of relying on
  // Radix's own `Dialog.Trigger`-based restoration.
  const setOpen = useCallback((next: boolean, trigger?: HTMLElement | null) => {
    if (next) {
      if (trigger) {
        lastTriggerRef.current = trigger;
      } else if (typeof document !== "undefined" && document.activeElement instanceof HTMLElement) {
        lastTriggerRef.current = document.activeElement;
      }
    }
    setOpenState(next);
  }, []);

  return (
    <MobileNavOpenContext.Provider value={{ open, setOpen, lastTriggerRef }}>{children}</MobileNavOpenContext.Provider>
  );
}
