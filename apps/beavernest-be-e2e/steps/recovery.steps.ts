/**
 * Aggregate BDD bindings for real CLI backup and stopped-app restore
 * observations. `backup`/`restore` run inside the disposable Compose
 * container against the exact published `BeaverNestBe.dll` the production
 * image ships (no SDK required). Verifying the resulting SQLite files' raw
 * contents runs `dotnet fsi` on the Playwright test runner's own host
 * machine against the same files via the Compose stack's host bind mounts —
 * see utils/host-runtime.ts.
 */
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import {
  backendShell,
  requireComposeRuntime,
  runBackendCommand,
  runStoppedBackendCommand,
  startBackend,
  stoppedBackendShell,
  stopBackend,
} from "../utils/compose-runtime";
import { hostBackupPath, hostDatabasePath, requireHostRuntimeAccess, runFsiOnHost } from "../utils/host-runtime";
import { expectCurrentReadiness } from "../utils/readiness";

const { Given, When, Then } = createBdd();

const backupName = "beavernest-e2e-snapshot.sqlite3";
const databaseCheckScript = (databasePath: string): string => `
#r "nuget: Microsoft.Data.Sqlite, 10.0.10"
open Microsoft.Data.Sqlite

use connection = new SqliteConnection("Data Source=${databasePath};Mode=ReadOnly")
connection.Open()
let scalar commandText =
    use command = connection.CreateCommand()
    command.CommandText <- commandText
    string (command.ExecuteScalar())
use foreignKeys = connection.CreateCommand()
foreignKeys.CommandText <- "PRAGMA foreign_key_check;"
use rows = foreignKeys.ExecuteReader()
printfn "integrity=%s" (scalar "PRAGMA integrity_check;")
printfn "foreignKeyRows=%b" (rows.Read())
printfn "journal=%d" (System.Convert.ToInt32(scalar "SELECT COUNT(*) FROM SchemaVersions;"))
`;

let backupCreated = false;
let restoreCompleted = false;

function outputValue(output: string, name: string): string {
  const match = new RegExp(`^${name}=(.+)$`, "m").exec(output);
  expect(match, output).not.toBeNull();
  return match?.[1] ?? "";
}

async function createValidatedBackup(): Promise<void> {
  await backendShell(`rm -f /var/backups/beavernest/${backupName}`);
  await runBackendCommand(["backup", "--name", backupName]);
  await backendShell(`test -f /var/backups/beavernest/${backupName}`);
  backupCreated = true;
}

Given("BeaverNest is ready with WAL enabled", async ({ request }) => {
  requireComposeRuntime();
  requireHostRuntimeAccess();
  await expectCurrentReadiness(request);
  const output = await runFsiOnHost(databaseCheckScript(hostDatabasePath()));
  expect(outputValue(output, "integrity")).toBe("ok");
});

When("I run the manual backup command while the application remains online", async () => {
  await createValidatedBackup();
});

Then("the backup completes through the SQLite backup API", async () => {
  expect(backupCreated).toBe(true);
  await backendShell(`test -f /var/backups/beavernest/${backupName}`);
});

// oxlint-disable-next-line no-empty-pattern
Then("integrity_check returns {string} for the backup", async ({}, result: string) => {
  const output = await runFsiOnHost(databaseCheckScript(hostBackupPath(backupName)));
  expect(outputValue(output, "integrity")).toBe(result);
});

Then("foreign_key_check returns no rows for the backup", async () => {
  const output = await runFsiOnHost(databaseCheckScript(hostBackupPath(backupName)));
  expect(outputValue(output, "foreignKeyRows")).toBe("false");
});

Given("a validated backup and the application is stopped", async ({ request }) => {
  requireComposeRuntime();
  requireHostRuntimeAccess();
  await expectCurrentReadiness(request);
  await createValidatedBackup();
  await stopBackend();
});

When("I run the restore command against the configured durable directory", async () => {
  await runStoppedBackendCommand(["restore", "--name", backupName]);
  restoreCompleted = true;
});

Then("the replaced database is preserved at a recoverable path", async () => {
  expect(restoreCompleted).toBe(true);
  await stoppedBackendShell(
    "test \"$(find /var/lib/beavernest -maxdepth 1 -name 'beavernest.sqlite3.replaced-*' | wc -l)\" -eq 1",
  );
});

Then("the restored migration journal is current", async () => {
  const output = await runFsiOnHost(databaseCheckScript(hostDatabasePath()));
  expect(outputValue(output, "journal")).toBe("1");
});

Then("the restarted application reports ready", async ({ request }) => {
  await startBackend();
  await expectCurrentReadiness(request);
});

// The six steps below back the two `@unit`-tagged scenarios in
// verified-restore.feature (rollback and rollback-of-rollback). Those
// scenarios exercise `promoteStagedOverPreviousLive`'s injected `moveFile`
// seam directly in BeaverNestBe.UnitTests (see DatabaseOperationsTests.fs)
// and are excluded from this project's collection by the `tags: "not @unit"`
// filter in playwright.config.ts — real filesystem-move failures cannot be
// injected deterministically into the published CLI binary running inside
// the disposable Compose container. These bindings exist only so the
// text-traceability coverage check (which does not read Playwright BDD tags)
// finds a matching implementation; they throw if ever actually invoked so a
// tag-filter regression fails loudly instead of silently passing.
function unitOnlyStep(stepText: string): () => never {
  return () => {
    throw new Error(
      `"${stepText}" is a @unit-only step (see verified-restore.feature) and must never run under Playwright — check the "not @unit" tag filter in playwright.config.ts`,
    );
  };
}

Given(
  "the final promote of the staged database will fail",
  unitOnlyStep("the final promote of the staged database will fail"),
);

Then(
  "the pre-restore database is restored at the live path",
  unitOnlyStep("the pre-restore database is restored at the live path"),
);

Then("the command reports that the restore failed", unitOnlyStep("the command reports that the restore failed"));

Given(
  "the rollback to the preserved database will also fail",
  unitOnlyStep("the rollback to the preserved database will also fail"),
);

Given(
  "companion removal for the live database will fail",
  unitOnlyStep("companion removal for the live database will fail"),
);

Then(
  "the command reports that the restore failed and the rollback failed",
  unitOnlyStep("the command reports that the restore failed and the rollback failed"),
);

Then(
  "the command instructs the operator to recover the live database manually",
  unitOnlyStep("the command instructs the operator to recover the live database manually"),
);
