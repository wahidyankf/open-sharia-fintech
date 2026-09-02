import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: ".",
  testMatch: "**/*.visual.spec.ts",
  snapshotDir: "./screenshots",
  snapshotPathTemplate: "{snapshotDir}/{testFilePath}/{arg}{ext}",
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
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.01,
    },
  },
  webServer: {
    command: "npx storybook dev -p 6006 --no-open --ci",
    port: 6006,
    reuseExistingServer: true,
    cwd: "../..",
  },
});
