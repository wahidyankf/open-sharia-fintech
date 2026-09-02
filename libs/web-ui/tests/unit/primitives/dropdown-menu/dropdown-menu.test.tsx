import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuLabel,
  DropdownMenuItem,
  DropdownMenuCheckboxItem,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuSubTrigger,
  DropdownMenuSubContent,
} from "../../../../src/primitives/dropdown-menu/dropdown-menu";

describe("DropdownMenu primitive", () => {
  it("mounts trigger in the DOM", () => {
    render(
      <DropdownMenu>
        <DropdownMenuTrigger>Open Menu</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>Item 1</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>,
    );
    expect(screen.getByText("Open Menu")).toBeTruthy();
  });

  it("renders every content subcomponent with its data-slot when open", () => {
    // DropdownMenuContent (and DropdownMenuSubContent) portal into `document.body`, outside the
    // `container` RTL scopes render output to — query the document instead.
    render(
      <DropdownMenu open>
        <DropdownMenuTrigger>Open Menu</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuLabel>Actions</DropdownMenuLabel>
          <DropdownMenuGroup>
            <DropdownMenuItem>
              Item 1<DropdownMenuShortcut>Ctrl+I</DropdownMenuShortcut>
            </DropdownMenuItem>
          </DropdownMenuGroup>
          <DropdownMenuCheckboxItem checked>Checkbox item</DropdownMenuCheckboxItem>
          <DropdownMenuRadioGroup value="a">
            <DropdownMenuRadioItem value="a">Radio item</DropdownMenuRadioItem>
          </DropdownMenuRadioGroup>
          <DropdownMenuSeparator />
          <DropdownMenuSub open>
            <DropdownMenuSubTrigger>More</DropdownMenuSubTrigger>
            <DropdownMenuSubContent>
              <DropdownMenuItem>Sub item</DropdownMenuItem>
            </DropdownMenuSubContent>
          </DropdownMenuSub>
        </DropdownMenuContent>
      </DropdownMenu>,
    );

    expect(screen.getByText("Actions").getAttribute("data-slot")).toBe("dropdown-menu-label");
    expect(document.body.querySelector("[data-slot='dropdown-menu-group']")).toBeTruthy();
    expect(screen.getByText("Ctrl+I").getAttribute("data-slot")).toBe("dropdown-menu-shortcut");
    expect(document.body.querySelector("[data-slot='dropdown-menu-checkbox-item']")).toBeTruthy();
    expect(document.body.querySelector("[data-slot='dropdown-menu-radio-group']")).toBeTruthy();
    expect(document.body.querySelector("[data-slot='dropdown-menu-separator']")).toBeTruthy();
    expect(screen.getByText("More").getAttribute("data-slot")).toBe("dropdown-menu-sub-trigger");
    expect(screen.getByText("Sub item").closest("[data-slot='dropdown-menu-sub-content']")).toBeTruthy();
  });
});
