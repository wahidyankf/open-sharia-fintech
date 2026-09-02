import { defineConfig, devices } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

// Pin the tier deterministically for e2e runs — leaving APP_ENV unset would fall back to
// "local" per the loader contract in plans/in-progress/restrict-env-access-to-prod-and-stag,
// which would read a developer's real .env.local instead of test fixtures.
process.env.APP_ENV ??= "test";

const testDir = defineBddConfig({
  featuresRoot: "../../specs/apps/organiclever/app-web/behaviors",
  features: "../../specs/apps/organiclever/app-web/behaviors/**/*.feature",
  steps: ["./steps/**/*.steps.ts"],
  // Default is 'fail-on-gen': bddgen refuses to generate ANY test file while ANY scenario in
  // the globbed features lacks a matching step def. env-loader.feature's scenarios are @unit-only
  // (covered by this app's own unit test, not e2e-relevant — a Node-process env-loading concern
  // with no browser equivalent). 'skip-scenario' lets generation succeed and renders those
  // scenarios as `test.fixme` instead of hard-blocking the whole suite.
  //
  // `tags: "not @unit"` was tried and reverted: this app's Gherkin surface tags many already-
  // IMPLEMENTED e2e scenarios `@unit @e2e` (13 files — journal/home-screen.feature,
  // settings/dark-mode.feature, and others), not just env-loader's plain-`@unit` ones. A tag
  // filter excludes by tag regardless of co-tags, so `not @unit` silently drops those real,
  // already-bound scenarios from generation too — confirmed via `specs:e2e:coverage`, which flags
  // them as newly unbound. `missingSteps: "skip-scenario"` stays glob-wide here for the same
  // reason ayokoding-www-fe-e2e keeps it (see that config's comment): the gap population is not
  // cleanly separable by tag.
  missingSteps: "skip-scenario",
});

// When the staging URL sits behind Vercel Deployment Protection, the workflow
// supplies a Protection Bypass for Automation token via this env var. Playwright
// then sends `x-vercel-protection-bypass` on every request so navigations land
// on the actual app instead of the Vercel SSO auth wall. Local dev (no Vercel)
// leaves the var unset and the headers map stays empty.
const vercelBypass = process.env.VERCEL_AUTOMATION_BYPASS_SECRET;
const extraHTTPHeaders: Record<string, string> = vercelBypass
  ? {
      "x-vercel-protection-bypass": vercelBypass,
      "x-vercel-set-bypass-cookie": "true",
    }
  : {};

// Optional grep filter via env var. Used by the staging E2E workflow to skip
// scenarios tagged `@local-fullstack` (which need a real backend). Local dev
// runs every scenario by default.
const grepInvert = process.env.PLAYWRIGHT_GREP_INVERT ? new RegExp(process.env.PLAYWRIGHT_GREP_INVERT) : undefined;

export default defineConfig({
  testDir,
  timeout: 60000,
  // Tests run sequentially to avoid auth state conflicts across scenarios.
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: process.env.CI ? [["list"], ["html"]] : "list",
  grepInvert,
  use: {
    baseURL: process.env.WEB_BASE_URL || "http://localhost:3202",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    extraHTTPHeaders,
  },
  // Only start a local server for local dev. When WEB_BASE_URL is set the suite
  // targets an already-running server — the remote Vercel Preview (staging gate)
  // or the docker-compose frontend (local-CI) — so no local server is started.
  webServer: process.env.WEB_BASE_URL
    ? undefined
    : {
        command:
          "cp -r apps/organiclever-app-web/.next/static apps/organiclever-app-web/.next/standalone/apps/organiclever-app-web/.next/ && cp -r apps/organiclever-app-web/public apps/organiclever-app-web/.next/standalone/apps/organiclever-app-web/ && node apps/organiclever-app-web/.next/standalone/apps/organiclever-app-web/server.js",
        url: "http://localhost:3202",
        reuseExistingServer: !process.env.CI,
        timeout: 120000,
        cwd: "../..",
        env: {
          PORT: "3202",
          NODE_ENV: "production",
        },
      },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
