"use client";

import { Globe } from "lucide-react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { Button } from "@open-sharia-enterprise/web-ui";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@open-sharia-enterprise/web-ui";
import { LOCALE_LABELS, SUPPORTED_LOCALES } from "@/features/i18n/core/config";

interface LanguageSwitcherProps {
  locale: string;
}

/**
 * Pure URL builder for a locale switch: replaces the path's locale segment, preserving both the
 * rest of the path and the current query string (e.g. the AI benchmark's `?harness=`/`?class=`
 * filters). Extracted as a standalone pure function (functional core / imperative shell) so the
 * fix for Rule-15 EWT-002 — a prior version rewrote the URL from `pathname` alone, silently
 * dropping any active filter on every locale switch — has a direct unit test, without needing to
 * drive the Radix dropdown menu through jsdom.
 */
export function buildLocaleSwitchHref(pathname: string, searchParams: URLSearchParams, newLocale: string): string {
  const segments = pathname.split("/").filter(Boolean);
  if (segments.length > 0) {
    segments[0] = newLocale;
  }
  const qs = searchParams.toString();
  return "/" + segments.join("/") + (qs ? `?${qs}` : "");
}

export function LanguageSwitcher({ locale }: LanguageSwitcherProps) {
  const pathname = usePathname();
  const router = useRouter();
  const searchParams = useSearchParams();

  function switchLocale(newLocale: string) {
    router.push(buildLocaleSwitchHref(pathname, searchParams, newLocale));
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="sm" className="gap-1" aria-label="Switch language">
          <Globe className="h-4 w-4" />
          <span className="hidden sm:inline">{LOCALE_LABELS[locale as keyof typeof LOCALE_LABELS]}</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        {SUPPORTED_LOCALES.map((loc) => (
          <DropdownMenuItem key={loc} onClick={() => switchLocale(loc)} className={locale === loc ? "font-bold" : ""}>
            {LOCALE_LABELS[loc]}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
