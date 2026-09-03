import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { buildTrpcUrl, extractTrpcData, backendState } from "./backend-helpers";

const { When, Then } = createBdd();

When("the health endpoint is called", async ({ request }) => {
  const url = buildTrpcUrl("health.check", undefined);
  const response = await request.get(url);
  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  backendState.healthResult = extractTrpcData(body);
});

// @covers specs/apps/ose/www/behaviors/backend/health/health.feature:Health endpoint returns ok status
Then("the response contains status {string}", async ({}, expectedStatus: string) => {
  expect(backendState.healthResult).toMatchObject({ status: expectedStatus });
});
