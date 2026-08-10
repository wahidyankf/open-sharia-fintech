/**
 * Aggregate Playwright-BDD bindings for durable-store observations. These
 * bindings use only the disposable Compose runtime: no production test route
 * or host database access is introduced.
 */
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { composeResult, requireComposeRuntime, runFsi, startBackend, stopBackend } from "../utils/compose-runtime";
import { expectCurrentReadiness, expectReadinessResponse } from "../utils/readiness";

const { Given, When, Then } = createBdd();

type DatabaseSnapshot = {
  journalEntries: number;
  tables: string[];
};

const journalSnapshotScript = `
#r "nuget: Microsoft.Data.Sqlite, 10.0.10"
open Microsoft.Data.Sqlite

use connection = new SqliteConnection("Data Source=/var/lib/beavernest/beavernest.sqlite3;Mode=ReadOnly")
connection.Open()
use journal = connection.CreateCommand()
journal.CommandText <- "SELECT COUNT(*) FROM SchemaVersions;"
let journalEntries = System.Convert.ToInt32(journal.ExecuteScalar())
use tables = connection.CreateCommand()
tables.CommandText <- "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name;"
use rows = tables.ExecuteReader()
let names = [ while rows.Read() do rows.GetString(0) ]
printfn "journal=%d" journalEntries
printfn "tables=%s" (System.String.Join(",", names))
`;

const configuredSettingsScript = `
#r "nuget: Microsoft.Data.Sqlite, 10.0.10"
#r "/workspace/src/BeaverNestBe/bin/Debug/net10.0/BeaverNestBe.dll"
open Microsoft.Data.Sqlite
open BeaverNestBe.Domain.DatabaseConfiguration
open BeaverNestBe.Infrastructure.Sqlite.Connection

let configuration = create "/var/lib/beavernest" 1000 |> Result.defaultWith failwith
use connection = openConfigured configuration
let scalar commandText =
    use command = connection.CreateCommand()
    command.CommandText <- commandText
    string (command.ExecuteScalar())

printfn "foreignKeys=%s" (scalar "PRAGMA foreign_keys;")
printfn "journalMode=%s" (scalar "PRAGMA journal_mode;")
printfn "busyTimeout=%s" (scalar "PRAGMA busy_timeout;")
`;

const contentionScript = `
#r "nuget: Microsoft.Data.Sqlite, 10.0.10"
#r "/workspace/src/BeaverNestBe/bin/Debug/net10.0/BeaverNestBe.dll"
open System
open BeaverNestBe.Domain.DatabaseConfiguration
open BeaverNestBe.Infrastructure.Sqlite.Connection
open BeaverNestBe.Infrastructure.Sqlite.Errors

let configuration = create "/var/lib/beavernest" 1000 |> Result.defaultWith failwith
use first = openConfigured configuration
use setup = first.CreateCommand()
setup.CommandText <- "CREATE TABLE IF NOT EXISTS E2eContentionFixture (Id INTEGER PRIMARY KEY);"
setup.ExecuteNonQuery() |> ignore
use lockCommand = first.CreateCommand()
lockCommand.CommandText <- "BEGIN IMMEDIATE; INSERT INTO E2eContentionFixture DEFAULT VALUES;"
lockCommand.ExecuteNonQuery() |> ignore
use second = openConfigured configuration
use secondCommand = second.CreateCommand()
secondCommand.CommandText <- "INSERT INTO E2eContentionFixture DEFAULT VALUES;"
let started = DateTime.UtcNow
let outcome =
    try
        secondCommand.ExecuteNonQuery() |> ignore
        "success"
    with exceptionValue ->
        classify exceptionValue |> string
let elapsed = int (DateTime.UtcNow - started).TotalMilliseconds
use rollback = first.CreateCommand()
rollback.CommandText <- "ROLLBACK;"
rollback.ExecuteNonQuery() |> ignore
printfn "outcome=%s" outcome
printfn "elapsedMs=%d" elapsed
`;

let freshSnapshot: DatabaseSnapshot | undefined;
let restartedSnapshot: DatabaseSnapshot | undefined;
let brokenMigrationOutput: string | undefined;
let contentionOutput: string | undefined;
let settingsOutput: string | undefined;

async function databaseSnapshot(): Promise<DatabaseSnapshot> {
  const output = await runFsi(journalSnapshotScript);
  const journalMatch = /^journal=(\d+)$/m.exec(output);
  const tablesMatch = /^tables=(.*)$/m.exec(output);

  expect(journalMatch, output).not.toBeNull();
  expect(tablesMatch, output).not.toBeNull();
  const tables = tablesMatch?.[1] ?? "";
  return {
    journalEntries: Number(journalMatch?.[1]),
    tables: tables === "" ? [] : tables.split(","),
  };
}

