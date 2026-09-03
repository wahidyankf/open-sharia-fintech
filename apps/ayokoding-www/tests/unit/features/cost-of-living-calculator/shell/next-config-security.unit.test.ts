import { describe, expect, it } from "vitest";

describe("EWT-013 — next.config security headers", () => {
  it("EWT-013: next.config exports a config with a headers function", async () => {
    const mod = await import("../../../../../next.config");
    const config = mod.default;
    expect(typeof config.headers).toBe("function");
  });

  it("EWT-013: headers function returns X-Content-Type-Options, X-Frame-Options, Referrer-Policy headers", async () => {
    const mod = await import("../../../../../next.config");
    const config = mod.default;
    const headersResult = await config.headers!();

    expect(Array.isArray(headersResult)).toBe(true);
    const allHeaders = headersResult.flatMap((r) => r.headers);

    const keys = allHeaders.map((h) => h.key);
    expect(keys).toContain("X-Content-Type-Options");
    expect(keys).toContain("X-Frame-Options");
    expect(keys).toContain("Referrer-Policy");
  });

  it("EWT-013: config has poweredByHeader set to false", async () => {
    const mod = await import("../../../../../next.config");
    const config = mod.default;
    expect(config.poweredByHeader).toBe(false);
  });
});
