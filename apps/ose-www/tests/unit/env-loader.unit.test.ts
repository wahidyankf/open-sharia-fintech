import { beforeEach, describe, expect, it, vi } from "vitest";

const loaderSpies = vi.hoisted(() => ({
  loadTierEnv: vi.fn(),
  resolveTier: vi.fn(),
  tierEnvFilePath: vi.fn(),
}));

vi.mock("@open-sharia-enterprise/ts-env-loader", () => loaderSpies);

describe("env-loader composition wrapper", () => {
  beforeEach(() => {
    vi.resetModules();
    loaderSpies.loadTierEnv.mockClear();
  });

  it("invokes the shared loader on import and re-exports its public API", async () => {
    const module = await import("../../src/env-loader");

    expect(loaderSpies.loadTierEnv).toHaveBeenCalledOnce();
    expect(module.loadTierEnv).toBeTypeOf("function");
    expect(module.resolveTier).toBeTypeOf("function");
    expect(module.tierEnvFilePath).toBeTypeOf("function");
  });
});
