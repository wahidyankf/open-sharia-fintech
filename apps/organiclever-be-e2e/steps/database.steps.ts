import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { assertBackendStopped, readJson, readStatus, resetDatabaseToPending, startBackend } from "./backend-process";

const { Given, When, Then } = createBdd();

let pendingBeforeStartup = false;

Given("a fresh test database has pending organiclever-be migrations", async () => {
  await assertBackendStopped();
  resetDatabaseToPending();
  pendingBeforeStartup = true;
});

When("organiclever-be starts against that database", async () => {
  await startBackend();
});

Then("organiclever-be reaches its public health endpoint after applying migrations", async () => {
  expect(pendingBeforeStartup).toBe(true);
  expect(await readJson("/api/v1/system/status/database")).toEqual({ migration_state: "applied" });
  expect(await readStatus("/api/v1/health")).toBe(200);
});
