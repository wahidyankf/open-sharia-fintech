import { describe, expect, it } from "vitest";
import { PathManifestSchema } from "../../../../../src/features/course-paths/core/schemas";

// A minimal, otherwise-valid 3-segment careers manifest used as the base fixture for the
// negative-path assertions below (each test overrides or removes exactly one field).
const careersManifest = {
  pathId: "careers/interview-ready/software-engineer",
  arc: "interview-ready",
  title: "Interview-Ready Software Engineer",
  description: "Interview-first track for an experienced engineer re-entering the market.",
  courseOrder: ["just-enough-python", "capstone-forge-ready"],
};

describe("PathManifestSchema", () => {
  it("(a) accepts a manifest whose courseOrder mixes bare course-ID strings with framing objects", () => {
    const manifest = {
      ...careersManifest,
      courseOrder: [
        "just-enough-python",
        {
          id: "capstone-forge-ready",
          framing: {
            intro: "Before you start the capstone, revisit your interview notes.",
            outro: "You are ready to walk into the interview loop.",
          },
        },
      ],
    };

    const result = PathManifestSchema.safeParse(manifest);

    expect(result.success).toBe(true);
  });

  it("(b) accepts a 3-segment careers fixture, a 2-segment skills fixture, and a 4-segment forward-compatibility fixture — no fixed segment count", () => {
    const threeSegmentCareers = careersManifest;
    const twoSegmentSkills = {
      pathId: "skills/conventional-accounting",
      arc: "immediately-effective",
      title: "Conventional Accounting",
      description: "A from-scratch skills track in conventional accounting fundamentals.",
      courseOrder: ["just-enough-python"],
    };
    const fourSegmentForwardCompat = {
      pathId: "careers/a/b/c",
      arc: "interview-ready",
      title: "Forward-compatibility fixture",
      description: "Proves the schema never bounds pathId depth above.",
      courseOrder: ["just-enough-python"],
    };

    expect(PathManifestSchema.safeParse(threeSegmentCareers).success).toBe(true);
    expect(PathManifestSchema.safeParse(twoSegmentSkills).success).toBe(true);
    expect(PathManifestSchema.safeParse(fourSegmentForwardCompat).success).toBe(true);
  });

  it("(c) rejects a manifest whose pathId's first segment is neither careers nor skills", () => {
    const manifest = { ...careersManifest, pathId: "bogus/foo" };

    const result = PathManifestSchema.safeParse(manifest);

    expect(result.success).toBe(false);
  });

  it("(d) rejects a bare single-segment pathId, with or without a trailing slash", () => {
    const bareCategory = { ...careersManifest, pathId: "careers" };
    const bareCategoryTrailingSlash = { ...careersManifest, pathId: "careers/" };

    expect(PathManifestSchema.safeParse(bareCategory).success).toBe(false);
    expect(PathManifestSchema.safeParse(bareCategoryTrailingSlash).success).toBe(false);
  });

  it("(e) rejects a manifest missing arc, even on an otherwise-valid 2-segment skills fixture", () => {
    const { arc: _arc, ...manifestWithoutArc } = {
      pathId: "skills/conventional-accounting",
      arc: "immediately-effective",
      title: "Conventional Accounting",
      description: "A from-scratch skills track in conventional accounting fundamentals.",
      courseOrder: ["just-enough-python"],
    };

    const result = PathManifestSchema.safeParse(manifestWithoutArc);

    expect(result.success).toBe(false);
  });

  it("(f) rejects a manifest missing courseOrder", () => {
    const { courseOrder: _courseOrder, ...manifestWithoutCourseOrder } = careersManifest;

    const result = PathManifestSchema.safeParse(manifestWithoutCourseOrder);

    expect(result.success).toBe(false);
  });

  it("(g) rejects a pathId carrying a '..' path-traversal segment even though it otherwise satisfies the category-prefix and minimum-arity checks", () => {
    const manifest = { ...careersManifest, pathId: "careers/../../../etc/passwd" };

    const result = PathManifestSchema.safeParse(manifest);

    expect(result.success).toBe(false);
  });

  it("(h) rejects a pathId carrying a bare '.' segment", () => {
    const manifest = { ...careersManifest, pathId: "careers/./software-engineer" };

    const result = PathManifestSchema.safeParse(manifest);

    expect(result.success).toBe(false);
  });

  it("(i) rejects a pathId containing a backslash", () => {
    const manifest = { ...careersManifest, pathId: "careers\\interview-ready\\software-engineer" };

    const result = PathManifestSchema.safeParse(manifest);

    expect(result.success).toBe(false);
  });

  it("(j) rejects a pathId containing a null byte", () => {
    const manifest = { ...careersManifest, pathId: "careers/interview-ready\0" };

    const result = PathManifestSchema.safeParse(manifest);

    expect(result.success).toBe(false);
  });

  // RED (PR review finding #1, pr-review-synthesis-maker review 4770318960, cycle 2): the
  // pre-fix schema forbade only `\`, `\0`, `.`, and `..` — a pathId containing `&`, `=`, `#`, `%`,
  // or whitespace passed `safeParse` even though `contentUrl` interpolates it unencoded into a
  // `?path=` query string, corrupting or truncating it on the `URLSearchParams` round-trip in
  // `parsePathContext`.
  it("(k) rejects a pathId containing query-string-hazard characters ('&', '=', '#', '%', whitespace)", () => {
    const ampersand = { ...careersManifest, pathId: "careers/soft&ware=engineer" };
    const hash = { ...careersManifest, pathId: "careers/soft#ware" };
    const percent = { ...careersManifest, pathId: "careers/soft%20ware" };
    const whitespace = { ...careersManifest, pathId: "careers/soft ware" };

    expect(PathManifestSchema.safeParse(ampersand).success).toBe(false);
    expect(PathManifestSchema.safeParse(hash).success).toBe(false);
    expect(PathManifestSchema.safeParse(percent).success).toBe(false);
    expect(PathManifestSchema.safeParse(whitespace).success).toBe(false);
  });

  // RED (PR review finding #2, pr-review-synthesis-maker review 4770318960, cycle 2): the pre-fix
  // arity floor counted segments AFTER `.split("/").filter(Boolean)` dropped empty tokens, so a
  // trailing slash or a doubled slash on an otherwise-valid, multi-segment pathId validated
  // identically to its clean form — two "equal" paths that differ by string.
  it("(l) rejects an otherwise-valid pathId carrying a trailing slash or a doubled internal slash", () => {
    const trailingSlash = { ...careersManifest, pathId: "careers/interview-ready/software-engineer/" };
    const doubledSlash = { ...careersManifest, pathId: "careers//interview-ready" };

    expect(PathManifestSchema.safeParse(trailingSlash).success).toBe(false);
    expect(PathManifestSchema.safeParse(doubledSlash).success).toBe(false);
  });
});
