module CraneCore.Logic.SkiplistManager

open System
open System.IO
open System.Text
open CraneCore.Domain.Report

[<Literal>]
let private DefaultPath = "generated-reports/.known-false-positives.md"

[<Literal>]
let private FalsePositivePrefix = "## FALSE_POSITIVE:"

[<Literal>]
let private DefaultReason = "Auto-accepted via crane skiplist --add"

type Dependencies =
    { FileExists: string -> bool
      ReadAllLines: string -> string array
      ReadAllText: string -> string
      WriteAllText: string -> string -> unit
      AppendAllText: string -> string -> unit
      EnsureDirectory: string -> unit
      GetDirectoryName: string -> string option
      ResolvePath: unit -> string
      Now: unit -> DateTime
      Warn: string -> unit }

/// Resolve the skip-list path. CRANE_SKIPLIST_PATH overrides for tests; otherwise
/// the canonical repo-wide global markdown file is used.
let resolveSkiplistPath () : string =
    match Environment.GetEnvironmentVariable("CRANE_SKIPLIST_PATH") with
    | null
    | "" -> DefaultPath
    | overridePath -> overridePath

let stableKey (mdBasename: string) (category: string) (description: string) : string =
    let combined = sprintf "%s|%s|%s" mdBasename category description
    let bytes = Encoding.UTF8.GetBytes(combined)
    let hash = System.Security.Cryptography.SHA256.HashData(bytes)
    BitConverter.ToString(hash).Replace("-", "").ToLowerInvariant().[..15]

let private systemDependencies =
    { FileExists = File.Exists
      ReadAllLines = File.ReadAllLines
      ReadAllText = File.ReadAllText
      WriteAllText = fun path content -> File.WriteAllText(path, content)
      AppendAllText = fun path content -> File.AppendAllText(path, content)
      EnsureDirectory = fun path -> Directory.CreateDirectory(path) |> ignore
      GetDirectoryName = fun path -> Path.GetDirectoryName(path) |> Option.ofObj
      ResolvePath = resolveSkiplistPath
      Now = fun () -> DateTime.Now
      Warn = fun message -> eprintfn "%s" message }

let private parseHeading (line: string) : (string * string * string) option =
    let body = line.Substring(FalsePositivePrefix.Length).TrimStart()
    let parts = body.Split([| " | " |], StringSplitOptions.None)

    if parts.Length = 3 then
        Some(parts.[0].Trim(), parts.[1].Trim(), parts.[2].Trim())
    else
        None

let private parseMetadata (block: string list) : Map<string, string> =
    block
    |> List.choose (fun line ->
        let trimmed = line.TrimStart()

        if trimmed.StartsWith("**", System.StringComparison.Ordinal) then
            let endMarker = trimmed.IndexOf("**:", 2, System.StringComparison.Ordinal)

            if endMarker > 0 then
                let key = trimmed.Substring(2, endMarker - 2).Trim()
                let value = trimmed.Substring(endMarker + 3).Trim()
                Some(key, value)
            else
                None
        else
            None)
    |> Map.ofList

let private parseEntriesWith (dependencies: Dependencies) (path: string) : SkipListEntry list =
    if not (dependencies.FileExists path) then
        []
    else
        let lines = dependencies.ReadAllLines path |> Array.toList

        let rec walk (acc: SkipListEntry list) (remaining: string list) =
            match remaining with
            | [] -> List.rev acc
            | line :: rest when line.StartsWith(FalsePositivePrefix, System.StringComparison.Ordinal) ->
                let metaLines =
                    rest
                    |> List.takeWhile (fun l ->
                        not (l.StartsWith("## ", System.StringComparison.Ordinal)) && l.Trim() <> "---")

                let nextRest = rest |> List.skip metaLines.Length

                match parseHeading line with
                | Some(category, mdBasename, description) ->
                    let meta = parseMetadata metaLines
                    let accepted = meta |> Map.tryFind "Accepted" |> Option.defaultValue ""
                    let reason = meta |> Map.tryFind "Reason" |> Option.defaultValue ""

                    let key =
                        meta
                        |> Map.tryFind "Key"
                        |> Option.defaultWith (fun () -> stableKey mdBasename category description)

                    let entry =
                        { MdBasename = mdBasename
                          Category = category
                          Description = description
                          Key = key
                          Accepted = accepted
                          Reason = reason }

                    walk (entry :: acc) nextRest
                | None ->
                    dependencies.Warn $"Warning: skipping malformed FALSE_POSITIVE heading: {line}"
                    walk acc nextRest
            | _ :: rest -> walk acc rest

        walk [] lines

