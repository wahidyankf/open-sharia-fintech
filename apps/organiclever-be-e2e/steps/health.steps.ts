import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { setResponse, getResponse } from "../utils/response-store";

const { When, Then } = createBdd();

When(/^an operations engineer sends GET \/health$/, async ({ request }) => {
  setResponse(await request.get("/api/v1/health"));
});

When(/^an unauthenticated engineer sends GET \/health$/, async ({ request }) => {
  setResponse(await request.get("/api/v1/health"));
});

// @covers specs/apps/organiclever/be/behaviors/health/health-check.feature:Health endpoint reports the service as UP
// oxlint-disable-next-line no-empty-pattern
Then("the health status should be {string}", async ({}, status: string) => {
  const body = (await getResponse().json()) as Record<string, unknown>;
  expect(body["status"]).toBe(status);
});

// @covers specs/apps/organiclever/be/behaviors/health/health-check.feature:Anonymous health check does not expose component details
Then("the response should not include detailed component health information", async () => {
  const body = (await getResponse().json()) as Record<string, unknown>;
  expect(body["components"]).toBeUndefined();
});
