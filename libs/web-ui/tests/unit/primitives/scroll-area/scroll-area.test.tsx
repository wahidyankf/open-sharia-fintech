import { render } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { ScrollArea, ScrollBar } from "../../../../src/primitives/scroll-area/scroll-area";

describe("ScrollArea primitive", () => {
  it("mounts in the DOM", () => {
    const { container } = render(<ScrollArea>Scrollable content</ScrollArea>);
    expect(container.querySelector("[data-slot='scroll-area']")).toBeTruthy();
  });

  it("renders a horizontal-orientation ScrollBar", () => {
    // jsdom never reports overflow, so Radix's default `type="hover"` visibility heuristic keeps a
    // real scrollbar unmounted regardless of `forceMount` (a nested, un-forwarded `Presence` gate).
    // `type="always"` (forwarded through `ScrollArea`'s `{...props}`) selects Radix's unconditional
    // `ScrollAreaScrollbarVisible` variant instead, so the `orientation === "horizontal"` class
    // branch actually executes.
    const { container } = render(
      <ScrollArea type="always">
        <ScrollBar orientation="horizontal" />
        content
      </ScrollArea>,
    );
    const scrollbar = container.querySelector("[data-slot='scroll-area-scrollbar'][data-orientation='horizontal']");
    expect(scrollbar).not.toBeNull();
  });
});
