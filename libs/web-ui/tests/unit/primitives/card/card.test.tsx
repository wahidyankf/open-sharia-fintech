import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardAction,
  CardContent,
  CardFooter,
} from "../../../../src/primitives/card/card";

describe("Card primitive", () => {
  it("mounts in the DOM", () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
        </CardHeader>
        <CardContent>Card body content</CardContent>
      </Card>,
    );
    expect(screen.getByText("Card Title")).toBeTruthy();
  });

  it("renders CardDescription, CardAction, and CardFooter with their data-slots", () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
          <CardDescription>Card description text</CardDescription>
          <CardAction>Action</CardAction>
        </CardHeader>
        <CardFooter>Footer content</CardFooter>
      </Card>,
    );
    expect(screen.getByText("Card description text").getAttribute("data-slot")).toBe("card-description");
    expect(screen.getByText("Action").getAttribute("data-slot")).toBe("card-action");
    expect(screen.getByText("Footer content").getAttribute("data-slot")).toBe("card-footer");
  });
});
