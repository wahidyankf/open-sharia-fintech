import path from "node:path";
import { defineConfig, devices } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

const workspaceRoot = path.resolve(__dirname, "../../../..");
const bddTestDir = defineBddConfig({
  featuresRoot: workspaceRoot,
  features: path.join(workspaceRoot, "specs/libs/web-ui/behaviours/**/*.feature"),
  steps: "./steps/**/*.steps.ts",
  tags: "not @e2e-exempt",
});

export default defineConfig({
  testDir: ".",
  snapshotDir: "./screenshots/components.visual.spec.ts",
  snapshotPathTemplate: "{snapshotDir}/{arg}{ext}",
  fullyParallel: false,
  workers: 1,
  forbidOnly: !!process.env.CI,
  reporter: "list",
  use: {
    baseURL: "http://localhost:6006",
    // Stock Chromium's glyph anti-aliasing/hinting is not bit-identical between separate process
    // launches, which drifted a handful of text-heavy screenshots ~1% between runs even with
    // identical content — `font-render-hinting=none` makes glyph rasterization reproducible.
    launchOptions: {
      args: ["--font-render-hinting=none", "--disable-lcd-text", "--force-color-profile=srgb"],
    },
  },
  expect: {
    toMatchSnapshot: {
      maxDiffPixelRatio: 0.02,
    },
    toHaveScreenshot: {
      // Full-page Storybook captures include glyph anti-aliasing from the browser process. Keep a
      // narrow 2% raster tolerance so text hinting cannot fail an otherwise identical component,
      // while layout, colour, spacing, and missing-element regressions still exceed the budget.
      maxDiffPixelRatio: 0.02,
    },
  },
  webServer: {
    command: "npx storybook dev -p 6006 --no-open --ci",
    port: 6006,
    reuseExistingServer: true,
    cwd: "../..",
  },
  projects: [
    {
      name: "gherkin",
      testDir: bddTestDir,
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "visual-regression",
      testDir: ".",
      testMatch: "**/*.visual.spec.ts",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
