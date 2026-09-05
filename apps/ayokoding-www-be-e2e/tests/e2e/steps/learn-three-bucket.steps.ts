import fs from "node:fs";
import path from "node:path";
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";

const { Given, When, Then } = createBdd();
const workspaceRoot = path.resolve(process.cwd(), "../..");

// Shared Background step for this project's own added glob entry (learn-three-bucket.feature) —
// distinct from "the API is running" (common.steps.ts), which is this project's real background
// for every backend/**/*.feature scenario.
Given("the app is running", async ({ request }) => {
  const response = await request.get("/");
  expect(response.status(), "the public app root must be reachable before the scenario runs").toBeLessThan(400);
});

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

When("a visitor navigates to {string}", async ({ page }, url: string) => {
  const response = await page.goto(url, { waitUntil: "domcontentloaded" });
  expect(response, `navigation to ${url} returned no response`).not.toBeNull();
});

Then("the current URL should contain {string}", async ({ page }, expectedPath: string) => {
  expect(new URL(page.url()).pathname).toContain(expectedPath);
});

Then("the current URL should not contain {string}", async ({ page }, fragment: string) => {
  expect(new URL(page.url()).pathname).not.toContain(fragment);
});

Then("the response status should not be a client or server error", async ({ page }) => {
  const response = await page.request.get(page.url());
  expect(response.status(), `${page.url()} responded ${response.status()}`).toBeLessThan(400);
});

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
