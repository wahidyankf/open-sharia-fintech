/**
 * Step definitions for the OSE Application BE health endpoint feature.
 *
 * Covers: specs/apps/ose/be/behaviours/health/health.feature
 */
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { setResponse, getResponse, clearResponse } from "../utils/response-store";
import { ensureBackendStarted } from "./backend-process";

const { Given, When, Then, Before } = createBdd();

Before(() => {
  clearResponse();
});

Given("the ose-be service is running", async ({ request }) => {
  await ensureBackendStarted();
  const readinessResponse = await request.get("/api/v1/health");
  expect(readinessResponse.status()).toBe(200);
});

When(/^I send GET \/api\/v1\/health$/, async ({ request }) => {
  setResponse(await request.get("/api/v1/health"));
});

// oxlint-disable-next-line no-empty-pattern
Then("the response status is {int}", async ({}, expectedStatus: number) => {
  expect(getResponse().status()).toBe(expectedStatus);
});

Then(
  "the response body has a {string} field equal to {string}",
  // oxlint-disable-next-line no-empty-pattern
  async ({}, field: string, value: string) => {
    const body = (await getResponse().json()) as Record<string, unknown>;
    expect(body[field]).toBe(value);
  },
);
