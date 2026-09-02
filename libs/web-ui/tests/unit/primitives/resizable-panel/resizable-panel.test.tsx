import { render, screen, cleanup, fireEvent } from "@testing-library/react";
import { renderToStaticMarkup } from "react-dom/server";
import { axe } from "vitest-axe";
import { describe, it, expect, afterEach, beforeEach, vi } from "vitest";

import { ResizablePanel } from "../../../../src/primitives/resizable-panel/resizable-panel";

function getHandle(container: HTMLElement): HTMLElement {
  const handle = container.querySelector('[data-slot="resizable-panel-handle"]');
  if (!(handle instanceof HTMLElement)) {
    throw new Error("resizable handle not found");
  }
  return handle;
}

function getPanelWidthPx(container: HTMLElement): number {
  const panel = container.querySelector('[data-slot="resizable-panel"]');
  if (!(panel instanceof HTMLElement)) {
    throw new Error("resizable panel not found");
  }
  return Number.parseFloat(panel.style.width);
}

/** Simulates a single pointer drag: press down at x=0, move by `deltaX`, release. */
function dragHandleBy(handle: HTMLElement, deltaX: number) {
  fireEvent.pointerDown(handle, { clientX: 0 });
  fireEvent.pointerMove(document, { clientX: deltaX });
  fireEvent.pointerUp(document);
}

