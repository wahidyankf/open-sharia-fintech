module RhinoCli.Tests.E2E.Steps.CargoTargetShareProcessSteps

open System
open System.Diagnostics
open System.IO
open TickSpec
open Xunit

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/system/cargo-target-share.feature" ]

let private repositoryRoot =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "..", ".."))

let private executable =
    Path.Combine(repositoryRoot, "apps", "rhino-cli", "src", "dist", "rhino-cli-fsharp")

type private RunResult =
    { ExitCode: int
      Stdout: string
      Stderr: string }

let private run exe args cwd environment =
    let info =
        ProcessStartInfo(
            FileName = exe,
            WorkingDirectory = cwd,
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true
        )

    args |> List.iter info.ArgumentList.Add
    environment |> List.iter (fun (key, value) -> info.Environment.[key] <- value)
    use proc = Process.Start info
    let stdout = proc.StandardOutput.ReadToEnd()
    let stderr = proc.StandardError.ReadToEnd()
    proc.WaitForExit()

    { ExitCode = proc.ExitCode
      Stdout = stdout
      Stderr = stderr }

let private gitPath =
    (run "/usr/bin/which" [ "git" ] repositoryRoot []).Stdout.Trim()

let private git cwd args =
    let result =
        run gitPath args cwd [ "GIT_CONFIG_GLOBAL", "/dev/null"; "GIT_CONFIG_SYSTEM", "/dev/null" ]

    Assert.Equal(0, result.ExitCode)

let private writeCargoCrate root parent name =
    let crate = Path.Combine(root, parent, name)
    Directory.CreateDirectory(Path.Combine(crate, "src")) |> ignore

    File.WriteAllText(
        Path.Combine(crate, "Cargo.toml"),
        $"[package]\nname = \"{name}\"\nversion = \"0.1.0\"\nedition = \"2021\"\n"
    )

    File.WriteAllText(Path.Combine(crate, "src", "main.rs"), "fn main() {}\n\n#[test]\nfn works() { assert!(true); }\n")
    crate

