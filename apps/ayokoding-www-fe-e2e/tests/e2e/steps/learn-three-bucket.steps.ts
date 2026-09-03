import fs from "node:fs";
import path from "node:path";
import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";
import { getResilient } from "../support/resilient-request";

const { When, Then } = createBdd();
const workspaceRoot = path.resolve(process.cwd(), "../..");

// The former subject-domain directories DD-41's relocation moved under legacy/ (matches the
// redirect Examples tables elsewhere in this same feature file).
const formerSubjectDomains = [
  "software-engineering",
  "artificial-intelligence",
  "information-security",
  "personal-development",
  "it-governance",
  "business",
];

let structuralBuckets: string[] = [];

// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/learn-three-bucket.feature:The learn section exposes exactly three structural buckets
When("the content tree under the en learn section is inspected", async () => {
  // A real filesystem read of the build-time content tree (DD-40/DD-45's own invariant), the same
  // workspaceRoot-relative `fs.readdirSync` convention this project's own
  // skills-path-composition.steps.ts already establishes for structural/build-time content-tree
  // assertions — no live browser navigation exposes this specific invariant anywhere on the site,
  // so a direct filesystem read (this test file runs as a plain Node process, per
  // Playwright's own model) is the genuine check, mirroring the identical binding at
  // ayokoding-www-be-e2e's integration level.
  const learnDir = path.join(workspaceRoot, "apps/ayokoding-www/content/en/learn");
  structuralBuckets = fs
    .readdirSync(learnDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
});

Then("its only structural buckets are paths, courses, and legacy", async () => {
  expect(structuralBuckets).toEqual(["courses", "legacy", "paths"]);
});

Then("no former subject domain remains as a direct child of the learn section", async () => {
  for (const domain of formerSubjectDomains) {
    expect(structuralBuckets).not.toContain(domain);
  }
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/learn-three-bucket.feature:A relocated legacy domain URL redirects to its legacy address in one hop
// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/learn-three-bucket.feature:A stale /c-bookmarked legacy domain URL redirects to its legacy address in two hops
// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/learn-three-bucket.feature:A historical learn-reorg source chains through to its legacy address
// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/learn-three-bucket.feature:A deep legacy path keeps its sub-taxonomy verbatim
Then("the response status should not be a client or server error", async ({ page }) => {
  // Re-fetch whatever URL the browser landed on after following every redirect hop, so this
  // check is independent of how many hops the prior "a visitor navigates to" step's own
  // page.goto() Response object already discarded.
  const response = await getResilient(page, page.url());
  expect(response.status(), `${page.url()} responded ${response.status()}`).toBeLessThan(400);
});
