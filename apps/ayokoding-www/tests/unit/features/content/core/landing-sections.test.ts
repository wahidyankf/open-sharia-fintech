import { describe, expect, it } from "vitest";
import type { TreeNode } from "../../../../../src/features/content/core/types";
import {
  LANDING_SECTION_OVERRIDES,
  mergeLandingSections,
} from "../../../../../src/features/content/core/landing-sections";

function section(slug: string, title: string): TreeNode {
  return { slug, title, weight: 0, isSection: true, children: [] };
}

const FALLBACK = "Explore this section.";

describe("mergeLandingSections", () => {
  it("falls back to the tree title and the fallback blurb when no override exists", () => {
    const tree = [section("misc", "Miscellany")];
    const result = mergeLandingSections(tree, {}, FALLBACK);

    expect(result).toHaveLength(1);
    expect(result[0]).toMatchObject({
      slug: "misc",
      title: "Miscellany",
      blurb: FALLBACK,
      icon: undefined,
    });
  });

  it("applies an override blurb and icon when present", () => {
    const tree = [section("learn", "Learn")];
    const overrides = {
      learn: { order: 1, icon: "code", blurb: "Languages, architecture, system design." },
    };
    const result = mergeLandingSections(tree, overrides, FALLBACK);

    expect(result[0]).toMatchObject({
      slug: "learn",
      title: "Learn",
      blurb: "Languages, architecture, system design.",
      icon: "code",
    });
  });

  it("orders sections by the override order, ascending", () => {
    const tree = [section("rants", "Rants"), section("learn", "Learn")];
    const overrides = {
      learn: { order: 1 },
      rants: { order: 2 },
    };
    const result = mergeLandingSections(tree, overrides, FALLBACK);

    expect(result.map((s) => s.slug)).toEqual(["learn", "rants"]);
  });

  it("drops sections flagged hidden so they produce no card", () => {
    const tree = [section("learn", "Learn"), section("secret", "Secret")];
    const overrides = {
      secret: { hide: true },
    };
    const result = mergeLandingSections(tree, overrides, FALLBACK);

    expect(result.map((s) => s.slug)).toEqual(["learn"]);
  });

  it("keeps non-overridden sections after overridden ones, preserving tree order among ties", () => {
    const tree = [section("a", "A"), section("b", "B"), section("c", "C")];
    const overrides = {
      c: { order: 1 },
    };
    const result = mergeLandingSections(tree, overrides, FALLBACK);

    // c is pulled to the front by its explicit order; a, b keep tree order.
    expect(result.map((s) => s.slug)).toEqual(["c", "a", "b"]);
  });

  it("derives id-locale descriptors from the id tree (Belajar/Celoteh)", () => {
    const tree = [section("belajar", "Belajar"), section("celoteh", "Celoteh")];
    const result = mergeLandingSections(tree, LANDING_SECTION_OVERRIDES.id, FALLBACK);

    const slugs = result.map((s) => s.slug);
    expect(slugs).toContain("belajar");
    expect(slugs).toContain("celoteh");
    const celoteh = result.find((s) => s.slug === "celoteh");
    expect(celoteh?.title).toBe("Celoteh");
  });
});

describe("LANDING_SECTION_OVERRIDES", () => {
  it("provides a curated config for both locales", () => {
    expect(LANDING_SECTION_OVERRIDES.en).toBeDefined();
    expect(LANDING_SECTION_OVERRIDES.id).toBeDefined();
  });
});
