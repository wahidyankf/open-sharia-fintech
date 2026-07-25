"use client";

import { useState, type ReactNode } from "react";
import { MobileNavOpenContext } from "./use-mobile-nav-open";

export function MobileNavOpenProvider({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(false);

  return <MobileNavOpenContext.Provider value={{ open, setOpen }}>{children}</MobileNavOpenContext.Provider>;
}
