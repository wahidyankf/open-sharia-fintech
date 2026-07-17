"use client";

import { useCallback, useEffect, useRef, useState } from "react";

/** How long the `copied` flag stays true before auto-reverting, in milliseconds. */
const DEFAULT_RESET_MS = 2000;

export interface UseCopyToClipboardOptions {
  /**
   * How long the `copied` flag stays true before auto-reverting. Defaults to
   * `DEFAULT_RESET_MS` (2000ms) — the same duration the button's success icon/label persists.
   */
  resetMs?: number;
}

export interface UseCopyToClipboardResult {
  /**
   * `true` only after a **resolved** `navigator.clipboard.writeText`. Deliberately never set on a
   * rejection (non-secure context / permission denied) so the UI can't show a false success.
   */
  copied: boolean;
  /**
   * `true` after a **rejected** `navigator.clipboard.writeText`, so the UI can give the visitor an
   * explicit failure cue instead of appearing to do nothing (a silent no-op is indistinguishable
   * from a click that never registered). Mutually exclusive with `copied`; auto-reverts on the same
   * `resetMs` timer, and clears the moment a later attempt resolves.
   */
  error: boolean;
  /**
   * Writes `value` to the clipboard via `navigator.clipboard.writeText`. On resolve it flips
   * `copied` true (clearing any prior `error`) and schedules the auto-revert; on reject it flips
   * `error` true (leaving `copied` false — no false success) and schedules the same revert. No
   * `document.execCommand` fallback — the async Clipboard API is universally available in the secure
   * contexts (HTTPS / localhost) both consuming sites run in.
   */
  copy: (value: string) => Promise<void>;
}

/**
 * Owns the copy side effect and the transient `copied`/`error` flags so `CopyButton` and its tests
 * share one implementation. Mirrors `use-resizable-width.ts`'s `"use client"` +
 * timeout-cleanup-on-unmount shape: the pending reset timeout is cleared both on unmount and before
 * scheduling a fresh one, and a mounted-ref guard makes the post-`await` state writes no-ops once the
 * component has unmounted — so **neither** `setCopied`/`setError` (from the async clipboard write) nor
 * the revert timer can ever touch an unmounted tree, and rapid re-copies don't stack overlapping
 * reverts.
 */
export function useCopyToClipboard({
  resetMs = DEFAULT_RESET_MS,
}: UseCopyToClipboardOptions = {}): UseCopyToClipboardResult {
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState(false);
  // A ref (not state) because the timeout id is bookkeeping the render output never reads; storing
  // it in state would trigger needless re-renders on every schedule/clear.
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  // Tracks live-ness so an `await`ed clipboard write that resolves after unmount doesn't call
  // `setState` on a gone component (a React 18 no-op, but guarding keeps the contract exact).
  const mountedRef = useRef(true);

  const clearPending = useCallback(() => {
    if (timeoutRef.current !== null) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  }, []);

  // Mark unmounted and clear any in-flight revert so neither the timer nor a late-resolving write
  // can call `setState` on an unmounted tree.
  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
      clearPending();
    };
  }, [clearPending]);

  const copy = useCallback(
    async (value: string) => {
      let ok = false;
      try {
        await navigator.clipboard.writeText(value);
        ok = true;
      } catch {
        // Rejected write (non-secure context / denied): fall through to the error branch below.
        ok = false;
      }
      // The write is async; bail if the component unmounted while it was in flight.
      if (!mountedRef.current) return;
      // Cancel a still-pending revert from a prior copy before starting a fresh success/error window.
      clearPending();
      // `copied` and `error` are mutually exclusive: a resolved write shows success and clears any
      // prior error; a rejected write shows the error cue without ever faking success.
      setCopied(ok);
      setError(!ok);
      timeoutRef.current = setTimeout(() => {
        setCopied(false);
        setError(false);
        timeoutRef.current = null;
      }, resetMs);
    },
    [clearPending, resetMs],
  );

  return { copied, error, copy };
}
