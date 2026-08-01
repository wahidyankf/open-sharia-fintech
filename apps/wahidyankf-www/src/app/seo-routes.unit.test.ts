import { describe, expect, it } from "vitest";
import robots from "./robots";
import sitemap from "./sitemap";

describe("SEO metadata routes", () => {
  it("advertises the canonical sitemap to crawlers", () => {
    expect(robots()).toEqual({
      rules: [{ userAgent: "*", allow: "/" }],
      sitemap: "https://www.wahidyankf.com/sitemap.xml",
    });
  });

  it("lists every public portfolio route at the canonical domain", () => {
    expect(sitemap()).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ url: "https://www.wahidyankf.com" }),
        expect.objectContaining({ url: "https://www.wahidyankf.com/cv" }),
        expect.objectContaining({ url: "https://www.wahidyankf.com/personal-projects" }),
      ]),
    );
  });
});
