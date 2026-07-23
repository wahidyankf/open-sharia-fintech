import { describe, expect, it } from "vitest";
import { PathManifestSchema } from "./schemas";

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
});
