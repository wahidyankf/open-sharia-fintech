"use client";

import Link from "next/link";
import {
  Button,
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  parsePersistedWidth,
} from "@open-sharia-enterprise/web-ui/primitives";
import { SidebarTree } from "@/features/navigation/shell/sidebar-tree";
import { useEffect, useState } from "react";
import type { TreeNode } from "@/features/content/core/types";
import { trpcClient } from "@/lib/trpc/client";
import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import { PRIMARY_NAV_LINKS } from "@/features/app-shell/core/nav-links";

interface MobileNavProps {
  locale: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

/**
 * `localStorage` key under which the mobile drawer's chosen preset width is
 * persisted (DD-7 — preset widths, not free drag, on an overlay drawer).
 */
const MOBILE_NAV_WIDTH_STORAGE_KEY = "ayokoding-mobilenav-width";

/**
 * The mobile nav drawer's fixed preset widths. Replaces the previously
 * hardcoded `w-[280px]` with a default and a wider preset the reader can
 * pick from — see prd.md's "Mobile drawer preset widths" scenario / DD-7.
 */
const MOBILE_NAV_WIDTH_PRESETS = [
  { id: "default", labelKey: "mobileNavWidthDefault", widthPx: 280 },
  { id: "wide", labelKey: "mobileNavWidthWide", widthPx: 360 },
] as const;

export function MobileNav({ locale, open, onOpenChange }: MobileNavProps) {
  const [tree, setTree] = useState<TreeNode[]>([]);
  const [widthPx, setWidthPx] = useState<number>(MOBILE_NAV_WIDTH_PRESETS[0].widthPx);

  // Mount-effect read of the persisted preset width — mirrors the pattern
  // `useResizableWidth` (libs/web-ui) uses for the desktop rail. Only one of
  // the two declared presets is accepted; a stale/tampered value (there is no
  // free-drag range to clamp into here) falls back to the default preset.
  useEffect(() => {
    const persisted = parsePersistedWidth(localStorage.getItem(MOBILE_NAV_WIDTH_STORAGE_KEY));
    const isValidPreset = MOBILE_NAV_WIDTH_PRESETS.some((preset) => preset.widthPx === persisted);
    if (isValidPreset) {
      setWidthPx(persisted as number);
    }
  }, []);

  useEffect(() => {
    if (open && tree.length === 0) {
      trpcClient.content.getTree.query({ locale: locale as "en" | "id" }).then((data) => {
        const raw = data as TreeNode[];
        // Skip the root locale node (e.g., "English Content") — mirror desktop Sidebar behaviour
        const rootNode = raw.find((n) => n.slug === "");
        setTree(rootNode ? rootNode.children : raw);
      });
    }
  }, [open, locale, tree.length]);

  function selectPreset(presetWidthPx: number) {
    setWidthPx(presetWidthPx);
    localStorage.setItem(MOBILE_NAV_WIDTH_STORAGE_KEY, String(presetWidthPx));
  }

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent side="left" className="overflow-y-auto p-4" style={{ width: `${widthPx}px` }}>
        <SheetHeader>
          <SheetTitle className="text-left text-lg font-bold">AyoKoding</SheetTitle>
          <fieldset className="m-0 mb-2 border-0 p-0">
            <legend className="mb-1 block text-xs font-medium text-muted-foreground">
              {t(locale as Locale, "mobileNavWidthLabel")}
            </legend>
            <div className="flex items-center gap-1">
              {MOBILE_NAV_WIDTH_PRESETS.map((preset) => (
                <Button
                  key={preset.id}
                  type="button"
                  variant={widthPx === preset.widthPx ? "secondary" : "outline"}
                  size="xs"
                  aria-pressed={widthPx === preset.widthPx}
                  onClick={() => selectPreset(preset.widthPx)}
                >
                  {t(locale as Locale, preset.labelKey)}
                </Button>
              ))}
            </div>
          </fieldset>
        </SheetHeader>
        <nav className="mt-4" aria-label="Mobile navigation">
          <p className="px-1 text-xs font-semibold tracking-wide text-muted-foreground uppercase">Menu</p>
          <ul className="mt-2 mb-4 space-y-1">
            {PRIMARY_NAV_LINKS.map((link) => (
              <li key={link.labelKey}>
                <Link
                  href={link.hrefFor(locale as Locale)}
                  onClick={() => onOpenChange(false)}
                  className="block rounded-md px-3 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground"
                >
                  {t(locale as Locale, link.labelKey)}
                </Link>
              </li>
            ))}
          </ul>
          <SidebarTree nodes={tree} locale={locale} />
        </nav>
      </SheetContent>
    </Sheet>
  );
}
