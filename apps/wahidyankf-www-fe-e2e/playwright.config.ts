import { defineConfig, devices } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

// Pin the tier deterministically for e2e runs — leaving APP_ENV unset would fall back to
// "local" per the loader contract in plans/in-progress/restrict-env-access-to-prod-and-stag,
// which would read a developer's real .env.local instead of test fixtures.
process.env.APP_ENV ??= "test";

const testDir = defineBddConfig({
  featuresRoot: "../../specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin",
  steps: "./steps/**/*.ts",
  // env-loader.feature's scenarios are plain @unit (covered by this app's own unit test, not
  // e2e-relevant — a Node-process env-loading concern with no browser equivalent). Excluding them
  // by tag, rather than the glob-wide `missingSteps: "skip-scenario"`, keeps default
  // 'fail-on-gen' — bddgen still hard-fails generation if any non-@unit scenario in this app's
  // Gherkin surface lacks a matching step def, instead of permanently weakening that safety net
  // for every future scenario in this app.
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
