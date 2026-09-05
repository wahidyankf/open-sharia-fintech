/// `git lockfile sync` — regenerates a staged app's `package-lock.json`
/// when it disagrees with its `package.json` manifest, then stages the
/// regenerated lockfile, so a stale lockfile never reaches a commit
/// [Repo-grounded — `apps/rhino-cli/src/commands/git/lockfile.rs`].
module RhinoCli.Application.Git

open System
open System.Diagnostics.CodeAnalysis
open System.Diagnostics
open System.IO
open System.Text.Json

/// Root package fields that must agree with the lockfile's root package
/// entry for that lockfile to be considered current
/// [Repo-grounded — `commands/git/lockfile.rs::LOCKFILE_ROOT_FIELDS`].
let private lockfileRootFields: string list =
    [ "name"
      "version"
      "license"
      "dependencies"
      "devDependencies"
      "optionalDependencies"
      "peerDependencies"
      "peerDependenciesMeta"
      "engines"
      "bin"
      "workspaces"
      "os"
      "cpu" ]

/// Deep, key-order-independent JSON equality mirroring `serde_json::Value`'s
/// own `PartialEq` — objects compare as maps regardless of member order,
/// arrays compare element-by-element in order, and scalars compare by
/// value, not by source formatting.
let rec private jsonValueEquals (a: JsonElement) (b: JsonElement) : bool =
    if a.ValueKind <> b.ValueKind then
        false
    else
        match a.ValueKind with
        | JsonValueKind.Object ->
            let bProps = b.EnumerateObject() |> Seq.map (fun p -> p.Name, p.Value) |> Map.ofSeq

            let aProps = a.EnumerateObject() |> List.ofSeq

            List.length aProps = Map.count bProps
            && aProps
               |> List.forall (fun p ->
                   match Map.tryFind p.Name bProps with
                   | Some bValue -> jsonValueEquals p.Value bValue
                   | None -> false)
        | JsonValueKind.Array ->
            let aItems = a.EnumerateArray() |> List.ofSeq
            let bItems = b.EnumerateArray() |> List.ofSeq

            List.length aItems = List.length bItems
            && List.forall2 jsonValueEquals aItems bItems
        | JsonValueKind.String -> a.GetString() = b.GetString()
        | JsonValueKind.True
        | JsonValueKind.False -> a.GetBoolean() = b.GetBoolean()
        | _ -> a.GetRawText() = b.GetRawText()

/// Determines whether `packageLock`'s root package entry
/// (`packages.""` for a v2+ lockfile, falling back to the lockfile's own
/// top level otherwise) agrees with `packageJson` on every
/// `lockfileRootFields` field, a field present in neither counting as
/// agreement [Repo-grounded — `commands/git/lockfile.rs::lockfile_is_current`].
let lockfileIsCurrentContent (packageJson: string) (packageLock: string) : Result<bool, string> =
    try
        use packageDoc = JsonDocument.Parse(packageJson)
        use lockDoc = JsonDocument.Parse(packageLock)
        let packageRoot = packageDoc.RootElement

        let lockRoot =
            match lockDoc.RootElement.TryGetProperty "packages" with
            | true, packages when packages.ValueKind = JsonValueKind.Object ->
                match packages.TryGetProperty "" with
                | true, rootEntry -> rootEntry
                | false, _ -> lockDoc.RootElement
            | _ -> lockDoc.RootElement

        let fieldAgrees (field: string) =
            match packageRoot.TryGetProperty field, lockRoot.TryGetProperty field with
            | (false, _), (false, _) -> true
            | (true, packageValue), (true, lockValue) -> jsonValueEquals packageValue lockValue
            | _ -> false

        Ok(lockfileRootFields |> List.forall fieldAgrees)
    with ex ->
        Error(sprintf "failed to read lockfile fields: %s" ex.Message)

type LockfileSyncPorts =
    { StagedPaths: unit -> Result<string list, string>
      FileExists: string -> bool
      ReadAllText: string -> string
      RegenerateLockfile: string -> Result<unit, string>
      Stage: string -> Result<unit, string> }

/// Pure lockfile synchronization policy. Paths are repository-relative and
/// every resource operation is supplied by the caller, keeping selection,
/// comparison, ordering, reporting, and error propagation Unit-testable.
let syncWith (ports: LockfileSyncPorts) (writer: TextWriter) : Result<unit, string> =
    match ports.StagedPaths() with
    | Error message -> Error message
    | Ok staged ->
        let manifests =
            staged
            |> List.filter (fun path ->
                path.StartsWith("apps/", StringComparison.Ordinal)
                && path.EndsWith("/package.json", StringComparison.Ordinal))

        let rec loop remaining =
            match remaining with
            | [] -> Ok()
            | packagePath :: rest ->
                let appDir = Path.GetDirectoryName(packagePath: string).Replace('\\', '/')
                let lockfilePath = appDir + "/package-lock.json"

                if not (ports.FileExists lockfilePath) then
                    loop rest
                else
                    match lockfileIsCurrentContent (ports.ReadAllText packagePath) (ports.ReadAllText lockfilePath) with
                    | Error message -> Error message
                    | Ok true -> loop rest
                    | Ok false ->
                        writer.Write(sprintf "Syncing %s...\n" lockfilePath)

                        match ports.RegenerateLockfile appDir with
                        | Error message -> Error message
                        | Ok() ->
                            match ports.Stage lockfilePath with
                            | Error message -> Error message
                            | Ok() -> loop rest

        loop manifests

