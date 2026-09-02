import { render } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Separator } from "../../../../src/primitives/separator/separator";

describe("Separator primitive", () => {
  it("mounts in the DOM", () => {
    const { container } = render(<Separator />);
    expect(container.querySelector("[data-slot='separator']")).toBeTruthy();
  });
});
