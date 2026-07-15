import { render, screen, cleanup, fireEvent } from "@testing-library/react";
import { renderToStaticMarkup } from "react-dom/server";
import { axe } from "vitest-axe";
import { describe, it, expect, afterEach, beforeEach } from "vitest";

import { ResizablePanel } from "./resizable-panel";

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
});
