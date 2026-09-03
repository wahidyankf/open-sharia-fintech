import { describe, it, expect } from "vitest";
import { siteMetadata } from "../../../src/app/metadata";

describe("siteMetadata", () => {
  it("declares the OrganicLever title and description", () => {
    expect(siteMetadata.title).toEqual({
      default: "OrganicLever",
      template: "%s | OrganicLever",
    });
    expect(siteMetadata.description).toContain("OrganicLever");
  });
});
