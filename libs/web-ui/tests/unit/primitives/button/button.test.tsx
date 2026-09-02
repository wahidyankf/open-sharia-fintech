import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Button } from "../../../../src/primitives/button/button";

describe("Button primitive", () => {
  it("mounts in the DOM", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole("button", { name: /click me/i })).toBeTruthy();
  });

  it("renders as its child element when asChild is true", () => {
    render(
      <Button asChild>
        <a href="#go">Go</a>
      </Button>,
    );
    const link = screen.getByRole("link", { name: "Go" });
    expect(link.getAttribute("data-slot")).toBe("button");
  });
});
