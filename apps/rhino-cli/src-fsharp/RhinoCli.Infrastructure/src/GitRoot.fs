/// Git repository root locator — IO adapter shelling out to
/// `git rev-parse --show-toplevel`, worktree-aware since that flag returns
/// the linked worktree's own path rather than the main repository's
/// [Repo-grounded — `apps/rhino-cli/src/infrastructure/git/root.rs`].
module RhinoCli.Infrastructure.GitRoot

open System.Diagnostics

/// Runs `git rev-parse --show-toplevel` from the current working directory
/// and returns the trimmed absolute repository root, or an error message
/// mirroring the Rust port's wording when git is missing, the command
/// fails, or the output is empty.
let findRoot () : Result<string, string> =
    use proc = new Process()
    proc.StartInfo.FileName <- "git"
    proc.StartInfo.ArgumentList.Add("rev-parse")
    proc.StartInfo.ArgumentList.Add("--show-toplevel")
    proc.StartInfo.EnvironmentVariables.Remove("GIT_DIR")
    proc.StartInfo.EnvironmentVariables.Remove("GIT_WORK_TREE")
    proc.StartInfo.RedirectStandardOutput <- true
    proc.StartInfo.RedirectStandardError <- true
    proc.StartInfo.UseShellExecute <- false

    try
        proc.Start() |> ignore
        let stdout = proc.StandardOutput.ReadToEnd()
        let stderr = proc.StandardError.ReadToEnd()
        proc.WaitForExit()

        if proc.ExitCode <> 0 then
            Error(sprintf "git rev-parse failed: %s" (stderr.Trim()))
        else
            let path = stdout.Trim()

            if path = "" then
                Error "git rev-parse returned empty path"
            else
                Ok path
    with :? System.ComponentModel.Win32Exception as ex ->
        Error(sprintf "failed to invoke git rev-parse: %s" ex.Message)

/// Runs `git rev-parse --path-format=absolute --git-common-dir` from
/// `repoRoot` and returns the trimmed absolute path to the git common
/// directory — the **main** repository's `.git`, not the calling
/// worktree's own path, so every linked worktree of the same repo resolves
/// to the same value [Repo-grounded —
/// `infrastructure/git/common_dir.rs::find_common_dir_from`].
let findCommonDir (repoRoot: string) : Result<string, string> =
    use proc = new Process()
    proc.StartInfo.FileName <- "git"
    proc.StartInfo.ArgumentList.Add("rev-parse")
    proc.StartInfo.ArgumentList.Add("--path-format=absolute")
    proc.StartInfo.ArgumentList.Add("--git-common-dir")
    proc.StartInfo.WorkingDirectory <- repoRoot
    proc.StartInfo.RedirectStandardOutput <- true
    proc.StartInfo.RedirectStandardError <- true
    proc.StartInfo.UseShellExecute <- false

    try
        proc.Start() |> ignore
        let stdout = proc.StandardOutput.ReadToEnd()
        let stderr = proc.StandardError.ReadToEnd()
        proc.WaitForExit()

        if proc.ExitCode <> 0 then
            Error(sprintf "git rev-parse --git-common-dir failed: %s" (stderr.Trim()))
        else
            let path = stdout.Trim()

            if path = "" then
                Error "git rev-parse --git-common-dir returned empty path"
            else
                Ok path
    with :? System.ComponentModel.Win32Exception as ex ->
        Error(sprintf "failed to invoke git rev-parse --git-common-dir: %s" ex.Message)

/// Runs `git diff --cached --name-only --diff-filter=AM` from `repoRoot` and
/// returns the staged paths, one per line, blank lines dropped
/// [Repo-grounded — `env_staged_guard.rs::run`]. Strips `GIT_DIR`/
/// `GIT_WORK_TREE` from the inherited environment before running, matching
/// `findRoot`/`findCommonDir` above (Wave D PR11) — an ambient value from an
/// outer worktree-management call would otherwise redirect this staged-file
/// query away from `repoRoot`, the exact class of bug those two functions
/// already guard against.
let getStagedFiles (repoRoot: string) : Result<string list, string> =
    use proc = new Process()
    proc.StartInfo.FileName <- "git"
    proc.StartInfo.ArgumentList.Add("diff")
    proc.StartInfo.ArgumentList.Add("--cached")
    proc.StartInfo.ArgumentList.Add("--name-only")
    proc.StartInfo.ArgumentList.Add("--diff-filter=AM")
    proc.StartInfo.WorkingDirectory <- repoRoot
    proc.StartInfo.EnvironmentVariables.Remove("GIT_DIR")
    proc.StartInfo.EnvironmentVariables.Remove("GIT_WORK_TREE")
    proc.StartInfo.RedirectStandardOutput <- true
    proc.StartInfo.RedirectStandardError <- true
    proc.StartInfo.UseShellExecute <- false

    try
        proc.Start() |> ignore
        let stdout = proc.StandardOutput.ReadToEnd()
        let stderr = proc.StandardError.ReadToEnd()
        proc.WaitForExit()

        if proc.ExitCode <> 0 then
            Error(sprintf "git diff --cached failed: %s" (stderr.Trim()))
        else
            stdout.Split('\n')
            |> Array.filter (fun line -> line <> "")
            |> List.ofArray
            |> Ok
    with :? System.ComponentModel.Win32Exception as ex ->
        Error(sprintf "failed to run git diff --cached: %s" ex.Message)