type CargoTargetShareProcessWorld() =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-cargo-e2e-" + Guid.NewGuid().ToString("N"))

    let cache = Path.Combine(root, "shared-cache")
    let repo = Path.Combine(root, "repo")
    let mutable crate: string option = None
    let mutable linkedCrate: string option = None
    let mutable ci = false
    let mutable fix = false
    let mutable prune = false
    let mutable dryRun = false
    let mutable result: RunResult option = None
    let mutable linkBefore: string option = None
    let mutable resolvedLinks: string list = []
    let commandPath = Path.GetDirectoryName gitPath

    let orphan () =
        Path.Combine(cache, Path.GetFileName(repo), "orphan-crate")

    do
        Directory.CreateDirectory repo |> ignore
        git repo [ "init"; "--quiet"; "-b"; "main" ]
        git repo [ "config"; "user.name"; "Rhino Fixture" ]
        git repo [ "config"; "user.email"; "rhino@example.invalid" ]
        File.WriteAllText(Path.Combine(repo, "README.md"), "fixture")
        git repo [ "add"; "." ]
        git repo [ "commit"; "--quiet"; "-m"; "init" ]

    let invoke cwd =
        let args =
            [ "doctor"; "--tools"; "git" ]
            @ (if fix then [ "--fix" ] else [])
            @ (if prune then [ "--prune-cargo-cache" ] else [])
            @ (if dryRun then [ "--dry-run" ] else [])

        let environment =
            [ "PATH", commandPath
              "HOME", Path.Combine(root, "home")
              "OSE_CARGO_TARGET_CACHE", cache
              "GIT_CONFIG_GLOBAL", "/dev/null"
              "GIT_CONFIG_SYSTEM", "/dev/null"
              "CI", if ci then "1" else ""
              "GITHUB_ACTIONS", "" ]

        result <- Some(run executable args cwd environment)
        Assert.Equal(0, result.Value.ExitCode)

    let commitCrates () =
        git repo [ "add"; "." ]
        git repo [ "commit"; "--quiet"; "-m"; "add crates" ]

    let addLinkedWorktree () =
        let linked = Path.Combine(root, "linked")
        git repo [ "worktree"; "add"; "--quiet"; "--detach"; linked ]
        linked

    [<Given>]
    member _.``a Rust crate with a plain target directory exists in a repo checkout outside CI``() =
        let value = writeCargoCrate repo "apps" "foo"
        Directory.CreateDirectory(Path.Combine(value, "target")) |> ignore
        crate <- Some value

    [<Given>]
    member _.``a crate's target is already the correct symlink into the shared cache``() =
        let value = writeCargoCrate repo "apps" "foo"
        crate <- Some value
        fix <- true
        invoke repo
        linkBefore <- Some(DirectoryInfo(Path.Combine(value, "target")).LinkTarget)

    [<Given>]
    member _.``a crate's target is a plain rebuildable directory containing stale artifacts``() =
        let value = writeCargoCrate repo "apps" "foo"
        Directory.CreateDirectory(Path.Combine(value, "target")) |> ignore
        File.WriteAllText(Path.Combine(value, "target", "stale"), "stale")
        crate <- Some value

    [<Given>]
    member _.``a crate's target is a plain directory not yet symlinked into the shared cache``() =
        let value = writeCargoCrate repo "apps" "foo"
        Directory.CreateDirectory(Path.Combine(value, "target")) |> ignore
        crate <- Some value

    [<Given>]
    member _.``the environment variable CI is set``() =
        ci <- true

        if crate.IsNone then
            crate <- Some(writeCargoCrate repo "apps" "foo")

        Directory.CreateDirectory(orphan ()) |> ignore

    [<Given>]
    member _.``a repo checkout contains multiple Rust crates under apps and libs outside CI``() =
        writeCargoCrate repo "apps" "a" |> ignore
        writeCargoCrate repo "apps" "b" |> ignore
        writeCargoCrate repo "libs" "c" |> ignore

    [<Given>]
    member _.``two worktrees of the same repo each have a crate's target symlinked by the doctor``() =
        let main = writeCargoCrate repo "apps" "foo"
        crate <- Some main
        commitCrates ()
        let linked = addLinkedWorktree ()
        linkedCrate <- Some(Path.Combine(linked, "apps", "foo"))
        fix <- true
        invoke repo

    [<Given>]
    member _.``a linked worktree holds a crate whose target is still a plain directory outside CI``() =
        let main = writeCargoCrate repo "apps" "foo"
        crate <- Some main
        commitCrates ()
        let linked = addLinkedWorktree ()
        let linkedValue = Path.Combine(linked, "apps", "foo")
        Directory.CreateDirectory(Path.Combine(linkedValue, "target")) |> ignore
        linkedCrate <- Some linkedValue

    [<Given>]
    member _.``a crate's target is a symlink into the shared cache``() =
        let value = writeCargoCrate repo "apps" "foo"
        crate <- Some value
        fix <- true
        invoke repo

    [<Given>]
    member _.``the shared cache holds an entry for a crate that no longer exists in the repo outside CI``() =
        Directory.CreateDirectory(orphan ()) |> ignore

    [<Given>]
    member _.``a shared-cache entry is the symlink target of a crate in a live worktree``() =
        let value = writeCargoCrate repo "apps" "foo"
        crate <- Some value
        fix <- true
        invoke repo
        Directory.CreateDirectory(orphan ()) |> ignore

    [<Given>]
    member _.``a shared-cache entry is referenced only by a crate in a separate linked worktree``() =
        let main = writeCargoCrate repo "apps" "foo"
        crate <- Some main
        commitCrates ()
        let linked = addLinkedWorktree ()
        let linkedValue = Path.Combine(linked, "apps", "foo")
        linkedCrate <- Some linkedValue
        fix <- true
        invoke repo
        Directory.Delete(Path.Combine(main, "target"), false)
        Directory.CreateDirectory(orphan ()) |> ignore

    [<Given>]
    member _.``the shared cache holds at least one orphaned entry outside CI``() =
        Directory.CreateDirectory(orphan ()) |> ignore

    [<Given>]
    member _.``cargo-sweep is not installed on the developer's PATH``() =
        let candidate = Path.Combine(commandPath, "cargo-sweep")
        Assert.False(File.Exists(candidate), sprintf "unexpected cargo-sweep fixture at %s" candidate)

    [<When>]
    member _.``the developer runs the doctor command with the fix flag``() =
        fix <- true
        invoke repo

    [<When>]
    member _.``the developer runs the doctor command with the fix flag outside CI``() =
        fix <- true
        invoke repo

    [<When>]
    member _.``the developer runs the doctor command with the fix flag from the main checkout``() =
        fix <- true
        invoke repo

    [<When>]
    member _.``the developer runs the doctor command without the fix flag``() = invoke repo

    [<When>]
    member _.``the developer runs the doctor command with the fix flag a second time``() =
        fix <- true
        invoke repo

    [<When>]
    member _.``both symlinks are resolved``() =
        resolvedLinks <-
            [ crate.Value; linkedCrate.Value ]
            |> List.map (fun value -> DirectoryInfo(Path.Combine(value, "target")).LinkTarget)

    [<When>]
    member _.``the developer builds and tests that crate through Cargo``() =
        let manifest = Path.Combine(crate.Value, "Cargo.toml")
        Assert.Equal(0, (run "cargo" [ "build"; "--quiet"; "--manifest-path"; manifest ] repo []).ExitCode)
        Assert.Equal(0, (run "cargo" [ "test"; "--quiet"; "--manifest-path"; manifest ] repo []).ExitCode)

    [<When>]
    member _.``the developer runs the doctor command with the prune flag``() =
        prune <- true
        invoke repo

    [<When>]
    member _.``the developer runs the doctor command with the prune and dry-run flags``() =
        prune <- true
        dryRun <- true
        invoke repo

    [<Then>]
    member _.``the crate's target becomes a symlink into the shared cargo-target cache``() =
        Assert.NotNull(DirectoryInfo(Path.Combine(crate.Value, "target")).LinkTarget)

    [<Then>]
    member _.``the symlink resolves under the repo's own shared-cache namespace``() =
        Assert.StartsWith(cache, DirectoryInfo(Path.Combine(crate.Value, "target")).LinkTarget)

    [<Then>]
    member _.``the command exits successfully without recreating or altering the symlink``() =
        Assert.Equal(linkBefore.Value, DirectoryInfo(Path.Combine(crate.Value, "target")).LinkTarget)

    [<Then>]
    member _.``the plain directory is discarded and the target becomes a symlink into the shared cache``() =
        let link = DirectoryInfo(Path.Combine(crate.Value, "target")).LinkTarget in
        Assert.NotNull(link)
        Assert.False(File.Exists(Path.Combine(link, "stale")))

    [<Then>]
    member _.``the output reports that crate's target as needing to be shared``() =
        Assert.Contains("need sharing", result.Value.Stdout)

    [<Then>]
    member _.``the plain target directory is left unchanged``() =
        Assert.Null(DirectoryInfo(Path.Combine(crate.Value, "target")).LinkTarget)

    [<Then>]
    member _.``no target symlink is created for any crate``() =
        Assert.Null(DirectoryInfo(Path.Combine(crate.Value, "target")).LinkTarget)

    [<Then>]
    member _.``the command exits successfully with a message that CI was detected``() =
        Assert.Contains("CI detected", result.Value.Stdout)

    [<Then>]
    member _.``every discovered crate's target is a symlink into the shared cache``() =
        [ "apps/a"; "apps/b"; "libs/c" ]
        |> List.iter (fun rel -> Assert.NotNull(DirectoryInfo(Path.Combine(repo, rel, "target")).LinkTarget))

    [<Then>]
    member _.``no crate is skipped due to a hardcoded crate list``() =
        Assert.Contains("3 created", result.Value.Stdout)

    [<Then>]
    member _.``both point at the same shared-cache directory for that repo and crate``() =
        Assert.Equal(resolvedLinks.[0], resolvedLinks.[1])

    [<Then>]
    member _.``a disk usage measurement across the worktrees counts that directory only once``() =
        Assert.Single(List.distinct resolvedLinks) |> ignore

    [<Then>]
    member _.``that linked worktree's crate target becomes a symlink into the shared cache``() =
        Assert.NotNull(DirectoryInfo(Path.Combine(linkedCrate.Value, "target")).LinkTarget)

    [<Then>]
    member _.``it resolves to the same shared-cache entry as the main checkout's crate``() =
        Assert.Equal(
            DirectoryInfo(Path.Combine(crate.Value, "target")).LinkTarget,
            DirectoryInfo(Path.Combine(linkedCrate.Value, "target")).LinkTarget
        )

    [<Then>]
    member _.``the build emits the expected dist binary``() =
        Assert.True(File.Exists(Path.Combine(crate.Value, "target", "debug", "foo")))

    [<Then>]
    member _.``the tests pass without reference to a per-worktree target directory``() =
        Assert.StartsWith(cache, DirectoryInfo(Path.Combine(crate.Value, "target")).LinkTarget)

    [<Then>]
    member _.``the orphaned cache entry is deleted``() =
        Assert.False(Directory.Exists(orphan ()))

    [<Then>]
    member _.``every entry still referenced by a live worktree or checkout is preserved``() =
        if crate.IsSome then
            Assert.True(Directory.Exists(DirectoryInfo(Path.Combine(crate.Value, "target")).LinkTarget))

    [<Then>]
    member _.``that referenced cache entry is left in place``() =
        Assert.True(Directory.Exists(DirectoryInfo(Path.Combine(crate.Value, "target")).LinkTarget))

    [<Then>]
    member _.``only entries with no live referrer are removed``() =
        Assert.False(Directory.Exists(orphan ()))

    [<Then>]
    member _.``the entry referenced only by the linked worktree is left in place``() =
        Assert.True(Directory.Exists(DirectoryInfo(Path.Combine(linkedCrate.Value, "target")).LinkTarget))

    [<Then>]
    member _.``no cache entry is deleted``() =
        Assert.True(Directory.Exists(orphan ()))

    [<Then>]
    member _.``the orphaned entry is reported as a candidate for deletion``() =
        Assert.Contains("candidate", result.Value.Stdout)

    [<Then>]
    member _.``no cache entry is actually removed``() =
        Assert.True(Directory.Exists(orphan ()))

    [<Then>]
    member _.``the sweep step is reported as skipped rather than failing the command``() =
        Assert.Contains("cargo-sweep not installed", result.Value.Stdout)

    [<Then>]
    member _.``the command exits successfully``() = Assert.Equal(0, result.Value.ExitCode)

    [<AfterScenario>]
    member _.Cleanup() =
        if Directory.Exists root then
            Directory.Delete(root, true)

