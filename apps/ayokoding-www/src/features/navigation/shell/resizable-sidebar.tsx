"use client";

import { ResizablePanel } from "@open-sharia-enterprise/web-ui/primitives";

import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";

/** `localStorage` key under which the docs sidebar's chosen width is persisted. */
const SIDEBAR_STORAGE_KEY = "ayokoding-sidebar-width";

/** Lower/upper band bounds, as a percentage of the viewport width (prd.md's 15%-35% band). */
const MIN_WIDTH_PCT = 15;
const MAX_WIDTH_PCT = 35;

interface ResizableSidebarProps {
  locale: Locale;
  children: React.ReactNode;
}

/**
 * Client wrapper bridging the async server `ContentLayout` to the client-only
 * `ResizablePanel` primitive (which internally wires `useResizableWidth`).
 *
 * Renders the docs sidebar's `<aside>` shell itself — hidden below `md`, a
 * sticky rail from `md` up — with `ResizablePanel` nested inside it
 * (providing width + the drag/keyboard handle), rather than the reverse.
 * `ResizablePanel`'s content wrapper is `overflow-hidden` by design (see
 * `resizable-panel.tsx`), and `overflow: hidden` on any ancestor of a
 * `position: sticky` element breaks its stickiness — so `sticky`,
 * `overflow-y-auto`, and the fixed height live on `<aside>` itself (which has
 * no such ancestor above it), never on a div nested inside `ResizablePanel`'s
 * children. `<aside>` deliberately has no `border-r` of its own — the
 * `ResizablePanel` handle already renders the sidebar/content boundary, and a
 * second static border on the same edge produced an unintentional compound
 * double-border with no visible seam between the two (see DWT-003 in this
 * plan's rule-15 retest).
 */
export function ResizableSidebar({ locale, children }: ResizableSidebarProps) {
  return (
    <aside className="sticky top-16 hidden h-[calc(100vh-4rem)] shrink-0 overflow-y-auto md:block">
      <ResizablePanel
        storageKey={SIDEBAR_STORAGE_KEY}
        minPct={MIN_WIDTH_PCT}
        maxPct={MAX_WIDTH_PCT}
        className="h-full"
        handleAriaLabel={t(locale, "resizableSidebarHandleLabel")}
      >
        <div className="p-4">{children}</div>
      </ResizablePanel>
    </aside>
  );
}
