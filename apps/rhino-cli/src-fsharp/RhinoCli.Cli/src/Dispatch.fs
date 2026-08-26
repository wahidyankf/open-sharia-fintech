/// Top-level argv routing for the namespaces flipped so far
/// [Repo-grounded — `apps/rhino-cli/src/cli.rs`'s `run`/`dispatch`]. Each
/// wave's flip PR extends `route` with its own namespace's leaves; nothing
/// here handles a namespace still routed to the Rust binary by
/// `apps/rhino-cli/scripts/rhino-bin.sh`'s `FSHARP_NAMESPACES`.
module RhinoCli.Cli.Dispatch

open System
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
        | a :: _ when a.StartsWith("--output=", StringComparison.Ordinal) -> Some(a.Substring("--output=".Length))
        | _ :: rest -> find rest

    match find args with
    | None
    | Some "" -> Ok Text
    | Some "text" -> Ok Text
    | Some "json" -> Ok Json
    | Some "markdown" -> Ok Markdown
    | Some other -> Error(sprintf "unknown output format \"%s\": must be text, json, or markdown" other)

/// `true` when any of `names` appears verbatim in `args` — a bare boolean
/// flag such as `--force`/`-f`.
let private hasFlag (names: string list) (args: string list) : bool =
    args |> List.exists (fun a -> List.contains a names)

/// Finds the value following the first occurrence of any of `names` in
/// `args` (space-separated form only, matching this file's existing
/// `collectPathFlags`/`collectSkipFlags` convention).
let private stringFlag (names: string list) (args: string list) : string option =
    let rec loop (args: string list) : string option =
        match args with
        | [] -> None
        | a :: v :: _ when List.contains a names -> Some v
        | _ :: rest -> loop rest

    loop args

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
        | a :: rest when a.StartsWith("--output=", StringComparison.Ordinal) -> loop rest acc
        | a :: rest when a.StartsWith("-", StringComparison.Ordinal) -> loop rest acc
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

// ---------------------------------------------------------------------------
// Wave B: repo-config, env
// ---------------------------------------------------------------------------

/// `repo-config validate` ignores `-o`/`--output` entirely, always printing
/// plain text [Repo-grounded — `repo_config_validate.rs::run`'s unused
/// `_output` parameter]. On a schema-deserialization failure nothing reaches
/// stdout — the whole message surfaces only as the trailing `Error:` line,
/// mirroring `run_at_root`'s `?`-propagated `Err` never reaching its own
/// `writeln!` calls.
let private runRepoConfigValidateLeaf (repoRoot: string) : int =
    match RepoConfig.load repoRoot with
    | Error message ->
        eprintfn "Error: repo-config validate: repo-config.yml failed strict schema deserialization: %s" message

        1
    | Ok config ->
        match RepoConfig.semanticFindings config with
        | [] ->
            printfn "repo-config validate: repo-config.yml matches the canonical schema (key set + enums OK)"
            0
        | findings ->
            findings |> List.iter (printfn "%s")

            eprintfn
                "Error: repo-config validate: %d schema finding(s); fix the key(s) listed above"
                (List.length findings)

            1

/// `env init` also ignores `-o`/`--output` — it always prints the same plain
/// text and always exits `0`, regardless of per-file outcome [Repo-grounded —
/// `env_init.rs::run`, whose only failure mode (git-root lookup) `route`
/// already handles before reaching this leaf].
let private runEnvInitLeaf (repoRoot: string) (args: string list) : int =
    let force = hasFlag [ "--force" ] args
    printf "%s" (Env.formatEnvInitText (Env.runEnvInit repoRoot force))
    0

/// Resolves `env backup`'s effective backup directory: the best-effort
/// canonicalization applies to both the default (`~/ose-public-env-backup`)
/// and an explicit `--dir` [Repo-grounded — `env_backup.rs::run`].
let private resolveBackupDir (dirArg: string) : Result<string, string> =
    let canonicalizeOrFallback (path: string) : string =
        match Env.canonicalizeBestEffort path with
        | Ok canon -> canon
        | Error _ -> path

    if dirArg = "" then
        Env.expandTilde "~"
        |> Result.map (fun home -> canonicalizeOrFallback (IO.Path.Combine(home, Env.DefaultBackupDir)))
    else
        Env.expandTilde dirArg |> Result.map canonicalizeOrFallback

