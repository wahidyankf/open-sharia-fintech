module CraneCli.Tests.Unit.Steps.InMemoryBoundaries

open System
open System.Collections.Generic
open CraneCore.Logic

let private files = Dictionary<string, string>(StringComparer.Ordinal)

let fixedUtcNow = DateTimeOffset(2026, 9, 5, 4, 30, 0, TimeSpan.Zero)
let fixedLocalNow = fixedUtcNow.LocalDateTime

let reset () = files.Clear()
let exists path = files.ContainsKey(path)

let readAllText path =
    match files.TryGetValue(path) with
    | true, content -> content
    | false, _ -> raise (System.IO.FileNotFoundException("In-memory file not found", path))

let readAllLines path =
    readAllText path
    |> fun content -> content.Replace("\r\n", "\n", StringComparison.Ordinal).Split('\n')

let writeAllText path content = files[path] <- content

let appendAllText path content =
    let existing =
        match files.TryGetValue(path) with
        | true, value -> value
        | false, _ -> ""

    files[path] <- existing + content

let private directoryName (path: string) =
    let index = path.LastIndexOfAny([| '/'; '\\' |])
    if index > 0 then Some(path.Substring(0, index)) else None

let reportDependencies: ReportManager.Dependencies =
    { FileExists = exists
      ReadAllText = readAllText
      WriteAllText = writeAllText
      EnsureDirectory = ignore
      UtcNow = fun () -> fixedUtcNow
      NewId = fun () -> "def456" }

let skiplistDependencies path : SkiplistManager.Dependencies =
    { FileExists = exists
      ReadAllLines = readAllLines
      ReadAllText = readAllText
      WriteAllText = writeAllText
      AppendAllText = appendAllText
      EnsureDirectory = ignore
      GetDirectoryName = directoryName
      ResolvePath = fun () -> path
      Now = fun () -> fixedLocalNow
      Warn = ignore }
