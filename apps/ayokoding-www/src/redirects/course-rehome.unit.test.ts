import { describe, expect, it } from "vitest";
import { courseRehomeRedirects, REHOMED_COURSE_SLUGS } from "./course-rehome";

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

describe("courseRehomeRedirects", () => {
  it("declares exactly 37 rules, one per Phase-0 re-home slug", () => {
    expect(courseRehomeRedirects.length).toBe(37);
  });

  it("every rule is a permanent (308) redirect with non-empty source/destination", () => {
    for (const rule of courseRehomeRedirects) {
      expect(rule.permanent).toBe(true);
      expect(rule.source.length).toBeGreaterThan(0);
      expect(rule.destination.length).toBeGreaterThan(0);
    }
  });

  it("each rule's source is the legacy fundamentally-strong path and its destination is the courses path, for the same slug", () => {
    for (const rule of courseRehomeRedirects) {
      const match = rule.source.match(/^\/en\/learn\/fundamentally-strong\/software-engineer\/([a-z0-9-]+)$/);
      expect(match, `source not in expected shape: ${rule.source}`).not.toBeNull();
      const [, slug] = match as RegExpMatchArray;
      expect(rule.destination).toBe(`/en/learn/courses/${slug}`);
    }
  });

  it("the rule set's slug list equals the Phase-0 re-home inventory exactly (no extra, no missing)", () => {
    const actualSlugs = courseRehomeRedirects
      .map((rule) => rule.source.match(/\/([a-z0-9-]+)$/)?.[1])
      .filter((slug): slug is string => Boolean(slug))
      .sort();
    expect(actualSlugs).toEqual(EXPECTED_SLUGS);
  });

  it("REHOMED_COURSE_SLUGS is the single source of truth the rule builder maps over", () => {
    expect([...REHOMED_COURSE_SLUGS].sort()).toEqual(EXPECTED_SLUGS);
    expect(courseRehomeRedirects.length).toBe(REHOMED_COURSE_SLUGS.length);
  });
});
