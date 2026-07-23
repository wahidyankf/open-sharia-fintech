import { describe, expect, it } from "vitest";
import { readdirSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import matter from "gray-matter";

// This suite reads the real, checked-in course content directory rather than a
// fixture — the 37 re-homed course bundles ARE the subject under test (their
// frontmatter), mirroring how `generate-indexes`/`validate-indexes` operate
// directly against `apps/ayokoding-www/content`.
const COURSES_DIR = resolve(__dirname, "../../../../content/en/learn/courses");

function courseSlugs(): string[] {
  return readdirSync(COURSES_DIR, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
}

function readPrerequisites(slug: string): unknown {
  const raw = readFileSync(resolve(COURSES_DIR, slug, "_index.md"), "utf-8");
  return matter(raw).data.prerequisites;
}

describe("course prerequisites frontmatter", () => {
  const slugs = courseSlugs();

  it("finds the 37 re-homed course directories", () => {
    expect(slugs.length).toBe(37);
  });

  it("every course directory's _index.md declares a prerequisites array", () => {
    const missing = slugs.filter((slug) => !Array.isArray(readPrerequisites(slug)));
    expect(missing, `courses missing a prerequisites array: ${missing.join(", ")}`).toEqual([]);
  });

  it("every named prerequisite resolves to another course directory in the library", () => {
    const slugSet = new Set(slugs);
    const unresolved: string[] = [];
    for (const slug of slugs) {
      const prereqs = readPrerequisites(slug) as string[];
      for (const prereq of prereqs) {
        if (!slugSet.has(prereq)) unresolved.push(`${slug} -> ${prereq}`);
      }
    }
    expect(unresolved, `unresolved prerequisites: ${unresolved.join(", ")}`).toEqual([]);
  });

  it("no course declares itself as its own prerequisite", () => {
    const selfRefs = slugs.filter((slug) => (readPrerequisites(slug) as string[]).includes(slug));
    expect(selfRefs, `self-referencing courses: ${selfRefs.join(", ")}`).toEqual([]);
  });

  it("an empty prerequisites list is valid for a course with no library prerequisite", () => {
    // At least one entry-point course (no library prerequisite) is expected in a
    // 37-course library built from a linear-ordered legacy curriculum.
    const entryPoints = slugs.filter((slug) => (readPrerequisites(slug) as string[]).length === 0);
    expect(entryPoints.length).toBeGreaterThan(0);
  });

  it("the declared prerequisite edges form an acyclic graph (data-shape guard, not the full DAG resolver)", () => {
    const edges = new Map<string, string[]>(slugs.map((slug) => [slug, readPrerequisites(slug) as string[]]));

    const visiting = new Set<string>();
    const visited = new Set<string>();
    let cyclePath: string[] = [];

    function hasCycle(node: string, path: string[]): boolean {
      if (visited.has(node)) return false;
      if (visiting.has(node)) {
        cyclePath = [...path, node];
        return true;
      }
      visiting.add(node);
      for (const dep of edges.get(node) ?? []) {
        if (hasCycle(dep, [...path, node])) return true;
      }
      visiting.delete(node);
      visited.add(node);
      return false;
    }

    const cyclic = slugs.some((slug) => hasCycle(slug, []));
    expect(cyclic, `cycle detected: ${cyclePath.join(" -> ")}`).toBe(false);
  });
});
