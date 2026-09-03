import path from "node:path";
import { defineConfig, devices } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

// Pin the tier deterministically for e2e runs — leaving APP_ENV unset would fall back to
// "local" per the loader contract in plans/in-progress/restrict-env-access-to-prod-and-stag,
// which would read a developer's real .env.local instead of test fixtures.
process.env.APP_ENV ??= "test";

const workspaceRoot = path.resolve(__dirname, "../..");

const testDir = defineBddConfig({
  featuresRoot: workspaceRoot,
  features: [
    path.join(workspaceRoot, "specs/apps/ayokoding/www/behaviors/frontend/**/*.feature"),
    // The resizable-panel primitive's own Gherkin lives under libs/web-ui (see
    // specs/libs/web-ui/behaviors/README.md). Its drag/clamp/keyboard scenarios are bound a
    // second time here — real browser, real docs page — alongside their existing web-ui
    // unit-level binding (resizable-panel.steps.tsx), matching this plan's "Gherkin (binds)"
    // dual-test-level convention rather than duplicating the scenario text under this app's
    // own gherkin/ tree.
    path.join(workspaceRoot, "specs/libs/web-ui/behaviors/resizable-panel/resizable-panel.feature"),
  ],
  steps: "./tests/e2e/steps/**/*.steps.ts",
  // Default is 'fail-on-gen': bddgen refuses to generate ANY test file while ANY scenario in
  // the globbed features lacks a matching step def. This app's Gherkin surface (many features,
  // most scenarios tagged plain @unit or @unit @e2e) has grown well past this project's own
  // e2e step-def coverage — ~104 preexisting scenarios across unrelated features (content
  // links, search, i18n, etc.) have no e2e implementation. 'skip-scenario' lets generation
  // succeed for every feature that IS covered, rendering the rest as `test.fixme` (visibly
  // pending, not silently passing) instead of hard-blocking the whole suite.
  //
  // `tags` (a Cucumber tag expression scoping which scenarios get GENERATED at all) was
  // considered as a narrower alternative — e.g. `tags: "@e2e"` + `missingSteps: "fail-on-gen"`,
  // keeping the hard-fail guarantee for every scenario declaring e2e intent while excluding
  // plain-`@unit` scenarios (42 repo-wide, confirmed via
  // `grep -rhoE "^\s*@unit\s*$" specs/apps/ayokoding/www/behaviors/frontend/ | wc -l`)
  // that were never meant to run at e2e level. It does not solve this project's actual blocker:
  // every one of the ~104 gap scenarios is ALREADY tagged `@unit @e2e` (149 such scenarios exist
  // repo-wide; zero scenarios anywhere carry a literal `@unit-only` tag, despite earlier
  // phrasing in this comment implying one exists). A tag filter can only include/exclude
  // scenarios by their declared tags — it cannot
  // distinguish "declared e2e intent, not yet implemented" from "declared e2e intent,
  // implemented"; that distinction is exactly what `missingSteps` exists to handle. Excluding
  // the gap scenarios via tags instead would mean manually re-tagging ~104 scenarios across many
  // unrelated preexisting features — the same per-scenario bookkeeping `skip-scenario` already
  // does automatically via `test.fixme`, done by hand, and a far larger unrelated-scope change
  // than this plan's own resizable-sidebar work. `skip-scenario` is deliberately project-wide
  // because the gap it papers over is already project-wide; the follow-up
  // (`plans/ideas/ayokoding-www-e2e-coverage-gaps.md`) is to burn the ~104 scenarios down and
  // revert to `fail-on-gen`.
  missingSteps: "skip-scenario",
});

export default defineConfig({
  testDir,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  // Default (30s) is too tight for the handful of scenarios that fan out several
  // `page.request.get()` calls (with `getResilient`'s single-retry, and per-request timeouts up
  // to 30s) against the single local production server instance under full-suite parallel load —
  // see `src/support/resilient-request.ts`. It also has to accommodate the `expect.poll` calls in
  // `cost-of-living-calculator.steps.ts` (up to 60s each) that wait out a lagging React re-render
  // under the same contention. 150s gives that combined class of scenario room to retry without
  // hitting the test's own deadline first.
  timeout: 150000,
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
      // course-paths plan (Phase 3): points the standalone server's manifest loader
      // (`defaultManifestsDir()`, `AYOKODING_WEB_MANIFESTS_DIR`) at this app's own fixture manifest
      // set instead of the real, still-unpopulated `manifests/` directory — see
      // `apps/ayokoding-www-fe-e2e/fixtures/manifests/README.md`.
      AYOKODING_WEB_MANIFESTS_DIR: path.join(workspaceRoot, "apps/ayokoding-www-fe-e2e/fixtures/manifests"),
      // course-paths plan (Phase 3, PR-review fix): the `skills/e2e-fixture-{alpha,beta}` content
      // pages (`apps/ayokoding-www/content/en/learn/paths/skills/e2e-fixture-{alpha,beta}/`) are
      // authored `draft: true` so they never render on prod-ayokoding-www — this reader-level flag
      // (`content/shell/repository-fs.ts`) is what makes them visible to the e2e run that actually
      // needs their authored body content (skills-path-landing-body.feature).
      AYOKODING_WEB_SHOW_DRAFTS: "true",
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
