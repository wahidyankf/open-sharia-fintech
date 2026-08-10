module BeaverNestBe.Domain.DatabaseConfiguration

open System
open System.IO

type DatabaseConfiguration =
    private
        { DataDirectory: string
          DatabasePath: string
          BusyTimeoutMilliseconds: int }

let databaseFileName = "beavernest.sqlite3"

let private normalizeDirectoryPath (path: string) =
    Path.GetFullPath(path) |> Path.TrimEndingDirectorySeparator

let private isDisallowedDirectory (path: string) =
    let normalized = normalizeDirectoryPath path
    let root = Path.GetPathRoot normalized

    let home =
        Environment.GetFolderPath Environment.SpecialFolder.UserProfile
        |> normalizeDirectoryPath

    let repository = Directory.GetCurrentDirectory() |> normalizeDirectoryPath
    normalized = root || normalized = home || normalized = repository

let private isSymbolicLink (path: string) =
    try
        (File.GetAttributes(path) &&& FileAttributes.ReparsePoint) <> enum 0
    with
    | :? FileNotFoundException
    | :? DirectoryNotFoundException -> false
    | :? UnauthorizedAccessException
    | :? IOException -> true

/// Checks every existing component without resolving it. `/var` and `/tmp` are
/// platform-owned aliases on macOS, whereas all operator-controlled components
/// must be direct directories rather than symbolic links.
let hasSymbolicLinkComponent (path: string) =
    let rec inspect current =
        let parent = Directory.GetParent(current)
        let isSystemTemporaryAlias = current = "/var" || current = "/tmp"

        let isLink = not isSystemTemporaryAlias && isSymbolicLink current

        if isLink then true
        elif isNull parent then false
        else inspect parent.FullName

    inspect (normalizeDirectoryPath path)

let create (dataDirectory: string) (busyTimeoutMilliseconds: int) : Result<DatabaseConfiguration, string> =
    if String.IsNullOrWhiteSpace dataDirectory then
        Error "database data directory is not permitted"
    else
        let directory = normalizeDirectoryPath dataDirectory

        if isDisallowedDirectory directory then
            Error "database data directory is not permitted"
        elif hasSymbolicLinkComponent directory then
            Error "database data directory may not contain a symbolic link"
        elif File.Exists directory then
            Error "database data directory must be a directory"
        elif busyTimeoutMilliseconds <= 0 then
            Error "SQLite busy timeout must be finite and positive"
        else
            Ok
                { DataDirectory = directory
                  DatabasePath = Path.Combine(directory, databaseFileName)
                  BusyTimeoutMilliseconds = busyTimeoutMilliseconds }

let fromEnvironment (readEnvironment: string -> string) =
    let directory =
        match readEnvironment "BEAVERNEST_BE_DATA_DIRECTORY" with
        | null
        | "" -> "/var/lib/beavernest"
        | value -> value

    let timeout =
        match Int32.TryParse(readEnvironment "BEAVERNEST_BE_SQLITE_BUSY_TIMEOUT_MILLISECONDS") with
        | true, value -> value
        | _ -> 5000

    create directory timeout

let dataDirectory configuration = configuration.DataDirectory
let databasePath configuration = configuration.DatabasePath
let busyTimeoutMilliseconds configuration = configuration.BusyTimeoutMilliseconds
