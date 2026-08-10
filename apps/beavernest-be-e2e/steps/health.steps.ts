/**
 * Step definitions for the beavernest-be health endpoint feature, plus the
 * shared Given/When/Then steps reused by the greeting and 404-fallback
 * scenarios in ../steps/greeting.steps.ts.
 *
 * Covers: specs/apps/beavernest/behavior/beavernest-be/gherkin/health/service-health.feature
 */
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { setResponse, getResponse, clearResponse } from "../utils/response-store";

const { Given, When, Then, Before } = createBdd();

Before(() => {
  clearResponse();
});

Given("the service has finished starting", async () => {
  // No-op: same assumption as above.
});

When("I send a GET request to {string}", async ({ request }, path: string) => {
  setResponse(await request.get(path));
});

// @covers specs/apps/beavernest/behavior/beavernest-be/gherkin/health/service-health.feature:The service reports liveness
// oxlint-disable-next-line no-empty-pattern
Then("the response status is {int}", async ({}, expectedStatus: number) => {
  expect(getResponse().status()).toBe(expectedStatus);
});

// oxlint-disable-next-line no-empty-pattern
Then("the response body field {string} is a non-empty string", async ({}, field: string) => {
  const body = (await getResponse().json()) as Record<string, unknown>;
  const value = body[field];
  expect(typeof value).toBe("string");
  expect((value as string).length).toBeGreaterThan(0);
});
