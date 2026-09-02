import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "../../../../src/primitives/tooltip/tooltip";

describe("Tooltip primitive", () => {
  it("mounts trigger in the DOM", () => {
    render(
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger>Hover me</TooltipTrigger>
          <TooltipContent>Tooltip text</TooltipContent>
        </Tooltip>
      </TooltipProvider>,
    );
    expect(screen.getByText("Hover me")).toBeTruthy();
  });
});
