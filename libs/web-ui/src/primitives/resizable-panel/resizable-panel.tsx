"use client";

import * as React from "react";

import { cn } from "../../utils/cn";
import { clampWidth, DEFAULT_WIDTH, MIN_PCT, MAX_PCT } from "./width-model";
import { useResizableWidth } from "./use-resizable-width";

/**
 * Applies a pixel delta (from a pointer drag or a keyboard step) to a base width, clamping the
 * result into the `[minPct, maxPct]` band of the viewport. Shared by both the drag and keyboard
 * width-update paths so clamping logic never lives in more than one place.
 */
function applyWidth(baseWidth: number, deltaPx: number, viewportPx: number, minPct: number, maxPct: number): number {
  return clampWidth(baseWidth + deltaPx, viewportPx, minPct, maxPct);
}

/** Default pixel step applied per ArrowLeft/ArrowRight keypress on the handle. */
const KEYBOARD_STEP = 10;

/** Maps each supported resize key to the sign of the step it applies (-1 shrinks, +1 grows). */
const KEY_DELTA_SIGN: Record<string, 1 | -1> = {
  ArrowRight: 1,
  ArrowLeft: -1,
};

interface ResizablePanelProps extends Omit<React.ComponentProps<"div">, "children"> {
  /** `localStorage` key under which the width is persisted (see `useResizableWidth`). */
  storageKey: string;
  /** Width to use when no persisted value exists. Defaults to `DEFAULT_WIDTH`. */
  defaultWidth?: number;
  /** Lower band bound, as a percentage of the viewport. Defaults to `MIN_PCT`. */
  minPct?: number;
  /** Upper band bound, as a percentage of the viewport. Defaults to `MAX_PCT`. */
  maxPct?: number;
  /** Viewport width in pixels, used to compute the min/max band. Defaults to `window.innerWidth`. */
  viewportPx?: number;
  /** Pixel step applied per ArrowLeft/ArrowRight keypress on the handle. Defaults to `KEYBOARD_STEP`. */
  keyboardStep?: number;
  /**
   * Accessible name for the handle (`aria-label`). Web-ui primitives are locale-agnostic, so
   * consuming apps must supply a localized string; defaults to the English "Resize panel".
   */
  handleAriaLabel?: string;
  children: React.ReactNode;
}

function ResizablePanel({
  storageKey,
  defaultWidth = DEFAULT_WIDTH,
  minPct = MIN_PCT,
  maxPct = MAX_PCT,
  viewportPx,
  keyboardStep = KEYBOARD_STEP,
  handleAriaLabel,
  className,
  children,
  ...props
}: ResizablePanelProps) {
  const { width, commitWidth } = useResizableWidth({ storageKey, defaultWidth });
  // Starts at `viewportPx ?? 0` (never reads `window` during render) so the initial client
  // render matches the server-rendered HTML exactly; the effect below corrects it to the real
  // viewport width right after mount, avoiding a React hydration-mismatch warning.
  const [resolvedViewportPx, setResolvedViewportPx] = React.useState(() => viewportPx ?? 0);

  React.useEffect(() => {
    setResolvedViewportPx(viewportPx ?? window.innerWidth);
  }, [viewportPx]);

  const minPx = (minPct / 100) * resolvedViewportPx;
  const maxPx = (maxPct / 100) * resolvedViewportPx;

  const handleDelta = (deltaPx: number) => {
    commitWidth(applyWidth(width, deltaPx, resolvedViewportPx, minPct, maxPct));
  };

  return (
    <div
      data-slot="resizable-panel"
      className={cn("relative flex", className)}
      style={{ width: `${width}px` }}
      {...props}
    >
      <div data-slot="resizable-panel-content" className="min-w-0 flex-1 overflow-hidden">
        {children}
      </div>
      <ResizableHandle
        width={width}
        minPx={minPx}
        maxPx={maxPx}
        keyboardStep={keyboardStep}
        onDelta={handleDelta}
        aria-label={handleAriaLabel}
      />
    </div>
  );
}

interface ResizableHandleProps extends Omit<React.ComponentProps<"div">, "onPointerDown"> {
  /** The panel's current width, in pixels — exposed to assistive tech via `aria-valuenow`. */
  width: number;
  /** The band's lower bound in pixels — exposed via `aria-valuemin`. */
  minPx: number;
  /** The band's upper bound in pixels — exposed via `aria-valuemax`. */
  maxPx: number;
  /** Pixel step applied per ArrowLeft/ArrowRight keypress. */
  keyboardStep: number;
  onDelta: (deltaPx: number) => void;
}

function ResizableHandle({
  width,
  minPx,
  maxPx,
  keyboardStep,
  onDelta,
  className,
  "aria-label": ariaLabel = "Resize panel",
  ...props
}: ResizableHandleProps) {
  const handlePointerDown = (event: React.PointerEvent<HTMLDivElement>) => {
    const startX = event.clientX;

    const handlePointerMove = (moveEvent: PointerEvent) => {
      onDelta(moveEvent.clientX - startX);
    };

    const handlePointerUp = () => {
      document.removeEventListener("pointermove", handlePointerMove);
      document.removeEventListener("pointerup", handlePointerUp);
    };

    document.addEventListener("pointermove", handlePointerMove);
    document.addEventListener("pointerup", handlePointerUp);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    const sign = KEY_DELTA_SIGN[event.key];
    if (sign !== undefined) {
      onDelta(sign * keyboardStep);
    }
  };

  return (
    <div
      data-slot="resizable-panel-handle"
      role="separator"
      aria-orientation="vertical"
      aria-label={ariaLabel}
      aria-valuemin={minPx}
      aria-valuemax={maxPx}
      aria-valuenow={width}
      tabIndex={0}
      onPointerDown={handlePointerDown}
      onKeyDown={handleKeyDown}
      className={cn(
        "w-1 shrink-0 cursor-col-resize touch-none bg-border hover:bg-accent focus-visible:bg-accent focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none",
        className,
      )}
      {...props}
    />
  );
}

export { ResizablePanel, ResizableHandle };
