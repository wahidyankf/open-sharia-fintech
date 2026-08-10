import { render, screen, waitFor } from "@testing-library/react";
import { afterAll, afterEach, beforeAll, describe, expect, it } from "vitest";
import { App } from "./App";
import { server } from "./test/msw/server";

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("workspace home", () => {
  it("renders the shell before its same-origin readiness request resolves", async () => {
    render(<App />);

    expect(screen.getByRole("heading", { level: 1, name: "BeaverNest" })).toBeVisible();
    expect(screen.getByRole("heading", { name: "Foundation status" })).toBeVisible();
    expect(screen.getByText("No workspace features yet")).toBeVisible();
    expect(screen.getByRole("region", { name: "Foundation status" })).toHaveAttribute("aria-live", "polite");

    await waitFor(() => expect(screen.getByText("Current")).toBeVisible());
  });

  it("contains neither the retired promotion nor an external GitHub call to action", async () => {
    render(<App />);

    expect(screen.queryByText(/personal operating layer/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("link", { name: /github/i })).not.toBeInTheDocument();
  });
});
