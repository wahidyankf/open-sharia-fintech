import { describe, it, expect, beforeAll } from "vitest";

describe("env", () => {
  beforeAll(() => {
    process.env.SKIP_ENV_VALIDATION = "1";
  });

  it("exports OSE_WEB_SHOW_DRAFTS validated by createEnv", async () => {
    const { env } = await import("../../src/env");
    expect(env).toBeDefined();
    expect(Object.prototype.hasOwnProperty.call(env, "OSE_WEB_SHOW_DRAFTS")).toBe(true);
  });
});
