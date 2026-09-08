/**
 * Step definitions for the islamic-be health endpoint feature.
 *
 * Covers: specs/apps/islamic/be/behaviours/health/health.feature
 */
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { setResponse, getResponse, clearResponse } from "../utils/response-store";
import { ensureBackendStarted } from "./backend-process";

const { Given, When, Then, Before } = createBdd();

Before(() => {
  clearResponse();
});

Given("the islamic-be service is running", async ({ request }) => {
  await ensureBackendStarted();
  const readinessResponse = await request.get("/api/v1/health");
  expect(readinessResponse.status()).toBe(200);
});

// One binding for both request paths the feature exercises. Splitting it per path would leave the
// unknown-route scenario with a step nothing else could reuse, and playwright-bdd requires exactly
// one binding per step anyway.
When(/^I send GET (\/api\/v1\/[a-z0-9-]+)$/, async ({ request }, path: string) => {
  setResponse(await request.get(path));
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

Then(
  "the response {string} header starts with {string}",
  // oxlint-disable-next-line no-empty-pattern
  async ({}, header: string, prefix: string) => {
    const headers = getResponse().headers();
    // Playwright lowercases header names; the feature names them as an operator would write them.
    // Absence collapses to "" so the missing-header case fails on its own assertion with a clear
    // message rather than on an undefined dereference inside the prefix check.
    const actual = headers[header.toLowerCase()] ?? "";
    expect(actual, `the response carries no ${header} header`).not.toBe("");
    expect(actual.startsWith(prefix), `${header} was "${actual}"`).toBe(true);
  },
);