function outputValue(output: string, name: string): string {
  const match = new RegExp(`^${name}=(.+)$`, "m").exec(output);
  expect(match, output).not.toBeNull();
  return match?.[1] ?? "";
}

Given("the configured durable database directory is writable and contains no database", async () => {
  requireComposeRuntime();
  freshSnapshot = undefined;
});

When("the BeaverNest application starts", async ({ request }) => {
  await expectCurrentReadiness(request);
  freshSnapshot = await databaseSnapshot();
});

Then("DbUp creates its migration journal before the HTTP endpoint begins listening", async ({ request }) => {
  await expectCurrentReadiness(request);
  expect(freshSnapshot?.journalEntries).toBe(1);
});

Then("no product or domain table is created", async () => {
  expect(freshSnapshot?.tables).toEqual(["SchemaVersions"]);
});

Given("the database contains a completed DbUp migration journal", async () => {
  requireComposeRuntime();
  freshSnapshot = await databaseSnapshot();
  expect(freshSnapshot.journalEntries).toBe(1);
});

When("the BeaverNest application restarts against the same mounted directory", async () => {
  await stopBackend();
  await startBackend();
  restartedSnapshot = await databaseSnapshot();
});

Then("every completed migration remains recorded exactly once", async () => {
  expect(restartedSnapshot?.journalEntries).toBe(freshSnapshot?.journalEntries);
  expect(restartedSnapshot?.journalEntries).toBe(1);
});

Then("readiness reports schema {string}", async ({ request }, schema: string) => {
  const response = await request.get("/api/v1/readiness");
  await expectReadinessResponse(response, "ready", "ready", schema);
});

Given("the migration set contains an intentionally invalid SQL script in an isolated test fixture", async () => {
  requireComposeRuntime();
  brokenMigrationOutput = undefined;
});

When("the BeaverNest application starts against a disposable database", async () => {
  const result = await composeResult([
    "run",
    "--rm",
    "--no-deps",
    "beavernest-app",
    "sh",
    "-ceu",
    `source=/tmp/beavernest-e2e-broken-source
rm -rf "$source"
mkdir -p "$source"
cp -a /workspace/. "$source"
printf '%s\\n' 'not valid SQL' > "$source/src/BeaverNestBe/Migrations/999-e2e-broken.sql"
dotnet build "$source/src/BeaverNestBe/BeaverNestBe.fsproj" --no-restore >/dev/null
BEAVERNEST_BE_DATA_DIRECTORY="$source/data" BEAVERNEST_BE_HTTP_LISTEN_ADDRESS=127.0.0.1 BEAVERNEST_BE_HTTP_LISTEN_PORT=19321 dotnet "$source/src/BeaverNestBe/bin/Debug/net10.0/BeaverNestBe.dll"`,
  ]);
  expect(result.exitCode, result.output).not.toBe(0);
  brokenMigrationOutput = result.output;
});

Then("startup exits non-zero before publishing the HTTP endpoint", async () => {
  expect(brokenMigrationOutput).toBeDefined();
  expect(brokenMigrationOutput).toContain("database migration failed");
});

Then("the migration failure is logged without exposing sensitive configuration", async () => {
  const output = brokenMigrationOutput ?? "";
  expect(output).not.toContain("not valid SQL");
  expect(output).not.toContain("/tmp/beavernest-e2e-broken-source/data");
});

Given("a migrated BeaverNest database is open", async () => {
  requireComposeRuntime();
});

When("the SQLite operating settings are inspected", async () => {
  settingsOutput = await runFsi(configuredSettingsScript);
});

Then("foreign key enforcement is enabled", async () => {
  expect(outputValue(settingsOutput ?? "", "foreignKeys")).toBe("1");
});

Then("journal mode is WAL", async () => {
  expect(outputValue(settingsOutput ?? "", "journalMode")).toBe("wal");
});

Then("a finite busy timeout is configured", async () => {
  expect(outputValue(settingsOutput ?? "", "busyTimeout")).toBe("1000");
});

Given("one disposable SQLite connection holds a short write transaction", async () => {
  requireComposeRuntime();
});

When("a second connection attempts a write through the configured data boundary", async () => {
  contentionOutput = await runFsi(contentionScript);
});

Then("the second operation retries only until the configured busy timeout", async () => {
  const elapsed = Number(outputValue(contentionOutput ?? "", "elapsedMs"));
  expect(elapsed).toBeGreaterThanOrEqual(900);
  expect(elapsed).toBeLessThan(2_000);
});

Then("the result is returned as a controlled database-busy error rather than an unbounded hang", async () => {
  expect(outputValue(contentionOutput ?? "", "outcome")).toBe("Busy");
});