module private FeatureRunner =
    let private path =
        Path.GetFullPath(
            Path.Combine(
                __SOURCE_DIRECTORY__,
                "..",
                "..",
                "..",
                "..",
                "..",
                "specs",
                "apps",
                "rhino",
                "cli",
                "behaviours",
                "system",
                "cargo-target-share.feature"
            )
        )

    let run title =
        let lines = File.ReadAllLines path

        let featureLine =
            lines |> Array.find (fun line -> line.TrimStart().StartsWith("Feature:"))

        let start =
            lines |> Array.findIndex (fun line -> line.Trim() = "Scenario: " + title)

        let finish =
            lines
            |> Array.skip (start + 1)
            |> Array.tryFindIndex (fun line -> line.TrimStart().StartsWith("Scenario:"))
            |> Option.map (fun offset -> start + 1 + offset)
            |> Option.defaultValue lines.Length

        let feature =
            StepDefinitions([| typeof<CargoTargetShareProcessWorld> |])
                .GenerateFeature(path, Array.append [| featureLine; "" |] lines.[start .. finish - 1])

        (Seq.exactlyOne feature.Scenarios).Action.Invoke()

[<Theory>]
[<InlineData("doctor --fix symlinks a crate's target into the shared cache")>]
[<InlineData("the doctor fix step is idempotent")>]
[<InlineData("doctor --fix replaces an existing plain target directory with a symlink")>]
[<InlineData("doctor check reports a crate whose target is not yet shared")>]
[<InlineData("the doctor symlink step no-ops under CI")>]
[<InlineData("dynamic discovery covers every crate under apps and libs")>]
[<InlineData("two worktrees of the same repo share one physical target")>]
[<InlineData("doctor --fix from the main checkout also shares every linked worktree's target")>]
[<InlineData("builds and tests resolve through the symlink")>]
[<InlineData("prune removes an orphaned shared-cache entry")>]
[<InlineData("prune preserves a cache entry referenced by a live worktree")>]
[<InlineData("prune from the main worktree preserves an entry referenced only by a linked worktree")>]
[<InlineData("the prune step no-ops under CI")>]
[<InlineData("prune dry-run previews deletions without removing anything")>]
[<InlineData("stale-artifact sweep degrades gracefully when cargo-sweep is absent")>]
let ``cargo target-share behaviour crosses the published process`` title = FeatureRunner.run title
