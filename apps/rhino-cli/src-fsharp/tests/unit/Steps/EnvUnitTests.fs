/// Plain xunit tests for `RhinoCli.Application.Env`'s pure helpers and the
/// `backup` confirm-callback design — behaviour with no dedicated Gherkin
/// scenario, or exercised only indirectly there (mirrors the rationale
/// `RepoConfigValidateUnitTests.fs`'s module doc comment states for its own
/// split from `RepoConfigValidateSteps.fs`). Ported from
/// `apps/rhino-cli/src/application/env/backup.rs`'s `#[cfg(test)] mod tests`.
module RhinoCli.Tests.Unit.Steps.EnvUnitTests

open System
open System.IO
open System.Text.Json
open Xunit
open RhinoCli.Application.Env

let private newTempDir () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-env-unit-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private defaultOptions (repoRoot: string) (backupDir: string) : EnvOptions =
    { RepoRoot = repoRoot
      BackupDir = backupDir
      SkipDirs = defaultSkipDirs
      MaxSize = DefaultMaxSize
      WorktreeAware = false
      WorktreeName = ""
      Force = false
      IncludeConfig = false
      DryRun = false }

let private neverConfirm () : bool =
    failwith "confirm callback must not be invoked"

// ---- expandTilde ----

[<Fact>]
let ``expandTilde replaces a leading tilde with HOME`` () =
    match expandTilde "~/foo" with
    | Ok r -> Assert.EndsWith("/foo", r)
    | Error message -> Assert.Fail(message)

[<Fact>]
let ``expandTilde leaves an absolute path unchanged`` () =
    Assert.Equal(Ok "/abs/path", expandTilde "/abs/path")

// ---- isInsideRepo ----

[<Fact>]
let ``isInsideRepo is true for a child directory`` () =
    Assert.True(isInsideRepo "/repo/sub/backup" "/repo")

[<Fact>]
let ``isInsideRepo is false for a sibling directory`` () =
    Assert.False(isInsideRepo "/other" "/repo")

// ---- canonicalizeBestEffort ----

[<Fact>]
let ``canonicalizeBestEffort resolves an existing path directly`` () =
    let dir = newTempDir ()

    try
        match canonicalizeBestEffort dir with
        | Ok resolved -> Assert.Equal(Path.GetFullPath dir, resolved)
        | Error message -> Assert.Fail(message)
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``canonicalizeBestEffort walks up to the nearest existing ancestor and rejoins the tail`` () =
    let dir = newTempDir ()

    try
        let candidate = Path.Combine(dir, "does-not-exist-yet", "nested")

        match canonicalizeBestEffort candidate with
        | Ok resolved -> Assert.Equal(Path.GetFullPath candidate, resolved)
        | Error message -> Assert.Fail(message)
    finally
        Directory.Delete(dir, true)

// ---- isSecretFile ----

[<Fact>]
let ``isSecretFile matches cert and key extensions`` () =
    Assert.True(isSecretFile "cert.pem" "cert.pem")
    Assert.True(isSecretFile "sub/dir/id.key" "id.key")
    Assert.True(isSecretFile "server.crt" "server.crt")
    Assert.True(isSecretFile "bundle.pfx" "bundle.pfx")
    Assert.False(isSecretFile "README.md" "README.md")

[<Fact>]
let ``isSecretFile matches dotenv files, secrets.json, and the .secrets directory`` () =
    Assert.True(isSecretFile ".env" ".env")
    Assert.True(isSecretFile ".env.local" ".env.local")
    Assert.True(isSecretFile "secrets.json" "secrets.json")
    Assert.True(isSecretFile ".secrets/notes.md" "notes.md")

// ---- discover ----

