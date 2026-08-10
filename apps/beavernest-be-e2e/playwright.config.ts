import { defineConfig } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

const testDir = defineBddConfig({
  featuresRoot: "../../specs/apps/beavernest/behavior/beavernest-be/gherkin",
  features: "../../specs/apps/beavernest/behavior/beavernest-be/gherkin/**/*.feature",
  steps: ["./steps/**/*.ts"],
});

export default defineConfig({
  testDir,
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: [["list"], ["html"], ["junit", { outputFile: "test-results/junit.xml" }]],
  use: {
    baseURL: process.env.API_BASE_URL || "http://localhost:19320",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
});