/// Resolves `env restore`'s effective backup directory. Unlike `env backup`,
/// the default (empty `--dir`) is used as-is with no canonicalization at all,
/// and an explicit `--dir` uses a real (existence-requiring) canonicalize
/// that falls back to the expanded-but-uncanonicalized path on failure
/// [Repo-grounded — `env_restore.rs::run`].
let private resolveRestoreDir (dirArg: string) : Result<string, string> =
    if dirArg = "" then
        Env.expandTilde "~"
        |> Result.map (fun home -> IO.Path.Combine(home, Env.DefaultBackupDir))
    else
        Env.expandTilde dirArg
        |> Result.map (fun expanded ->
            try
                if IO.Directory.Exists expanded then
                    IO.Path.GetFullPath expanded
                else
                    expanded
            with _ ->
                expanded)

/// The `env backup`/`env restore` flags this dispatch shim threads through to
/// `EnvOptions` [Repo-grounded — `EnvBackupArgs`/`EnvRestoreArgs`].
type private BackupRestoreArgs =
    { Dir: string
      WorktreeAware: bool
      Force: bool
      IncludeConfig: bool
      DryRun: bool
      Verbose: bool
      Quiet: bool }

let private parseBackupRestoreArgs (args: string list) : BackupRestoreArgs =
    { Dir = stringFlag [ "--dir" ] args |> Option.defaultValue ""
      WorktreeAware = hasFlag [ "--worktree-aware" ] args
      Force = hasFlag [ "--force"; "-f" ] args
      IncludeConfig = hasFlag [ "--include-config" ] args
      DryRun = hasFlag [ "--dry-run" ] args
      Verbose = hasFlag [ "--verbose"; "-v" ] args
      Quiet = hasFlag [ "--quiet"; "-q" ] args }

/// Applies `--worktree-aware` to `opts`, resolving the worktree name via
/// `Env.detectWorktree` [Repo-grounded — `env_backup.rs::run`,
/// `env_restore.rs::run`].
let private applyWorktreeAware
    (repoRoot: string)
    (parsed: BackupRestoreArgs)
    (opts: Env.EnvOptions)
    : Result<Env.EnvOptions, string> =
    if parsed.WorktreeAware then
        Env.detectWorktree repoRoot
        |> Result.mapError (sprintf "worktree detection failed: %s")
        |> Result.map (fun info ->
            { opts with
                WorktreeName = info.WorktreeName })
    else
        Ok opts

/// Prints an [`Env.EnvOperationResult`] the same way `env_backup.rs`'s and
/// `env_restore.rs`'s own `match output { ... }` blocks do: `Text`/`Markdown`
/// via `print!` (their formatters already end in `\n`), `Json` via `println!`
/// (`format_json` does not) [Repo-grounded — `env_backup.rs::run`].
let private printEnvOperationResult
    (format: OutputFormat)
    (parsed: BackupRestoreArgs)
    (result: Env.EnvOperationResult)
    : unit =
    match format with
    | Text -> printf "%s" (Env.formatText result parsed.Verbose parsed.Quiet)
    | Json -> printfn "%s" (Env.formatJson result)
    | Markdown -> printf "%s" (Env.formatMarkdown result)

/// `confirm` always answers "yes": the real Rust binary never prompts either
/// — `Options.force` is threaded through but never read inside `backup()`'s
/// or `restore()`'s body (see `Env.fs`'s module doc comment) — so answering
/// unconditionally reproduces that always-overwrite behaviour exactly rather
/// than risking a shadow-diff mismatch by blocking on a real prompt this CLI
/// shim has no terminal to service.
let private alwaysConfirm () : bool = true

let private runEnvBackupLeaf (repoRoot: string) (format: OutputFormat) (args: string list) : int =
    let parsed = parseBackupRestoreArgs args

    match resolveBackupDir parsed.Dir with
    | Error message ->
        eprintfn "Error: %s" message
        1
    | Ok backupDir ->
        let force = parsed.Force || format <> Text

        let baseOpts: Env.EnvOptions =
            { RepoRoot = repoRoot
              BackupDir = backupDir
              SkipDirs = Env.defaultSkipDirs
              MaxSize = Env.DefaultMaxSize
              WorktreeAware = parsed.WorktreeAware
              WorktreeName = ""
              Force = force
              IncludeConfig = parsed.IncludeConfig
              DryRun = parsed.DryRun }

        match applyWorktreeAware repoRoot parsed baseOpts with
        | Error message ->
            eprintfn "Error: %s" message
            1
        | Ok opts ->
            match Env.backup opts alwaysConfirm with
            | Error message ->
                eprintfn "Error: env backup failed: %s" message
                1
            | Ok result ->
                printEnvOperationResult format parsed result
                0

