import { describe, it, expect } from "vitest";

describe("env wrapper", () => {
  it("calling createEnv() on import does not throw, and produces the validated env object", async () => {
    const mod = await import("../../src/env");

    expect(mod.env).toBeTypeOf("object");
  });
});
