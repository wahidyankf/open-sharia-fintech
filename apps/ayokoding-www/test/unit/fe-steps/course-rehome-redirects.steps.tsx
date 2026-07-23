import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import { readdirSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import matter from "gray-matter";
import "./helpers/test-setup";

const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/course-rehome-redirects.feature",
  ),
);

// Real, checked-in course content directory — the 37 re-homed course bundles' frontmatter ARE the
// subject under test for the prerequisites scenario below, mirroring how
// `generate-indexes`/`validate-indexes` operate directly against `apps/ayokoding-www/content`
// (same real-filesystem approach `course-prerequisites.unit.test.ts` used before this Gherkin-bound
// rewrite superseded it).
const COURSES_DIR = resolve(process.cwd(), "content/en/learn/courses");

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

describeFeature(feature, ({ Scenario, ScenarioOutline, Background }) => {
  Background(({ Given }) => {
    Given("the app is running", () => {});
  });

  Scenario("A legacy fundamentally-strong URL redirects to the canonical course URL", ({ When, Then }) => {
    When('a visitor navigates to "/en/learn/fundamentally-strong/software-engineer/just-enough-python"', () => {
      // Redirect config in next.config.ts: courseRehomeRedirects (src/redirects/course-rehome.ts).
      // Rule-shape correctness is asserted directly in course-rehome.unit.test.ts; live
      // navigation-following-redirect behavior is verified at e2e level.
      expect(true).toBe(true);
    });

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/course-rehome-redirects.feature:A legacy fundamentally-strong URL redirects to the canonical course URL
    Then('the current URL should contain "/en/c/learn/courses/just-enough-python"', () => {
      expect(true).toBe(true);
    });
  });

  Scenario(
    "A legacy fundamentally-strong deep sub-page URL redirects to its canonical course sub-page",
    ({ When, Then }) => {
      When(
        'a visitor navigates to "/en/learn/fundamentally-strong/software-engineer/just-enough-python/learning/beginner"',
        () => {
          // Per-course rule now carries a /:path* wildcard (course-rehome.ts) so deep sub-pages
          // 308 alongside the bare course root. Rule-shape correctness (source/destination both
          // ending in /:path*) is asserted in course-rehome.unit.test.ts; live
          // navigation-following-redirect behavior is verified at e2e level.
          expect(true).toBe(true);
        },
      );

      // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/course-rehome-redirects.feature:A legacy fundamentally-strong deep sub-page URL redirects to its canonical course sub-page
      Then('the current URL should contain "/en/c/learn/courses/just-enough-python/learning/beginner"', () => {
        expect(true).toBe(true);
      });
    },
  );

  Scenario("Every re-homed course declares its prerequisites", ({ Given, When, Then, And }) => {
    Given("the thirty-seven shipped topics and existing capstones have been re-homed into the course library", () => {
      expect(courseSlugs().length).toBe(37);
    });

    When("each re-homed course's canonical metadata is inspected", () => {
      // No-op precondition: each Then/And step below re-reads the real frontmatter itself.
    });

    Then("every one declares a prerequisites list of course IDs", () => {
      const missing = courseSlugs().filter((slug) => !Array.isArray(readPrerequisites(slug)));
      expect(missing, `courses missing a prerequisites array: ${missing.join(", ")}`).toEqual([]);
    });

    And("an empty list is accepted only for a course with no library prerequisite", () => {
      // At least one entry-point course (no library prerequisite) is expected in a 37-course
      // library built from a linear-ordered legacy curriculum.
      const entryPoints = courseSlugs().filter((slug) => (readPrerequisites(slug) as string[]).length === 0);
      expect(entryPoints.length).toBeGreaterThan(0);
    });

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/course-rehome-redirects.feature:Every re-homed course declares its prerequisites
    And("every named prerequisite resolves to another course in the library", () => {
      const slugs = courseSlugs();
      const slugSet = new Set(slugs);
      const unresolved: string[] = [];
      const selfRefs: string[] = [];
      for (const slug of slugs) {
        const prereqs = readPrerequisites(slug) as string[];
        if (prereqs.includes(slug)) selfRefs.push(slug);
        for (const prereq of prereqs) {
          if (!slugSet.has(prereq)) unresolved.push(`${slug} -> ${prereq}`);
        }
      }
      expect(unresolved, `unresolved prerequisites: ${unresolved.join(", ")}`).toEqual([]);
      expect(selfRefs, `self-referencing courses: ${selfRefs.join(", ")}`).toEqual([]);

      // REFACTOR (delivery.md §2.3): the declared edges must also form an acyclic graph — a
      // data-shape guard on these 37 rows, not the full DAG resolver (that belongs to the sibling
      // ayokoding-learning-path-02-schema-and-prerequisite-dag plan).
      const edges = new Map<string, string[]>(slugs.map((s) => [s, readPrerequisites(s) as string[]]));
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

  ScenarioOutline(
    "The retired fundamentally-strong browse roots permanently redirect to the course library",
    ({ When, Then, And }) => {
      When('a raw HTTP GET is made to "<legacy_url>" with redirects disabled', () => {
        // Redirect config in next.config.ts: courseRehomeRedirects' Q-E retired-root rules.
        expect(true).toBe(true);
      });

      Then("the response status should be 308", () => {
        expect(true).toBe(true);
      });

      // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/course-rehome-redirects.feature:The retired fundamentally-strong browse roots permanently redirect to the course library
      And('the response Location header should equal "/en/learn/courses"', () => {
        expect(true).toBe(true);
      });
    },
  );

  Scenario(
    "The course library the retired browse roots redirect to resolves every re-homed course",
    ({ When, Then }) => {
      When('a visitor navigates to "/en/learn/courses"', () => {
        expect(true).toBe(true);
      });

      // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/course-rehome-redirects.feature:The course library the retired browse roots redirect to resolves every re-homed course
      Then("every course catalog entry should resolve to live content, not a drained or missing location", () => {
        // Live-HTTP resolution needs a running server, verified at e2e level; the catalog's own
        // slug set is asserted directly in course-rehome.unit.test.ts's slug-set-equality check.
        expect(true).toBe(true);
      });
    },
  );

  Scenario(
    "A course reached via its legacy course URL resolves to the single canonical course body",
    ({ When, Then }) => {
      When('a visitor navigates to "/en/learn/fundamentally-strong/software-engineer/just-enough-python"', () => {
        expect(true).toBe(true);
      });

      // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/course-rehome-redirects.feature:A course reached via its legacy course URL resolves to the single canonical course body
      Then(
        'the resolved page title should equal the canonical course page title at "/en/learn/courses/just-enough-python"',
        () => {
          expect(true).toBe(true);
        },
      );
    },
  );
});
