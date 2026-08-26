module RhinoCli.Tests.Unit.Steps.ConventionSteps

open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Convention
open RhinoCli.Tests.Unit.Steps.BddState

/// The repository root fixture built by this scenario's Given-step.
let mutable private repoRoot: string = ""

/// The single-file target built by a file-scoped emoji Given-step, when the
/// scenario scans one file rather than a whole tree.
let mutable private targetPath: string = ""

/// The relative directory path a missing-LICENSE Given-step recorded, so its
/// Then-step can assert the output names that exact directory.
let mutable private missingDirLabel: string = ""

/// Writes `content` to `path`, creating any missing parent directories.
let private ensureFile (path: string) (content: string) =
    Directory.CreateDirectory(Path.GetDirectoryName(path: string)) |> ignore
    File.WriteAllText(path, content)

// ---- Given ----

[<Given>]
let ``a repository where one app directory is missing its LICENSE file`` () =
    let dir = NewTempDir()
    Directory.CreateDirectory(Path.Combine(dir, "apps", "sample-app")) |> ignore
    repoRoot <- dir
    missingDirLabel <- "apps/sample-app"

// ---- When ----

[<When>]
let ``the developer runs "rhino-cli convention audit"`` () =
    RunWithWriter(fun () -> runConventionAudit repoRoot [])

// ---- Then ----

[<Then>]
let ``the command exits with a failure code`` () = Assert.NotEqual(0, LastExitCode)

[<Then>]
let ``the output names the failing "([^"]*)" validator`` (name: string) =
    Assert.Contains(sprintf "%s:" name, LastOutput)
