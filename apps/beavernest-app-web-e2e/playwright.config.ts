import { defineConfig, devices } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

const testDir = defineBddConfig({
  featuresRoot: "../../specs/apps/beavernest/behavior/beavernest-app-web/gherkin",
  features: "../../specs/apps/beavernest/behavior/beavernest-app-web/gherkin/**/*.feature",
  steps: ["./steps/**/*.steps.ts"],
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
