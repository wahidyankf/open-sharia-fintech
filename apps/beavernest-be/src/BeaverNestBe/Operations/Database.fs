module BeaverNestBe.Operations.Database

open System
open System.IO
open Microsoft.Data.Sqlite
open BeaverNestBe.Domain.DatabaseConfiguration
open BeaverNestBe.Infrastructure.Sqlite.Connection

let private backupDirectory = "/var/backups/beavernest"
let private operationLockFileName = ".beavernest-operation.lock"
let private serviceLockFileName = ".beavernest-service.lock"

let private validName name =
    not (String.IsNullOrWhiteSpace name)
    && name.EndsWith(".sqlite3", StringComparison.Ordinal)
    && name.Length > ".sqlite3".Length
    && (name.Substring(0, name.Length - ".sqlite3".Length)
        |> Seq.forall (fun character -> Char.IsAsciiLetterOrDigit character || character = '-' || character = '_'))

let private normalizeDirectoryPath (path: string) =
    Path.GetFullPath(path) |> Path.TrimEndingDirectorySeparator

let private isDisallowedDirectory (path: string) =
    let root = Path.GetPathRoot path

    let home =
        Environment.GetFolderPath Environment.SpecialFolder.UserProfile
        |> normalizeDirectoryPath

    let repository = Directory.GetCurrentDirectory() |> normalizeDirectoryPath
    path = root || path = home || path = repository

let private isSymbolicLink (path: string) =
    try
        (File.GetAttributes(path) &&& FileAttributes.ReparsePoint) <> enum 0
    with
    | :? FileNotFoundException
    | :? DirectoryNotFoundException -> false
    | :? UnauthorizedAccessException
    | :? IOException -> true

let private pathExists (path: string) =
    try
        File.GetAttributes(path) |> ignore
        true
    with
    | :? FileNotFoundException
    | :? DirectoryNotFoundException -> false
    | :? UnauthorizedAccessException
    | :? IOException -> true

let private validateDirectory errorDescription (directory: string) =
    if String.IsNullOrWhiteSpace directory then
        Error(errorDescription + " is invalid")
    else
        let normalized = normalizeDirectoryPath directory

        if isDisallowedDirectory normalized then
            Error(errorDescription + " is invalid")
        elif hasSymbolicLinkComponent normalized then
            Error(errorDescription + " may not contain a symbolic link")
        elif File.Exists normalized then
            Error(errorDescription + " must be a directory")
        else
            Ok normalized

let private backupPath backupRoot name =
    if validName name then
        Ok(Path.Combine(backupRoot, name) |> Path.GetFullPath)
    else
        Error "backup name is invalid"

let validateBackupName = backupPath backupDirectory

let private createConnection path mode =
    let builder = SqliteConnectionStringBuilder()
    builder.DataSource <- path
    builder.Mode <- mode
    builder.Pooling <- false
    new SqliteConnection(builder.ToString())

let private verify (path: string) =
    use connection = createConnection path SqliteOpenMode.ReadOnly
    connection.Open()
    use integrity = connection.CreateCommand()
    integrity.CommandText <- "PRAGMA integrity_check;"
    let integrityResult: string = string (integrity.ExecuteScalar())
    use foreignKeys = connection.CreateCommand()
    foreignKeys.CommandText <- "PRAGMA foreign_key_check;"
    use rows = foreignKeys.ExecuteReader()
    integrityResult = "ok" && not (rows.Read())

let private verifyFile path =
    if isSymbolicLink path then
        Error "database file may not be a symbolic link"
    elif not (File.Exists path) then
        Error "backup does not exist"
    else
        try
            if verify path then
                Ok()
            else
                Error "backup verification failed"
        with
        | :? IOException -> Error "backup verification failed"
        | :? SqliteException -> Error "backup verification failed"

let private ensureSeparateDirectories backupRoot configuration =
    let dataRoot = dataDirectory configuration |> normalizeDirectoryPath

    if backupRoot = dataRoot then
        Error "backup directory must be distinct from the data directory"
    elif hasSymbolicLinkComponent dataRoot || File.Exists dataRoot then
        Error "database data directory is invalid"
    else
        Ok()

