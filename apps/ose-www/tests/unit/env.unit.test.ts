import { describe, it, expect } from "vitest";

describe("env", () => {
  it("exports the content-boundary settings validated by createEnv", async () => {
    const { env } = await import("../../src/env");
    expect(env).toBeDefined();
    expect(Object.prototype.hasOwnProperty.call(env, "OSE_WEB_CONTENT_DIR")).toBe(true);
    expect(Object.prototype.hasOwnProperty.call(env, "OSE_WEB_SEARCH_DATA_PATH")).toBe(true);
    expect(Object.prototype.hasOwnProperty.call(env, "OSE_WEB_SHOW_DRAFTS")).toBe(true);
  });
});
