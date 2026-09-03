import { describe, expect, it } from "vitest";
import { normalizeSlug, slugFromSegments } from "../../../../../src/features/content/core/slug";

describe("normalizeSlug", () => {
  it("strips a single leading and trailing slash", () => {
    expect(normalizeSlug("/learn/se/")).toBe("learn/se");
  });

  it("trims surrounding whitespace", () => {
    expect(normalizeSlug("  learn/se  ")).toBe("learn/se");
  });

  it("returns empty string for empty input", () => {
    expect(normalizeSlug("")).toBe("");
  });
});

describe("slugFromSegments", () => {
  it("joins catch-all segments into a canonical slug", () => {
    expect(slugFromSegments(["learn", "software-engineering"])).toBe("learn/software-engineering");
  });

  it("returns the root slug for undefined or empty segments", () => {
    expect(slugFromSegments(undefined)).toBe("");
    expect(slugFromSegments([])).toBe("");
  });

  it("joins segments as-is — no namespace prefix to strip (DD-48)", () => {
    expect(slugFromSegments(["belajar", "ikhtisar"])).toBe("belajar/ikhtisar");
  });
});
