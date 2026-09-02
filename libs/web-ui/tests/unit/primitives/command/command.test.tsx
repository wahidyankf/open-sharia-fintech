import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import {
  Command,
  CommandDialog,
  CommandInput,
  CommandList,
  CommandEmpty,
  CommandGroup,
  CommandItem,
  CommandSeparator,
  CommandShortcut,
} from "../../../../src/primitives/command/command";

describe("Command primitive", () => {
  it("mounts in the DOM", () => {
    render(
      <Command>
        <CommandInput placeholder="Search..." />
        <CommandList>
          <CommandItem>Option 1</CommandItem>
        </CommandList>
      </Command>,
    );
    expect(screen.getByPlaceholderText("Search...")).toBeTruthy();
  });

  it("renders CommandEmpty, CommandGroup, CommandSeparator, and CommandShortcut with their data-slots", () => {
    const { container } = render(
      <Command>
        <CommandList>
          <CommandEmpty>No results</CommandEmpty>
          <CommandGroup heading="Group">
            <CommandItem>
              Option 1<CommandShortcut>Ctrl+K</CommandShortcut>
            </CommandItem>
          </CommandGroup>
          <CommandSeparator />
        </CommandList>
      </Command>,
    );
    expect(container.querySelector("[data-slot='command-group']")).toBeTruthy();
    expect(container.querySelector("[data-slot='command-separator']")).toBeTruthy();
    expect(screen.getByText("Ctrl+K").getAttribute("data-slot")).toBe("command-shortcut");
  });

  it("renders CommandDialog with a default title/description, wrapping Command in a modal", () => {
    render(
      <CommandDialog open>
        <CommandInput placeholder="Type a command..." />
        <CommandList>
          <CommandItem>Option 1</CommandItem>
        </CommandList>
      </CommandDialog>,
    );
    expect(screen.getByText("Command Palette")).toBeTruthy();
    expect(screen.getByText("Search for a command to run...")).toBeTruthy();
    expect(screen.getByPlaceholderText("Type a command...")).toBeTruthy();
  });

  it("renders CommandDialog with a custom title/description and hidden close button", () => {
    render(
      <CommandDialog open title="Jump to" description="Search pages" showCloseButton={false}>
        <CommandInput placeholder="Search pages..." />
      </CommandDialog>,
    );
    expect(screen.getByText("Jump to")).toBeTruthy();
    expect(screen.getByText("Search pages")).toBeTruthy();
    expect(screen.queryByText("Close")).toBeNull();
  });
});
