import { describe, expect, it } from "vitest";
import { PRIMARY_NAV_LINKS } from "../../../../../src/features/app-shell/core/nav-links";

describe("PRIMARY_NAV_LINKS", () => {
  it("exposes Learn and Tools entries in order", () => {
    expect(PRIMARY_NAV_LINKS.map((l) => l.labelKey)).toEqual(["navLearn", "navTools"]);
  });

  it("builds locale-aware hrefs for en", () => {
    const hrefs = PRIMARY_NAV_LINKS.map((l) => l.hrefFor("en"));
    expect(hrefs).toEqual(["/en/browse", "/en/tools"]);
  });

  it("builds locale-aware hrefs for id", () => {
    const hrefs = PRIMARY_NAV_LINKS.map((l) => l.hrefFor("id"));
    expect(hrefs).toEqual(["/id/browse", "/id/tools"]);
  });
});