let private acquireDataDirectoryLock fileName unavailableMessage configuration : Result<IDisposable, string> =
    let directory = dataDirectory configuration |> normalizeDirectoryPath

    if hasSymbolicLinkComponent directory || File.Exists directory then
        Error "database data directory is invalid"
    else
        try
            Directory.CreateDirectory directory |> ignore
            let lockPath = Path.Combine(directory, fileName)

            if isSymbolicLink lockPath then
                Error "database operation lock is invalid"
            else
                let lockStream =
                    new FileStream(lockPath, FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.None)

                // The process umask governs FileStream's default mode, which
                // varies by how the process was spawned (e.g. `docker
                // compose exec` never inherits container-entrypoint.sh's own
                // `umask 0077`). container-entrypoint.sh's own validator
                // requires exactly mode 600 on every file under the data
                // directory on the next fresh container start, so this must
                // not depend on umask.
                File.SetUnixFileMode(lockPath, UnixFileMode.UserRead ||| UnixFileMode.UserWrite)

                Ok(lockStream :> IDisposable)
        with
        | :? IOException -> Error unavailableMessage
        | :? UnauthorizedAccessException -> Error unavailableMessage

/// Acquires an exclusive, cross-process operation lock. Backup and restore use
/// it to serialize one-shot mutations without blocking a healthy online service.
let acquireDataDirectoryOperationLock configuration =
    acquireDataDirectoryLock operationLockFileName "database operation is already running" configuration

/// The long-running host holds this lease for its lifetime. Restore holds the
/// same lease while it runs, so it fails closed if the service is running and
/// prevents a service start from racing the replacement.
let acquireDataDirectoryServiceLock configuration =
    acquireDataDirectoryLock serviceLockFileName "restore refused while service is active" configuration

let private withDataDirectoryOperationLock configuration operation =
    match acquireDataDirectoryOperationLock configuration with
    | Error error -> Error error
    | Ok operationLock ->
        use _operationLock = operationLock
        operation ()

let private withStoppedServiceLock configuration operation =
    match acquireDataDirectoryServiceLock configuration with
    | Error error -> Error error
    | Ok serviceLock ->
        use _serviceLock = serviceLock
        operation ()

let private checkpoint (path: string) =
    use connection = createConnection path SqliteOpenMode.ReadWrite
    connection.Open()
    use command = connection.CreateCommand()
    command.CommandText <- "PRAGMA wal_checkpoint(TRUNCATE);"
    command.ExecuteNonQuery() |> ignore

let private removeCompanion path =
    if isSymbolicLink path then
        Error "database companion may not be a symbolic link"
    elif pathExists path then
        try
            File.Delete path
            Ok()
        with
        | :? IOException -> Error "database companion could not be removed"
        | :? UnauthorizedAccessException -> Error "database companion could not be removed"
    else
        Ok()

let private removeCompanions live =
    [ live + "-wal"; live + "-shm" ]
    |> List.fold (fun result companion -> result |> Result.bind (fun () -> removeCompanion companion)) (Ok())

let private validateCompanions live =
    if [ live + "-wal"; live + "-shm" ] |> List.exists isSymbolicLink then
        Error "database companion may not be a symbolic link"
    else
        Ok()

let private validateLiveForRestore live =
    if isSymbolicLink live then
        Error "live database may not be a symbolic link"
    elif File.Exists live then
        validateCompanions live
    else
        Ok()

