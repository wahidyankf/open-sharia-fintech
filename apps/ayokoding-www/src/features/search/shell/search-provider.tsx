"use client";

import { useCallback, useRef, useState, type ReactNode } from "react";
import { SearchContext } from "@/features/search/shell/use-search";
import { SearchDialog } from "./search-dialog";

export function SearchProvider({ children }: { children: ReactNode }) {
  const [open, setOpenState] = useState(false);
  const openerRef = useRef<HTMLElement | null>(null);

  const setOpen = useCallback((nextOpen: boolean, opener?: HTMLElement) => {
    if (nextOpen) {
      const activeElement = document.activeElement;
      openerRef.current =
        opener ?? (activeElement instanceof HTMLElement && activeElement !== document.body ? activeElement : null);
      setOpenState(true);
      return;
    }

    setOpenState(false);
    const openerToRestore = openerRef.current;
    if (openerToRestore) {
      // Radix releases its modal focus scope during the same close. Restore the exact external
      // opener on the following task, after that teardown has completed.
      setTimeout(() => openerToRestore.focus(), 0);
    }
  }, []);

  return (
    <SearchContext.Provider value={{ open, setOpen }}>
      {children}
      <SearchDialog />
    </SearchContext.Provider>
  );
}
