/**
 * Step definitions for the LMS backend's HTTP-observable features.
 *
 * Covers: specs/apps/ose/lms-be/behaviours/health/health.feature
 *         specs/apps/ose/lms-be/behaviours/hello/hello.feature
 *         specs/apps/ose/lms-be/behaviours/health/actuator.feature
 *
 * These are the same four step expressions the Unit adapter binds in
 * apps/ose-lms-be/src/test/java/com/oseplatform/lms/steps/HttpSteps.java. The Unit adapter proves
 * them against MockMvc; this adapter proves them against a really-started process over real HTTP,
 * which is what makes the Actuator exposure scenario meaningful — a 404 from a MOCK servlet
 * environment and a 404 from a running Tomcat are different claims.
 */
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { setResponse, getResponse, clearResponse } from "../utils/response-store";
import { ensureBackendStarted } from "./backend-process";

const { Given, When, Then, Before } = createBdd();

Before(() => {
  clearResponse();
});

Given("the ose-lms-be service is running", async ({ request }) => {
  await ensureBackendStarted();
  const readinessResponse = await request.get("/api/v1/health");
  expect(readinessResponse.status()).toBe(200);
});

// `{word}` matches the Java binding's parameter type, so one expression serves every path the
// features exercise: /api/v1/health, /api/v1/hello, /actuator/health, and /actuator/env.
When("I send GET {word}", async ({ request }, path: string) => {
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
