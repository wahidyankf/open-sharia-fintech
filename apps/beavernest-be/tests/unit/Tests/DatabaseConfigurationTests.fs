/// `isDisallowedDirectory` compares its argument against `Directory.GetCurrentDirectory()`,
/// which is process-wide state. `EnvTierLoaderTests` in this same assembly calls
/// `Directory.SetCurrentDirectory` to exercise tier-file discovery, so with xUnit's default
/// collection parallelism the swap can land between this module computing a case from the
/// current directory and the validator re-reading it — the guard then sees no containment and
/// the input is wrongly accepted. `xunit.runner.json` disables that parallelism for this
/// assembly; do not re-enable it without first removing the shared mutable directory.
module BeaverNestBe.Tests.Unit.Tests.DatabaseConfigurationTests

open System
open System.IO
open Xunit
open BeaverNestBe.Domain.DatabaseConfiguration

[<Fact>]
let ``database configuration derives the fixed SQLite filename from a data directory`` () =
    let directory =
        Path.Combine(Path.GetTempPath(), "beavernest-test-" + Guid.NewGuid().ToString("N"))

    let configuration = create directory 100 |> Result.defaultWith failwith
    Assert.Equal(Path.Combine(Path.GetFullPath(directory), databaseFileName), databasePath configuration)
    Assert.Equal(Path.GetFullPath(directory), dataDirectory configuration)
    Assert.Equal(100, busyTimeoutMilliseconds configuration)

[<Fact>]
let ``database configuration refuses empty, root, home, repository, and nonpositive timeout values`` () =
    let invalidCases =
        [ "", 100
          "   ", 100
          Path.GetPathRoot(Path.GetTempPath()), 100
          Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), 100
          Directory.GetCurrentDirectory(), 100
          Path.Combine(Path.GetTempPath(), "beavernest-timeout-" + Guid.NewGuid().ToString("N")), 0
          Path.Combine(Path.GetTempPath(), "beavernest-timeout-" + Guid.NewGuid().ToString("N")), -1 ]

    invalidCases
    |> List.iter (fun (directory, timeout) -> Assert.True(create directory timeout |> Result.isError))

[<Fact>]
let ``database configuration refuses a directory nested inside the current working directory`` () =
    let subdirectory =
        Path.Combine(Directory.GetCurrentDirectory(), "beavernest-subdir-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(subdirectory) |> ignore

    try
        Assert.True(create subdirectory 100 |> Result.isError)
    finally
        Directory.Delete(subdirectory, true)

[<Fact>]
let ``database configuration refuses a directory that is an ancestor of the current working directory`` () =
    // The reverse containment direction from the "nested inside cwd" case above:
    // a data directory that is an *ancestor* of cwd (e.g. cwd's parent) must be
    // rejected too, mirroring infra/dev/beavernest-app/scripts/lib.sh's second
    // `case "$beavernest_repository_root" in "$beavernest_canonical"/*)` arm.
    let ancestor = Directory.GetParent(Directory.GetCurrentDirectory()).FullName

    Assert.True(create ancestor 100 |> Result.isError)

[<Fact>]
let ``database configuration refuses an explicit symbolic-link component`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "beavernest-link-" + Guid.NewGuid().ToString("N"))

    let target = Path.Combine(root, "target")
    let link = Path.Combine(root, "link")
    Directory.CreateDirectory(target) |> ignore
    Directory.CreateSymbolicLink(link, target) |> ignore

    try
        Assert.True(create (Path.Combine(link, "child")) 100 |> Result.isError)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``database configuration rejects an existing file passed as its data directory`` () =
    let filePath =
        Path.Combine(Path.GetTempPath(), "beavernest-data-file-" + Guid.NewGuid().ToString("N"))

    File.WriteAllText(filePath, "not a directory")

    try
        Assert.Equal(Error "database data directory must be a directory", create filePath 100)
    finally
        File.Delete(filePath)

[<Fact>]
let ``database environment uses safe defaults and parses only positive timeouts`` () =
    let from entries =
        fromEnvironment (fun key -> entries |> Map.tryFind key |> Option.toObj)

    let defaultConfiguration = from Map.empty |> Result.defaultWith failwith
    Assert.Equal("/var/lib/beavernest", dataDirectory defaultConfiguration)
    Assert.Equal(5000, busyTimeoutMilliseconds defaultConfiguration)

    let explicitDirectory =
        Path.Combine(Path.GetTempPath(), "beavernest-env-" + Guid.NewGuid().ToString("N"))

    let explicitConfiguration =
        from (
            Map.ofList
                [ "BEAVERNEST_BE_DATA_DIRECTORY", explicitDirectory
                  "BEAVERNEST_BE_SQLITE_BUSY_TIMEOUT_MILLISECONDS", "75" ]
        )
        |> Result.defaultWith failwith

    Assert.Equal(Path.GetFullPath(explicitDirectory), dataDirectory explicitConfiguration)
    Assert.Equal(75, busyTimeoutMilliseconds explicitConfiguration)

    let fallbackTimeout =
        from (
            Map.ofList
                [ "BEAVERNEST_BE_DATA_DIRECTORY", explicitDirectory
                  "BEAVERNEST_BE_SQLITE_BUSY_TIMEOUT_MILLISECONDS", "not-a-number" ]
        )
        |> Result.defaultWith failwith

    Assert.Equal(5000, busyTimeoutMilliseconds fallbackTimeout)
