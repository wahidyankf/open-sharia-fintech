/// Narrow operating-system adapter used by `Doctor`.
///
/// This module owns only filesystem, environment, platform, and child-process
/// access. Doctor policy remains in `Doctor.fs`, where Unit tests can exercise
/// decisions without touching the host. The adapter is covered by the Doctor
/// Integration and published-process E2E suites.
module RhinoCli.Application.DoctorResource

open System
open System.Diagnostics
open System.IO
open System.Runtime.InteropServices

let environmentVariable (name: string) : string option =
    match Environment.GetEnvironmentVariable(name) with
    | null
    | "" -> None
    | value -> Some value

let fileExists (path: string) : bool = File.Exists path

let directoryExists (path: string) : bool = Directory.Exists path

let directories (path: string) : string array = Directory.GetDirectories path

let readAllText (path: string) : string = File.ReadAllText path

let readAllLines (path: string) : string array = File.ReadAllLines path

let createDirectory (path: string) : unit =
    Directory.CreateDirectory(path) |> ignore

let deleteDirectory (path: string) (recursive: bool) : unit = Directory.Delete(path, recursive)

let deleteFile (path: string) : unit = File.Delete path

let createDirectorySymbolicLink (path: string) (target: string) : unit =
    Directory.CreateSymbolicLink(path, target) |> ignore

let linkTarget (path: string) : string option =
    match DirectoryInfo(path).LinkTarget with
    | null -> None
    | target -> Some target

let platformFlags () : bool * bool =
    RuntimeInformation.IsOSPlatform(OSPlatform.OSX), RuntimeInformation.IsOSPlatform(OSPlatform.Linux)

let runCaptured
    (command: string)
    (args: string list)
    (workingDirectory: string option)
    (removeGitOverrides: bool)
    : Result<string * string * int, string> =
    try
        use proc = new Process()
        proc.StartInfo.FileName <- command
        args |> List.iter proc.StartInfo.ArgumentList.Add

        workingDirectory
        |> Option.iter (fun directory -> proc.StartInfo.WorkingDirectory <- directory)

        if removeGitOverrides then
            proc.StartInfo.EnvironmentVariables.Remove("GIT_DIR")
            proc.StartInfo.EnvironmentVariables.Remove("GIT_WORK_TREE")

        proc.StartInfo.RedirectStandardOutput <- true
        proc.StartInfo.RedirectStandardError <- true
        proc.StartInfo.UseShellExecute <- false
        proc.Start() |> ignore
        let stdout = proc.StandardOutput.ReadToEnd()
        let stderr = proc.StandardError.ReadToEnd()
        proc.WaitForExit()
        Ok(stdout, stderr, proc.ExitCode)
    with ex ->
        Error ex.Message

let runInherited (command: string) (args: string list) : Result<unit, string> =
    try
        use proc = new Process()
        proc.StartInfo.FileName <- command
        args |> List.iter proc.StartInfo.ArgumentList.Add
        proc.StartInfo.UseShellExecute <- false
        proc.Start() |> ignore
        proc.WaitForExit()

        if proc.ExitCode = 0 then
            Ok()
        else
            Error(sprintf "exit %d" proc.ExitCode)
    with ex ->
        Error ex.Message
