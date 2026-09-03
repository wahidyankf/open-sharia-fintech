import { describe, expect, it } from "vitest";
import {
  courseRehomeRedirects,
  REHOMED_COURSE_SLUGS,
  RETIRED_FUNDAMENTALLY_STRONG_ROOTS,
} from "../../../src/redirects/course-rehome";

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

  it("no two rules share the same source (all 40 sources are unique)", () => {
    const sources = courseRehomeRedirects.map((rule) => rule.source);
    expect(new Set(sources).size).toBe(sources.length);
  });

  it("each per-course rule's source is the legacy fundamentally-strong path and its destination is the courses path, for the same slug, both wildcarded with :path*", () => {
    for (const rule of perCourseRules) {
      const match = rule.source.match(/^\/en\/learn\/fundamentally-strong\/software-engineer\/([a-z0-9-]+)\/:path\*$/);
      expect(match, `source not in expected shape: ${rule.source}`).not.toBeNull();
      const [, slug] = match as RegExpMatchArray;
      expect(rule.destination).toBe(`/en/learn/courses/${slug}/:path*`);
    }
  });

  // Maintainer decision (2026-07-23): broadened from an exact-source rule to :path* so the ~520
  // deep course sub-pages (learning/*, drilling/*) 308 instead of 404ing after the git mv — a
  // single wildcard rule covers both the bare course root (path resolves to an empty segment
  // list) and any deep sub-page, verified empirically against this Next.js version's existing
  // /en/learn/:path* rule (content-namespace.ts) which already 308s the bare /en/learn root.
  it("every per-course source ends with /:path* and its destination mirrors :path* for the same slug (deep-path coverage)", () => {
    for (const rule of perCourseRules) {
      expect(rule.source.endsWith("/:path*"), `source missing /:path* wildcard: ${rule.source}`).toBe(true);
      expect(rule.destination.endsWith("/:path*"), `destination missing /:path* wildcard: ${rule.destination}`).toBe(
        true,
      );
      const sourceSlug = rule.source.match(
        /^\/en\/learn\/fundamentally-strong\/software-engineer\/([a-z0-9-]+)\/:path\*$/,
      )?.[1];
      const destinationSlug = rule.destination.match(/^\/en\/learn\/courses\/([a-z0-9-]+)\/:path\*$/)?.[1];
      expect(sourceSlug, `could not extract slug from source: ${rule.source}`).toBeTruthy();
      expect(destinationSlug).toBe(sourceSlug);
    }
  });

  it("the per-course rule set's slug list equals the Phase-0 re-home inventory exactly (no extra, no missing)", () => {
    const actualSlugs = perCourseRules
      .map((rule) => rule.source.match(/\/([a-z0-9-]+)\/:path\*$/)?.[1])
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
