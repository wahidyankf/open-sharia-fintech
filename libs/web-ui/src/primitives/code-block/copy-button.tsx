"use client";

import * as React from "react";
import { Check, Copy, X } from "lucide-react";

import { cn } from "../../utils/cn";
import { Button } from "../button/button";
import { useCopyToClipboard } from "./use-copy-to-clipboard";

export interface CopyButtonProps extends React.ComponentProps<"button"> {
  /** Exact text written to the clipboard. */
  value: string;
  /**
   * `aria-label` in the resting state. Web-ui primitives are locale-agnostic, so consuming apps
   * pass a localized string; defaults to the English "Copy" (mirrors the resizable-panel
   * `handleAriaLabel` locale-agnostic-with-English-default precedent).
   */
  copyLabel?: string;
  /** Announced via the live region on success and used as the success-state `aria-label`. */
  copiedLabel?: string;
  /**
   * Announced via the live region on failure and used as the error-state `aria-label`/`title`, so a
   * denied/failed clipboard write gives the visitor an explicit cue instead of a silent no-op.
   * Defaults to the English "Copy failed".
   */
  errorLabel?: string;
  /** How long the success/error state persists before reverting. Defaults to 2000ms. */
  resetMs?: number;
}

/**
 * A standalone, reusable copy affordance (copy any string). Composes the `Button` primitive
 * (`variant="ghost" size="icon-sm"`, which auto-sizes the lucide svg and supplies the
 * `focus-visible` ring) and adds the `Copy`→`Check`/`X` icon swap plus a visually-hidden
 * `role="status"` live region so assistive tech hears the success **or** the failure. A native
 * `title` mirrors the current `aria-label` so sighted mouse users get a tooltip too. Icons are
 * `aria-hidden` because the accessible name comes from `aria-label`; keyboard operability
 * (Enter/Space) is native to the underlying `<button>`.
 */
function CopyButton({
  value,
  copyLabel = "Copy",
  copiedLabel = "Copied",
  errorLabel = "Copy failed",
  resetMs = 2000,
  className,
  onClick,
  ...props
}: CopyButtonProps) {
  const { copied, error, copy } = useCopyToClipboard({ resetMs });

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    onClick?.(event);
    void copy(value);
  };

  // Current state's label drives both the accessible name and the native `title` tooltip.
  const label = copied ? copiedLabel : error ? errorLabel : copyLabel;

  return (
    <>
      <Button
        type="button"
        variant="ghost"
        size="icon-sm"
        data-slot="code-block-copy"
        aria-label={label}
        title={label}
        onClick={handleClick}
        className={cn(
          // Resting icon meets WCAG AA non-text contrast against both Shiki grounds; hover/focus
          // deepens it. Success/failure switch to theme-token green/red (Tailwind palette, not raw
          // hex). Light-mode success uses green-700 so the "Copied" icon clears WCAG SC 1.4.11
          // (~4.5:1) against the light code ground with real margin, not the ~3.0:1 green-600 floor.
          "text-muted-foreground transition-colors hover:text-foreground",
          copied && "text-green-700 hover:text-green-700 dark:text-green-500 dark:hover:text-green-500",
          error && "text-red-600 hover:text-red-600 dark:text-red-500 dark:hover:text-red-500",
          className,
        )}
        {...props}
      >
        {copied ? <Check aria-hidden="true" /> : error ? <X aria-hidden="true" /> : <Copy aria-hidden="true" />}
      </Button>
      {/*
        Always-present polite live region: a native `<output>` (implicit `role="status"` +
        `aria-live="polite"`, with the redundant `aria-live` kept per MDN's recommendation) that
        starts empty and only carries text while `copied`/`error`, so AT announces the outcome
        without stealing focus. This aria-live status pattern is new to web-ui. Using `<output>`
        (rather than a `<span role="status">`) keeps the markup jsx-a11y-clean while preserving the
        same role.
      */}
      <output aria-live="polite" className="sr-only">
        {copied ? copiedLabel : error ? errorLabel : ""}
      </output>
    </>
  );
}

export { CopyButton };
