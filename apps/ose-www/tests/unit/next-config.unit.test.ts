import { describe, expect, it } from "vitest";

import nextConfig from "../../next.config";

describe("ose-www development origin policy", () => {
  it("allows the documented loopback origin for development HMR", () => {
    expect(nextConfig.allowedDevOrigins).toEqual(["127.0.0.1"]);
  });
});