let private renderEntry (entry: SkipListEntry) : string =
    let sb = StringBuilder()

    sb
        .Append("## FALSE_POSITIVE: ")
        .Append(entry.Category)
        .Append(" | ")
        .Append(entry.MdBasename)
        .Append(" | ")
        .Append(entry.Description)
        .AppendLine()
        .AppendLine()
        .Append("**Accepted**: ")
        .Append(entry.Accepted)
        .AppendLine()
        .Append("**Category**: ")
        .Append(entry.Category)
        .AppendLine()
        .Append("**File**: ")
        .Append(entry.MdBasename)
        .AppendLine()
        .Append("**Finding**: ")
        .Append(entry.Description)
        .AppendLine()
        .Append("**Key**: ")
        .Append(entry.Key)
        .AppendLine()
        .Append("**Reason**: ")
        .Append(entry.Reason)
        .AppendLine()
        .AppendLine()
        .AppendLine("---")
        .AppendLine()
    |> ignore

    sb.ToString()

let private appendEntryWith (dependencies: Dependencies) (path: string) (entry: SkipListEntry) =
    let text = renderEntry entry

    if dependencies.FileExists path then
        let existing = dependencies.ReadAllText path

        let needsBlankLine =
            not (existing.EndsWith("\n\n", System.StringComparison.Ordinal))
            && existing.Length > 0

        let prefix = if needsBlankLine then "\n" else ""
        dependencies.AppendAllText path (prefix + text)
    else
        match dependencies.GetDirectoryName path with
        | Some dir when dir.Length > 0 -> dependencies.EnsureDirectory dir
        | _ -> ()

        dependencies.WriteAllText path text

let addWith
    (dependencies: Dependencies)
    (mdBasename: string)
    (category: string)
    (description: string)
    : Result<bool, string> =
    try
        let path = dependencies.ResolvePath()
        let key = stableKey mdBasename category description
        let existing = parseEntriesWith dependencies path

        if existing |> List.exists (fun e -> e.Key = key) then
            Ok false
        else
            let entry =
                { MdBasename = mdBasename
                  Category = category
                  Description = description
                  Key = key
                  Accepted = dependencies.Now().ToString("yyyy-MM-dd--HH-mm")
                  Reason = DefaultReason }

            appendEntryWith dependencies path entry
            Ok true
    with ex ->
        Error $"Failed to add entry: {ex.Message}"

let add (mdBasename: string) (category: string) (description: string) : Result<bool, string> =
    addWith systemDependencies mdBasename category description

let checkWith
    (dependencies: Dependencies)
    (mdBasename: string)
    (category: string)
    (description: string)
    : Result<bool, string> =
    let path = dependencies.ResolvePath()
    let key = stableKey mdBasename category description
    let existing = parseEntriesWith dependencies path
    Ok(existing |> List.exists (fun e -> e.Key = key))

let check (mdBasename: string) (category: string) (description: string) : Result<bool, string> =
    checkWith systemDependencies mdBasename category description

let listWith (dependencies: Dependencies) (mdBasename: string) : Result<SkipListEntry list, string> =
    let path = dependencies.ResolvePath()
    let all = parseEntriesWith dependencies path
    Ok(all |> List.filter (fun e -> e.MdBasename = mdBasename))

let list (mdBasename: string) : Result<SkipListEntry list, string> = listWith systemDependencies mdBasename
