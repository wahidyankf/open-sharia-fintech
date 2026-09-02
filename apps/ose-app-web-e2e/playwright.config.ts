import { defineConfig, devices } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

// Pin the tier deterministically for e2e runs — leaving APP_ENV unset would fall back to
// "local" per the loader contract in plans/in-progress/restrict-env-access-to-prod-and-stag,
// which would read a developer's real .env.local instead of test fixtures.
process.env.APP_ENV ??= "test";

const testDir = defineBddConfig({
  featuresRoot: "../../specs/apps/ose/app-web/behaviors",
  features: "../../specs/apps/ose/app-web/behaviors/**/*.feature",
  steps: ["./steps/**/*.steps.ts"],
  // env-loader.feature's scenarios are the only `@unit`-tagged ones anywhere in this app's
  // Gherkin surface (verified: no other feature co-tags `@unit` with `@e2e`), so excluding them
  // by tag — rather than the glob-wide `missingSteps: "skip-scenario"` — is safe and keeps
  // default 'fail-on-gen': bddgen still hard-fails generation if any non-`@unit` scenario lacks a
  // matching step def, instead of permanently weakening that safety net for every future scenario
  // in this app. Contrast with organiclever-www-fe-e2e/organiclever-app-web-e2e, where this same
  // tag filter was tried and reverted because those apps tag real, already-implemented e2e
  // scenarios `@unit @e2e` too.
  tags: "not @unit",
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

// CI supplies WEB_BASE_URL for an already-running staging or local-stack app.
// A developer running this E2E target directly gets the same deterministic
// server lifecycle from Playwright instead of needing a separate terminal.
const webServer = process.env.WEB_BASE_URL
  ? undefined
  : {
      command: "npx nx run ose-app-web:dev",
      url: "http://localhost:3300",
      reuseExistingServer: !process.env.CI,
      timeout: 120000,
      cwd: "../..",
      env: {
        APP_ENV: "test",
        OSE_APP_WEB_PORT: "3300",
      },
    };

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
    baseURL: process.env.WEB_BASE_URL || "http://localhost:3300",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    extraHTTPHeaders,
  },
  webServer,
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
