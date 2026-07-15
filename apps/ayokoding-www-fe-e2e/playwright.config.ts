import path from "node:path";
import { defineConfig, devices } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

const workspaceRoot = path.resolve(__dirname, "../..");

const testDir = defineBddConfig({
  featuresRoot: workspaceRoot,
  features: [
    path.join(workspaceRoot, "specs/apps/ayokoding/behavior/ayokoding-www/gherkin/**/*.feature"),
    // The resizable-panel primitive's own Gherkin lives under libs/web-ui (see
    // specs/libs/web-ui/behavior/README.md). Its drag/clamp/keyboard scenarios are bound a
    // second time here — real browser, real docs page — alongside their existing web-ui
    // unit-level binding (resizable-panel.steps.tsx), matching this plan's "Gherkin (binds)"
    // dual-test-level convention rather than duplicating the scenario text under this app's
    // own gherkin/ tree.
    path.join(workspaceRoot, "specs/libs/web-ui/behavior/gherkin/resizable-panel/resizable-panel.feature"),
  ],
  steps: "./src/steps/**/*.steps.ts",
  // Default is 'fail-on-gen': bddgen refuses to generate ANY test file while ANY scenario in
  // the globbed features lacks a matching step def. This app's Gherkin surface (many features,
  // most scenarios tagged @unit-only or @unit @e2e) has grown well past this project's own
  // e2e step-def coverage — dozens of preexisting scenarios across unrelated features (content
  // links, search, i18n, etc.) have no e2e implementation. 'skip-scenario' lets generation
  // succeed for every feature that IS covered, rendering the rest as `test.fixme` (visibly
  // pending, not silently passing) instead of hard-blocking the whole suite.
  missingSteps: "skip-scenario",
});

export default defineConfig({
  testDir,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [["list"], ["html"], ["junit", { outputFile: "test-results/junit.xml" }]],
  use: {
    baseURL: process.env.BASE_URL || "http://localhost:3101",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  webServer: {
    command:
      "cp -r apps/ayokoding-www/.next/static apps/ayokoding-www/.next/standalone/apps/ayokoding-www/.next/ && cp -r apps/ayokoding-www/public apps/ayokoding-www/.next/standalone/apps/ayokoding-www/ && node apps/ayokoding-www/.next/standalone/apps/ayokoding-www/server.js",
    url: "http://localhost:3101",
    reuseExistingServer: true,
    timeout: 120000,
    cwd: workspaceRoot,
    env: {
      PORT: "3101",
      NODE_ENV: "production",
    },
  },
  projects: process.env.CI
    ? [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }]
    : [
        { name: "chromium", use: { ...devices["Desktop Chrome"] } },
        { name: "firefox", use: { ...devices["Desktop Firefox"] } },
        { name: "webkit", use: { ...devices["Desktop Safari"] } },
      ],
});
