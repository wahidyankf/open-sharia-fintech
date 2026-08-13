/**
 * Hosted diagnostics contract assertions. The unit suite owns deterministic
 * dependency seams; these steps instead exercise the published Docker image
 * and prove that its live response stays within the safe HTTP allowlist.
 */
import { createBdd } from "playwright-bdd";
import { backendShell, requireComposeRuntime } from "../utils/compose-runtime";
import {
  expectReadyDiagnosticsComponents,
  expectReadyDiagnosticsSnapshot,
  expectUnavailableDiagnostics,
  expectUnavailableDiagnosticsDisclosure,
} from "../utils/diagnostics";
import { getResponse } from "../utils/response-store";

const { Given, Then } = createBdd();

Given("the diagnostics clock, version and uptime are deterministic", async () => {
  // The production image deliberately provides live process values. The
  // corresponding handler unit test pins them; the hosted assertion below
  // validates their safe shape and exact public field set.
});

Given("diagnostics observes unavailable readiness", async () => {
  requireComposeRuntime();
  await backendShell(
    "printf '%s' 'invalid sqlite fixture' > /var/lib/beavernest/beavernest.sqlite3.next && mv /var/lib/beavernest/beavernest.sqlite3.next /var/lib/beavernest/beavernest.sqlite3 && rm -f /var/lib/beavernest/beavernest.sqlite3-wal /var/lib/beavernest/beavernest.sqlite3-shm",
  );
});

// @covers specs/apps/beavernest/behavior/beavernest-be/gherkin/diagnostics/ready.feature:Ready workspace returns a safe live snapshot
Then(
  "the JSON response reports status {string}, safe version, whole-second uptime and UTC server time",
  // oxlint-disable-next-line no-empty-pattern
  async ({}, status: string) => {
    await expectReadyDiagnosticsSnapshot(getResponse(), status);
  },
);

// oxlint-disable-next-line no-empty-pattern
Then("the response reports the named database and schema readiness components", async () => {
  await expectReadyDiagnosticsComponents(getResponse());
});

// @covers specs/apps/beavernest/behavior/beavernest-be/gherkin/diagnostics/unavailable.feature:Unavailable workspace withholds diagnostic causes
Then(
  "the JSON response reports status {string} with only unavailable readiness components",
  // oxlint-disable-next-line no-empty-pattern
  async ({}, status: string) => {
    await expectUnavailableDiagnostics(getResponse(), status);
  },
);

Then("the diagnostics response reveals no cause, version, uptime or server time", async () => {
  await expectUnavailableDiagnosticsDisclosure(getResponse());
});
