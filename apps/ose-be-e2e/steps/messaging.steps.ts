/**
 * Step definitions for the OSE Application BE messaging feature.
 *
 * Covers: specs/apps/ose/be/behaviors/messaging/
 */
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { clearResponse } from "../utils/response-store";

const { Given, When, Then, Before } = createBdd();

Before(() => {
  clearResponse();
});

Given("OSE_BE_NATS_URL points to a running NATS server with JetStream enabled", async () => {
  // No-op: compose brings up NATS; host-running backend connects at startup
});

Given("ose-be has a JetStream durable stream and consumer for its demo subject", async () => {
  // No-op: backend runs the JetStream demo at startup
});

When("ose-be starts up", async () => {
  // The health endpoint confirms startup; no-op here
});

When("ose-be publishes a demo message to that subject", async () => {
  // Demo runs at startup; just read the status endpoint in Then steps
});

Then("the NATS connection is established", async ({ request }) => {
  // If the backend is healthy, NATS connected (backend fails fast on missing NATS)
  const resp = await request.get("/api/v1/health");
  expect(resp.ok()).toBeTruthy();
});

// @covers specs/apps/ose/be/behaviors/messaging/live/nats-connect.feature:ose-be connects to its NATS server at startup
Then("the backend reports healthy after connecting", async ({ request }) => {
  const resp = await request.get("/api/v1/health");
  expect(resp.ok()).toBeTruthy();
});

Then("the durable consumer receives the message", async ({ request }) => {
  const resp = await request.get("/api/v1/system/status/messaging");
  expect(resp.ok()).toBeTruthy();
});

Then("the message is acknowledged", async ({ request }) => {
  const resp = await request.get("/api/v1/system/status/messaging");
  const body = (await resp.json()) as Record<string, string>;
  expect(body["jetstream_demo"]).not.toBe("pending");
});

// @covers specs/apps/ose/be/behaviors/messaging/live/jetstream-demo.feature:ose-be publishes and durably consumes its demo subject with ack
Then("the messaging status surface reports the demo delivered and acked", async ({ request }) => {
  const resp = await request.get("/api/v1/system/status/messaging");
  const body = (await resp.json()) as Record<string, string>;
  expect(body["jetstream_demo"]).toBe("delivered_and_acked");
});

// ── @unit step stubs ───────────────────────────────────────────────────────
// These steps appear in @unit Gherkin scenarios whose assertions are executed
// by F# xUnit unit tests (dotnet test), not by this Playwright e2e runner.
// The stubs satisfy the spec-coverage tool; the scenarios themselves are
// excluded from the e2e run via the `tags: "not @unit"` filter in playwright.config.ts.

Given("OSE_BE_NATS_URL is unset", async () => {
  // @unit only — covered by F# xUnit unit tests; no-op in e2e runner
});

When("ose-be reads its messaging configuration", async () => {
  // @unit only — covered by F# xUnit unit tests; no-op in e2e runner
});

Then("startup aborts with a clear missing-variable error", async () => {
  // @unit only — covered by F# xUnit unit tests; no-op in e2e runner
});
