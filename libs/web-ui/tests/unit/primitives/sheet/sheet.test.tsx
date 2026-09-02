import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import {
  Sheet,
  SheetClose,
  SheetTrigger,
  SheetContent,
  SheetHeader,
  SheetFooter,
  SheetTitle,
  SheetDescription,
} from "../../../../src/primitives/sheet/sheet";

describe("Sheet primitive", () => {
  it("mounts trigger in the DOM", () => {
    render(
      <Sheet>
        <SheetTrigger>Open</SheetTrigger>
        <SheetContent>
          <SheetHeader>
            <SheetTitle>Sheet Title</SheetTitle>
          </SheetHeader>
        </SheetContent>
      </Sheet>,
    );
    expect(screen.getByText("Open")).toBeTruthy();
  });

  it("renders header, footer, title, and description with their data-slots when open", () => {
    render(
      <Sheet open>
        <SheetContent showCloseButton={false}>
          <SheetHeader>
            <SheetTitle>Title</SheetTitle>
            <SheetDescription>Description</SheetDescription>
          </SheetHeader>
          <SheetFooter>Footer</SheetFooter>
        </SheetContent>
      </Sheet>,
    );
    expect(screen.getByText("Title").getAttribute("data-slot")).toBe("sheet-title");
    expect(screen.getByText("Description").getAttribute("data-slot")).toBe("sheet-description");
    expect(screen.getByText("Footer").getAttribute("data-slot")).toBe("sheet-footer");
  });

  it("renders the default close button when open", () => {
    render(
      <Sheet open>
        <SheetContent>
          <SheetTitle>Title</SheetTitle>
        </SheetContent>
      </Sheet>,
    );
    expect(screen.getByText("Close")).toBeTruthy();
  });

  it("renders SheetClose with data-slot", () => {
    render(
      <Sheet open>
        <SheetContent showCloseButton={false}>
          <SheetTitle>Title</SheetTitle>
          <SheetClose>Dismiss</SheetClose>
        </SheetContent>
      </Sheet>,
    );
    expect(screen.getByText("Dismiss").getAttribute("data-slot")).toBe("sheet-close");
  });
});
