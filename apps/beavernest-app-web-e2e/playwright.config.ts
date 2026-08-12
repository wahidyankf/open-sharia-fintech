import { defineConfig, devices } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

// Pin the tier deterministically for e2e runs — leaving APP_ENV unset would fall back to
// "local" per the loader contract in plans/in-progress/restrict-env-access-to-prod-and-stag,
// which would read a developer's real .env.local instead of test fixtures.
process.env.APP_ENV ??= "test";

const testDir = defineBddConfig({
  featuresRoot: "../../specs/apps/beavernest/behavior/beavernest-app-web/gherkin",
  features: "../../specs/apps/beavernest/behavior/beavernest-app-web/gherkin/**/*.feature",
  steps: ["./steps/**/*.steps.ts"],
  // configuration/env-tier-loading.feature's scenarios are the only `@unit`-tagged ones anywhere
  // in this app's Gherkin surface (verified: no other feature co-tags `@unit` with `@e2e`), so
  // excluding them by tag — rather than the glob-wide `missingSteps: "skip-scenario"` — is safe
  // and keeps default 'fail-on-gen': bddgen still hard-fails generation if any non-`@unit`
  // scenario lacks a matching step def, instead of permanently weakening that safety net for
  // every future scenario in this app. Contrast with organiclever-www-fe-e2e/
  // organiclever-app-web-e2e/wahidyankf-www-fe-e2e, where this same tag filter was tried and
  // reverted because those apps tag real, already-implemented e2e scenarios `@unit @e2e` too.
  tags: "not @unit",
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
    baseURL: process.env.WEB_BASE_URL || "http://localhost:19310",
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