[<Fact>]
let ``discover finds .env files`` () =
    let dir = newTempDir ()

    try
        File.WriteAllText(Path.Combine(dir, ".env"), "x=1")
        File.WriteAllText(Path.Combine(dir, ".env.local"), "y=2")
        File.WriteAllText(Path.Combine(dir, "README.md"), "x")
        let opts = defaultOptions dir dir
        let entries = discover opts
        Assert.Equal(2, List.length entries)
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``discover finds a pem file`` () =
    let dir = newTempDir ()

    try
        File.WriteAllText(Path.Combine(dir, "cert.pem"), "x")
        let entries = discover (defaultOptions dir dir)
        Assert.Equal<string list>([ "cert.pem" ], entries |> List.map (fun e -> e.RelPath))
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``discover skips oversized files`` () =
    let dir = newTempDir ()

    try
        File.WriteAllBytes(Path.Combine(dir, ".env"), Array.zeroCreate<byte> 100)

        let opts =
            { defaultOptions dir dir with
                MaxSize = 10L }

        let entries = discover opts
        Assert.Single(entries) |> ignore
        Assert.True(entries.[0].Skipped)
        Assert.Contains("exceeds", entries.[0].Reason)
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``discover skips configured skip-dirs`` () =
    let dir = newTempDir ()

    try
        Directory.CreateDirectory(Path.Combine(dir, "node_modules")) |> ignore
        File.WriteAllText(Path.Combine(dir, "node_modules", ".env"), "x")
        File.WriteAllText(Path.Combine(dir, ".env"), "y")
        let entries = discover (defaultOptions dir dir)
        Assert.Equal<string list>([ ".env" ], entries |> List.map (fun e -> e.RelPath))
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``discover finds a file inside the .secrets directory`` () =
    let dir = newTempDir ()

    try
        Directory.CreateDirectory(Path.Combine(dir, ".secrets")) |> ignore
        File.WriteAllText(Path.Combine(dir, ".secrets", "notes.md"), "secret")
        let entries = discover (defaultOptions dir dir)
        Assert.Contains(".secrets/notes.md", entries |> List.map (fun e -> e.RelPath))
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``discover still skips the .git directory`` () =
    let dir = newTempDir ()

    try
        Directory.CreateDirectory(Path.Combine(dir, ".git")) |> ignore
        File.WriteAllText(Path.Combine(dir, ".git", "config"), "gitconfig")
        File.WriteAllText(Path.Combine(dir, ".env"), "k=v")
        let entries = discover (defaultOptions dir dir)
        Assert.DoesNotContain(entries, fun (e: EnvFileEntry) -> e.RelPath.StartsWith(".git/", StringComparison.Ordinal))
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``discover finds secrets.json`` () =
    let dir = newTempDir ()

    try
        File.WriteAllText(Path.Combine(dir, "secrets.json"), "{\"key\":\"val\"}")
        let entries = discover (defaultOptions dir dir)
        Assert.Contains("secrets.json", entries |> List.map (fun e -> e.RelPath))
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``discover marks a symlinked secret file as skipped`` () =
    let dir = newTempDir ()

    try
        let target = Path.Combine(dir, "target.txt")
        File.WriteAllText(target, "x")
        let link = Path.Combine(dir, ".env.link")
        File.CreateSymbolicLink(link, target) |> ignore
        let entries = discover (defaultOptions dir dir)
        let entry = entries |> List.find (fun e -> e.RelPath = ".env.link")
        Assert.True(entry.Skipped)
        Assert.Equal("symlink", entry.Reason)
    finally
        Directory.Delete(dir, true)

// ---- discoverConfig ----

[<Fact>]
let ``discoverConfig picks up an existing pattern`` () =
    let dir = newTempDir ()

    try
        Directory.CreateDirectory(Path.Combine(dir, ".claude")) |> ignore
        File.WriteAllText(Path.Combine(dir, ".claude", "settings.local.json"), "{}")
        let entries = discoverConfig dir defaultConfigPatterns DefaultMaxSize
        Assert.NotEmpty(entries)
        Assert.Equal("config", entries.[0].Source)
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``discoverConfig returns nothing when no pattern exists`` () =
    let dir = newTempDir ()

    try
        Assert.Empty(discoverConfig dir defaultConfigPatterns DefaultMaxSize)
    finally
        Directory.Delete(dir, true)

// ---- findExisting ----

[<Fact>]
let ``findExisting returns the intersection of entries and destination files`` () =
    let dir = newTempDir ()

    try
        File.WriteAllText(Path.Combine(dir, "a.txt"), "x")

        let entries =
            [ { RelPath = "a.txt"
                AbsPath = ""
                Size = 0L
                Skipped = false
                Reason = ""
                Source = "" }
              { RelPath = "b.txt"
                AbsPath = ""
                Size = 0L
                Skipped = false
                Reason = ""
                Source = "" } ]

        Assert.Equal<string list>([ "a.txt" ], findExisting entries dir)
    finally
        Directory.Delete(dir, true)

// ---- detectWorktree ----

