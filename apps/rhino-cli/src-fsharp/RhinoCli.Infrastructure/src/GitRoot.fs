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
