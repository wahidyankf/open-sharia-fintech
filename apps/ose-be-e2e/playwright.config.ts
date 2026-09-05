import { defineConfig } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

// Pin the tier deterministically for e2e runs — leaving APP_ENV unset would fall back to
// "local" per the loader contract in plans/in-progress/restrict-env-access-to-prod-and-stag,
// which would read a developer's real .env.local instead of test fixtures.
process.env.APP_ENV ??= "test";

const testDir = defineBddConfig({
  featuresRoot: "../../specs/apps/ose/be/behaviours",
  features: "../../specs/apps/ose/be/behaviours/**/*.feature",
  steps: ["./steps/**/*.ts"],
  tags: "not @e2e-exempt",
});

export default defineConfig({
  testDir,
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: [["list"], ["html"], ["junit", { outputFile: "test-results/junit.xml" }]],
  use: {
    baseURL: process.env.API_BASE_URL || "http://localhost:8302",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
});
