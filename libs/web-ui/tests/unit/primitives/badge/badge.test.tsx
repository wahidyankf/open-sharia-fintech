import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Badge } from "../../../../src/primitives/badge/badge";

describe("Badge primitive", () => {
  it("mounts in the DOM", () => {
    render(<Badge>New</Badge>);
    expect(screen.getByText("New")).toBeTruthy();
  });

  it("renders as its child element when asChild is true", () => {
    render(
      <Badge asChild>
        <a href="#new">New</a>
      </Badge>,
    );
    const link = screen.getByRole("link", { name: "New" });
    expect(link.getAttribute("data-slot")).toBe("badge");
  });
});
