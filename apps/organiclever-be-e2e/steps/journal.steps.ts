/**
 * Step definitions for the OrganicLever BE journal CRUD feature.
 *
 * Covers: specs/apps/organiclever/be/behaviours/journal/journal-crud.feature
 *
 * All HTTP calls target POST/GET/PUT/DELETE /api/v1/journal/entries (and /{id}),
 * which are implemented by the F# Giraffe journal context.
 */
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { setResponse, getResponse, clearResponse } from "../utils/response-store";
import { ensureBackendStarted } from "./backend-process";

const { Given, When, Then, Before } = createBdd();

// Scenario-scoped state: holds the id of an entry created in a Given step.
let createdEntryId: string | null = null;

Before(() => {
  clearResponse();
  createdEntryId = null;
});

Given("the journal API is running", async ({ request }) => {
  await ensureBackendStarted();
  const readinessResponse = await request.get("/api/v1/health");
  expect(readinessResponse.status()).toBe(200);
});

Given("a journal entry has been created", async ({ request }) => {
  const resp = await request.post("/api/v1/journal/entries", {
    data: { name: "workout" },
    headers: { "Content-Type": "application/json" },
  });
  expect(resp.status()).toBe(201);
  const body = (await resp.json()) as Record<string, unknown>;
  createdEntryId = body["id"] as string;
  expect(typeof createdEntryId).toBe("string");
});

When("a client posts a valid journal entry", async ({ request }) => {
  setResponse(
    await request.post("/api/v1/journal/entries", {
      data: { name: "reading" },
      headers: { "Content-Type": "application/json" },
    }),
  );
});

When("a client posts a journal entry with a blank name", async ({ request }) => {
  setResponse(
    await request.post("/api/v1/journal/entries", {
      data: { name: "" },
      headers: { "Content-Type": "application/json" },
    }),
  );
});

When("a client lists the journal entries", async ({ request }) => {
  setResponse(await request.get("/api/v1/journal/entries"));
});

When("a client fetches a journal entry that does not exist", async ({ request }) => {
  setResponse(await request.get("/api/v1/journal/entries/nonexistent-id-that-does-not-exist"));
});

When("a client updates the journal entry name", async ({ request }) => {
  expect(createdEntryId).not.toBeNull();
  setResponse(
    await request.put(`/api/v1/journal/entries/${createdEntryId}`, {
      data: { name: "focus" },
      headers: { "Content-Type": "application/json" },
    }),
  );
});

When("a client deletes the journal entry", async ({ request }) => {
  expect(createdEntryId).not.toBeNull();
  setResponse(await request.delete(`/api/v1/journal/entries/${createdEntryId}`));
});

// oxlint-disable-next-line no-empty-pattern
Then("the journal response status code should be {int}", async ({}, expectedStatus: number) => {
  expect(getResponse().status()).toBe(expectedStatus);
});

Then("the journal response body should include an id", async () => {
  const body = (await getResponse().json()) as Record<string, unknown>;
  expect(typeof body["id"]).toBe("string");
  expect((body["id"] as string).length).toBeGreaterThan(0);
});

Then("the journal list should include the created entry", async () => {
  expect(createdEntryId).not.toBeNull();
  const entries = (await getResponse().json()) as Array<Record<string, unknown>>;
  const found = entries.some((e) => e["id"] === createdEntryId);
  expect(found).toBe(true);
});

Then("the updated journal entry should reflect the new name", async () => {
  const body = (await getResponse().json()) as Record<string, unknown>;
  expect(body["name"]).toBe("focus");
});

Then("fetching the deleted journal entry should return 404", async ({ request }) => {
  expect(createdEntryId).not.toBeNull();
  const resp = await request.get(`/api/v1/journal/entries/${createdEntryId}`);
  expect(resp.status()).toBe(404);
});
