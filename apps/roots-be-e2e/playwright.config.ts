import { defineConfig } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

// Pin the tier deterministically. Leaving APP_ENV unset falls back to "local" per the loader
// contract, which would read a developer's real .env.local instead of test fixtures.
process.env.APP_ENV ??= "test";

const testDir = defineBddConfig({
  featuresRoot: "../../specs/apps/roots/be/behaviours",
  features: "../../specs/apps/roots/be/behaviours/**/*.feature",
  steps: ["./steps/**/*.ts"],
  // The config scenarios each carry an @e2e-exempt tag with a written reason and a named
  // alternative proof: which source supplied the port is not observable through the service's
  // public HTTP boundary, only that it listens. The same tag is what
  // scripts/behaviour-coverage.mjs honours, so the filter here and the static coverage validator
  // read one declaration rather than two.
  tags: "not @e2e-exempt",
});

export default defineConfig({
  testDir,
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  // No retries, in CI or out. A test that only passes on the second attempt is a defect to fix at
  // its root cause, and a retry would hide it. This deliberately diverges from apps/ose-be-e2e.
  retries: 0,
  workers: 1,
  reporter: [["list"], ["html"], ["junit", { outputFile: "test-results/junit.xml" }]],
  use: {
    baseURL: process.env.API_BASE_URL || "http://localhost:8402",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
});
