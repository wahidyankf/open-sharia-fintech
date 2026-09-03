/**
 * Placeholder step definitions for the organiclever-www FE E2E slot.
 *
 * organiclever-www is a pure marketing site with no backend API (no tRPC
 * route handlers). This project exists to satisfy the standardized
 * {app}-be-e2e + {app}-fe-e2e reusable workflow pair.
 *
 * The scenario below asserts the "no backend API" invariant with a real browser navigation: the
 * live app (started by this project's own `webServer`) is asked for a plausible API path, and the
 * response is confirmed to be Next.js's own 404 — there is no route handler answering it.
 *
 * Covers: specs/apps/organiclever/www/behaviors/backend/placeholder/placeholder.feature
 */
import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Given, When, Then } = createBdd();

let status: number | undefined;

Given("no backend API exists for organiclever-www", async () => {
  // No-op: organiclever-www is a static marketing site with no backend API.
});

When("organiclever-www is checked for a backend API surface", async ({ page }) => {
  const response = await page.goto("/api/health");
  status = response?.status();
});

// @covers specs/apps/organiclever/www/behaviors/backend/placeholder/placeholder.feature:no backend API scenarios exist for organiclever-www
Then("no backend API surface is found", async () => {
  expect(status).toBe(404);
});