[<Fact>]
let ``detectWorktree reports a normal repository`` () =
    let dir = newTempDir ()

    try
        Directory.CreateDirectory(Path.Combine(dir, ".git")) |> ignore

        match detectWorktree dir with
        | Ok info ->
            Assert.False(info.IsWorktree)
            Assert.NotEqual<string>("", info.WorktreeName)
        | Error message -> Assert.Fail(message)
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``detectWorktree reports a linked worktree`` () =
    let dir = newTempDir ()

    try
        File.WriteAllText(Path.Combine(dir, ".git"), "gitdir: /elsewhere/.git")

        match detectWorktree dir with
        | Ok info -> Assert.True(info.IsWorktree)
        | Error message -> Assert.Fail(message)
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``detectWorktree fails when no .git is present`` () =
    let dir = newTempDir ()

    try
        match detectWorktree dir with
        | Error _ -> ()
        | Ok _ -> Assert.Fail("expected an error when no .git is present")
    finally
        Directory.Delete(dir, true)

// ---- backup ----

[<Fact>]
let ``backup rejects a backup dir inside the repo`` () =
    let dir = newTempDir ()

    try
        let opts = defaultOptions dir (Path.Combine(dir, "subdir"))

        match backup opts neverConfirm with
        | Error _ -> ()
        | Ok _ -> Assert.Fail("expected an error for a backup dir inside the repo")
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``backup copies files`` () =
    let repo = newTempDir ()
    let dest = newTempDir ()

    try
        File.WriteAllText(Path.Combine(repo, ".env"), "k=v")

        let opts =
            { defaultOptions repo dest with
                Force = true }

        match backup opts neverConfirm with
        | Ok r ->
            Assert.Equal(1, r.Copied)
            Assert.True(File.Exists(Path.Combine(dest, ".env")))
        | Error message -> Assert.Fail(message)
    finally
        Directory.Delete(repo, true)
        Directory.Delete(dest, true)

[<Fact>]
let ``backup dry-run writes nothing`` () =
    let repo = newTempDir ()
    let dest = newTempDir ()

    try
        File.WriteAllText(Path.Combine(repo, ".env"), "k=v")

        let opts =
            { defaultOptions repo dest with
                Force = true
                DryRun = true }

        match backup opts neverConfirm with
        | Ok r ->
            Assert.Equal(0, r.Copied)
            Assert.False(File.Exists(Path.Combine(dest, ".env")))
        | Error message -> Assert.Fail(message)
    finally
        Directory.Delete(repo, true)
        Directory.Delete(dest, true)

[<Fact>]
let ``backup with Force never invokes confirm and overwrites unconditionally`` () =
    let repo = newTempDir ()
    let dest = newTempDir ()

    try
        File.WriteAllText(Path.Combine(repo, ".env"), "new")
        File.WriteAllText(Path.Combine(dest, ".env"), "old")

        let opts =
            { defaultOptions repo dest with
                Force = true }

        match backup opts neverConfirm with
        | Ok r ->
            Assert.Equal(1, r.Copied)
            Assert.Equal("new", File.ReadAllText(Path.Combine(dest, ".env")))
        | Error message -> Assert.Fail(message)
    finally
        Directory.Delete(repo, true)
        Directory.Delete(dest, true)

[<Fact>]
let ``backup with no conflicts never invokes confirm`` () =
    let repo = newTempDir ()
    let dest = newTempDir ()

    try
        File.WriteAllText(Path.Combine(repo, ".env"), "k=v")
        let opts = defaultOptions repo dest

        match backup opts neverConfirm with
        | Ok r -> Assert.Equal(1, r.Copied)
        | Error message -> Assert.Fail(message)
    finally
        Directory.Delete(repo, true)
        Directory.Delete(dest, true)

[<Fact>]
let ``backup invokes confirm exactly once on a real conflict and proceeds when it returns true`` () =
    let repo = newTempDir ()
    let dest = newTempDir ()

    try
        File.WriteAllText(Path.Combine(repo, ".env"), "new")
        File.WriteAllText(Path.Combine(dest, ".env"), "old")
        let opts = defaultOptions repo dest
        let mutable callCount = 0

        let confirm () =
            callCount <- callCount + 1
            true

        match backup opts confirm with
        | Ok r ->
            Assert.Equal(1, callCount)
            Assert.False(r.Cancelled)
            Assert.Equal("new", File.ReadAllText(Path.Combine(dest, ".env")))
        | Error message -> Assert.Fail(message)
    finally
        Directory.Delete(repo, true)
        Directory.Delete(dest, true)

[<Fact>]
let ``backup cancels and leaves the destination unchanged when confirm returns false`` () =
    let repo = newTempDir ()
    let dest = newTempDir ()

    try
        File.WriteAllText(Path.Combine(repo, ".env"), "new")
        File.WriteAllText(Path.Combine(dest, ".env"), "old")
        let opts = defaultOptions repo dest
        let mutable callCount = 0

        let confirm () =
            callCount <- callCount + 1
            false

        match backup opts confirm with
        | Ok r ->
            Assert.Equal(1, callCount)
            Assert.True(r.Cancelled)
            Assert.Equal("old", File.ReadAllText(Path.Combine(dest, ".env")))
        | Error message -> Assert.Fail(message)
    finally
        Directory.Delete(repo, true)
        Directory.Delete(dest, true)

