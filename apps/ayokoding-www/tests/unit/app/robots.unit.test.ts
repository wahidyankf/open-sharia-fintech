import { describe, expect, it } from "vitest";
import robots from "../../../src/app/robots";

describe("robots", () => {
  it("publishes the sitemap from the canonical www host", () => {
    expect(robots().sitemap).toBe("https://www.ayokoding.com/sitemap.xml");
  });
});
