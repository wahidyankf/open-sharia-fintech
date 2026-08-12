import { defineConfig, devices } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

// Pin the tier deterministically for e2e runs — leaving APP_ENV unset would fall back to
// "local" per the loader contract in plans/in-progress/restrict-env-access-to-prod-and-stag,
// which would read a developer's real .env.local instead of test fixtures.
process.env.APP_ENV ??= "test";

const testDir = defineBddConfig({
  featuresRoot: "../../specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin",
  steps: "./steps/**/*.ts",
  // Default is 'fail-on-gen': bddgen refuses to generate ANY test file while ANY scenario in
  // the globbed features lacks a matching step def. env-loader.feature's scenarios are @unit-only
  // (covered by this app's own unit test, not e2e-relevant — a Node-process env-loading concern
  // with no browser equivalent). 'skip-scenario' lets generation succeed and renders those
  // scenarios as `test.fixme` instead of hard-blocking the whole suite.
  //
  // `tags: "not @unit"` was tried and reverted: this app's Gherkin surface tags many already-
  // IMPLEMENTED e2e scenarios `@unit @e2e` (8 files — home.feature, cv.feature, search.feature,
  // and others), not just env-loader's plain-`@unit` ones. A tag filter excludes by tag
  // regardless of co-tags, so `not @unit` silently drops those real, already-bound scenarios from
  // generation too — confirmed via `specs:e2e:coverage`, which flags 31 of them as newly unbound.
  // `missingSteps: "skip-scenario"` stays glob-wide here for the same reason ayokoding-www-fe-e2e
  // keeps it (see that config's comment): the gap population is not cleanly separable by tag.
  missingSteps: "skip-scenario",
});

export default defineConfig({
  testDir,
  timeout: 60000,
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: process.env.CI ? [["list"], ["html"]] : "list",
  use: {
    baseURL: process.env.BASE_URL || "http://localhost:3201",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
