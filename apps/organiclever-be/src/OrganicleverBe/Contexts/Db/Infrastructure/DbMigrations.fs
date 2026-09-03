namespace OrganicleverBe.Contexts.Db

open System.Diagnostics.CodeAnalysis
open System.Reflection
open DbUp

/// Infrastructure layer for the db bounded context: the on-boot migration
/// routine. DbUp applies the embedded db/migrations/*.sql scripts before the
/// HTTP server starts, so the schema is always up to date without manual
/// intervention.
module Infrastructure =

    /// Applies all pending embedded migrations to the given PostgreSQL connection
    /// string. The migration scripts live as embedded resources in the
    /// OrganicleverBe assembly. Fails fast if any script cannot be applied.
    [<ExcludeFromCodeCoverage(Justification = "Integration-tested against real PostgreSQL — see tests/integration/DatabaseBootTests.fs")>]
    let runMigrations (connStr: string) : unit =
        let result =
            DeployChanges.To
                .PostgresqlDatabase(connStr)
                .WithScriptsEmbeddedInAssembly(Assembly.GetExecutingAssembly())
                .LogToConsole()
                .Build()
                .PerformUpgrade()

        if not result.Successful then
            failwith (sprintf "Database migration failed: %s" result.Error.Message)
