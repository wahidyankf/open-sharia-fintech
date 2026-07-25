import { describe, expect, it } from "vitest";
import { buildCourseLibrary } from "./course-library";
import type { ContentMeta } from "@/features/content/core/types";

function meta(overrides: Partial<ContentMeta> & { slug: string }): ContentMeta {
  return {
    title: overrides.title ?? "Untitled",
    slug: overrides.slug,
    locale: overrides.locale ?? "en",
    weight: overrides.weight ?? 0,
    tags: overrides.tags ?? [],
    draft: overrides.draft ?? false,
    isSection: overrides.isSection ?? false,
    filePath: overrides.filePath ?? "/tmp/x.md",
    prerequisites: overrides.prerequisites,
  };
}

describe("buildCourseLibrary", () => {
  it("collects course IDs and prerequisites for the given locale's course pages only", () => {
    const contentMap = new Map<string, ContentMeta>([
      [
        "en:learn/courses/data-structures-and-algorithms-essentials",
        meta({
          slug: "learn/courses/data-structures-and-algorithms-essentials",
          prerequisites: ["version-control-and-git"],
        }),
      ],
      ["en:learn/courses/version-control-and-git", meta({ slug: "learn/courses/version-control-and-git" })],
      // Non-course page — must be excluded from the library.
      ["en:learn/paths", meta({ slug: "learn/paths", isSection: true })],
      // Different locale — must be excluded when building the "en" library.
      [
        "id:learn/courses/version-control-and-git",
        meta({ slug: "learn/courses/version-control-and-git", locale: "id" }),
      ],
    ]);

    const { libraryCourseIds, prerequisitesByCourse } = buildCourseLibrary(contentMap, "en");

    expect([...libraryCourseIds].sort()).toEqual([
      "data-structures-and-algorithms-essentials",
      "version-control-and-git",
    ]);
    expect(prerequisitesByCourse["data-structures-and-algorithms-essentials"]).toEqual(["version-control-and-git"]);
  });

  it("defaults a course's prerequisites to an empty array when the field is absent", () => {
    const contentMap = new Map<string, ContentMeta>([
      ["en:learn/courses/just-enough-python", meta({ slug: "learn/courses/just-enough-python" })],
    ]);

    const { prerequisitesByCourse } = buildCourseLibrary(contentMap, "en");

    expect(prerequisitesByCourse["just-enough-python"]).toEqual([]);
  });
});