let private runEnvRestoreLeaf (repoRoot: string) (format: OutputFormat) (args: string list) : int =
    let parsed = parseBackupRestoreArgs args

    match resolveRestoreDir parsed.Dir with
    | Error message ->
        eprintfn "Error: %s" message
        1
    | Ok backupDir ->
        let force = parsed.Force || format <> Text

        let baseOpts: Env.EnvOptions =
            { RepoRoot = repoRoot
              BackupDir = backupDir
              SkipDirs = []
              MaxSize = Env.DefaultMaxSize
              WorktreeAware = parsed.WorktreeAware
              WorktreeName = ""
              Force = force
              IncludeConfig = parsed.IncludeConfig
              DryRun = parsed.DryRun }

        match applyWorktreeAware repoRoot parsed baseOpts with
        | Error message ->
            eprintfn "Error: %s" message
            1
        | Ok opts ->
            match Env.restore opts alwaysConfirm with
            | Error message ->
                eprintfn "Error: env restore failed: %s" message
                1
            | Ok result ->
                printEnvOperationResult format parsed result
                0

/// `env validate` also ignores `-o`/`--output`, always printing plain text to
/// stdout on success and per-finding `DRIFT` lines to stderr on failure
/// [Repo-grounded — `env_validate.rs::run_at_root`]. The env-injection
/// manifest-consistency pass (`envinjection.rs::validate_manifest`) is not
/// yet ported to this application layer, so this leaf's total is drift
/// findings only — the two contribute independently to Rust's own `total`,
/// and this checkout carries zero of either today.
let private runEnvValidateLeaf (repoRoot: string) (args: string list) : int =
    let warnOnly = hasFlag [ "--warn-only" ] args

    match Env.loadContract repoRoot with
    | Error message ->
        eprintfn "Error: %s" message
        1
    | Ok contract ->
        match Env.validateAll repoRoot contract with
        | Error message ->
            eprintfn "Error: %s" message
            1
        | Ok findings ->
            let total = List.length findings

            if total = 0 then
                printfn "env validate: no drift detected across all surfaces; env-injection manifest consistent"
                0
            else
                findings |> List.iter (fun f -> eprintfn "%s" (Env.formatFinding f))

                if warnOnly then
                    eprintfn "env validate: %d finding(s) — warn-only mode, not failing" total
                    0
                else
                    eprintfn
                        "Error: env validate: %d finding(s); fix the divergent keys/manifest entries listed above"
                        total

                    1

/// `env staged-guard validate` reads the real git index (unlike its own unit
/// tests, which drive `checkStagedFiles` directly) [Repo-grounded —
/// `env_staged_guard.rs::run`]. Also ignores `-o`/`--output`.
let private runEnvStagedGuardValidateLeaf (repoRoot: string) : int =
    match RhinoCli.Infrastructure.GitRoot.getStagedFiles repoRoot with
    | Error message ->
        eprintfn "Error: %s" message
        1
    | Ok stagedFiles ->
        match Env.checkStagedFiles stagedFiles with
        | [] -> 0
        | offending ->
            printfn "%s" (Env.formatEnvStagedGuardFailure offending)

            eprintfn "Error: %d offending .env file(s) staged (policy: guard-env-file-access)" (List.length offending)

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
            | "repo-config" :: "validate" :: rest -> Some "repo-config-validate", rest
            | "env" :: "init" :: rest -> Some "env-init", rest
            | "env" :: "backup" :: rest -> Some "env-backup", rest
            | "env" :: "restore" :: rest -> Some "env-restore", rest
            | "env" :: "validate" :: rest -> Some "env-validate", rest
            | "env" :: "staged-guard" :: "validate" :: rest -> Some "env-staged-guard-validate", rest
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
                    | "repo-config-validate" -> runRepoConfigValidateLeaf repoRoot
                    | "env-init" -> runEnvInitLeaf repoRoot rest
                    | "env-backup" -> runEnvBackupLeaf repoRoot format rest
                    | "env-restore" -> runEnvRestoreLeaf repoRoot format rest
                    | "env-validate" -> runEnvValidateLeaf repoRoot rest
                    | "env-staged-guard-validate" -> runEnvStagedGuardValidateLeaf repoRoot
                    | _ -> 2
