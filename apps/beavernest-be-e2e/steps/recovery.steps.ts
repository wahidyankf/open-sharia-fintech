/** Aggregate BDD bindings for real CLI backup and stopped-app restore observations. */
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import {
  backendShell,
  requireComposeRuntime,
  runBackendCommand,
  runFsi,
  runStoppedBackendCommand,
  startBackend,
  stoppedBackendShell,
  stopBackend,
} from "../utils/compose-runtime";
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
  await expectCurrentReadiness(request);
  const output = await runFsi(databaseCheckScript("/var/lib/beavernest/beavernest.sqlite3"));
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
  const output = await runFsi(databaseCheckScript(`/var/backups/beavernest/${backupName}`));
  expect(outputValue(output, "integrity")).toBe(result);
});

Then("foreign_key_check returns no rows for the backup", async () => {
  const output = await runFsi(databaseCheckScript(`/var/backups/beavernest/${backupName}`));
  expect(outputValue(output, "foreignKeyRows")).toBe("false");
});

Given("a validated backup and the application is stopped", async ({ request }) => {
  requireComposeRuntime();
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
  const output = await runFsi(databaseCheckScript("/var/lib/beavernest/beavernest.sqlite3"), true);
  expect(outputValue(output, "journal")).toBe("1");
});

Then("the restarted application reports ready", async ({ request }) => {
  await startBackend();
  await expectCurrentReadiness(request);
});
