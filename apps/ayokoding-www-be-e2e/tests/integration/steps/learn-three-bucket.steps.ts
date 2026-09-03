import fs from "node:fs";
import path from "node:path";
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";

const { Given, When, Then } = createBdd();
const workspaceRoot = path.resolve(process.cwd(), "../..");

// Shared Background step for this project's own added glob entry (learn-three-bucket.feature) —
// distinct from "the API is running" (common.steps.ts), which is this project's real background
// for every backend/**/*.feature scenario.
Given("the app is running", async () => {});

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
  // A real filesystem read of the build-time content tree (DD-40/DD-45's own invariant), mirroring
  // ayokoding-www-fe-e2e's skills-path-composition.steps.ts convention for structural/build-time
  // assertions: this is a filesystem-backed invariant with no runtime API surface, so a direct
  // `fs.readdirSync` against the real content directory is the genuine check — not a live
  // navigation walk.
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
