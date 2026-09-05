"use client";

import type { MouseEvent } from "react";

import type { Locale } from "@/features/i18n/core/config";
import { t } from "@/features/i18n/core/translations";

type Props = {
  locale: Locale;
};

export function SkipLink({ locale }: Props) {
  // A bare `href="#main-content"` only scrolls the target into view — it does NOT move keyboard focus
  // there, so the next Tab resumes from the skip link and the user is dumped back into the header
  // (UWT-005). Programmatically focus the `<main>` (which carries `tabindex={-1}`) so subsequent
  // Tabbing continues from the main content, the whole point of a skip link.
  const focusMain = (event: MouseEvent<HTMLAnchorElement>) => {
    const main = document.getElementById("main-content");
    if (main) {
      event.preventDefault();
      main.focus();
      // Keep the URL hash in sync for deep-linking / back-button parity without triggering the
      // default (focus-less) hash jump.
      history.replaceState(null, "", "#main-content");
    }
  };

  return (
    <a
      href="#main-content"
      onClick={focusMain}
      className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:rounded focus:bg-primary focus:px-4 focus:py-2 focus:text-primary-foreground focus:outline-2 focus:outline-offset-2 focus:outline-black dark:focus:outline-white"
    >
      {t(locale, "skipToContent")}
    </a>
  );
}
