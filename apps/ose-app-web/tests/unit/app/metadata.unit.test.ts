import { describe, it, expect } from "vitest";
import { siteMetadata } from "../../../src/app/metadata";

describe("siteMetadata", () => {
  it("declares the OSE Application title and description", () => {
    expect(siteMetadata.title).toEqual({
      default: "OSE Application",
      template: "%s | OSE Application",
    });
    expect(siteMetadata.description).toContain("OSE Application");
  });
});
