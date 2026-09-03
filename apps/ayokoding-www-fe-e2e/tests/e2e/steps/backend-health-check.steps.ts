import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { buildTrpcUrl, extractTrpcData, backendState } from "./backend-helpers";

const { When, Then } = createBdd();

// Note: Given "the API is running" is in backend-common.steps.ts

When("the client calls meta.health", async ({ request }) => {
  const url = buildTrpcUrl("meta.health", undefined);
  const response = await request.get(url);
  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  backendState.healthResult = extractTrpcData(body);
});

// @covers specs/apps/ayokoding/www/behaviors/backend/health/health-check.feature:meta.health returns status ok
Then('the response should contain "status" equal to "ok"', async () => {
  expect(backendState.healthResult).toMatchObject({ status: "ok" });
});

When("the client calls meta.languages", async ({ request }) => {
  const url = buildTrpcUrl("meta.languages", undefined);
  const response = await request.get(url);
  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  backendState.languagesResult = extractTrpcData(body);
});

Then('the response should contain a non-null "languages" array', async () => {
  expect(backendState.languagesResult).not.toBeNull();
  expect(Array.isArray(backendState.languagesResult)).toBe(true);
});

Then('the "languages" array should include "en"', async () => {
  const languages = backendState.languagesResult as { code: string }[];
  expect(languages.some((l) => l.code === "en")).toBe(true);
});

// @covers specs/apps/ayokoding/www/behaviors/backend/health/health-check.feature:meta.languages returns the list of available locales
Then('the "languages" array should include "id"', async () => {
  const languages = backendState.languagesResult as { code: string }[];
  expect(languages.some((l) => l.code === "id")).toBe(true);
});
