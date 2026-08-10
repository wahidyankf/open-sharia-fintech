/**
 * Aggregate HTTP observations for liveness and readiness. Detailed database
 * fault injection remains in the F# integration suite; this BDD surface
 * verifies the externally observable contract of the disposable runtime.
 */
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { backendShell, requireComposeRuntime, resetBackendData } from "../utils/compose-runtime";
import { getResponse } from "../utils/response-store";
import { expectNoStorageDiagnostics, expectReadinessResponse } from "../utils/readiness";

const { Given, Then } = createBdd();

Given("the BeaverNest process is accepting HTTP requests", async () => {
  // The disposable runtime is started by scripts/run-e2e.sh before Playwright runs.
});

Given("startup migrations completed and SQLite accepts queries", async () => {
  // Startup is observed through the ready response below.
});

Given("SQLite cannot complete the readiness query", async () => {
  requireComposeRuntime();
  // Replacing only the disposable named-volume database forces the next
  // read-only readiness probe to fail, without adding a production test seam.
  await backendShell(
    "printf '%s' 'invalid sqlite fixture' > /var/lib/beavernest/beavernest.sqlite3.next && mv /var/lib/beavernest/beavernest.sqlite3.next /var/lib/beavernest/beavernest.sqlite3 && rm -f /var/lib/beavernest/beavernest.sqlite3-wal /var/lib/beavernest/beavernest.sqlite3-shm",
  );
});

// oxlint-disable-next-line no-empty-pattern
Then("the JSON response reports status {string}", async ({}, status: string) => {
  const body = (await getResponse().json()) as { status?: unknown };
  expect(body.status).toBe(status);
});

// oxlint-disable-next-line no-empty-pattern
Then(
  "the JSON response reports status {string}, database {string} and schema {string}",
  // oxlint-disable-next-line no-empty-pattern
  async ({}, status: string, database: string, schema: string) => {
    await expectReadinessResponse(getResponse(), status, database, schema);
  },
);

// oxlint-disable-next-line no-empty-pattern
Then("the response sends {string} without a cache validator", async ({}, cacheControl: string) => {
  const response = getResponse();
  const separator = cacheControl.indexOf(":");
  expect(separator).toBeGreaterThan(0);
  const headerName = cacheControl.slice(0, separator).toLowerCase();
  const expectedValue = cacheControl.slice(separator + 1).trim();
  expect(headerName).toBe("cache-control");
  expect(expectedValue).toBe("no-store");
  expect(response.headers()[headerName.toLowerCase()]).toBe(expectedValue);
  expect(response.headers().etag).toBeUndefined();
  expect(response.headers()["last-modified"]).toBeUndefined();

  if (response.status() === 503) {
    await resetBackendData();
  }
});

Then("the response reveals no database path or migration detail", async () => {
  await expectNoStorageDiagnostics(getResponse());
});

Then("the response reveals no database path, SQL text or exception detail", async () => {
  await expectNoStorageDiagnostics(getResponse());
});
