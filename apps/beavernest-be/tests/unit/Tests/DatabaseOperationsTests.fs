module BeaverNestBe.Tests.Unit.Tests.DatabaseOperationsTests

open System
open System.IO
open Microsoft.Data.Sqlite
open Xunit
open BeaverNestBe.Domain.DatabaseConfiguration
open BeaverNestBe.Infrastructure.Migrations
open BeaverNestBe.Infrastructure.Sqlite.Connection
open BeaverNestBe.Infrastructure.Sqlite.Errors
open BeaverNestBe.Operations.Database

[<Theory>]
[<InlineData("../escape.sqlite3")>]
[<InlineData("not-a-database")>]
[<InlineData("nested/backup.sqlite3")>]
[<InlineData("backup;Mode=ReadOnly.sqlite3")>]
[<InlineData("backup=unsafe.sqlite3")>]
[<InlineData("backup name.sqlite3")>]
let ``backup names cannot escape their fixed directory`` (name: string) =
    Assert.True(validateBackupName name |> Result.isError)

[<Fact>]
let ``valid backup names remain beneath the fixed backup directory`` () =
    Assert.Equal(Ok "/var/backups/beavernest/snapshot.sqlite3", validateBackupName "snapshot.sqlite3")

[<Fact>]
let ``backup and restore report safe errors when a valid backup is unavailable`` () =
    let directory =
        Path.Combine(Path.GetTempPath(), "beavernest-operation-" + Guid.NewGuid().ToString("N"))

    let configuration = create directory 100 |> Result.defaultWith failwith
    Assert.True(backup configuration "snapshot.sqlite3" |> Result.isError)
    Assert.True(restore configuration "snapshot.sqlite3" |> Result.isError)

[<Fact>]
let ``integrity verifies a migrated live database through the operation lock`` () =
    let directory =
        Path.Combine(Path.GetTempPath(), "beavernest-integrity-" + Guid.NewGuid().ToString("N"))

    let configuration = create directory 100 |> Result.defaultWith failwith

    try
        use connection = openConfigured configuration
        use setup = connection.CreateCommand()
        setup.CommandText <- "CREATE TABLE IntegrityProof (Value TEXT NOT NULL);"
        setup.ExecuteNonQuery() |> ignore
        connection.Close()
        Assert.Equal(Ok(), integrity configuration)
    finally
        Directory.Delete(directory, true)

