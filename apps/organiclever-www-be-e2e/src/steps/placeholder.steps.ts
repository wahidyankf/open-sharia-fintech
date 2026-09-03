/**
 * Placeholder step definitions for the organiclever-www BE E2E slot.
 *
 * organiclever-www is a pure marketing site with no backend API (no tRPC
 * route handlers). This project exists to satisfy the standardized
 * {app}-be-e2e + {app}-fe-e2e reusable workflow pair. The be-e2e slot is
 * tolerated-absent in CI (called with `|| true`) and holds no real scenarios.
 *
 * The scenario below asserts the "no backend API" invariant directly against organiclever-www's
 * real source tree: no Next.js App Router `route.ts`/`route.tsx` handler exists anywhere under
 * that app's own `src/app` directory. This is a filesystem check rather than a live HTTP probe so
 * it stays deterministic and fast without requiring the app server to be running.
 *
 * Covers: specs/apps/organiclever/www/behaviors/backend/placeholder/placeholder.feature
 */
import path from "node:path";
import { existsSync, readdirSync, statSync } from "node:fs";
import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Given, When, Then } = createBdd();

let routeHandlerFiles: string[] = [];

function findRouteHandlerFiles(dir: string): string[] {
  if (!existsSync(dir)) {
    return [];
  }

  const found: string[] = [];

  for (const entry of readdirSync(dir)) {
    const full = path.join(dir, entry);

    if (statSync(full).isDirectory()) {
      found.push(...findRouteHandlerFiles(full));
    } else if (/^route\.(ts|tsx|js)$/.test(entry)) {
      found.push(full);
    }
  }

  return found;
}

// Background step used by the placeholder scenario.
Given("no backend API exists for organiclever-www", async () => {
  // No-op: organiclever-www is a static marketing site with no backend API.
});

When("organiclever-www is checked for a backend API surface", async () => {
  routeHandlerFiles = findRouteHandlerFiles(path.resolve(__dirname, "../../../organiclever-www/src/app"));
});

// @covers specs/apps/organiclever/www/behaviors/backend/placeholder/placeholder.feature:no backend API scenarios exist for organiclever-www
Then("no backend API surface is found", async () => {
  expect(routeHandlerFiles).toHaveLength(0);
});
