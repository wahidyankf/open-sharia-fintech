module BeaverNestBe.Infrastructure.Migrations

open System
open System.IO
open System.Reflection
open System.Text
open DbUp
open Microsoft.Data.Sqlite
open BeaverNestBe.Domain.DatabaseConfiguration
open BeaverNestBe.Domain.Readiness
open BeaverNestBe.Infrastructure.Sqlite.Connection
open BeaverNestBe.Infrastructure.Sqlite.Errors

let initializationScriptName = "001-initialize.sql"

let private migrationsAssembly = typeof<DatabaseConfiguration>.Assembly

let private migrationResourcePrefix =
    migrationsAssembly.GetName().Name + ".Migrations."

/// Returns the embedded SQL resources in resource-name order so every process
/// applies the same migration set independently of the filesystem layout.
let embeddedScripts () =
    migrationsAssembly.GetManifestResourceNames()
    |> Array.filter (fun resourceName ->
        resourceName.StartsWith(migrationResourcePrefix, StringComparison.Ordinal)
        && resourceName.EndsWith(".sql", StringComparison.OrdinalIgnoreCase))
    |> Array.sort
    |> Array.map (fun resourceName ->
        match migrationsAssembly.GetManifestResourceStream resourceName with
        | null -> failwith "embedded migration resource is unavailable"
        | stream ->
            use reader = new StreamReader(stream, Encoding.UTF8, true)
            resourceName.Substring(migrationResourcePrefix.Length), reader.ReadToEnd())
    |> Array.toList

let apply configuration scripts =
    try
        Directory.CreateDirectory(dataDirectory configuration) |> ignore
        let builder = DeployChanges.To.SqliteDatabase(connectionString configuration)

        let configured =
            scripts
            |> List.fold
                (fun (state: DbUp.Builder.UpgradeEngineBuilder) (name: string, sql: string) ->
                    state.WithScript(name, sql))
                builder

        let result = configured.LogToNowhere().Build().PerformUpgrade()
        if result.Successful then Ok() else Error FailedMigration
    with exceptionValue ->
        Error(classify exceptionValue)

let initialize configuration =
    apply configuration (embeddedScripts ())

let journalState expectedScripts actualScripts =
    schemaState expectedScripts actualScripts

let private completedScripts (connection: SqliteConnection) =
    use command = connection.CreateCommand()
    command.CommandText <- "SELECT ScriptName FROM SchemaVersions ORDER BY ScriptName;"
    use reader = command.ExecuteReader()

    [ while reader.Read() do
          reader.GetString(0) ]

/// Performs only read-only observations. A missing database, journal, or
/// expected journal entry is unavailable rather than a reason to initialise it.
let isReady configuration =
    try
        use connection = openReadOnly configuration
        use probe = connection.CreateCommand()
        probe.CommandText <- "SELECT 1;"
        probe.ExecuteScalar() |> ignore

        let expectedScripts = embeddedScripts () |> List.map fst
        journalState expectedScripts (completedScripts connection) = "current"
    with _ ->
        false