/// Creates a `git` `Process` rooted explicitly at `repoRoot`, isolated from
/// ambient discovery and identity the same way the Rust command is
/// [Repo-grounded — `commands/git/lockfile.rs::git_command`].
// Coverage boundary: exercised by Git Integration and published-process E2E proof.
[<ExcludeFromCodeCoverage>]
let private gitProcess (repoRoot: string) (args: string list) : Process =
    let proc = new Process()
    proc.StartInfo.FileName <- "git"
    args |> List.iter proc.StartInfo.ArgumentList.Add
    proc.StartInfo.WorkingDirectory <- repoRoot
    proc.StartInfo.EnvironmentVariables.["GIT_DIR"] <- Path.Combine(repoRoot, ".git")
    proc.StartInfo.EnvironmentVariables.["GIT_CEILING_DIRECTORIES"] <- repoRoot
    proc.StartInfo.EnvironmentVariables.["GIT_CONFIG_GLOBAL"] <- "/dev/null"
    proc.StartInfo.EnvironmentVariables.["GIT_CONFIG_SYSTEM"] <- "/dev/null"
    proc.StartInfo.RedirectStandardOutput <- true
    proc.StartInfo.RedirectStandardError <- true
    proc.StartInfo.UseShellExecute <- false
    proc

/// Runs `git diff --cached --name-only --diff-filter=ACM` from `repoRoot`
/// and returns the staged paths, blank lines dropped
/// [Repo-grounded — `commands/git/lockfile.rs::sync_at_root`].
// Coverage boundary: real Git index access is exercised by Git Integration and published-process E2E proof.
[<ExcludeFromCodeCoverage>]
let private stagedPaths (repoRoot: string) : Result<string list, string> =
    use proc =
        gitProcess repoRoot [ "diff"; "--cached"; "--name-only"; "--diff-filter=ACM" ]

    try
        proc.Start() |> ignore
        let stdout = proc.StandardOutput.ReadToEnd()
        proc.StandardError.ReadToEnd() |> ignore
        proc.WaitForExit()

        if proc.ExitCode <> 0 then
            Error "git diff --cached failed"
        else
            stdout.Split('\n')
            |> Array.filter (fun line -> line <> "")
            |> List.ofArray
            |> Ok
    with :? System.ComponentModel.Win32Exception as ex ->
        Error(sprintf "failed to invoke git diff --cached: %s" ex.Message)

/// Stages `pathRelativeToRoot` with `git add`
/// [Repo-grounded — `commands/git/lockfile.rs::sync_at_root`].
// Coverage boundary: real Git staging is exercised by Git Integration and published-process E2E proof.
[<ExcludeFromCodeCoverage>]
let private gitAdd (repoRoot: string) (pathRelativeToRoot: string) : Result<unit, string> =
    use proc = gitProcess repoRoot [ "add"; pathRelativeToRoot ]

    try
        proc.Start() |> ignore
        proc.StandardOutput.ReadToEnd() |> ignore
        proc.StandardError.ReadToEnd() |> ignore
        proc.WaitForExit()

        if proc.ExitCode <> 0 then
            Error(sprintf "failed to stage %s" pathRelativeToRoot)
        else
            Ok()
    with :? System.ComponentModel.Win32Exception as ex ->
        Error(sprintf "failed to invoke git add: %s" ex.Message)

/// Regenerates `appDirRelativeToRoot`'s lockfile via
/// `npm install --package-lock-only --prefix <appDir> --silent`
/// [Repo-grounded — `commands/git/lockfile.rs::sync_at_root`].
// Coverage boundary: real npm process execution is exercised by Git Integration and published-process E2E proof.
[<ExcludeFromCodeCoverage>]
let private npmRegenerateLockfile (repoRoot: string) (appDirRelativeToRoot: string) : Result<unit, string> =
    use proc = new Process()
    proc.StartInfo.FileName <- "npm"
    proc.StartInfo.ArgumentList.Add("install")
    proc.StartInfo.ArgumentList.Add("--package-lock-only")
    proc.StartInfo.ArgumentList.Add("--prefix")
    proc.StartInfo.ArgumentList.Add(appDirRelativeToRoot)
    proc.StartInfo.ArgumentList.Add("--silent")
    proc.StartInfo.WorkingDirectory <- repoRoot
    proc.StartInfo.RedirectStandardOutput <- true
    proc.StartInfo.RedirectStandardError <- true
    proc.StartInfo.UseShellExecute <- false

    try
        proc.Start() |> ignore
        proc.StandardOutput.ReadToEnd() |> ignore
        proc.StandardError.ReadToEnd() |> ignore
        proc.WaitForExit()

        if proc.ExitCode <> 0 then
            Error(sprintf "failed to regenerate %s/package-lock.json" appDirRelativeToRoot)
        else
            Ok()
    with :? System.ComponentModel.Win32Exception as ex ->
        Error(sprintf "failed to invoke npm install: %s" ex.Message)

/// Synchronizes lockfiles for every staged `apps/*/package.json`: a
/// manifest whose current-lockfile check disagrees on any
/// `lockfileRootFields` field is regenerated via `npm` and the regenerated
/// lockfile is staged; a manifest with no sibling lockfile, or whose
/// lockfile already agrees, is left untouched. Writes one
/// `Syncing <path>...` line to `writer` per regenerated lockfile
/// [Repo-grounded — `commands/git/lockfile.rs::sync_at_root`].
// Coverage boundary: the filesystem/process composition root is exercised by Git Integration and published-process E2E proof.
[<ExcludeFromCodeCoverage>]
let syncAtRoot (repoRoot: string) (writer: TextWriter) : Result<unit, string> =
    syncWith
        { StagedPaths = fun () -> stagedPaths repoRoot
          FileExists = fun relative -> File.Exists(Path.Combine(repoRoot, relative))
          ReadAllText = fun relative -> File.ReadAllText(Path.Combine(repoRoot, relative))
          RegenerateLockfile = npmRegenerateLockfile repoRoot
          Stage = gitAdd repoRoot }
        writer
