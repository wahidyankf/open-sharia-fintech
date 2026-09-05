import path from "node:path";
import { defineConfig } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

// Pin the tier deterministically for e2e runs — leaving APP_ENV unset would fall back to
// "local" per the loader contract in plans/in-progress/restrict-env-access-to-prod-and-stag,
// which would read a developer's real .env.local instead of test fixtures.
process.env.APP_ENV ??= "test";

const workspaceRoot = path.resolve(__dirname, "../..");
const externalBaseUrl = process.env.WEB_BASE_URL ?? process.env.BASE_URL;
const localBaseUrl = "http://localhost:3190";

const testDir = defineBddConfig({
  featuresRoot: workspaceRoot,
  features: path.join(workspaceRoot, "specs/apps/ose/www/behaviours/backend/**/*.feature"),
  steps: "./src/steps/**/*.steps.ts",
  tags: "not @e2e-exempt",
});

export default defineConfig({
  testDir,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [["list"], ["html"], ["junit", { outputFile: "test-results/junit.xml" }]],
  use: {
    baseURL: externalBaseUrl ?? localBaseUrl,
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  webServer: externalBaseUrl
    ? undefined
    : {
        command:
          "cp -r apps/ose-www/.next/static apps/ose-www/.next/standalone/apps/ose-www/.next/ && cp -r apps/ose-www/public apps/ose-www/.next/standalone/apps/ose-www/ && node apps/ose-www/.next/standalone/apps/ose-www/server.js",
        url: localBaseUrl,
        reuseExistingServer: true,
        timeout: 120000,
        cwd: workspaceRoot,
        env: {
          PORT: "3190",
          NODE_ENV: "production",
          OSE_WEB_CONTENT_DIR: path.join(workspaceRoot, "apps/ose-www/tests/e2e-fixtures/content"),
          OSE_WEB_SEARCH_DATA_PATH: path.join(workspaceRoot, "apps/ose-www/tests/e2e-fixtures/search-data.json"),
          OSE_WEB_SHOW_DRAFTS: "false",
        },
      },
});
