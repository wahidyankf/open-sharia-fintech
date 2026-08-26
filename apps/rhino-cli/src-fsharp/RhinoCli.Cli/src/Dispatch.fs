/// Top-level argv routing for the namespaces flipped so far
/// [Repo-grounded — `apps/rhino-cli/src/cli.rs`'s `run`/`dispatch`]. Each
/// wave's flip PR extends `route` with its own namespace's leaves; nothing
/// here handles a namespace still routed to the Rust binary by
/// `apps/rhino-cli/scripts/rhino-bin.sh`'s `FSHARP_NAMESPACES`.
module RhinoCli.Cli.Dispatch

open RhinoCli.Domain.Types
open RhinoCli.Application

/// `-h`/`--help` always prints the same canonical top-level help and exits
/// `0`, regardless of where it appears or what subcommand precedes it
/// [Repo-grounded — `cli.rs`'s `disable_help_flag = true` plus its manual
/// `cli.help` check].
let private wantsHelp (argv: string[]) : bool =
    argv |> Array.exists (fun a -> a = "-h" || a = "--help")

/// Extracts a trailing `-o`/`--output <value>` (or `--output=value`) from
/// `args`, defaulting to `Text` when absent — the only global flag any
/// currently-flipped leaf's shadow-diff probe or real usage needs.
let private parseOutputFormat (args: string list) : Result<OutputFormat, string> =
    let rec find (args: string list) : string option =
        match args with
        | [] -> None
        | a :: v :: _ when a = "-o" || a = "--output" -> Some v
        | a :: _ when a.StartsWith("--output=") -> Some(a.Substring("--output=".Length))
        | _ :: rest -> find rest

    match find args with
    | None
    | Some "" -> Ok Text
    | Some "text" -> Ok Text
    | Some "json" -> Ok Json
    | Some "markdown" -> Ok Markdown
    | Some other -> Error(sprintf "unknown output format \"%s\": must be text, json, or markdown" other)

/// Collects every `-p`/`--path <value>` occurrence in `args`.
let private collectPathFlags (args: string list) : string list =
    let rec loop (args: string list) (acc: string list) : string list =
        match args with
        | [] -> List.rev acc
        | (a) :: v :: rest when (a = "-p" || a = "--path") -> loop rest (v :: acc)
        | _ :: rest -> loop rest acc

    loop args []

/// Collects every positional (non-flag, non-flag-value) argument in `args`
/// for `convention emoji validate` — `-o`/`--output`/`-p`/`--path` and their
/// values are excluded, mirroring `EmojiAuditArgs.positional`.
let private collectPositionals (args: string list) : string list =
    let rec loop (args: string list) (acc: string list) : string list =
        match args with
        | [] -> List.rev acc
        | a :: _ :: rest when a = "-o" || a = "--output" || a = "-p" || a = "--path" -> loop rest acc
        | a :: rest when a.StartsWith("--output=") -> loop rest acc
        | a :: rest when a.StartsWith("-") -> loop rest acc
        | a :: rest -> loop rest (a :: acc)

    loop args []

/// Collects every `--skip <name>` occurrence in `args`, for `convention audit`.
let private collectSkipFlags (args: string list) : string list =
    let rec loop (args: string list) (acc: string list) : string list =
        match args with
        | [] -> List.rev acc
        | a :: v :: rest when a = "--skip" -> loop rest (v :: acc)
        | _ :: rest -> loop rest acc

    loop args []

/// Resolves the emoji leaf's effective scan paths the same way the Rust CLI
/// layer does: positional overrides `-p`/`--path`, and an empty result of
/// both defaults to `["."]`, each resolved to an absolute path under
/// `repoRoot` [Repo-grounded —
/// `convention_validate_emoji.rs::run`'s path-resolution block].
let private resolveEmojiPaths (repoRoot: string) (args: string list) : string list =
    let positional = collectPositionals args
    let flagged = collectPathFlags args

    let relative =
        if not (List.isEmpty positional) then positional
        elif not (List.isEmpty flagged) then flagged
        else [ "." ]

    relative
    |> List.map (fun p ->
        if System.IO.Path.IsPathRooted p then
            p
        else
            System.IO.Path.Combine(repoRoot, p))

/// Prints `output` to stdout and, on a non-empty finding list, the trailing
/// `Error: {message}` line the Rust CLI's shared `dispatch()` appends to
/// stderr for every failing leaf [Repo-grounded — `cli.rs::dispatch`'s
/// `Err(e) => eprintln!("Error: {e}")`].
let private printResultAndExitCode (output: string) (errorMessage: string option) : int =
    printf "%s" output

    match errorMessage with
    | None -> 0
    | Some message ->
        eprintfn "Error: %s" message
        1