[<Fact>]
let ``backup operations reject blank, privileged, and file-shaped backup roots`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-invalid-backup-root-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let backupFilePath = Path.Combine(root, "backup-file")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    Directory.CreateDirectory(root) |> ignore
    File.WriteAllText(backupFilePath, "not a directory")

    try
        Assert.Equal(Error "backup directory is invalid", backupAt "" configuration "snapshot.sqlite3")
        Assert.Equal(Error "backup directory is invalid", backupAt "/" configuration "snapshot.sqlite3")

        Assert.Equal(
            Error "backup directory is invalid",
            backupAt (Environment.GetFolderPath(Environment.SpecialFolder.UserProfile)) configuration "snapshot.sqlite3"
        )

        Assert.Equal(
            Error "backup directory must be a directory",
            backupAt backupFilePath configuration "snapshot.sqlite3"
        )
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``backup operations reject a backup root nested inside the current working directory`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-invalid-nested-backup-root-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    let nestedBackupRoot =
        Path.Combine(Directory.GetCurrentDirectory(), "beavernest-subdir-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(root) |> ignore
    Directory.CreateDirectory(nestedBackupRoot) |> ignore

    try
        Assert.Equal(Error "backup directory is invalid", backupAt nestedBackupRoot configuration "snapshot.sqlite3")
    finally
        Directory.Delete(root, true)
        Directory.Delete(nestedBackupRoot, true)

[<Fact>]
let ``backup operations reject a backup root that is an ancestor of the current working directory`` () =
    // Reverse containment direction from the "nested inside cwd" case above —
    // mirrors infra/dev/beavernest-app/scripts/lib.sh's second
    // `case "$beavernest_repository_root" in "$beavernest_canonical"/*)` arm.
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-invalid-ancestor-backup-root-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    let ancestorBackupRoot =
        Directory.GetParent(Directory.GetCurrentDirectory()).FullName

    Directory.CreateDirectory(root) |> ignore

    try
        Assert.Equal(Error "backup directory is invalid", backupAt ancestorBackupRoot configuration "snapshot.sqlite3")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``backup and restore reject invalid names before touching the filesystem`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-invalid-operation-name-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let backupDirectoryPath = Path.Combine(root, "backups")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    Directory.CreateDirectory(root) |> ignore

    try
        Assert.Equal(Error "backup name is invalid", backupAt backupDirectoryPath configuration "invalid")
        Assert.Equal(Error "backup name is invalid", restoreAt backupDirectoryPath configuration "invalid")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``disposable SQLite backup and restore preserve a recoverable live database`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-backup-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let backupDirectoryPath = Path.Combine(root, "backups")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    use source = openConfigured configuration
    use setup = source.CreateCommand()
    setup.CommandText <- "CREATE TABLE BackupProof (Value TEXT NOT NULL); INSERT INTO BackupProof VALUES ('kept');"
    setup.ExecuteNonQuery() |> ignore
    setup.CommandText <- "PRAGMA wal_checkpoint(TRUNCATE);"
    setup.ExecuteNonQuery() |> ignore
    source.Close()

    let backupPath =
        backupAt backupDirectoryPath configuration "snapshot.sqlite3"
        |> Result.defaultWith failwith

    Assert.True(File.Exists backupPath)

    use changed = openConfigured configuration
    use change = changed.CreateCommand()
    change.CommandText <- "CREATE TABLE LaterChange (Value TEXT NOT NULL);"
    change.ExecuteNonQuery() |> ignore
    changed.Close()
    File.WriteAllText(databasePath configuration + "-wal", "stale")
    File.WriteAllText(databasePath configuration + "-shm", "stale")

    Assert.Equal(Ok(), restoreAt backupDirectoryPath configuration "snapshot.sqlite3")
    Assert.True(Directory.GetFiles(dataDirectoryPath, "beavernest.sqlite3.replaced-*").Length = 1)
    Assert.False(File.Exists(databasePath configuration + "-wal"))
    Assert.False(File.Exists(databasePath configuration + "-shm"))
    // Verifying the staged copy (even read-only) can leave its own -wal/-shm
    // companions on disk; only the staged database file itself is renamed to
    // `live`, so any companion left at the discarded `.restore-<guid>` path
    // would strand a file container-entrypoint.sh's file-mode validator
    // rejects on the next boot.
    Assert.Empty(Directory.GetFiles(dataDirectoryPath, "beavernest.sqlite3.restore-*"))
    // File.Copy leaves the new file's mode governed by the process umask —
    // the same container-entrypoint.sh validator requires exactly mode 600
    // on the live database on the next fresh container start, regardless of
    // what umask restored it.
    Assert.Equal(UnixFileMode.UserRead ||| UnixFileMode.UserWrite, File.GetUnixFileMode(databasePath configuration))

    use restored = openConfigured configuration
    use verify = restored.CreateCommand()
    verify.CommandText <- "SELECT Value FROM BackupProof;"
    Assert.Equal("kept", string (verify.ExecuteScalar()))

[<Fact>]
let ``restore rolls back to the preserved database when the final promote move fails`` () =
    // Regression test for a rollback gap: the final `File.Move(staged, live,
    // false)` inside `restoreAt` used to have no fault handling, unlike the
    // sibling `removeCompanions live` failure branch immediately above it —
    // a throw here left the service with nothing at `live` at all rather
    // than reverting to the pre-restore database. `promoteStagedOverPreviousLive`
    // is exercised directly (with an injected `moveFile`) instead of racing
    // real filesystem timing to reproduce a `File.Move` failure inside a
    // full `restoreAt` call deterministically.
    let mutable moves = []

    let failPromoteThenRecordRollback (source: string) (destination: string) =
        moves <- moves @ [ source, destination ]

        if moves.Length = 1 then
            raise (IOException "simulated final promote failure")

    Assert.Equal(
        Error "restore failed",
        promoteStagedOverPreviousLive failPromoteThenRecordRollback "staged.sqlite3" "live.sqlite3" "preserved.sqlite3"
    )

    Assert.Equal<(string * string) list>(
        [ ("staged.sqlite3", "live.sqlite3"); ("preserved.sqlite3", "live.sqlite3") ],
        moves
    )

[<Fact>]
let ``restore reports a distinguishable error when the rollback move also fails`` () =
    // Regression test for the rollback-of-rollback gap: the rollback move at
    // line 219 of Database.fs used to have no fault handling of its own, so a
    // throw there either escaped uncaught or (via `restoreAt`'s outer
    // try/with) collapsed to the exact same "restore failed" string as a
    // clean rollback — making "safe to retry" and "live database is now
    // missing entirely" indistinguishable from the return value alone.
    let mutable moves = []

    let failBothMoves (source: string) (destination: string) =
        moves <- moves @ [ source, destination ]
        raise (IOException "simulated failure")

    Assert.Equal(
        Error
            "restore failed and rollback failed - live database is missing; recover it manually from the preserved copy",
        promoteStagedOverPreviousLive failBothMoves "staged.sqlite3" "live.sqlite3" "preserved.sqlite3"
    )

    Assert.Equal<(string * string) list>(
        [ ("staged.sqlite3", "live.sqlite3"); ("preserved.sqlite3", "live.sqlite3") ],
        moves
    )

[<Fact>]
let ``restore returns sanitized errors for missing and corrupt backup files`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-invalid-restore-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let backupDirectoryPath = Path.Combine(root, "backups")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    Directory.CreateDirectory(backupDirectoryPath) |> ignore

    try
        Assert.Equal(Error "backup does not exist", restoreAt backupDirectoryPath configuration "missing.sqlite3")

        File.WriteAllText(Path.Combine(backupDirectoryPath, "corrupt.sqlite3"), "not a SQLite database")

        Assert.Equal(Error "backup verification failed", restoreAt backupDirectoryPath configuration "corrupt.sqlite3")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``backup and restore reject a foreign-key-invalid SQLite backup`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-invalid-foreign-key-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let backupDirectoryPath = Path.Combine(root, "backups")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    try
        use source = openConfigured configuration
        use setup = source.CreateCommand()

        setup.CommandText <-
            "PRAGMA foreign_keys = OFF; CREATE TABLE Parent (Id INTEGER PRIMARY KEY); CREATE TABLE Child (ParentId INTEGER REFERENCES Parent(Id)); INSERT INTO Child VALUES (1);"

        setup.ExecuteNonQuery() |> ignore
        source.Close()

        Assert.Equal(Error "backup verification failed", backupAt backupDirectoryPath configuration "invalid.sqlite3")

        Assert.Equal(Error "backup verification failed", restoreAt backupDirectoryPath configuration "invalid.sqlite3")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``backup refuses overwrite and restore installs a backup when no live database exists`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-no-live-restore-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let backupDirectoryPath = Path.Combine(root, "backups")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    try
        use source = openConfigured configuration
        use setup = source.CreateCommand()
        setup.CommandText <- "CREATE TABLE NoLiveRestoreProof (Value TEXT NOT NULL);"
        setup.ExecuteNonQuery() |> ignore
        source.Close()

        backupAt backupDirectoryPath configuration "snapshot.sqlite3"
        |> Result.defaultWith failwith
        |> ignore

        Assert.Equal(Error "backup already exists", backupAt backupDirectoryPath configuration "snapshot.sqlite3")

        File.Delete(databasePath configuration)
        Assert.Equal(Ok(), restoreAt backupDirectoryPath configuration "snapshot.sqlite3")
        Assert.True(File.Exists(databasePath configuration))
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``restore installs a verified backup into a separate previously absent data directory`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-absent-live-directory-" + Guid.NewGuid().ToString("N"))

    let sourceDirectoryPath = Path.Combine(root, "source")
    let restoredDirectoryPath = Path.Combine(root, "restored")
    let backupDirectoryPath = Path.Combine(root, "backups")

    let sourceConfiguration =
        create sourceDirectoryPath 100 |> Result.defaultWith failwith

    let restoredConfiguration =
        create restoredDirectoryPath 100 |> Result.defaultWith failwith

    try
        use source = openConfigured sourceConfiguration
        use setup = source.CreateCommand()
        setup.CommandText <- "CREATE TABLE AbsentLiveProof (Value TEXT NOT NULL);"
        setup.ExecuteNonQuery() |> ignore
        source.Close()

        backupAt backupDirectoryPath sourceConfiguration "snapshot.sqlite3"
        |> Result.defaultWith failwith
        |> ignore

        Assert.False(Directory.Exists(restoredDirectoryPath))
        Assert.Equal(Ok(), restoreAt backupDirectoryPath restoredConfiguration "snapshot.sqlite3")
        Assert.True(File.Exists(databasePath restoredConfiguration))
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``SQLite connection-string metacharacters in literal directories cannot inject backup options`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-connection-literal-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data;Mode=ReadOnly")
    let backupDirectoryPath = Path.Combine(root, "backups=literal")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    try
        use source = openConfigured configuration
        use setup = source.CreateCommand()
        setup.CommandText <- "CREATE TABLE ConnectionLiteralProof (Value TEXT NOT NULL);"
        setup.ExecuteNonQuery() |> ignore
        source.Close()

        let backupPath =
            backupAt backupDirectoryPath configuration "literal.sqlite3"
            |> Result.defaultWith failwith

        Assert.Equal(Path.Combine(backupDirectoryPath, "literal.sqlite3"), backupPath)
        Assert.True(File.Exists backupPath)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``backup and restore reject symbolic-link roots, files, and data-directory aliases`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-operation-links-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let backupDirectoryPath = Path.Combine(root, "backups")
    let backupLinkPath = Path.Combine(root, "backup-link")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    Directory.CreateDirectory(backupDirectoryPath) |> ignore
    Directory.CreateSymbolicLink(backupLinkPath, backupDirectoryPath) |> ignore

    try
        Assert.True(backupAt backupLinkPath configuration "snapshot.sqlite3" |> Result.isError)
        Assert.True(backupAt dataDirectoryPath configuration "snapshot.sqlite3" |> Result.isError)

        use source = openConfigured configuration
        use setup = source.CreateCommand()
        setup.CommandText <- "CREATE TABLE LinkProof (Value TEXT NOT NULL);"
        setup.ExecuteNonQuery() |> ignore
        source.Close()

        let backupPath =
            backupAt backupDirectoryPath configuration "snapshot.sqlite3"
            |> Result.defaultWith failwith

        let targetPath = Path.Combine(backupDirectoryPath, "actual.sqlite3")
        File.Move(backupPath, targetPath)
        File.CreateSymbolicLink(backupPath, targetPath) |> ignore

        Assert.Equal(
            Error "database file may not be a symbolic link",
            restoreAt backupDirectoryPath configuration "snapshot.sqlite3"
        )
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``the operation lock file is created with mode 600 regardless of the process umask`` () =
    // container-entrypoint.sh's file-mode validator runs on every fresh
    // `docker compose run` (e.g. a stopped-service restore), rejecting any
    // file under the data directory that isn't exactly mode 600 — including
    // a lock file left behind by an earlier `docker compose exec`, whose
    // process umask (unlike the entrypoint's own `umask 0077`) is never
    // guaranteed. The lock file's permissions must not depend on umask.
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-lock-mode-" + Guid.NewGuid().ToString("N"))

    let configuration = create root 1000 |> Result.defaultWith failwith

    use _operationLock =
        acquireDataDirectoryOperationLock configuration |> Result.defaultWith failwith

    let lockPath = Path.Combine(root, ".beavernest-operation.lock")
    Assert.Equal(UnixFileMode.UserRead ||| UnixFileMode.UserWrite, File.GetUnixFileMode(lockPath))

[<Fact>]
let ``database operations fail closed while another operation owns the data-directory lock`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-operation-lock-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let backupDirectoryPath = Path.Combine(root, "backups")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    let operationLock =
        acquireDataDirectoryOperationLock configuration |> Result.defaultWith failwith

    try
        Assert.Equal(
            Error "database operation is already running",
            backupAt backupDirectoryPath configuration "snapshot.sqlite3"
        )

        Assert.Equal(
            Error "database operation is already running",
            restoreAt backupDirectoryPath configuration "snapshot.sqlite3"
        )
    finally
        operationLock.Dispose()
        Directory.Delete(root, true)

[<Fact>]
let ``database operations reject a symbolic-link operation lock`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-operation-lock-link-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let lockTargetPath = Path.Combine(root, "lock-target")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    Directory.CreateDirectory(dataDirectoryPath) |> ignore
    File.WriteAllText(lockTargetPath, "not a lock")

    File.CreateSymbolicLink(Path.Combine(dataDirectoryPath, ".beavernest-operation.lock"), lockTargetPath)
    |> ignore

    try
        Assert.Equal(Error "database operation lock is invalid", acquireDataDirectoryOperationLock configuration)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``database operations fail closed when configured data directory becomes a file`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-data-directory-file-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let backupDirectoryPath = Path.Combine(root, "backups")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    Directory.CreateDirectory(dataDirectoryPath) |> ignore
    Directory.Delete(dataDirectoryPath)
    File.WriteAllText(dataDirectoryPath, "not a directory")

    try
        Assert.Equal(
            Error "database data directory is invalid",
            backupAt backupDirectoryPath configuration "snapshot.sqlite3"
        )

        Assert.Equal(Error "database data directory is invalid", acquireDataDirectoryOperationLock configuration)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``restore fails closed for a live service while online backup remains available`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-service-lock-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let backupDirectoryPath = Path.Combine(root, "backups")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    use source = openConfigured configuration
    use setup = source.CreateCommand()
    setup.CommandText <- "CREATE TABLE ServiceLockProof (Value TEXT NOT NULL);"
    setup.ExecuteNonQuery() |> ignore
    source.Close()

    let serviceLock =
        acquireDataDirectoryServiceLock configuration |> Result.defaultWith failwith

    try
        let backupPath =
            backupAt backupDirectoryPath configuration "snapshot.sqlite3"
            |> Result.defaultWith failwith

        Assert.True(File.Exists backupPath)

        Assert.Equal(
            Error "restore refused while service is active",
            restoreAt backupDirectoryPath configuration "snapshot.sqlite3"
        )
    finally
        serviceLock.Dispose()
        Directory.Delete(root, true)

[<Fact>]
let ``restore rejects symbolic-link database companions before replacing live data`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-companion-link-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let backupDirectoryPath = Path.Combine(root, "backups")
    let companionTarget = Path.Combine(root, "companion-target")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    try
        use source = openConfigured configuration
        use setup = source.CreateCommand()
        setup.CommandText <- "CREATE TABLE CompanionProof (Value TEXT NOT NULL);"
        setup.ExecuteNonQuery() |> ignore
        source.Close()

        backupAt backupDirectoryPath configuration "snapshot.sqlite3"
        |> Result.defaultWith failwith
        |> ignore

        File.WriteAllText(companionTarget, "not a database companion")
        let companionPath = databasePath configuration + "-shm"

        if File.Exists(companionPath) then
            File.Delete(companionPath)

        File.CreateSymbolicLink(companionPath, companionTarget) |> ignore

        Assert.Equal(
            Error "database companion may not be a symbolic link",
            restoreAt backupDirectoryPath configuration "snapshot.sqlite3"
        )

        Assert.True(File.Exists(databasePath configuration))
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``restore rejects a symbolic-link live database without replacing the target`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-live-link-" + Guid.NewGuid().ToString("N"))

    let dataDirectoryPath = Path.Combine(root, "data")
    let backupDirectoryPath = Path.Combine(root, "backups")
    let liveTargetPath = Path.Combine(root, "live-target.sqlite3")
    let configuration = create dataDirectoryPath 100 |> Result.defaultWith failwith

    try
        use source = openConfigured configuration
        use setup = source.CreateCommand()
        setup.CommandText <- "CREATE TABLE LiveLinkProof (Value TEXT NOT NULL);"
        setup.ExecuteNonQuery() |> ignore
        source.Close()

        backupAt backupDirectoryPath configuration "snapshot.sqlite3"
        |> Result.defaultWith failwith
        |> ignore

        File.Move(databasePath configuration, liveTargetPath)
        File.CreateSymbolicLink(databasePath configuration, liveTargetPath) |> ignore

        Assert.Equal(
            Error "live database may not be a symbolic link",
            restoreAt backupDirectoryPath configuration "snapshot.sqlite3"
        )

        Assert.True(File.Exists(liveTargetPath))
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``SQLite provider error classification is closed and safe`` () =
    let cases =
        [ SqliteException("busy", 5) :> exn, Busy, "database is busy"
          SqliteException("locked", 6) :> exn, Busy, "database is busy"
          SqliteException("corrupt", 11) :> exn, InvalidDatabase, "database operation failed"
          Exception("untrusted detail"), FailedMigration, "database migration failed" ]

    cases
    |> List.iter (fun (exceptionValue, expectedError, expectedMessage) ->
        let error = classify exceptionValue
        Assert.Equal(expectedError, error)
        Assert.Equal(expectedMessage, safeMessage error))

[<Fact>]
let ``configured SQLite connection applies required safeguards and DbUp journal is idempotent`` () =
    let directory =
        Path.Combine(Path.GetTempPath(), "beavernest-sqlite-" + Guid.NewGuid().ToString("N"))

    let configuration = create directory 250 |> Result.defaultWith failwith

    match initialize configuration with
    | Ok() -> ()
    | Error error -> failwithf "initial migration failed: %A" error

    match initialize configuration with
    | Ok() -> ()
    | Error error -> failwithf "restart migration failed: %A" error

    use connection = openConfigured configuration
    use settings = connection.CreateCommand()
    settings.CommandText <- "PRAGMA foreign_keys;"
    Assert.Equal(1L, unbox<int64> (settings.ExecuteScalar()))
    settings.CommandText <- "PRAGMA busy_timeout;"
    Assert.Equal(250L, unbox<int64> (settings.ExecuteScalar()))
    settings.CommandText <- "PRAGMA journal_mode;"
    Assert.Equal("wal", string (settings.ExecuteScalar()))
    Assert.Equal("current", journalState [ initializationScriptName ] [ initializationScriptName ])

[<Fact>]
let ``embedded migrations are readable in order and readiness observes without creating a database`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-readiness-observation-" + Guid.NewGuid().ToString("N"))

    let absentDirectoryPath = Path.Combine(root, "absent")
    let readyDirectoryPath = Path.Combine(root, "ready")

    let absentConfiguration =
        create absentDirectoryPath 100 |> Result.defaultWith failwith

    let readyConfiguration =
        create readyDirectoryPath 100 |> Result.defaultWith failwith

    try
        let scripts = embeddedScripts ()
        Assert.True([ initializationScriptName ] = (scripts |> List.map fst))
        Assert.True(scripts |> List.forall (snd >> String.IsNullOrWhiteSpace >> not))

        Assert.False(isReady absentConfiguration)
        Assert.False(Directory.Exists(absentDirectoryPath))

        match initialize readyConfiguration with
        | Ok() -> ()
        | Error error -> failwithf "migration failed: %A" error

        Assert.True(isReady readyConfiguration)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``DbUp migration failures are reduced to a safe provider-independent error`` () =
    let directory =
        Path.Combine(Path.GetTempPath(), "beavernest-broken-" + Guid.NewGuid().ToString("N"))

    let configuration = create directory 100 |> Result.defaultWith failwith
    Assert.Equal(Error FailedMigration, apply configuration [ "broken.sql", "not valid SQL" ])
