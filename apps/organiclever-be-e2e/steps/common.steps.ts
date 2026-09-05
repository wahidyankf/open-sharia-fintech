import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { getResponse, clearResponse } from "../utils/response-store";
import { ensureBackendStarted } from "./backend-process";

const { Given, Before, Then } = createBdd();

Before(() => {
  clearResponse();
});

Given("the API is running", async ({ request }) => {
  await ensureBackendStarted();
  const readinessResponse = await request.get("/api/v1/health");
  expect(readinessResponse.status()).toBe(200);
});

// oxlint-disable-next-line no-empty-pattern
Then("the response status code should be {int}", async ({}, code: number) => {
  const res = getResponse();
  expect(res.status()).toBe(code);
});