/// `Convention.runEmojiValidate`'s scan-itself-failed case (unreadable path,
/// etc.) is `Success = false` with `Findings = []` — the one case its
/// `Output` field cannot be reused for CLI rendering (it is always
/// text-shaped), and where Rust's `run()` returns before printing anything
/// to stdout at all [Repo-grounded —
/// `convention_validate_emoji.rs::run`'s `.context("emoji audit failed")?`,
/// which propagates before the `match output_format` print block runs].
let private runEmojiLeaf (repoRoot: string) (format: OutputFormat) (args: string list) : int =
    let paths = resolveEmojiPaths repoRoot args
    let result = Convention.runEmojiValidate paths

    if not result.Success && List.isEmpty result.Findings then
        eprintfn "Error: emoji audit failed: %s" result.Output
        1
    else
        let output =
            Formatters.render
                format
                (fun () -> Formatters.emojiText result.Findings)
                (fun () -> Formatters.emojiJson result.Findings)
                (fun () -> Formatters.emojiMarkdown result.Findings)

        let err =
            if List.isEmpty result.Findings then
                None
            else
                Some(sprintf "%d emoji finding(s) found" (List.length result.Findings))

        printResultAndExitCode output err

let private runLicenseLeaf (repoRoot: string) (format: OutputFormat) : int =
    let result = Convention.runLicenseValidate repoRoot

    let output =
        Formatters.render
            format
            (fun () -> Formatters.licenseText result.Findings)
            (fun () -> Formatters.licenseJson result.Findings)
            (fun () -> Formatters.licenseMarkdown result.Findings)

    let err =
        if List.isEmpty result.Findings then
            None
        else
            Some(sprintf "%d license finding(s) found" (List.length result.Findings))

    printResultAndExitCode output err

/// `convention audit`: runs emoji then license (each printing its own
/// format-rendered output as it goes, exactly as `convention_audit.rs::run`
/// does), then prints the aggregate PASSED/FAILED footer
/// [Repo-grounded — `convention_audit.rs::run`].
let private runAuditLeaf (repoRoot: string) (format: OutputFormat) (args: string list) : int =
    let skip = collectSkipFlags args
    let members = [ "emoji"; "license" ]

    let runMember (name: string) : string option =
        if name = "emoji" then
            let result = Convention.runEmojiValidate [ repoRoot ]

            printf
                "%s"
                (Formatters.render
                    format
                    (fun () -> Formatters.emojiText result.Findings)
                    (fun () -> Formatters.emojiJson result.Findings)
                    (fun () -> Formatters.emojiMarkdown result.Findings))

            if List.isEmpty result.Findings then
                None
            else
                Some(sprintf "emoji: %d emoji finding(s) found" (List.length result.Findings))
        else
            let result = Convention.runLicenseValidate repoRoot

            printf
                "%s"
                (Formatters.render
                    format
                    (fun () -> Formatters.licenseText result.Findings)
                    (fun () -> Formatters.licenseJson result.Findings)
                    (fun () -> Formatters.licenseMarkdown result.Findings))

            if List.isEmpty result.Findings then
                None
            else
                Some(sprintf "license: %d license finding(s) found" (List.length result.Findings))

    let failures =
        members
        |> List.filter (fun n -> not (List.contains n skip))
        |> List.choose runMember

    if List.isEmpty failures then
        printfn "CONVENTION AUDIT PASSED: all %d validators passed" (List.length members - List.length skip)
        0
    else
        eprintfn "CONVENTION AUDIT FAILED: %d validator(s) reported failures" (List.length failures)
        failures |> List.iter (eprintfn "  %s")
        eprintfn "Error: convention audit found %d failure(s)" (List.length failures)
        1

let private runParityGenerate (repoRoot: string) : int =
    match Parity.generateAtRoot repoRoot with
    | Ok() ->
        printfn "generated %s" Parity.ManifestPath
        0
    | Error message ->
        eprintfn "Error: %s" message
        1

let private runParityValidate (repoRoot: string) : int =
    match Parity.validateAtRoot repoRoot with
    | Ok() ->
        printfn "%s is current" Parity.ManifestPath
        0
    | Error message ->
        eprintfn "Error: %s" message
        1

/// Routes `argv` to the leaf it names, resolving the repository root via
/// `getRepoRoot` — injected so tests can point at a fixture directory
/// instead of shelling out to the real `git` in this checkout.
let route (getRepoRoot: unit -> Result<string, string>) (argv: string[]) : int =
    if wantsHelp argv then
        printf "%s" HelpText.Text
        0
    else
        let path, rest =
            match List.ofArray argv with
            | "convention" :: "emoji" :: "validate" :: rest -> Some "emoji", rest
            | "convention" :: "license" :: "validate" :: rest -> Some "license", rest
            | "convention" :: "audit" :: rest -> Some "audit", rest
            | "parity" :: "manifest" :: "generate" :: rest -> Some "generate", rest
            | "parity" :: "manifest" :: "validate" :: rest -> Some "validate", rest
            | _ -> None, []

        match path with
        | None ->
            eprintfn "rhino-cli-fsharp: unrecognized or not-yet-routed invocation: %s" (String.concat " " argv)
            2
        | Some leaf ->
            match getRepoRoot () with
            | Error message ->
                eprintfn "Error: failed to find git repository root: %s" message
                1
            | Ok repoRoot ->
                match parseOutputFormat rest with
                | Error message ->
                    eprintfn "Error: %s" message
                    1
                | Ok format ->
                    match leaf with
                    | "emoji" -> runEmojiLeaf repoRoot format rest
                    | "license" -> runLicenseLeaf repoRoot format
                    | "audit" -> runAuditLeaf repoRoot format rest
                    | "generate" -> runParityGenerate repoRoot
                    | "validate" -> runParityValidate repoRoot
                    | _ -> 2
