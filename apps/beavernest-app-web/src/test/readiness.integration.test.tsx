import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterAll, afterEach, beforeAll, describe, expect, it } from "vitest";
import { http, HttpResponse } from "msw";
import { App } from "../App";
import { fetchReadiness } from "../lib/readiness-client";
import { readinessReady, readinessUnavailable } from "./msw/handlers";
import { server } from "./msw/server";

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("workspace readiness", () => {
  it("shows a checking state before rendering readiness", async () => {
    let resolveResponse: (() => void) | undefined;
    server.use(
      http.get("*/api/v1/readiness", async () => {
        await new Promise<void>((resolve) => {
          resolveResponse = resolve;
        });
        return HttpResponse.json(readinessReady);
      }),
    );

    render(<App />);
    expect(screen.getByText("Checking foundation status")).toBeVisible();
    expect(screen.queryByText("Database")).not.toBeInTheDocument();

    await waitFor(() => expect(resolveResponse).toBeDefined());
    await act(async () => resolveResponse?.());
    expect(await screen.findByText("Current")).toBeVisible();
  });

  it("renders an unavailable response and retries in place", async () => {
    let attempts = 0;
    server.use(
      http.get("*/api/v1/readiness", () => {
        attempts += 1;
        return attempts === 1
          ? HttpResponse.json(readinessUnavailable, { status: 503 })
          : HttpResponse.json(readinessReady);
      }),
    );

    render(<App />);
    expect(await screen.findByRole("img", { name: "Unavailable" })).toBeVisible();

    const refresh = screen.getByRole("button", { name: /refresh status/i });
    fireEvent.click(refresh);

    expect(await screen.findByText("Current")).toBeVisible();
    expect(attempts).toBe(2);
    expect(window.location.pathname).toBe("/");
  });

  it("treats unexpected endpoint responses as unavailable", async () => {
    server.use(http.get("*/api/v1/readiness", () => HttpResponse.json({ error: "unexpected" }, { status: 500 })));

    await expect(fetchReadiness()).rejects.toThrow("foundation status");
    render(<App />);
    expect(await screen.findByRole("img", { name: "Unavailable" })).toBeVisible();
  });
});
