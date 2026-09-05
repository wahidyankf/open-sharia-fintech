import { describe, expect, it } from "vitest";
import { localeEntryRedirects, resolveLocaleEntryRedirect } from "../../../src/redirects/locale-entry";

describe("ayokoding-www locale redirects", () => {
  it("declares root and uppercase-locale redirects through the production policy", () => {
    expect(localeEntryRedirects).toContainEqual({ source: "/", destination: "/en", permanent: true });
    expect(resolveLocaleEntryRedirect("/EN/tools/cost-of-living-calculator")).toBe(
      "/en/tools/cost-of-living-calculator",
    );
    expect(resolveLocaleEntryRedirect("/ID/belajar")).toBe("/id/belajar");
    expect(resolveLocaleEntryRedirect("/en/learn")).toBeNull();
  });
});
