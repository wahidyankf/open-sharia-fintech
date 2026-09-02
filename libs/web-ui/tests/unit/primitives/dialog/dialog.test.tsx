import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import {
  Dialog,
  DialogClose,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
} from "../../../../src/primitives/dialog/dialog";

describe("Dialog primitive", () => {
  it("mounts trigger in the DOM", () => {
    render(
      <Dialog>
        <DialogTrigger>Open Dialog</DialogTrigger>
        <DialogContent>
          <DialogTitle>Dialog Title</DialogTitle>
        </DialogContent>
      </Dialog>,
    );
    expect(screen.getByText("Open Dialog")).toBeTruthy();
  });

  it("renders header, footer, title, and description with their data-slots when open", () => {
    render(
      <Dialog open>
        <DialogContent showCloseButton={false}>
          <DialogHeader>
            <DialogTitle>Title</DialogTitle>
            <DialogDescription>Description</DialogDescription>
          </DialogHeader>
          <DialogFooter>Footer</DialogFooter>
        </DialogContent>
      </Dialog>,
    );
    expect(screen.getByText("Title").getAttribute("data-slot")).toBe("dialog-title");
    expect(screen.getByText("Description").getAttribute("data-slot")).toBe("dialog-description");
    expect(screen.getByText("Footer").getAttribute("data-slot")).toBe("dialog-footer");
  });

  it("renders the default close button when open", () => {
    render(
      <Dialog open>
        <DialogContent>
          <DialogTitle>Title</DialogTitle>
        </DialogContent>
      </Dialog>,
    );
    expect(screen.getByText("Close")).toBeTruthy();
  });

  it("renders DialogClose with data-slot", () => {
    render(
      <Dialog open>
        <DialogContent showCloseButton={false}>
          <DialogTitle>Title</DialogTitle>
          <DialogClose>Dismiss</DialogClose>
        </DialogContent>
      </Dialog>,
    );
    expect(screen.getByText("Dismiss").getAttribute("data-slot")).toBe("dialog-close");
  });
});
