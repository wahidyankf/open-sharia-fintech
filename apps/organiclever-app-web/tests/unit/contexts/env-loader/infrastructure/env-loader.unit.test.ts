import { describe, it, expect } from "vitest";

describe("env-loader wrapper", () => {
  it("calling loadTierEnv() on import does not throw, and re-exports the shared loader API", async () => {
    const mod = await import("../../../../../src/contexts/env-loader/infrastructure/env-loader");

    expect(mod.loadTierEnv).toBeTypeOf("function");
    expect(mod.resolveTier).toBeTypeOf("function");
    expect(mod.tierEnvFilePath).toBeTypeOf("function");
  });
});