describe("ResizablePanel", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  afterEach(() => {
    cleanup();
  });

  it("widens the panel by dragging the handle right", () => {
    const { container } = render(
      <ResizablePanel storageKey="test-drag-widen" defaultWidth={250} minPct={15} maxPct={35} viewportPx={1000}>
        content
      </ResizablePanel>,
    );

    dragHandleBy(getHandle(container), 60);

    expect(getPanelWidthPx(container)).toBe(310);
  });

  it("stops at the maximum when dragging past it", () => {
    const { container } = render(
      <ResizablePanel storageKey="test-drag-clamp" defaultWidth={340} minPct={15} maxPct={35} viewportPx={1000}>
        content
      </ResizablePanel>,
    );

    dragHandleBy(getHandle(container), 100);

    expect(getPanelWidthPx(container)).toBe(350);
  });

  it("updates the visual width live but does not persist to localStorage on intermediate pointermove events", () => {
    const { container } = render(
      <ResizablePanel
        storageKey="test-drag-no-persist-mid-drag"
        defaultWidth={250}
        minPct={15}
        maxPct={35}
        viewportPx={1000}
      >
        content
      </ResizablePanel>,
    );
    const handle = getHandle(container);

    fireEvent.pointerDown(handle, { clientX: 0 });
    fireEvent.pointerMove(document, { clientX: 30 });

    expect(getPanelWidthPx(container)).toBe(280);
    expect(localStorage.getItem("test-drag-no-persist-mid-drag")).toBeNull();

    fireEvent.pointerUp(document);
  });

  it("persists to localStorage exactly once, at pointerup (drag end), not once per pointermove", () => {
    const { container } = render(
      <ResizablePanel
        storageKey="test-drag-persist-on-end"
        defaultWidth={250}
        minPct={15}
        maxPct={35}
        viewportPx={1000}
      >
        content
      </ResizablePanel>,
    );
    const handle = getHandle(container);
    const setItemSpy = vi.spyOn(Storage.prototype, "setItem");

    fireEvent.pointerDown(handle, { clientX: 0 });
    fireEvent.pointerMove(document, { clientX: 20 });
    fireEvent.pointerMove(document, { clientX: 40 });
    fireEvent.pointerMove(document, { clientX: 60 });
    expect(localStorage.getItem("test-drag-persist-on-end")).toBeNull();

    fireEvent.pointerUp(document);

    expect(localStorage.getItem("test-drag-persist-on-end")).toBe("310");
    expect(setItemSpy).toHaveBeenCalledTimes(1);

    setItemSpy.mockRestore();
  });

  it("widens the panel by the keyboard step and updates aria-valuenow on ArrowRight", () => {
    const { container } = render(
      <ResizablePanel storageKey="test-keyboard-widen" defaultWidth={250} minPct={15} maxPct={35} viewportPx={1000}>
        content
      </ResizablePanel>,
    );
    const handle = getHandle(container);
    handle.focus();

    fireEvent.keyDown(handle, { key: "ArrowRight" });

    const newWidth = getPanelWidthPx(container);
    expect(newWidth).toBeGreaterThan(250);
    expect(handle.getAttribute("aria-valuenow")).toBe(String(newWidth));
  });

  it("exposes separator semantics on the handle", () => {
    render(
      <ResizablePanel storageKey="test-separator-semantics" defaultWidth={250} viewportPx={1000}>
        content
      </ResizablePanel>,
    );

    const handle = screen.getByRole("separator");
    expect(handle.getAttribute("aria-orientation")).toBe("vertical");
  });

  it("has no accessibility violations", async () => {
    const { container } = render(
      <ResizablePanel storageKey="test-a11y" defaultWidth={250} viewportPx={1000}>
        content
      </ResizablePanel>,
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("renders a deterministic aria-valuemin/aria-valuemax during static (SSR) rendering when viewportPx is omitted, avoiding a hydration mismatch", () => {
    const html = renderToStaticMarkup(
      <ResizablePanel storageKey="test-ssr-deterministic" defaultWidth={250}>
        content
      </ResizablePanel>,
    );

    expect(html).toContain('aria-valuemin="0"');
    expect(html).toContain('aria-valuemax="0"');
  });

  it("corrects aria-valuemin/aria-valuemax to the real viewport width after mount when viewportPx is omitted", () => {
    const { container } = render(
      <ResizablePanel storageKey="test-viewport-mount-correction" defaultWidth={250}>
        content
      </ResizablePanel>,
    );

    const handle = getHandle(container);
    expect(Number(handle.getAttribute("aria-valuemin"))).toBeGreaterThan(0);
    expect(Number(handle.getAttribute("aria-valuemax"))).toBeGreaterThan(0);
  });

  it("accepts a custom handleAriaLabel so consuming apps can localize the handle's accessible name", () => {
    const { container } = render(
      <ResizablePanel
        storageKey="test-handle-aria-label"
        defaultWidth={250}
        viewportPx={1000}
        handleAriaLabel="Ubah ukuran panel"
      >
        content
      </ResizablePanel>,
    );

    expect(getHandle(container).getAttribute("aria-label")).toBe("Ubah ukuran panel");
  });

  it('defaults the handle\'s aria-label to "Resize panel" when handleAriaLabel is omitted', () => {
    const { container } = render(
      <ResizablePanel storageKey="test-handle-aria-label-default" defaultWidth={250} viewportPx={1000}>
        content
      </ResizablePanel>,
    );

    expect(getHandle(container).getAttribute("aria-label")).toBe("Resize panel");
  });

  it("resets to the default width when the handle is double-clicked", () => {
    const { container } = render(
      <ResizablePanel storageKey="test-double-click-reset" defaultWidth={250} minPct={15} maxPct={35} viewportPx={1000}>
        content
      </ResizablePanel>,
    );
    const handle = getHandle(container);

    dragHandleBy(handle, 60);
    expect(getPanelWidthPx(container)).toBe(310);

    fireEvent.doubleClick(handle);

    expect(getPanelWidthPx(container)).toBe(250);
  });

  it("jumps to the minimum band width when Home is pressed on the handle", () => {
    const { container } = render(
      <ResizablePanel storageKey="test-home-key" defaultWidth={250} minPct={15} maxPct={35} viewportPx={1000}>
        content
      </ResizablePanel>,
    );
    const handle = getHandle(container);
    handle.focus();

    fireEvent.keyDown(handle, { key: "Home" });

    expect(getPanelWidthPx(container)).toBe(150);
    expect(handle.getAttribute("aria-valuenow")).toBe("150");
  });

  it("jumps to the maximum band width when End is pressed on the handle", () => {
    const { container } = render(
      <ResizablePanel storageKey="test-end-key" defaultWidth={250} minPct={15} maxPct={35} viewportPx={1000}>
        content
      </ResizablePanel>,
    );
    const handle = getHandle(container);
    handle.focus();

    fireEvent.keyDown(handle, { key: "End" });

    expect(getPanelWidthPx(container)).toBe(350);
    expect(handle.getAttribute("aria-valuenow")).toBe("350");
  });

  it("prevents native text selection while dragging the handle", () => {
    const { container } = render(
      <ResizablePanel storageKey="test-select-none" defaultWidth={250} viewportPx={1000}>
        content
      </ResizablePanel>,
    );

    // `touch-none` alone only sets `touch-action: none` (touch-gesture handling); it does not
    // stop a mouse-based drag from starting a native text-selection drag over surrounding page
    // content, so `select-none` (user-select: none) is required alongside it — matching
    // scroll-area.tsx's own draggable-thumb precedent.
    expect(getHandle(container).className).toContain("select-none");
  });

  it("widens the handle's interactive hit target past its visible line so touch/coarse pointers meet the WCAG 2.5.8 minimum", () => {
    const { container } = render(
      <ResizablePanel storageKey="test-hit-target" defaultWidth={250} viewportPx={1000}>
        content
      </ResizablePanel>,
    );

    const handle = getHandle(container);
    // 4px visible line (w-1) + 10px padding on each side (-left-2.5/-right-2.5) = 24px,
    // meeting WCAG 2.5.8's 24x24 CSS px minimum without shifting the flex layout width.
    expect(handle.className).toContain("-left-2.5");
    expect(handle.className).toContain("-right-2.5");
  });

  it("exposes a title tooltip matching the handle's accessible name", () => {
    const { container } = render(
      <ResizablePanel storageKey="test-title" defaultWidth={250} viewportPx={1000} handleAriaLabel="Ubah ukuran panel">
        content
      </ResizablePanel>,
    );

    expect(getHandle(container).getAttribute("title")).toBe("Ubah ukuran panel");
  });

  it("does not persist a width when the handle is pressed and released without moving (a click, not a drag)", () => {
    const { container } = render(
      <ResizablePanel storageKey="test-click-no-drag" defaultWidth={250} minPct={15} maxPct={35} viewportPx={1000}>
        content
      </ResizablePanel>,
    );
    const handle = getHandle(container);
    const setItemSpy = vi.spyOn(Storage.prototype, "setItem");

    fireEvent.pointerDown(handle, { clientX: 0 });
    fireEvent.pointerUp(document);

    expect(getPanelWidthPx(container)).toBe(250);
    expect(setItemSpy).not.toHaveBeenCalled();

    setItemSpy.mockRestore();
  });

  it("ignores keys other than ArrowLeft/ArrowRight/Home/End", () => {
    const { container } = render(
      <ResizablePanel storageKey="test-unrelated-key" defaultWidth={250} minPct={15} maxPct={35} viewportPx={1000}>
        content
      </ResizablePanel>,
    );
    const handle = getHandle(container);
    handle.focus();

    fireEvent.keyDown(handle, { key: "Tab" });

    expect(getPanelWidthPx(container)).toBe(250);
  });

  it("gives the handle's visible line a rest-state token that meets the non-text contrast minimum", () => {
    const { container } = render(
      <ResizablePanel storageKey="test-contrast" defaultWidth={250} viewportPx={1000}>
        content
      </ResizablePanel>,
    );

    const visibleLine = getHandle(container).querySelector("span");
    expect(visibleLine).toBeInstanceOf(HTMLElement);
    // bg-border computed to ~1.26:1 against the page background (DWT-002); bg-muted-foreground
    // computes to ~4.7:1, clearing WCAG 2.1 SC 1.4.11's 3:1 minimum for a UI-component boundary.
    expect((visibleLine as HTMLElement).className).toContain("bg-muted-foreground");
    expect((visibleLine as HTMLElement).className).not.toContain("bg-border");
  });
});
