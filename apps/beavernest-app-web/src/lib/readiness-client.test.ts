import { afterAll, afterEach, beforeAll, describe, expect, it } from "vitest";
import { http, HttpResponse } from "msw";
import { fetchReadiness } from "./readiness-client";
import { readinessReady, readinessUnavailable } from "../test/msw/handlers";
import { server } from "../test/msw/server";

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("fetchReadiness", () => {
  it("resolves a well-formed ready body", async () => {
    server.use(http.get("*/api/v1/readiness", () => HttpResponse.json(readinessReady)));

    await expect(fetchReadiness()).resolves.toEqual(readinessReady);
  });

  it("resolves a well-formed unavailable body on a 503 response", async () => {
    server.use(http.get("*/api/v1/readiness", () => HttpResponse.json(readinessUnavailable, { status: 503 })));

    await expect(fetchReadiness()).resolves.toEqual(readinessUnavailable);
  });

  it("rejects a 200 response whose body does not match the readiness contract", async () => {
    // Regression test: a plain `as ReadinessResponse` cast trusted this shape
    // without checking it, so a malformed 200 body would previously have been
    // returned as if it were a valid ReadinessResponse.
    server.use(http.get("*/api/v1/readiness", () => HttpResponse.json({ unexpected: "shape" })));

    await expect(fetchReadiness()).rejects.toThrow("foundation status");
  });

  it("rejects a 503 response whose body does not match the readiness contract", async () => {
    server.use(http.get("*/api/v1/readiness", () => HttpResponse.json({ status: "degraded" }, { status: 503 })));

    await expect(fetchReadiness()).rejects.toThrow("foundation status");
  });
});