/// Shared operation body; the public command below supplies the fixed production
/// directory, while this function makes filesystem behavior testable in a
/// disposable directory without widening the production command surface.
let backupAt backupRoot configuration name =
    match validateDirectory "backup directory" backupRoot with
    | Error error -> Error error
    | Ok normalizedBackupRoot ->
        match ensureSeparateDirectories normalizedBackupRoot configuration with
        | Error error -> Error error
        | Ok() ->
            match backupPath normalizedBackupRoot name with
            | Error error -> Error error
            | Ok destination when pathExists destination -> Error "backup already exists"
            | Ok destination ->
                withDataDirectoryOperationLock configuration (fun () ->
                    try
                        Directory.CreateDirectory normalizedBackupRoot |> ignore

                        if hasSymbolicLinkComponent normalizedBackupRoot || isSymbolicLink destination then
                            Error "backup destination may not be a symbolic link"
                        else
                            use source = openConfigured configuration
                            use target = createConnection destination SqliteOpenMode.ReadWriteCreate
                            target.Open()
                            source.BackupDatabase target
                            // The SQLite provider creates `destination` under whatever umask the
                            // invoking process has — never guaranteed to be container-entrypoint.sh's
                            // own `umask 0077` (e.g. a `docker compose exec` backup command never
                            // goes through the entrypoint at all).
                            File.SetUnixFileMode(destination, UnixFileMode.UserRead ||| UnixFileMode.UserWrite)

                            if verify destination then
                                Ok destination
                            else
                                Error "backup verification failed"
                    with
                    | :? IOException -> Error "backup failed"
                    | :? UnauthorizedAccessException -> Error "backup failed"
                    | :? SqliteException -> Error "backup failed")

/// Shared restore body paired with `backupAt` for disposable real-SQLite tests.
let restoreAt backupRoot configuration name =
    match validateDirectory "backup directory" backupRoot with
    | Error error -> Error error
    | Ok normalizedBackupRoot ->
        match ensureSeparateDirectories normalizedBackupRoot configuration with
        | Error error -> Error error
        | Ok() ->
            match backupPath normalizedBackupRoot name with
            | Error error -> Error error
            | Ok source ->
                withStoppedServiceLock configuration (fun () ->
                    withDataDirectoryOperationLock configuration (fun () ->
                        match verifyFile source with
                        | Error error -> Error error
                        | Ok() ->
                            try
                                let live = databasePath configuration
                                let staged = live + ".restore-" + Guid.NewGuid().ToString("N")
                                let preserved = live + ".replaced-" + Guid.NewGuid().ToString("N")

                                match validateLiveForRestore live with
                                | Error error -> Error error
                                | Ok() ->
                                    File.Copy(source, staged, false)
                                    // File.Copy leaves `staged`'s mode governed by the process
                                    // umask, not the source backup's mode. `staged` becomes `live`
                                    // below, and container-entrypoint.sh's validator requires
                                    // exactly mode 600 on it at the next fresh container start.
                                    File.SetUnixFileMode(staged, UnixFileMode.UserRead ||| UnixFileMode.UserWrite)

                                    // Opening `staged` to verify it (even read-only) can leave
                                    // its own -wal/-shm companions on disk. Only the single
                                    // `staged` path below moves to `live` — leaving these behind
                                    // would strand a stray file container-entrypoint.sh's file-mode
                                    // validator rejects on the next boot.
                                    if not (verify staged) then
                                        File.Delete staged
                                        removeCompanions staged |> ignore
                                        Error "backup verification failed"
                                    else
                                        match removeCompanions staged with
                                        | Error error ->
                                            File.Delete staged
                                            Error error
                                        | Ok() ->
                                            if File.Exists live then
                                                checkpoint live
                                                File.Move(live, preserved, false)

                                                match removeCompanions live with
                                                | Error error ->
                                                    File.Move(preserved, live, false)
                                                    Error error
                                                | Ok() ->
                                                    File.Move(staged, live, false)
                                                    Ok()
                                            else
                                                File.Move(staged, live, false)
                                                Ok()
                            with
                            | :? IOException -> Error "restore failed"
                            | :? UnauthorizedAccessException -> Error "restore failed"
                            | :? SqliteException -> Error "restore failed"))

let backup configuration name =
    backupAt backupDirectory configuration name

/// Verifies the live SQLite database while serializing against other one-shot
/// operations. The long-running service remains available because verification
/// opens the database read-only.
let integrity configuration =
    withDataDirectoryOperationLock configuration (fun () ->
        try
            if verify (databasePath configuration) then
                Ok()
            else
                Error "database integrity verification failed"
        with
        | :? IOException -> Error "database integrity verification failed"
        | :? SqliteException -> Error "database integrity verification failed")

let restore configuration name =
    restoreAt backupDirectory configuration name
