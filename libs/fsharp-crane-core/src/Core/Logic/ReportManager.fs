module CraneCore.Logic.ReportManager

open System
open System.IO

let private chainWindowSeconds = 30L
let private utc7Offset = TimeSpan.FromHours(7.0)

/// Agent working state lives under `local-tmp/`. The chain file sits at that root rather than in
/// a family directory because a parent-child chain spans families by construction.
let private chainFilePath (scope: string) : string =
    sprintf "local-tmp/.execution-chain-%s" scope

/// Reports produced here are read by the paired fixer agent, not by a maintainer who asked for
/// them, so they belong to the `pdf-to-md` family directory rather than to `generated-reports/`.
let private reportDir = "local-tmp/pdf-to-md"

type Dependencies =
    { FileExists: string -> bool
      ReadAllText: string -> string
      WriteAllText: string -> string -> unit
      EnsureDirectory: string -> unit
      UtcNow: unit -> DateTimeOffset
      NewId: unit -> string }

let private systemDependencies =
    { FileExists = File.Exists
      ReadAllText = File.ReadAllText
      WriteAllText = fun path content -> File.WriteAllText(path, content)
      EnsureDirectory = fun path -> Directory.CreateDirectory(path) |> ignore
      UtcNow = fun () -> DateTimeOffset.UtcNow
      NewId = fun () -> Guid.NewGuid().ToString("N").Substring(0, 6) }

let getOrExtendChainWith (dependencies: Dependencies) (scope: string) : string =
    let chainFile = chainFilePath scope
    let now = dependencies.UtcNow().ToUnixTimeSeconds()
    let newId = dependencies.NewId()

    let existingChain =
        if dependencies.FileExists chainFile then
            let parts = dependencies.ReadAllText(chainFile).Trim().Split(' ', 2)

            if parts.Length = 2 then
                match Int64.TryParse(parts.[0]) with
                | true, ts when now - ts < chainWindowSeconds -> Some(parts.[1] + "__" + newId)
                | _ -> None
            else
                None
        else
            None

    let chain = existingChain |> Option.defaultValue newId
    dependencies.EnsureDirectory "local-tmp"
    dependencies.WriteAllText chainFile $"%d{now} %s{chain}"
    chain

let getOrExtendChain (scope: string) : string =
    getOrExtendChainWith systemDependencies scope

let utc7TimestampAt (now: DateTimeOffset) : string =
    now.ToOffset(utc7Offset).ToString("yyyy-MM-dd--HH-mm")

let utc7Timestamp () : string =
    utc7TimestampAt (systemDependencies.UtcNow())

let initReportWith (dependencies: Dependencies) (scope: string) (pdf: string) (md: string) : Result<string, string> =
    try
        let chain = getOrExtendChainWith dependencies scope
        let ts = utc7TimestampAt (dependencies.UtcNow())
        let reportPath = $"%s{reportDir}/%s{scope}__%s{chain}__%s{ts}__audit.md"
        dependencies.EnsureDirectory reportDir

        let header =
            $"# Audit Report\n\nScope: %s{scope}\nPDF: %s{pdf}\nMD: %s{md}\nStatus: IN_PROGRESS\n"

        dependencies.WriteAllText reportPath header
        Ok reportPath
    with ex ->
        Error $"Failed to init report: %s{ex.Message}"

let initReport (scope: string) (pdf: string) (md: string) : Result<string, string> =
    initReportWith systemDependencies scope pdf md

let finalizeReportWith (dependencies: Dependencies) (reportPath: string) (status: string) : Result<unit, string> =
    try
        if not (dependencies.FileExists reportPath) then
            Error $"Report not found: %s{reportPath}"
        else
            let content = dependencies.ReadAllText reportPath
            let updated = content.Replace("Status: IN_PROGRESS", $"Status: %s{status}")
            dependencies.WriteAllText reportPath updated
            Ok()
    with ex ->
        Error $"Failed to finalize report: %s{ex.Message}"

let finalizeReport (reportPath: string) (status: string) : Result<unit, string> =
    finalizeReportWith systemDependencies reportPath status
