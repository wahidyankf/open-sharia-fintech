import { describe, expect, it } from "vitest";
import { readinessReady, readinessUnavailable } from "../test/msw/handlers";
import { initialReadinessState, reduceReadiness } from "./readiness-state";

describe("reduceReadiness", () => {
  it("models request, ready, unavailable, and failed transitions as an immutable union", () => {
    const loading = reduceReadiness({ kind: "ready", response: readinessReady }, { type: "request" });
    const ready = reduceReadiness(loading, { type: "resolved", response: readinessReady });
    const unavailable = reduceReadiness(ready, { type: "resolved", response: readinessUnavailable });
    const failed = reduceReadiness(unavailable, { type: "failed" });

    expect(loading).toEqual(initialReadinessState);
    expect(ready).toMatchObject({ kind: "ready", response: readinessReady });
    expect(unavailable).toEqual({ kind: "unavailable" });
    expect(failed).toEqual({ kind: "unavailable" });
    expect(ready).not.toBe(loading);
  });
});
