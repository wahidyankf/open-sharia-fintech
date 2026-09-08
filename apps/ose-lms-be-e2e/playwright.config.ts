import { defineConfig } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

// Pin the tier deterministically for e2e runs, matching the ose-be-e2e sibling: leaving APP_ENV
// unset falls back to "local" per the loader contract, which would read a developer's real
// .env.local instead of test fixtures.
process.env.APP_ENV ??= "test";

// The three port-resolution scenarios are @e2e-exempt: they assert how the port is chosen before
// the process binds one, which a black-box HTTP client cannot observe. They are proven in the
// Unit adapter, which carries no exemption at all.
const testDir = defineBddConfig({
  featuresRoot: "../../specs/apps/ose/lms-be/behaviours",
  features: "../../specs/apps/ose/lms-be/behaviours/**/*.feature",
  steps: ["./steps/**/*.ts"],
  tags: "not @e2e-exempt",
});

export default defineConfig({
  testDir,
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: 1,
  reporter: [["list"], ["html"], ["junit", { outputFile: "test-results/junit.xml" }]],
  use: {
    baseURL: process.env.LMS_API_BASE_URL || "http://127.0.0.1:8403",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
});
