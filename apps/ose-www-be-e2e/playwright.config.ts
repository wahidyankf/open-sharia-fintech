import path from "node:path";
import { defineConfig } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

// Pin the tier deterministically for e2e runs — leaving APP_ENV unset would fall back to
// "local" per the loader contract in plans/in-progress/restrict-env-access-to-prod-and-stag,
// which would read a developer's real .env.local instead of test fixtures.
process.env.APP_ENV ??= "test";

const workspaceRoot = path.resolve(__dirname, "../..");

const testDir = defineBddConfig({
  featuresRoot: workspaceRoot,
  features: path.join(workspaceRoot, "specs/apps/ose/www/behaviors/backend/**/*.feature"),
  steps: "./src/steps/**/*.steps.ts",
});

export default defineConfig({
  testDir,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [["list"], ["html"], ["junit", { outputFile: "test-results/junit.xml" }]],
  use: {
    baseURL: process.env.BASE_URL || "http://localhost:3100",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  webServer: {
    command:
      "cp -r apps/ose-www/.next/static apps/ose-www/.next/standalone/apps/ose-www/.next/ && cp -r apps/ose-www/public apps/ose-www/.next/standalone/apps/ose-www/ && node apps/ose-www/.next/standalone/apps/ose-www/server.js",
    url: "http://localhost:3100",
    reuseExistingServer: true,
    timeout: 120000,
    cwd: workspaceRoot,
    env: {
      PORT: "3100",
      NODE_ENV: "production",
    },
  },
});
