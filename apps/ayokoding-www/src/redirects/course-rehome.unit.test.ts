import { describe, expect, it } from "vitest";
import { courseRehomeRedirects, REHOMED_COURSE_SLUGS, RETIRED_FUNDAMENTALLY_STRONG_ROOTS } from "./course-rehome";

// Phase-0 re-home inventory (frozen at `evidence/phase-0-rehome-slugs.txt`), reproduced here so this
// suite never depends on a `plans/` path that gets archived to `plans/done/` once the plan closes.
const EXPECTED_SLUGS = [
  "advanced-algorithms",
  "advanced-networking",
  "advanced-sql-and-query-performance",
  "agentic-coding",
  "backend-essentials",
  "build-your-own-orm-and-query-builder",
  "capstone-first-working-software",
  "capstone-forge-ready",
  "capstone-full-stack-app",
  "capstone-solid-core",
  "computer-architecture",
  "computer-science-foundations",
  "concurrency-and-parallelism",
  "data-access-orms-and-query-builders",
  "data-structures-and-algorithms-essentials",
  "debugging-and-profiling",
  "engineering-management",
  "extending-neovim",
  "frontend-essentials",
  "functional-programming",
  "just-enough-bash",
  "just-enough-lua",
  "just-enough-nvim",
  "just-enough-python",
  "just-enough-typescript",
  "networking-essentials",
  "object-oriented-design-and-patterns",
  "object-oriented-programming-essentials",
  "programming-paradigms",
  "project-management",
  "security-essentials",
  "software-engineering-practices",
  "software-product-engineering",
  "software-testing",
  "sql-essentials",
  "technical-communication",
  "version-control-and-git",
].sort();

// Q-E=C override (RESOLVED 2026-07-23): the three retired fundamentally-strong browse roots
// don't match the per-course source shape (no trailing course slug), so they're excluded from
// the per-course assertions below and asserted on their own.
const perCourseRules = courseRehomeRedirects.filter(
  (rule) => !(RETIRED_FUNDAMENTALLY_STRONG_ROOTS as readonly string[]).includes(rule.source),
);
const qERootRules = courseRehomeRedirects.filter((rule) =>
  (RETIRED_FUNDAMENTALLY_STRONG_ROOTS as readonly string[]).includes(rule.source),
);

describe("courseRehomeRedirects", () => {
  it("declares exactly 40 rules: 37 per-course + 3 retired fundamentally-strong roots (Q-E=C)", () => {
    expect(courseRehomeRedirects.length).toBe(40);
    expect(perCourseRules.length).toBe(37);
    expect(qERootRules.length).toBe(3);
  });

  it("every rule is a permanent (308) redirect with non-empty source/destination", () => {
    for (const rule of courseRehomeRedirects) {
      expect(rule.permanent).toBe(true);
      expect(rule.source.length).toBeGreaterThan(0);
      expect(rule.destination.length).toBeGreaterThan(0);
    }
  });

  it("each per-course rule's source is the legacy fundamentally-strong path and its destination is the courses path, for the same slug", () => {
    for (const rule of perCourseRules) {
      const match = rule.source.match(/^\/en\/learn\/fundamentally-strong\/software-engineer\/([a-z0-9-]+)$/);
      expect(match, `source not in expected shape: ${rule.source}`).not.toBeNull();
      const [, slug] = match as RegExpMatchArray;
      expect(rule.destination).toBe(`/en/learn/courses/${slug}`);
    }
  });

  it("the per-course rule set's slug list equals the Phase-0 re-home inventory exactly (no extra, no missing)", () => {
    const actualSlugs = perCourseRules
      .map((rule) => rule.source.match(/\/([a-z0-9-]+)$/)?.[1])
      .filter((slug): slug is string => Boolean(slug))
      .sort();
    expect(actualSlugs).toEqual(EXPECTED_SLUGS);
  });

  it("REHOMED_COURSE_SLUGS is the single source of truth the per-course rule builder maps over", () => {
    expect([...REHOMED_COURSE_SLUGS].sort()).toEqual(EXPECTED_SLUGS);
    expect(perCourseRules.length).toBe(REHOMED_COURSE_SLUGS.length);
  });

  it("all three retired fundamentally-strong roots resolve to a 308 with destination /en/learn/courses (Q-E=C)", () => {
    expect([...RETIRED_FUNDAMENTALLY_STRONG_ROOTS].sort()).toEqual(
      [
        "/en/learn/fundamentally-strong",
        "/en/learn/fundamentally-strong/software-engineer",
        "/en/learn/fundamentally-strong/software-engineer/overview",
      ].sort(),
    );
    expect(qERootRules.length).toBe(RETIRED_FUNDAMENTALLY_STRONG_ROOTS.length);
    for (const rule of qERootRules) {
      expect(rule.permanent).toBe(true);
      expect(rule.destination).toBe("/en/learn/courses");
    }
  });
});
