import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { assertBackendStopped, assertNatsReachable, readJson, readStatus, startBackend } from "./backend-process";
const { Given, When, Then } = createBdd();

let healthStatus = 0;
let messagingStatus = "";

async function captureStartupOutcome() {
  await startBackend();
  const body = await readJson("/api/v1/system/status/messaging");
  messagingStatus = String(body["jetstream_demo"] ?? "");
  healthStatus = await readStatus("/api/v1/health");
}

Given("ORGANICLEVER_BE_NATS_URL points to a running NATS server with JetStream enabled", async () => {
  await assertBackendStopped();
  await assertNatsReachable();
  messagingStatus = "not_started";
});

Given("NATS JetStream is running and organiclever-be is stopped", async () => {
  await assertBackendStopped();
  await assertNatsReachable();
  messagingStatus = "not_started";
});

When("organiclever-be starts up", async () => {
  await captureStartupOutcome();
});

When("organiclever-be publishes a demo message to that subject", async () => {
  await captureStartupOutcome();
});

Then("the NATS connection is established", async () => {
  expect(messagingStatus).toBe("delivered_and_acked");
});

Then("the backend reports healthy after connecting", async () => {
  expect(healthStatus).toBe(200);
});

Then("the durable consumer receives the message", async () => {
  expect(messagingStatus).toBe("delivered_and_acked");
});

Then("the message is acknowledged", async () => {
  expect(messagingStatus).toBe("delivered_and_acked");
});

Then("the messaging status surface reports the demo delivered and acked", async () => {
  expect(messagingStatus).toBe("delivered_and_acked");
});