[<Fact>]
let ``backup tags entries as env when include-config is set`` () =
    let repo = newTempDir ()
    let dest = newTempDir ()

    try
        File.WriteAllText(Path.Combine(repo, ".env"), "k=v")
        Directory.CreateDirectory(Path.Combine(repo, ".claude")) |> ignore
        File.WriteAllText(Path.Combine(repo, ".claude", "settings.local.json"), "{}")

        let opts =
            { defaultOptions repo dest with
                Force = true
                IncludeConfig = true }

        match backup opts neverConfirm with
        | Ok r ->
            Assert.Equal(2, r.Copied)
            let envEntry = r.Files |> List.find (fun f -> f.RelPath = ".env")
            Assert.Equal("env", envEntry.Source)

            let configEntry =
                r.Files |> List.find (fun f -> f.RelPath = ".claude/settings.local.json")

            Assert.Equal("config", configEntry.Source)
        | Error message -> Assert.Fail(message)
    finally
        Directory.Delete(repo, true)
        Directory.Delete(dest, true)

[<Fact>]
let ``backup namespaces the destination by worktree name when worktree-aware`` () =
    let repo = newTempDir ()
    let dest = newTempDir ()

    try
        File.WriteAllText(Path.Combine(repo, ".env"), "k=v")

        let opts =
            { defaultOptions repo dest with
                Force = true
                WorktreeAware = true
                WorktreeName = "feature-branch" }

        match backup opts neverConfirm with
        | Ok _ -> Assert.True(File.Exists(Path.Combine(dest, "feature-branch", ".env")))
        | Error message -> Assert.Fail(message)
    finally
        Directory.Delete(repo, true)
        Directory.Delete(dest, true)

// ---- capitalize ----

[<Fact>]
let ``capitalize upcases the first character only`` () =
    Assert.Equal("Backup", capitalize "backup")
    Assert.Equal("", capitalize "")

// ---- formatText / formatJson / formatMarkdown ----

let private sampleResult () : EnvOperationResult =
    { Direction = "backup"
      Dir = "/tmp/bk"
      Files =
        [ { RelPath = ".env"
            AbsPath = ""
            Size = 10L
            Skipped = false
            Reason = ""
            Source = "" }
          { RelPath = ".env.large"
            AbsPath = ""
            Size = 999_999_999L
            Skipped = true
            Reason = "exceeds 1 MB"
            Source = "" }
          { RelPath = ".envrc"
            AbsPath = ""
            Size = 50L
            Skipped = false
            Reason = ""
            Source = "config" } ]
      Copied = 2
      Skipped = 1
      Errors = []
      WorktreeName = ""
      Cancelled = false
      DryRun = false }

[<Fact>]
let ``formatText reports the summary and config count`` () =
    let s = formatText (sampleResult ()) false false
    Assert.Contains("Backup complete", s)
    Assert.Contains("(1 config)", s)

[<Fact>]
let ``formatText quiet mode suppresses per-file lines`` () =
    let s = formatText (sampleResult ()) false true
    Assert.Contains("Backup complete", s)
    Assert.DoesNotContain("BACKUP  .env", s)

[<Fact>]
let ``formatText verbose mode lists skipped files`` () =
    let s = formatText (sampleResult ()) true false
    Assert.Contains("SKIPPED  .env.large", s)

[<Fact>]
let ``formatText reports cancellation`` () =
    let r =
        { sampleResult () with
            Cancelled = true }

    Assert.Contains("cancelled", formatText r false false)

[<Fact>]
let ``formatJson round-trips through JsonDocument`` () =
    let s = formatJson (sampleResult ())
    use doc = JsonDocument.Parse(s)
    Assert.Equal("backup", doc.RootElement.GetProperty("direction").GetString())
    Assert.Equal(2, doc.RootElement.GetProperty("copied").GetInt32())

[<Fact>]
let ``formatMarkdown renders the report header and table`` () =
    let s = formatMarkdown (sampleResult ())
    Assert.Contains("## Backup Report", s)
    Assert.Contains("**Copied**: 2", s)
    Assert.Contains("| File |", s)

[<Fact>]
let ``formatMarkdown reports cancellation`` () =
    let r =
        { sampleResult () with
            Cancelled = true }

    Assert.Contains("cancelled", formatMarkdown r)
