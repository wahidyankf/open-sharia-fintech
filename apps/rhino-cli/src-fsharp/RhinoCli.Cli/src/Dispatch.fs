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

/// Parses one `--format` value [Repo-grounded — `domain/cliout.rs::parse`].
let private parseOutputFormatValue (value: string) : Result<OutputFormat, string> =
    match value with
    | ""
    | "text" -> Ok Text
    | "json" -> Ok Json
    | "markdown" -> Ok Markdown
    | other -> Error(sprintf "unknown output format \"%s\": must be text, json, or markdown" other)

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
/// values are excluded, mirroring `EmojiAuditArgs.positional`. `extraValueFlags`
/// names additional flags (e.g. `--exclude`, `--exempt`, `--paths`) whose
/// following value must also be skipped rather than leak into the result —
/// every caller that also reads one of those flags via
/// `collectRepeatableFlag`/`collectPathFlags` on the SAME `args` must list it
/// here, or that flag's value is misread as a positional path (observed for
/// real in `.husky/pre-commit`'s `md naming validate --exempt ...` and `md
/// mermaid validate --exclude ...` calls, Wave D integration).
let private collectPositionals (extraValueFlags: string list) (args: string list) : string list =
    let rec loop (args: string list) (acc: string list) : string list =
        match args with
        | [] -> List.rev acc
        | a :: _ :: rest when a = "-o" || a = "--output" || a = "-p" || a = "--path" -> loop rest acc
        | a :: _ :: rest when List.contains a extraValueFlags -> loop rest acc
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
    let positional = collectPositionals [] args
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

// ---------------------------------------------------------------------------
// Wave C: doctor, test-coverage
// ---------------------------------------------------------------------------

/// Parsed shape of `doctor`'s own flags
/// [Repo-grounded — `commands/doctor.rs::DoctorArgs`].
type private DoctorArgsParsed =
    { Scope: string
      Tools: string list option
      Fix: bool
      DryRun: bool
      PruneCargoCache: bool
      Quiet: bool }

/// Collects every `--tools value[,value...]` occurrence, comma-splitting
/// each and flattening in order, `None` when the flag never appears
/// [Repo-grounded — `DoctorArgs.tools`'s `value_delimiter = ','` plus
/// clap's repeat-to-append behavior for `Vec` args].
let private collectDoctorToolsFlag (args: string list) : string list option =
    let rec loop (args: string list) (acc: string list) : string list =
        match args with
        | [] -> List.rev acc
        | a :: v :: rest when a = "--tools" -> loop rest ((v.Split(',') |> Array.toList |> List.rev) @ acc)
        | _ :: rest -> loop rest acc

    match loop args [] with
    | [] -> None
    | values -> Some values

let private parseDoctorArgs (args: string list) : DoctorArgsParsed =
    { Scope = stringFlag [ "--scope" ] args |> Option.defaultValue "full"
      Tools = collectDoctorToolsFlag args
      Fix = hasFlag [ "--fix" ] args
      DryRun = hasFlag [ "--dry-run" ] args
      PruneCargoCache = hasFlag [ "--prune-cargo-cache" ] args
      Quiet = hasFlag [ "--quiet"; "-q" ] args }

/// Validates every explicitly-selected `--tools` name up front, mirroring
/// `commands/doctor.rs::parse_doctor_tool_name`'s value-parser rejection —
/// approximated as a plain domain error (exit `1`) rather than clap's own
/// exit-`2` value-parser shape, since no `shadow-diff.sh` probe exercises
/// `--tools` (only bare/`--help`/`-o` forms do) and the Gherkin scenario this
/// underpins already asserts against `Doctor.parseDoctorToolName` directly at
/// the application layer.
let private validateSelectedTools (tools: string list option) : Result<string list option, string> =
    match tools with
    | None -> Ok None
    | Some names ->
        names
        |> List.fold
            (fun acc name ->
                match acc with
                | Error _ -> acc
                | Ok _ ->
                    match Doctor.parseDoctorToolName name with
                    | Error message -> Error message
                    | Ok _ -> acc)
            (Ok())
        |> Result.map (fun () -> Some names)

/// Runs the cargo shared-target-directory check (and, when requested, the
/// fix/prune/sweep steps), printing the same plain-text report
/// `commands/doctor.rs::run_target_share_step` does — restricted to `Text`
/// output by the caller, matching Rust's own restriction. A missing/failed
/// git-common-dir lookup or an empty repo name silently skips the whole step,
/// mirroring `run_target_share_step`'s early `return`/empty-name guard.
let private runDoctorTargetShareStep (repoRoot: string) (parsed: DoctorArgsParsed) : unit =
    match RhinoCli.Infrastructure.GitRoot.findCommonDir repoRoot with
    | Error _ -> ()
    | Ok commonDir ->
        let name = Doctor.repoName commonDir

        if name <> "" then
            let ci = Doctor.isCiAmbient ()
            let cacheRoot = Doctor.cacheRootAmbient ()

            let unshared = Doctor.checkTargetShares repoRoot cacheRoot name ci
            printfn "%s" (Doctor.formatCheckReport unshared ci)

            if parsed.Fix then
                let outcome = Doctor.fixTargetShares repoRoot cacheRoot name ci
                printfn "%s" (Doctor.formatFixReport outcome)

            if parsed.PruneCargoCache then
                let prune = Doctor.pruneOrphans repoRoot cacheRoot name parsed.DryRun ci
                printfn "%s" (Doctor.formatPruneReport prune parsed.DryRun)

                let sweep =
                    Doctor.sweepStale cacheRoot name parsed.DryRun (Doctor.cargoSweepPresent ()) ci

                let sweepReport = Doctor.formatSweepReport sweep

                if sweepReport <> "" then
                    printfn "%s" sweepReport

/// `doctor` [Repo-grounded — `commands/doctor.rs::run`]. Has no required
/// positional arguments, so the blanket `wantsHelp` shortcut in `route`
/// already handles `-h`/`--help` correctly before this leaf ever runs.
let private runDoctorLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let parsed = parseDoctorArgs rawArgs

    match validateSelectedTools parsed.Tools with
    | Error message ->
        eprintfn "Error: %s" message
        1
    | Ok selectedTools ->
        let scope =
            Doctor.parseDoctorScope parsed.Scope |> Option.defaultValue Doctor.FullScope

        let opts: Doctor.CheckOptions =
            { RepoRoot = repoRoot
              Runner = None
              Scope = scope
              SelectedTools = selectedTools }

        let stopwatch = System.Diagnostics.Stopwatch.StartNew()
        let result = Doctor.checkAll opts
        stopwatch.Stop()

        // `commands/doctor.rs::run` prints Text/Markdown via `print!` (their
        // formatters already end in `\n`) but JSON via `println!` (`format_json`
        // does not) — mirrored here exactly, matching `Env.fs`'s
        // `printEnvOperationResult` precedent for the same Text/Json asymmetry.
        match format with
        | Text -> printf "%s" (Doctor.formatDoctorText result parsed.Quiet)
        | Json -> printfn "%s" (Doctor.formatDoctorJson result stopwatch.ElapsedMilliseconds)
        | Markdown -> printf "%s" (Doctor.formatDoctorMarkdown result)

        // Target-share reporting is plain, unstructured text — restricted to
        // the default text output so it never corrupts `-o json`/`-o
        // markdown`'s machine-/document-oriented shape, matching
        // `commands/doctor.rs::run`'s own `matches!(output, Text)` guard.
        if format = Text then
            runDoctorTargetShareStep repoRoot parsed

        let exitAfterFixAttempt: int option =
            if parsed.Fix && Doctor.hasRemediationWork result then
                let fr =
                    Doctor.fixAll
                        result
                        opts
                        { DryRun = parsed.DryRun
                          Runner = None }
                        (printf "%s")

                printf "%s" (Doctor.formatFixSummary fr)

                if fr.Failed > 0 then
                    eprintfn "Error: %d tool(s) failed to install" fr.Failed
                    Some 1
                elif not parsed.DryRun && fr.Fixed > 0 then
                    Some 0
                else
                    None
            elif parsed.Fix && not (Doctor.hasRemediationWork result) then
                printf "%s" Doctor.formatNothingToFix
                None
            else
                None

        match exitAfterFixAttempt with
        | Some code -> code
        | None ->
            if result.MissingCount > 0 then
                eprintfn "Error: %d tool(s) not found in PATH" result.MissingCount
                1
            else
                0

/// Extracts `test-coverage validate`'s two required positionals
/// (`COVERAGE_FILE`, `THRESHOLD`), skipping this leaf's own recognized flags
/// and their values as well as the shared global flags every leaf accepts
/// [Repo-grounded — `test_coverage_validate.rs::ValidateArgs`, `cli.rs::Cli`].
let private collectTestCoverageValidatePositionals (args: string list) : string list =
    let rec loop (args: string list) (acc: string list) : string list =
        match args with
        | [] -> List.rev acc
        | a :: _ :: rest when
            a = "-o"
            || a = "--output"
            || a = "--below-threshold"
            || a = "--exclude"
            || a = "--say"
            ->
            loop rest acc
        | a :: rest when a.StartsWith("--output=", StringComparison.Ordinal) -> loop rest acc
        | a :: rest when
            a = "--per-file"
            || a = "-h"
            || a = "--help"
            || a = "-v"
            || a = "--verbose"
            || a = "-q"
            || a = "--quiet"
            || a = "--no-color"
            ->
            loop rest acc
        | a :: rest when a.StartsWith("-", StringComparison.Ordinal) -> loop rest acc
        | a :: rest -> loop rest (a :: acc)

    loop args []

/// Collects every `--exclude <PATTERN>` occurrence, in order.
let private collectExcludeFlags (args: string list) : string list =
    let rec loop (args: string list) (acc: string list) : string list =
        match args with
        | [] -> List.rev acc
        | a :: v :: rest when a = "--exclude" -> loop rest (v :: acc)
        | _ :: rest -> loop rest acc

    loop args []

/// Approximates clap's "already-recognized-argument" echo in the `Usage:`
/// line of its missing-required-arguments error — captured empirically
/// against the real Rust binary for exactly the shapes `shadow-diff.sh`
/// exercises: bare, `-h`/`--help`, and each `-o`/`--output` value. A
/// combination of several flags at once (not a shape any probe or documented
/// real invocation produces) falls back to the bare form.
let private echoedTestCoverageValidateFlag (args: string list) : string option =
    if hasFlag [ "-h"; "--help" ] args then
        Some "--help"
    else
        match stringFlag [ "-o"; "--output" ] args with
        | Some _ -> Some "--output <OUTPUT>"
        | None ->
            if hasFlag [ "-v"; "--verbose" ] args then Some "--verbose"
            elif hasFlag [ "-q"; "--quiet" ] args then Some "--quiet"
            elif hasFlag [ "--no-color" ] args then Some "--no-color"
            else None

/// Reproduces clap's exact `error: the following required arguments were
/// not provided: ...` message for `test-coverage validate` byte-for-byte
/// [Repo-grounded — empirically captured from
/// `apps/rhino-cli/target/gate/rhino-cli test-coverage validate` with 0 or 1
/// positional arguments].
let private testCoverageValidateMissingArgsError (positionals: string list) (args: string list) : string =
    let placeholders = [ "<COVERAGE_FILE>"; "<THRESHOLD>" ]
    let alreadyGiven = min (List.length positionals) (List.length placeholders)
    let missing = placeholders |> List.skip alreadyGiven
    let missingLines = missing |> List.map (sprintf "  %s") |> String.concat "\n"

    let usageFlag =
        match echoedTestCoverageValidateFlag args with
        | Some f -> f + " "
        | None -> ""

    sprintf
        "error: the following required arguments were not provided:\n%s\n\nUsage: rhino-cli test-coverage validate %s<COVERAGE_FILE> <THRESHOLD>\n"
        missingLines
        usageFlag

/// `test-coverage validate` [Repo-grounded —
/// `test_coverage_validate.rs::run`]. Unlike every other currently-routed
/// leaf, this one has required positional arguments, so clap validates their
/// presence **before** the app ever reads a `--help`/`-o` flag — `route`
/// calls this leaf ahead of the blanket `wantsHelp` shortcut for exactly that
/// reason; a `--help` (or any other recognized flag) alongside missing
/// positionals still produces the missing-arguments error, never help text.
let private runTestCoverageValidateLeaf (repoRoot: string) (rawArgs: string list) : int =
    let positionals = collectTestCoverageValidatePositionals rawArgs

    if List.length positionals < 2 then
        eprintf "%s" (testCoverageValidateMissingArgsError positionals rawArgs)
        2
    elif wantsHelp (List.toArray rawArgs) then
        printf "%s" HelpText.Text
        0
    else
        match parseOutputFormat rawArgs with
        | Error message ->
            eprintfn "Error: %s" message
            1
        | Ok format ->
            let coverageFile = positionals.[0]
            let thresholdRaw = positionals.[1]

            match Double.TryParse(thresholdRaw, System.Globalization.CultureInfo.InvariantCulture) with
            | false, _ ->
                eprintfn "Error: invalid threshold \"%s\": must be a number (e.g. 85)" thresholdRaw
                1
            | true, threshold ->
                let absPath = IO.Path.Combine(repoRoot, coverageFile)

                let opts: TestCoverage.ValidateOptions =
                    { CoverageFile = absPath
                      Threshold = threshold
                      PerFile = hasFlag [ "--per-file" ] rawArgs
                      BelowThreshold =
                        stringFlag [ "--below-threshold" ] rawArgs
                        |> Option.bind (fun v ->
                            match Double.TryParse(v, System.Globalization.CultureInfo.InvariantCulture) with
                            | true, parsed -> Some parsed
                            | false, _ -> None)
                        |> Option.defaultValue 0.0
                      Exclude = collectExcludeFlags rawArgs
                      Json = (format = Json)
                      Markdown = (format = Markdown) }

                match TestCoverage.validate opts with
                | Error message ->
                    eprintfn "Error: %s" message
                    1
                | Ok outcome ->
                    printf "%s" outcome.Output

                    if outcome.Passed then
                        0
                    else
                        eprintfn "Error: coverage %.2f%% is below threshold %.0f%%" outcome.Pct outcome.Threshold

                        1

// ---------------------------------------------------------------------------
// Wave D — md, governance, git
// ---------------------------------------------------------------------------

/// Collects every repeatable `<name> <value>` occurrence, for any of `names`,
/// in order — the multi-name generalization of `collectExcludeFlags` used by
/// `--paths`/`--fail-kinds`/`--exempt`.
let private collectRepeatableFlag (names: string list) (args: string list) : string list =
    let rec loop (args: string list) (acc: string list) : string list =
        match args with
        | [] -> List.rev acc
        | a :: v :: rest when List.contains a names -> loop rest (v :: acc)
        | _ :: rest -> loop rest acc

    loop args []

/// Parses an integer-valued flag, falling back to `defaultVal` when absent
/// or unparsable.
let private intFlag (names: string list) (defaultVal: int) (args: string list) : int =
    match stringFlag names args with
    | Some v ->
        match Int32.TryParse v with
        | true, n -> n
        | false, _ -> defaultVal
    | None -> defaultVal

/// Resolves an effective scan-path list the same way every Wave D command's
/// `resolve_scan_paths` does: an explicit, non-empty override list wins;
/// `defaultPaths` is used unchanged otherwise. Each entry is then resolved
/// to an absolute path under `repoRoot`.
let private resolveAbsPaths (repoRoot: string) (defaultPaths: string list) (overridePaths: string list) : string list =
    let rel =
        if List.isEmpty overridePaths then
            defaultPaths
        else
            overridePaths

    rel
    |> List.map (fun p ->
        if IO.Path.IsPathRooted p then
            p
        else
            IO.Path.Combine(repoRoot, p))

/// Returns the staged `.md` files (repository-relative), or `Some []` when
/// `git diff --cached` itself fails — matching the Rust source's own
/// silent-empty-on-error fallback for this path
/// [Repo-grounded — `md_validate_links.rs`/`md_validate_mermaid.rs`'s
/// `get_staged_files`].
let private stagedMdFilesOption (repoRoot: string) : string list option =
    match RhinoCli.Infrastructure.GitRoot.getStagedFiles repoRoot with
    | Ok files -> Some files
    | Error _ -> Some []

/// Returns the `.md` files changed since upstream (`git diff --name-only
/// @{u}..HEAD`), or `None` when the command fails or reports nothing — the
/// caller falls back to a repo-wide scan in that case, matching
/// `md_validate_mermaid.rs::get_changed_files`.
let private changedMdFilesOption (repoRoot: string) : string list option =
    try
        let psi = Diagnostics.ProcessStartInfo("git")
        psi.WorkingDirectory <- repoRoot
        psi.ArgumentList.Add("diff")
        psi.ArgumentList.Add("--name-only")
        psi.ArgumentList.Add("@{u}..HEAD")
        psi.RedirectStandardOutput <- true
        psi.UseShellExecute <- false
        use p = Diagnostics.Process.Start psi
        let out = p.StandardOutput.ReadToEnd()
        p.WaitForExit()

        let files =
            out.Split('\n')
            |> Array.map (fun l -> l.Trim())
            |> Array.filter (fun l -> l.EndsWith(".md", StringComparison.Ordinal))
            |> Array.toList

        if List.isEmpty files then None else Some files
    with _ ->
        None

/// `md links validate` [Repo-grounded — `md_validate_links.rs::run`].
let private mdLinksValidateRun
    (repoRoot: string)
    (format: OutputFormat)
    (rawArgs: string list)
    : string * string option =
    let stagedOnly = hasFlag [ "--staged-only" ] rawArgs
    let exclude = collectRepeatableFlag [ "--exclude" ] rawArgs
    let stagedFiles = if stagedOnly then stagedMdFilesOption repoRoot else None

    let result: Md.LinkValidationResult =
        Md.validateAllLinksDetailed
            { RepoRoot = repoRoot
              StagedFiles = stagedFiles
              ExcludePrefixes = exclude }

    let output =
        Formatters.render
            format
            (fun () -> Formatters.linksText result)
            (fun () -> Formatters.linksJson result)
            (fun () -> Formatters.linksMarkdown result)

    let err =
        if List.isEmpty result.BrokenLinks then
            None
        else
            Some(sprintf "found %d broken links" (List.length result.BrokenLinks))

    output, err

let private runMdLinksValidateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let output, err = mdLinksValidateRun repoRoot format rawArgs
    printResultAndExitCode output err

/// `md mermaid validate` [Repo-grounded — `md_validate_mermaid.rs::run`].
let private runMdMermaidValidateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let positional = collectPositionals [ "--exclude" ] rawArgs
    let exclude = collectRepeatableFlag [ "--exclude" ] rawArgs
    let stagedOnly = hasFlag [ "--staged-only" ] rawArgs
    let changedOnly = hasFlag [ "--changed-only" ] rawArgs
    let verbose = hasFlag [ "-v"; "--verbose" ] rawArgs
    let quiet = hasFlag [ "-q"; "--quiet" ] rawArgs
    let maxLabelLen = intFlag [ "--max-label-len" ] 30 rawArgs
    let maxWidth = intFlag [ "--max-width" ] 4 rawArgs
    let maxDepthRaw = intFlag [ "--max-depth" ] 0 rawArgs
    let maxDepth = if maxDepthRaw = 0 then Int32.MaxValue else maxDepthRaw
    let maxSubgraphNodes = intFlag [ "--max-subgraph-nodes" ] 6 rawArgs

    let stagedFiles = if stagedOnly then stagedMdFilesOption repoRoot else None

    let changedFiles =
        if changedOnly && not stagedOnly then
            changedMdFilesOption repoRoot
        else
            None

    let opts: Md.MermaidScanOptions =
        { RepoRoot = repoRoot
          Paths = positional
          StagedFiles = stagedFiles
          ChangedFiles = changedFiles
          ExcludePrefixes = exclude
          Options =
            { MaxLabelLen = maxLabelLen
              MaxWidth = maxWidth
              MaxDepth = maxDepth
              MaxSubgraphNodes = maxSubgraphNodes } }

    let result = Md.validateMermaidDocs opts

    let output =
        Formatters.render
            format
            (fun () -> Md.formatMermaidText result verbose quiet)
            (fun () -> Md.formatMermaidJson result)
            (fun () -> Md.formatMermaidMarkdown result)

    let err =
        if List.isEmpty result.Violations then
            None
        else
            Some(sprintf "found %d violation(s)" (List.length result.Violations))

    printResultAndExitCode output err

/// `md heading-hierarchy validate` [Repo-grounded —
/// `md_validate_heading_hierarchy.rs::run`].
let private runMdHeadingHierarchyValidateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let positional = collectPositionals [ "--exclude" ] rawArgs
    let exclude = collectRepeatableFlag [ "--exclude" ] rawArgs

    let findings: Md.HeadingFinding list =
        if List.isEmpty positional then
            Md.validateDocsHeadingHierarchyAllowlistedDetailed repoRoot exclude
        else
            match Md.validateDocsHeadingHierarchyForPaths repoRoot positional with
            | genericFindings ->
                genericFindings
                |> List.map (fun f ->
                    { Md.HeadingFinding.File = f.Path |> Option.defaultValue ""
                      Line = 0
                      Severity = "high"
                      Kind = ""
                      Message = f.Message })

    let output =
        Formatters.render
            format
            (fun () -> Formatters.headingHierarchyText findings)
            (fun () -> Formatters.headingHierarchyJson findings)
            (fun () -> Formatters.headingHierarchyMarkdown findings)

    let err =
        if List.isEmpty findings then
            None
        else
            Some(sprintf "%d docs heading hierarchy finding(s) found" (List.length findings))

    printResultAndExitCode output err

/// `md naming validate` [Repo-grounded — `md_validate_naming.rs::run`].
let private runMdNamingValidateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let positional = collectPositionals [ "--exempt" ] rawArgs
    let absPaths = resolveAbsPaths repoRoot [ "docs/"; "repo-governance/" ] positional
    let exempt = collectRepeatableFlag [ "--exempt" ] rawArgs

    match Md.validateDocsNamingExempt absPaths exempt with
    | Error message ->
        eprintfn "Error: docs validate-naming failed: %s" message
        1
    | Ok findings ->
        let output =
            Formatters.render
                format
                (fun () -> Formatters.namingText findings)
                (fun () -> Formatters.namingJson findings)
                (fun () -> Formatters.namingMarkdown findings)

        let err =
            if List.isEmpty findings then
                None
            else
                Some(sprintf "%d docs naming finding(s) found" (List.length findings))

        printResultAndExitCode output err

/// `md frontmatter validate` [Repo-grounded —
/// `md_validate_frontmatter.rs::run`].
let private runMdFrontmatterValidateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let positional = collectPositionals [] rawArgs
    let absPaths = resolveAbsPaths repoRoot [ "docs/"; "repo-governance/" ] positional

    match Md.validateDocsFrontmatter absPaths with
    | Error message ->
        eprintfn "Error: docs validate-frontmatter failed: %s" message
        1
    | Ok findings ->
        let output =
            Formatters.render
                format
                (fun () -> Formatters.frontmatterText findings)
                (fun () -> Formatters.frontmatterJson findings)
                (fun () -> Formatters.frontmatterMarkdown findings)

        let failN =
            findings |> List.filter (fun f -> f.Severity = Severity.Blocking) |> List.length

        let err =
            if failN = 0 then
                None
            else
                Some(sprintf "%d docs frontmatter fail-level finding(s) found" failN)

        printResultAndExitCode output err

/// `md frontmatter-dates validate` [Repo-grounded —
/// `md_validate_frontmatter_dates.rs::run`].
let private runMdFrontmatterDatesValidateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let positional = collectPositionals [ "--exclude" ] rawArgs
    let pathFlags = collectPathFlags rawArgs
    let flagExclude = collectRepeatableFlag [ "--exclude" ] rawArgs

    let overridePaths =
        if not (List.isEmpty positional) then
            positional
        else
            pathFlags

    let defaultPaths =
        [ "repo-governance/"
          "docs/explanation/software-engineering/"
          ".claude/agents/"
          ".claude/skills/"
          "plans/" ]

    let absPaths = resolveAbsPaths repoRoot defaultPaths overridePaths

    let registeredExcludes =
        match Governance.registeredExcludesFor repoRoot "md-frontmatter-dates" with
        | Ok excludes -> excludes
        | Error _ -> []

    let excludes =
        registeredExcludes
        @ (flagExclude |> List.filter (fun e -> not (List.contains e registeredExcludes)))

    match Md.validateFrontmatterDatesDetailed absPaths excludes with
    | Error message ->
        eprintfn "Error: frontmatter-audit failed: %s" message
        1
    | Ok findings ->
        let output =
            Formatters.render
                format
                (fun () -> Formatters.frontmatterDatesText findings)
                (fun () -> Formatters.frontmatterDatesJson findings)
                (fun () -> Formatters.frontmatterDatesMarkdown findings)

        let err =
            if List.isEmpty findings then
                None
            else
                Some(sprintf "%d frontmatter finding(s) found" (List.length findings))

        printResultAndExitCode output err

/// `governance word-budget validate` [Repo-grounded —
/// `governance_validate_word_budget.rs::run`/`run_for_root`].
let private runGovernanceWordBudgetValidateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let flagExclude = collectRepeatableFlag [ "--exclude" ] rawArgs

    let registeredExcludes =
        match Governance.registeredExcludes repoRoot with
        | Ok excludes -> excludes
        | Error _ -> []

    let excludes = registeredExcludes @ flagExclude

    match Governance.mergedBudgetConfig repoRoot with
    | Error message ->
        eprintfn "Error: %s" message
        1
    | Ok None ->
        if format = Text then
            printfn "WORD BUDGET: SKIPPED (no governance-word-budget: section in repo-config.yml)"

        0
    | Ok(Some config) ->
        let findings =
            Governance.checkInstructionSizes repoRoot config excludes
            @ (Governance.checkResolvedTree repoRoot config |> Option.toList)

        let output =
            Formatters.render
                format
                (fun () -> Formatters.wordBudgetText findings)
                (fun () -> Formatters.wordBudgetJson findings)
                (fun () -> Formatters.wordBudgetMarkdown findings)

        let hasFail =
            findings
            |> List.exists (fun f -> f.Severity = Governance.WordBudgetSeverity.Fail)

        let err =
            if not hasFail then
                None
            else
                let failCount =
                    findings
                    |> List.filter (fun f -> f.Severity = Governance.WordBudgetSeverity.Fail)
                    |> List.length

                Some(
                    sprintf
                        "word-budget audit failed: %d Fail finding(s); apply progressive disclosure — see repo-governance/principles/content/progressive-disclosure.md"
                        failCount
                )

        printResultAndExitCode output err

/// `governance readme-index validate` [Repo-grounded —
/// `governance_validate_readme_index.rs::run`].
let private runGovernanceReadmeIndexValidateLeaf
    (repoRoot: string)
    (format: OutputFormat)
    (rawArgs: string list)
    : int =
    let positional = collectPositionals [ "--paths"; "--fail-kinds" ] rawArgs
    let pathsFlag = collectRepeatableFlag [ "--paths" ] rawArgs
    let failKinds = collectRepeatableFlag [ "--fail-kinds" ] rawArgs

    let overridePaths =
        if not (List.isEmpty pathsFlag) then
            pathsFlag
        else
            positional

    let relPaths = Governance.resolveScanPaths overridePaths

    let absPaths =
        relPaths
        |> List.map (fun p ->
            if IO.Path.IsPathRooted p then
                p
            else
                IO.Path.Combine(repoRoot, p))

    let findings = Governance.auditReadmeIndex repoRoot absPaths

    let output =
        Formatters.render
            format
            (fun () -> Formatters.readmeIndexText findings)
            (fun () -> Formatters.readmeIndexJson findings)
            (fun () -> Formatters.readmeIndexMarkdown findings)

    let err =
        if Governance.hasFailingFinding findings failKinds then
            Some(sprintf "%d readme-index finding(s) found" (List.length findings))
        else
            None

    printResultAndExitCode output err

/// `governance readme-index generate` [Repo-grounded —
/// `governance_generate_readme_index.rs::run`].
let private runGovernanceReadmeIndexGenerateLeaf
    (repoRoot: string)
    (format: OutputFormat)
    (rawArgs: string list)
    : int =
    let positional = collectPositionals [ "--paths" ] rawArgs
    let pathsFlag = collectRepeatableFlag [ "--paths" ] rawArgs

    let overridePaths =
        if not (List.isEmpty pathsFlag) then
            pathsFlag
        else
            positional

    let relPaths = Governance.resolveScanPaths overridePaths

    let absPaths =
        relPaths
        |> List.map (fun p ->
            if IO.Path.IsPathRooted p then
                p
            else
                IO.Path.Combine(repoRoot, p))

    let written = Governance.generateReadmeIndex repoRoot absPaths

    let output =
        Formatters.render
            format
            (fun () -> Formatters.readmeIndexGenerateText written)
            (fun () -> Formatters.readmeIndexGenerateJson written)
            (fun () -> Formatters.readmeIndexGenerateMarkdown written)

    printResultAndExitCode output None

/// Reproduces clap's exact `error: the following required arguments were
/// not provided: ...` message for `governance readme-index rewrite-paths`
/// byte-for-byte [Repo-grounded — empirically captured from
/// `apps/rhino-cli/target/gate/rhino-cli governance readme-index
/// rewrite-paths` with no arguments].
/// clap's own `--map`-missing usage line echoes every OTHER recognised flag
/// actually present in `rawArgs`, each rendered as `--<name> <PLACEHOLDER>`
/// (bare `--help`, no placeholder), in the order they appear in `rawArgs` —
/// not a fixed schema order. `--map <MAP>` (the missing required arg) always
/// comes first [Repo-grounded — clap's generated usage string; verified
/// against the real Rust binary's `--help`/`-o text`/`-o json`/`-o markdown`
/// output, Wave D integration].
let private readmeIndexRewritePathsMissingArgsError (rawArgs: string list) : string =
    let indexed = rawArgs |> List.mapi (fun i a -> i, a)

    let helpIndex =
        indexed
        |> List.tryFind (fun (_, a) -> a = "--help" || a = "-h")
        |> Option.map fst

    let outputIndex =
        indexed
        |> List.tryFind (fun (_, a) -> a = "-o" || a = "--output")
        |> Option.map fst

    let extras =
        [ helpIndex |> Option.map (fun i -> i, "--help")
          outputIndex |> Option.map (fun i -> i, "--output <OUTPUT>") ]
        |> List.choose id
        |> List.sortBy fst
        |> List.map snd

    let usage =
        ("Usage: rhino-cli governance readme-index rewrite-paths --map <MAP>" :: extras)
        |> String.concat " "

    sprintf "error: the following required arguments were not provided:\n  --map <MAP>\n\n%s\n" usage

/// `governance readme-index rewrite-paths` [Repo-grounded —
/// `governance_rewrite_readme_index_paths.rs::run`]. Unlike every other
/// Wave D leaf, `--map` is required, so — mirroring `test-coverage
/// validate`'s precedent — `route` calls this leaf ahead of the blanket
/// `wantsHelp` shortcut, and a missing `--map` wins over `--help`.
let private runGovernanceReadmeIndexRewritePathsLeaf (repoRoot: string) (rawArgs: string list) : int =
    match stringFlag [ "--map" ] rawArgs with
    | None ->
        eprintf "%s" (readmeIndexRewritePathsMissingArgsError rawArgs)
        2
    | Some mapPath ->
        if wantsHelp (List.toArray rawArgs) then
            printf "%s" HelpText.Text
            0
        else
            match parseOutputFormat rawArgs with
            | Error message ->
                eprintfn "Error: %s" message
                1
            | Ok format ->
                try
                    let mapRaw = IO.File.ReadAllText mapPath

                    let renames =
                        mapRaw.Split('\n')
                        |> Array.map (fun l -> l.TrimEnd('\r'))
                        |> Array.choose (fun line ->
                            let trimmed = line.Trim()

                            if trimmed = "" || trimmed.StartsWith("#", StringComparison.Ordinal) then
                                None
                            else
                                let cols = line.Split('\t')

                                if cols.Length = 2 && cols.[0].Trim() <> "" && cols.[1].Trim() <> "" then
                                    Some(cols.[0].Trim(), cols.[1].Trim())
                                else
                                    None)
                        |> Array.toList

                    let pathsFlag = collectRepeatableFlag [ "--paths" ] rawArgs
                    let relPaths = Governance.resolveScanPaths pathsFlag

                    let absPaths =
                        relPaths
                        |> List.map (fun p ->
                            if IO.Path.IsPathRooted p then
                                p
                            else
                                IO.Path.Combine(repoRoot, p))

                    let rewritten = Governance.rewriteIndexPaths repoRoot absPaths renames

                    let output =
                        Formatters.render
                            format
                            (fun () -> Formatters.readmeIndexRewritePathsText rewritten)
                            (fun () -> Formatters.readmeIndexRewritePathsJson rewritten)
                            (fun () -> Formatters.readmeIndexRewritePathsMarkdown rewritten)

                    printResultAndExitCode output None
                with ex ->
                    eprintfn "Error: read rename map %s: %s" mapPath ex.Message
                    1

/// `git lockfile sync` [Repo-grounded — `commands/git/lockfile.rs::run`].
let private runGitLockfileSyncLeaf (repoRoot: string) : int =
    use writer = new IO.StringWriter()

    match Git.syncAtRoot repoRoot writer with
    | Ok() ->
        printf "%s" (writer.ToString())
        0
    | Error message ->
        printf "%s" (writer.ToString())
        eprintfn "Error: %s" message
        1

/// Reads a `--flag=value` long option out of a leaf's remaining arguments.
let private longOptionValue (name: string) (args: string list) : string option =
    let prefix = sprintf "--%s=" name

    args
    |> List.tryPick (fun arg ->
        if arg.StartsWith(prefix, StringComparison.Ordinal) then
            Some(arg.Substring prefix.Length)
        else
            None)

/// `gate list` [Repo-grounded — `commands/gate/list.rs::run`].
let private runGateListLeaf (repoRoot: string) (args: string list) : int =
    let surface = longOptionValue "surface" args |> Option.defaultValue ""

    let requested = longOptionValue "format" args |> Option.defaultValue "text"

    match parseOutputFormatValue requested with
    | Error message ->
        eprintfn "Error: %s" message
        1
    | Ok format ->
        match Gate.listAtRoot repoRoot surface format (List.contains "--by-group" args) with
        | Ok output ->
            printf "%s" output
            0
        | Error message ->
            eprintfn "Error: %s" message
            1

/// `gate run` [Repo-grounded — `commands/gate/run.rs::run`].
let private runGateRunLeaf (repoRoot: string) (args: string list) : int =
    let surface = longOptionValue "surface" args |> Option.defaultValue ""
    let only = longOptionValue "only" args
    let group = longOptionValue "group" args

    let commitMessageFile =
        args
        |> List.tryFindIndex (fun a -> a = "--")
        |> Option.bind (fun index -> args |> List.skip (index + 1) |> List.tryHead)

    let result =
        match commitMessageFile with
        | Some file -> Gate.runAtRootWithOnlyAndMessageFile repoRoot surface only group (Some file) (printf "%s")
        | None -> Gate.runAtRootWithOnlyAndMessageFile repoRoot surface only group None (printf "%s")

    match result with
    | Ok() -> 0
    | Error message ->
        eprintfn "Error: %s" message
        1

/// `gate emit` [Repo-grounded — `commands/gate/emit.rs::run`].
let private runGateEmitLeaf (repoRoot: string) (args: string list) : int =
    let surface = longOptionValue "surface" args |> Option.defaultValue ""

    match Gate.emitAtRoot repoRoot surface with
    | Ok output ->
        printf "%s" output
        0
    | Error message ->
        eprintfn "Error: %s" message
        1

/// `md audit` [Repo-grounded — `md_audit.rs::run`]. Each member prints its
/// own format-rendered output as it runs — exactly like `convention audit`
/// composes `emoji`/`license` — then the aggregate PASSED/FAILED banner is
/// printed unconditionally as plain text, regardless of `-o`, matching the
/// Rust source's own unconditional `println!`/`eprintln!` for that banner.
/// Runs `leaf`, capturing whatever it writes to stderr instead of letting it
/// reach the real stderr stream, and returns its exit code alongside the
/// captured text (its own `"Error: ..."` line, when it fails) — `md audit`
/// discards each member's own stderr and instead prints one aggregated
/// `"  {name}: {message}"` line per failure, mirroring Rust's `run_member`
/// dispatching straight to each validator's library `run()` (which never
/// touches stderr itself; only the top-level CLI error printer does)
/// [Repo-grounded — `md_audit.rs::run`].
let private captureStderr (leaf: unit -> int) : int * string =
    let original = Console.Error
    use sw = new IO.StringWriter()
    Console.SetError sw

    try
        let code = leaf ()
        code, sw.ToString()
    finally
        Console.SetError original

let private runMdAuditLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let skip = collectRepeatableFlag [ "--skip" ] rawArgs

    let members: (string * (unit -> int)) list =
        [ "validate-naming", (fun () -> runMdNamingValidateLeaf repoRoot format [])
          "validate-frontmatter", (fun () -> runMdFrontmatterValidateLeaf repoRoot format [])
          "validate-heading-hierarchy", (fun () -> runMdHeadingHierarchyValidateLeaf repoRoot format [])
          "validate-links", (fun () -> runMdLinksValidateLeaf repoRoot format [])
          "validate-mermaid", (fun () -> runMdMermaidValidateLeaf repoRoot format [])
          "frontmatter-dates", (fun () -> runMdFrontmatterDatesValidateLeaf repoRoot format [])
          "readme-index", (fun () -> runGovernanceReadmeIndexValidateLeaf repoRoot format []) ]

    let active = members |> List.filter (fun (name, _) -> not (List.contains name skip))

    let failures =
        active
        |> List.choose (fun (name, run) ->
            let code, stderrText = captureStderr run

            if code = 0 then
                None
            else
                // Each leaf's own stderr is exactly one `"Error: {message}\n"`
                // line (mirroring Rust's `anyhow::Error` `Display`) — strip
                // the prefix and trailing newline to recover the bare message.
                let message =
                    stderrText.TrimEnd('\n', '\r')
                    |> fun s ->
                        if s.StartsWith("Error: ", StringComparison.Ordinal) then
                            s.Substring("Error: ".Length)
                        else
                            s

                Some(name, message))

    if List.isEmpty failures then
        printfn "MD AUDIT PASSED: all %d validators passed" (List.length active)
        0
    else
        eprintfn "MD AUDIT FAILED: %d validator(s) reported failures" (List.length failures)

        for name, message in failures do
            eprintfn "  %s: %s" name message

        eprintfn "Error: md audit found %d failure(s)" (List.length failures)
        1

/// The command paths `route` recognises, in match order: each entry pairs the
/// literal argv prefix with the leaf name `route` dispatches on. Held as data
/// rather than as one `match` over cons-of-string-literal patterns because
/// FSharpLint's project-mode analysis is super-linear in that pattern's arm
/// count — at 25 arms a `dotnet fsharplint lint` of this project ran over an
/// hour without finishing, against 7 seconds for this form
/// [Repo-grounded — measured on both shapes of this file; see
/// `plans/in-progress/rewrite-rhino-cli-to-fsharp/learnings.md`].
/// `repo-governance vendor validate` [Repo-grounded —
/// `governance_vendor_audit.rs::run`]. The optional positional path defaults
/// to `repo-governance/`.
let private runRepoGovernanceVendorValidateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let scanPath =
        match collectPositionals [] rawArgs with
        | path :: _ -> path
        | [] -> "repo-governance"

    let fullPath =
        if System.IO.Path.IsPathRooted scanPath then
            scanPath
        else
            System.IO.Path.Combine(repoRoot, scanPath)

    let findings = RepoGovernance.walkVendor fullPath

    let output =
        Formatters.render
            format
            (fun () -> Formatters.vendorAuditText findings)
            (fun () -> Formatters.vendorAuditJson findings)
            (fun () -> Formatters.vendorAuditMarkdown findings)

    let err =
        if List.isEmpty findings then
            None
        else
            Some(sprintf "%d violation(s) found" (List.length findings))

    printResultAndExitCode output err

/// `repo-governance layer-coherence validate` [Repo-grounded —
/// `governance_layer_coherence.rs::run`].
let private runRepoGovernanceLayerCoherenceValidateLeaf (repoRoot: string) (format: OutputFormat) : int =
    let findings = RepoGovernance.auditLayerCoherence repoRoot

    let output =
        Formatters.render
            format
            (fun () -> Formatters.layerCoherenceText findings)
            (fun () -> Formatters.layerCoherenceJson findings)
            (fun () -> Formatters.layerCoherenceMarkdown findings)

    let err =
        if List.isEmpty findings then
            None
        else
            Some(sprintf "%d layer-coherence finding(s) reported" (List.length findings))

    printResultAndExitCode output err

/// `repo-governance traceability validate` [Repo-grounded —
/// `governance_traceability_audit.rs::run`].
let private runRepoGovernanceTraceabilityValidateLeaf (repoRoot: string) (format: OutputFormat) : int =
    let findings = RepoGovernance.auditTraceability repoRoot

    let output =
        Formatters.render
            format
            (fun () -> Formatters.traceabilityText findings)
            (fun () -> Formatters.traceabilityJson findings)
            (fun () -> Formatters.traceabilityMarkdown findings)

    let err =
        if List.isEmpty findings then
            None
        else
            Some(sprintf "%d traceability finding(s) reported" (List.length findings))

    printResultAndExitCode output err

/// `repo-governance audit` [Repo-grounded — `governance_audit.rs::run`].
/// `RHINO_AUDIT_NOW` pins the envelope's `ran_at`, the one field a
/// byte-identity comparison cannot otherwise stabilise.
let private runRepoGovernanceAuditLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let envNow = Environment.GetEnvironmentVariable "RHINO_AUDIT_NOW"

    let opts: RepoGovernance.AuditOptions =
        { RepoRoot = repoRoot
          Skip = collectRepeatableFlag [ "--skip" ] rawArgs
          IncludeOnly = collectRepeatableFlag [ "--include-category" ] rawArgs
          Now = (if String.IsNullOrEmpty envNow then None else Some envNow)
          KnownFalsePositivesPath = None
          ExcludeGlobs = collectRepeatableFlag [ "--exclude" ] rawArgs }

    let envelope = RepoGovernance.runAudit opts

    let output =
        Formatters.render
            format
            (fun () -> Formatters.governanceAuditText envelope)
            (fun () -> Formatters.governanceAuditJson envelope)
            (fun () -> Formatters.governanceAuditMarkdown envelope)

    let err =
        if envelope.Result.TotalFindings = 0 then
            None
        else
            Some(
                sprintf
                    "%d governance finding(s) reported across %d categor(ies)"
                    envelope.Result.TotalFindings
                    (List.length envelope.Result.Categories)
            )

    printResultAndExitCode output err

/// `specs counts validate` [Repo-grounded — `specs_validate_counts.rs::run_at_root`].
/// A positional folder wins over `--apps`; with neither, the folder list is
/// `repo-config.yml`'s `specs.ddd-areas`, so the default scan targets are repo
/// data rather than a hard-coded allowlist.
let private specsCountsValidateRun (repoRoot: string) (rawArgs: string list) : string * string option =
    let positional = collectPositionals [ "--apps" ] rawArgs

    let apps =
        collectRepeatableFlag [ "--apps" ] rawArgs
        |> List.collect (fun v -> v.Split(',') |> List.ofArray)
        |> List.map (fun s -> s.Trim())
        |> List.filter (fun s -> s <> "")

    let folders =
        match positional with
        | folder :: _ -> [ folder ]
        | [] ->
            let defaults =
                if List.isEmpty apps then
                    (RepoConfig.loadOrDefault repoRoot).Specs.DddAreas
                else
                    apps

            defaults |> List.map (sprintf "specs/apps/%s")

    let sb = Text.StringBuilder()
    let mutable total = 0

    for folder in folders do
        let findings = Specs.validateSpecCounts repoRoot folder
        total <- total + List.length findings

        if List.isEmpty findings then
            sb.Append(sprintf "specs validate-counts: 0 finding(s) for \"%s\"\n" folder)
            |> ignore
        else
            for f in findings do
                sb.Append(sprintf "%s: %s: %s\n" f.File f.Criticality f.Evidence) |> ignore

    let err =
        if total = 0 then
            None
        else
            Some(sprintf "%d finding(s) found by specs validate-counts" total)

    sb.ToString(), err

let private runSpecsCountsValidateLeaf (repoRoot: string) (rawArgs: string list) : int =
    let output, err = specsCountsValidateRun repoRoot rawArgs
    printResultAndExitCode output err

/// `specs structure validate` [Repo-grounded —
/// `specs_structure_validate.rs::run_at_root`]. Layers adoption → tree →
/// counts for every app, plus the bounded-context and glossary layers for
/// apps `repo-config.yml` declares a DDD area.
let private specsStructureValidateRun (repoRoot: string) (rawArgs: string list) : string * string option =
    let config = RepoConfig.loadOrDefault repoRoot
    let dddAreas = config.Specs.DddAreas
    let positional = collectPositionals [ "--apps" ] rawArgs

    let flagApps =
        collectRepeatableFlag [ "--apps" ] rawArgs
        |> List.collect (fun v -> v.Split(',') |> List.ofArray)
        |> List.map (fun s -> s.Trim())
        |> List.filter (fun s -> s <> "")

    let apps =
        match positional with
        | app :: _ -> [ app ]
        | [] when not (List.isEmpty flagApps) -> flagApps
        | [] ->
            let specsApps = IO.Path.Combine(repoRoot, "specs", "apps")

            if IO.Directory.Exists specsApps then
                IO.Directory.GetDirectories specsApps
                |> Array.map IO.Path.GetFileName
                |> Array.sortWith (fun a b -> String.CompareOrdinal(a, b))
                |> List.ofArray
            else
                []

    let sb = Text.StringBuilder()
    let mutable total = 0

    for app in apps do
        let isDddArea = List.contains app dddAreas
        let adoption = Specs.validateSpecAdoptionDddAware repoRoot app isDddArea

        for f in adoption do
            sb.Append(sprintf "adoption: %s: HIGH: %s\n" f.File f.Evidence) |> ignore

        let tree =
            Specs.validateSpecTree repoRoot app
            @ Specs.validateSpecGherkinDomains repoRoot app

        for f in tree do
            sb.Append(sprintf "tree: %s: HIGH: %s\n" f.File f.Evidence) |> ignore

        let counts = Specs.validateSpecCounts repoRoot (sprintf "specs/apps/%s" app)

        for f in counts do
            sb.Append(sprintf "counts: %s: HIGH: %s\n" f.File f.Evidence) |> ignore

        let mutable bcCount = 0
        let mutable ulCount = 0

        if isDddArea then
            match
                Ddd.validateBoundedContexts
                    { RepoRoot = repoRoot
                      App = app
                      Severity = None }
            with
            | Ok findings ->
                for f in findings do
                    sb.Append(sprintf "bc: %s: %s: %s\n" f.File (Ddd.severityCode f.Severity) f.Message)
                    |> ignore

                bcCount <- List.length findings
            | Error message ->
                sb.Append(sprintf "bc: %s: HIGH: %s\n" app message) |> ignore
                bcCount <- 1

            match
                Glossary.validateAll
                    { RepoRoot = repoRoot
                      App = app
                      Severity = None }
            with
            | Ok findings ->
                for f in findings do
                    sb.Append(sprintf "ul: %s: %s: %s\n" f.File (Ddd.severityCode f.Severity) f.Message)
                    |> ignore

                ulCount <- List.length findings
            | Error message ->
                sb.Append(sprintf "ul: %s: HIGH: %s\n" app message) |> ignore
                ulCount <- 1

        total <-
            total
            + List.length adoption
            + List.length tree
            + List.length counts
            + bcCount
            + ulCount

        if
            List.isEmpty adoption
            && List.isEmpty tree
            && List.isEmpty counts
            && bcCount = 0
            && ulCount = 0
        then
            sb.Append(sprintf "specs structure validate: 0 finding(s) for \"%s\"\n" app)
            |> ignore

    let err =
        if total = 0 then
            None
        else
            Some(sprintf "%d finding(s) found by specs structure validate" total)

    sb.ToString(), err

let private runSpecsStructureValidateLeaf (repoRoot: string) (rawArgs: string list) : int =
    let output, err = specsStructureValidateRun repoRoot rawArgs
    printResultAndExitCode output err

/// `specs gherkin-cardinality validate` [Repo-grounded —
/// `specs_gherkin_cardinality.rs::run`]. Positional paths win over `-p`/`--path`;
/// with neither, the whole repository is scanned.
let private specsCardinalityRun
    (repoRoot: string)
    (format: OutputFormat)
    (rawArgs: string list)
    : string * string option =
    let positional = collectPositionals [] rawArgs
    let flagged = collectPathFlags rawArgs

    let relative =
        if not (List.isEmpty positional) then positional
        elif not (List.isEmpty flagged) then flagged
        else [ "." ]

    let fullPaths =
        relative
        |> List.map (fun p ->
            if IO.Path.IsPathRooted p then
                p
            else
                IO.Path.Combine(repoRoot, p))

    match Specs.auditGherkinKeywordCardinality fullPaths with
    | Error message -> "", Some message
    | Ok findings ->
        let output =
            Formatters.render
                format
                (fun () -> Formatters.cardinalityText findings)
                (fun () -> Formatters.cardinalityJson findings)
                (fun () -> Formatters.cardinalityMarkdown findings)

        let err =
            if List.isEmpty findings then
                None
            else
                Some(sprintf "%d gherkin keyword cardinality finding(s) found" (List.length findings))

        output, err

let private runSpecsCardinalityLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let output, err = specsCardinalityRun repoRoot format rawArgs
    printResultAndExitCode output err

/// `specs scaffold dart` [Repo-grounded — `specs_scaffold_dart.rs::run`].
/// `--dir` defaults to the process working directory, not the repo root.
let private runSpecsScaffoldDartLeaf (format: OutputFormat) (rawArgs: string list) : int =
    let dir = stringFlag [ "--dir" ] rawArgs |> Option.defaultValue "."

    match Contracts.scaffoldDart { Dir = IO.Path.GetFullPath dir } with
    | Error message ->
        eprintfn "Error: %s" message
        1
    | Ok result ->
        let output =
            Formatters.render
                format
                (fun () -> Formatters.dartScaffoldText result)
                (fun () -> Formatters.dartScaffoldJson result)
                (fun () -> Formatters.dartScaffoldMarkdown result)

        printResultAndExitCode output None

/// `specs audit` [Repo-grounded — `specs_audit.rs::run`]. Runs the three
/// default-argument validators in order; `behavior-coverage`, `domain-coverage`,
/// `bc`, and `ul` are excluded because they need positional arguments `audit`
/// cannot default.
let private runSpecsAuditLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let skip = collectRepeatableFlag [ "--skip" ] rawArgs
    let members = [ "structure-validate"; "validate-links"; "gherkin-cardinality" ]
    let failures = ResizeArray<string>()

    for name in members do
        if not (List.contains name skip) then
            let output, err =
                match name with
                | "structure-validate" -> specsStructureValidateRun repoRoot []
                | "validate-links" -> mdLinksValidateRun repoRoot format []
                | _ -> specsCardinalityRun repoRoot format []

            printf "%s" output

            match err with
            | Some message -> failures.Add(sprintf "%s: %s" name message)
            | None -> ()

    if failures.Count = 0 then
        printfn "SPECS AUDIT PASSED: all %d validators passed" (List.length members - List.length skip)
        0
    else
        eprintfn "SPECS AUDIT FAILED: %d validator(s) reported failures" failures.Count

        for f in failures do
            eprintfn "  %s" f

        eprintfn "Error: specs audit found %d failure(s)" failures.Count
        1

/// Value-taking flags on `specs behavior-coverage validate`, listed so
/// `collectPositionals` never mistakes a flag's value for a path.
let private coverageValueFlags =
    [ "--exclude-dir"
      "--exclude-source-dir"
      "--unit-dir"
      "--integration-dir"
      "--e2e-dir"
      "--unit-report"
      "--integration-report"
      "--e2e-report" ]

/// One level of a three-level coverage run.
type private LevelDir =
    { Name: string
      TestLevel: Specs.TestLevel
      Dir: string
      Report: string option }

let private capitalizeFirst (s: string) : string =
    if s = "" then
        s
    else
        string (Char.ToUpperInvariant s.[0]) + s.Substring 1

/// `Ok None` when no level dir is given, `Ok (Some levels)` when all three
/// are, and `Error` for a partial set [Repo-grounded —
/// `specs_coverage.rs::resolve_level_dirs`].
let private resolveLevelDirs (repoRoot: string) (rawArgs: string list) : Result<LevelDir list option, string> =
    let dirOf (flag: string) = stringFlag [ flag ] rawArgs

    let unitDir = dirOf "--unit-dir"
    let integrationDir = dirOf "--integration-dir"
    let e2eDir = dirOf "--e2e-dir"

    let present =
        [ unitDir; integrationDir; e2eDir ] |> List.filter Option.isSome |> List.length

    let level name testLevel (dir: string option) (reportFlag: string) =
        { Name = name
          TestLevel = testLevel
          Dir = IO.Path.Combine(repoRoot, Option.get dir)
          Report = dirOf reportFlag |> Option.map (fun r -> IO.Path.Combine(repoRoot, r)) }

    match present with
    | 0 -> Ok None
    | 3 ->
        Ok(
            Some
                [ level "unit" Specs.Unit unitDir "--unit-report"
                  level "integration" Specs.Integration integrationDir "--integration-report"
                  level "e2e" Specs.E2e e2eDir "--e2e-report" ]
        )
    | _ -> Error "must provide all three or none of --unit-dir, --integration-dir, --e2e-dir"

let private scanOptionsFor
    (repoRoot: string)
    (specsDirs: string list)
    (appDir: string)
    (rawArgs: string list)
    : Specs.ScanOptions =
    { RepoRoot = repoRoot
      SpecsDir = List.head specsDirs
      SpecsDirs = specsDirs
      AppDir = appDir
      SharedSteps = hasFlag [ "--shared-steps" ] rawArgs
      ExcludeDirs = collectRepeatableFlag [ "--exclude-dir" ] rawArgs
      ExcludeSourceDirs = collectRepeatableFlag [ "--exclude-source-dir" ] rawArgs }

let private coverageHasGaps (result: Specs.CheckResult) : bool =
    not (
        List.isEmpty result.Gaps
        && List.isEmpty result.ScenarioGaps
        && List.isEmpty result.StepGaps
        && List.isEmpty result.OrphanStepImpls
    )

let private printCoverageResult (format: OutputFormat) (result: Specs.CheckResult) : unit =
    printf
        "%s"
        (Formatters.render
            format
            (fun () -> Formatters.coverageText result)
            (fun () -> Formatters.coverageJson result)
            (fun () -> Formatters.coverageMarkdown result))

let private levelName (level: Specs.TestLevel) : string = Specs.testLevelName level

let private printMarkerViolations (violations: Specs.BehaviorCoverageViolation list) : unit =
    if not (List.isEmpty violations) then
        printfn "\n@covers marker violations (%d):" (List.length violations)

        for v in violations do
            match v with
            | Specs.UntaggedScenario(featurePath, title) ->
                printfn "  - %s\n    → Scenario: \"%s\" has no @unit/@integration/@e2e level tag" featurePath title
            | Specs.LevelOutsideEnvelope(featurePath, title, requiredLevel) ->
                printfn
                    "  - %s\n    → Scenario: \"%s\" requires level [%s], which is outside the project envelope"
                    featurePath
                    title
                    (levelName requiredLevel)
            | Specs.MissingCoverage(featurePath, title, missingLevel) ->
                printfn
                    "  - %s\n    → Scenario: \"%s\" has no @covers marker at the [%s] level"
                    featurePath
                    title
                    (levelName missingLevel)
            | Specs.CoverageAtUndeclaredLevel(sourceFile, featurePath, title, extraLevel) ->
                printfn
                    "  - %s\n    → marks \"%s\" (%s) covered at [%s], a level not declared on that scenario"
                    sourceFile
                    title
                    featurePath
                    (levelName extraLevel)
            | Specs.OrphanMarker(sourceFile, featurePath, scenarioTitle) ->
                printfn
                    "  - %s\n    → marks \"%s\" (%s), which no feature file contains (orphan marker)"
                    sourceFile
                    scenarioTitle
                    featurePath

let private printRuntimeViolations (violations: Specs.RuntimeCoverageViolation list) : unit =
    if not (List.isEmpty violations) then
        printfn "\nRuntime cross-check violations (%d):" (List.length violations)

        for v in violations do
            match v with
            | Specs.NotExecuted(sourceFile, featurePath, scenarioTitle, level) ->
                printfn
                    "  - %s\n    → Scenario: \"%s\" [%s] marked-but-not-executed (marker: %s)"
                    featurePath
                    scenarioTitle
                    (levelName level)
                    sourceFile
            | Specs.RunFailed(sourceFile, featurePath, scenarioTitle, level) ->
                printfn
                    "  - %s\n    → Scenario: \"%s\" [%s] marked-but-failed (marker: %s)"
                    featurePath
                    scenarioTitle
                    (levelName level)
                    sourceFile

/// Three-level mode: one coverage pass per level dir, then the opt-in
/// `@covers` marker and runtime cross-checks [Repo-grounded —
/// `specs_coverage.rs::run_three_level`].
let private runThreeLevel
    (repoRoot: string)
    (levels: LevelDir list)
    (specsDirs: string list)
    (format: OutputFormat)
    (rawArgs: string list)
    : int =
    let failingLevels = ResizeArray<string>()

    for level in levels do
        printfn "=== %s level ===" (capitalizeFirst level.Name)
        let result = Specs.checkAll (scanOptionsFor repoRoot specsDirs level.Dir rawArgs)
        printCoverageResult format result

        if coverageHasGaps result then
            failingLevels.Add level.Name

            if format = Text then
                eprintfn
                    "\nERROR: [%s] spec coverage gaps found: %d file gap(s), %d scenario gap(s), %d step gap(s), %d orphan step impl(s)"
                    level.Name
                    (List.length result.Gaps)
                    (List.length result.ScenarioGaps)
                    (List.length result.StepGaps)
                    (List.length result.OrphanStepImpls)

    // The marker and runtime checks stay opt-in: without a `--<level>-report`
    // every existing three-level caller would start failing on level-tag
    // violations it never opted into.
    let coversEnabled = levels |> List.exists (fun l -> l.Report.IsSome)

    let markerViolations, runtimeViolations =
        if not coversEnabled then
            [], []
        else
            let scenarios =
                specsDirs
                |> List.collect (fun specsDir ->
                    Specs.coverageWalkFeatureFiles specsDir []
                    |> List.collect (fun featureFile ->
                        let featurePath =
                            if featureFile.StartsWith(repoRoot, StringComparison.Ordinal) then
                                featureFile.Substring(repoRoot.Length).TrimStart(IO.Path.DirectorySeparatorChar)
                            else
                                featureFile

                        Specs.extractScenarioSpecs featureFile featurePath))

            let markers =
                levels
                |> List.collect (fun level -> Specs.extractCoversMarkers level.Dir level.TestLevel repoRoot)

            let envelope: Specs.ProjectEnvelope =
                { Levels = set [ Specs.Unit; Specs.Integration; Specs.E2e ] }

            let runtime =
                levels
                |> List.collect (fun level ->
                    match level.Report with
                    | None -> []
                    | Some reportPath ->
                        let levelMarkers = Specs.extractCoversMarkers level.Dir level.TestLevel repoRoot

                        if List.isEmpty levelMarkers then
                            []
                        else
                            match Specs.parseRunReport (IO.File.ReadAllText reportPath) with
                            | Error message -> failwith message
                            | Ok report -> Specs.checkRuntime levelMarkers report)

            Specs.validate scenarios markers envelope, runtime

    if format = Text then
        printMarkerViolations markerViolations
        printRuntimeViolations runtimeViolations

    if
        failingLevels.Count = 0
        && List.isEmpty markerViolations
        && List.isEmpty runtimeViolations
    then
        0
    else
        let parts =
            [ if failingLevels.Count > 0 then
                  sprintf "level(s) %s" (String.concat ", " failingLevels)
              if not (List.isEmpty markerViolations) then
                  sprintf "%d @covers marker violation(s)" (List.length markerViolations)
              if not (List.isEmpty runtimeViolations) then
                  sprintf "%d runtime cross-check violation(s)" (List.length runtimeViolations) ]

        eprintfn "Error: spec coverage gaps found: %s" (String.concat "; " parts)
        1

/// Reproduces clap's own missing-required-argument diagnostic for the
/// coverage leaves, whose two-positional arity is enforced by
/// `#[arg(required = true, num_args = 2..)]` rather than by handler code
/// [Repo-grounded — observed `rhino-cli specs behavior-coverage validate`
/// output]. The usage line echoes back the flags clap actually saw, and both
/// shapes exit `2`, the clap parse-failure code.
let private printMissingPathsError (leafPath: string) (rawArgs: string list) (provided: int) : int =
    let flagSegment =
        if hasFlag [ "--help"; "-h" ] rawArgs then
            "--help "
        elif
            rawArgs
            |> List.exists (fun a ->
                a = "-o"
                || a = "--output"
                || a.StartsWith("--output=", StringComparison.Ordinal))
        then
            "--output <OUTPUT> "
        elif provided > 0 then
            "[OPTIONS] "
        else
            ""

    if provided = 0 then
        eprintfn "error: the following required arguments were not provided:"
        eprintfn "  <PATHS> <PATHS>..."
    else
        eprintfn "error: %d values required by '<PATHS> <PATHS>...'; only %d was provided" 2 provided

    eprintfn ""
    eprintfn "Usage: rhino-cli %s %s<PATHS> <PATHS>..." leafPath flagSegment
    2

/// `specs behavior-coverage validate` [Repo-grounded — `specs_coverage.rs::run`].
let private runSpecsBehaviorCoverageLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let paths = collectPositionals coverageValueFlags rawArgs

    if List.length paths < 2 then
        printMissingPathsError "specs behavior-coverage validate" rawArgs (List.length paths)
    else
        let specsDirs =
            paths
            |> List.take (List.length paths - 1)
            |> List.map (fun sd -> IO.Path.Combine(repoRoot, sd))

        match resolveLevelDirs repoRoot rawArgs with
        | Error message ->
            eprintfn "Error: %s" message
            1
        | Ok(Some levels) -> runThreeLevel repoRoot levels specsDirs format rawArgs
        | Ok None ->
            let appDir = IO.Path.Combine(repoRoot, List.last paths)
            let result = Specs.checkAll (scanOptionsFor repoRoot specsDirs appDir rawArgs)
            printCoverageResult format result

            if not (coverageHasGaps result) then
                0
            else
                if format = Text then
                    if not (List.isEmpty result.Gaps) then
                        eprintfn "\nERROR: Found %d spec(s) without matching test files" (List.length result.Gaps)

                    if not (List.isEmpty result.ScenarioGaps) then
                        eprintfn
                            "ERROR: Found %d scenario(s) without matching test implementations"
                            (List.length result.ScenarioGaps)

                    if not (List.isEmpty result.StepGaps) then
                        eprintfn
                            "ERROR: Found %d step(s) without matching step definitions"
                            (List.length result.StepGaps)

                    if not (List.isEmpty result.OrphanStepImpls) then
                        eprintfn
                            "ERROR: Found %d orphan step implementation(s) (no Gherkin step matches them)"
                            (List.length result.OrphanStepImpls)

                eprintfn
                    "Error: spec coverage gaps found: %d file gap(s), %d scenario gap(s), %d step gap(s), %d orphan step impl(s)"
                    (List.length result.Gaps)
                    (List.length result.ScenarioGaps)
                    (List.length result.StepGaps)
                    (List.length result.OrphanStepImpls)

                1

/// `specs domain-coverage validate` [Repo-grounded —
/// `specs_coverage.rs::run_domain`]. A project absent from
/// `repo-config.yml`'s `specs.domain-areas` is skipped, not scanned.
let private runSpecsDomainCoverageLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let paths = collectPositionals coverageValueFlags rawArgs

    if List.length paths < 2 then
        printMissingPathsError "specs domain-coverage validate" rawArgs (List.length paths)
    else
        let appDirPath = List.last paths
        let projectName = IO.Path.GetFileName(appDirPath.TrimEnd('/'))
        let config = RepoConfig.loadOrDefault repoRoot

        if Specs.isEligible projectName config.Specs.DomainAreas then
            runSpecsBehaviorCoverageLeaf repoRoot format rawArgs
        else
            let message =
                sprintf
                    "specs domain-coverage validate: skipped — \"%s\" is not listed in repo-config.yml's specs.domain-areas"
                    projectName

            match format with
            | Text -> printfn "%s" message
            | Json ->
                printfn "{\"skipped\":true,\"project\":\"%s\",\"reason\":\"not in specs.domain-areas\"}" projectName
            | Markdown -> printfn "- %s" message

            0

/// Resolves a `--features` glob relative to `projectDir`, returning matched
/// `.feature` paths [Repo-grounded — `specs_e2e_coverage.rs::collect_declared`,
/// which delegates to the `glob` crate].
let private globFeatureFiles (projectDir: string) (pattern: string) : string list =
    let combined = IO.Path.Combine(projectDir, pattern)
    let normalized = combined.Replace('\\', '/')

    match normalized.IndexOf '*' with
    | -1 -> if IO.File.Exists combined then [ combined ] else []
    | starIndex ->
        let lastSlashBeforeStar = normalized.LastIndexOf('/', starIndex)

        let root =
            if lastSlashBeforeStar < 0 then
                "."
            else
                normalized.Substring(0, lastSlashBeforeStar)

        let tail = normalized.Substring(lastSlashBeforeStar + 1)

        if not (IO.Directory.Exists root) then
            []
        else
            let searchOption =
                if tail.Contains "**" then
                    IO.SearchOption.AllDirectories
                else
                    IO.SearchOption.TopDirectoryOnly

            let filePattern =
                let last = tail.Split('/') |> Array.last
                if last = "" then "*" else last

            IO.Directory.GetFiles(root, filePattern, searchOption)
            |> Array.sortWith (fun a b -> String.CompareOrdinal(a, b))
            |> List.ofArray

/// `specs e2e-coverage validate` [Repo-grounded — `specs_e2e_coverage.rs::run`].
let private runSpecsE2eCoverageLeaf (format: OutputFormat) (rawArgs: string list) : int =
    let valueFlags = [ "--features"; "--features-gen"; "--baseline"; "--project" ]
    let features = collectRepeatableFlag [ "--features" ] rawArgs
    let featuresGen = stringFlag [ "--features-gen" ] rawArgs
    let baseline = stringFlag [ "--baseline" ] rawArgs
    let project = stringFlag [ "--project" ] rawArgs

    let missing =
        [ if List.isEmpty features then
              "  --features <GLOB>"
          if featuresGen.IsNone then
              "  --features-gen <DIR>"
          if baseline.IsNone then
              "  --baseline <PATH>"
          if project.IsNone then
              "  --project <NAME>" ]

    if not (List.isEmpty missing) then
        // clap reports every missing required flag at once, then echoes the
        // full required-argument usage line including the flags it did see.
        eprintfn "error: the following required arguments were not provided:"

        for m in missing do
            eprintfn "%s" m

        let seen =
            [ if hasFlag [ "--help"; "-h" ] rawArgs then
                  "--help"
              if
                  rawArgs
                  |> List.exists (fun a ->
                      a = "-o"
                      || a = "--output"
                      || a.StartsWith("--output=", StringComparison.Ordinal))
              then
                  "--output <OUTPUT>" ]

        eprintfn ""

        eprintfn
            "Usage: rhino-cli specs e2e-coverage validate --features <GLOB> --features-gen <DIR> --baseline <PATH> --project <NAME>%s [PROJECT_DIR]"
            (if List.isEmpty seen then
                 ""
             else
                 " " + String.concat " " seen)

        2
    else
        let projectDir =
            match collectPositionals valueFlags rawArgs with
            | dir :: _ -> dir
            | [] -> "."

        let featuresGenDir = IO.Path.Combine(projectDir, Option.get featuresGen)
        let baselinePath = IO.Path.Combine(projectDir, Option.get baseline)

        let declaredWithPaths =
            features
            |> List.collect (fun pattern ->
                globFeatureFiles projectDir pattern
                |> List.collect (fun path ->
                    let canonical = IO.Path.GetFullPath path

                    Specs.extractScenarioSpecs path path
                    |> Specs.declaredE2eEntries
                    |> List.map (fun entry -> canonical, entry)))

        let anyFeatureFileMatched =
            features
            |> List.exists (fun pattern -> not (List.isEmpty (globFeatureFiles projectDir pattern)))

        // The generated-output scan runs before the empty-glob guard: a
        // missing `.features-gen` is the more specific diagnostic, and both
        // conditions can hold at once on a freshly scaffolded project.
        match Specs.scanFixmeDir featuresGenDir with
        | Error message ->
            eprintfn "Error: %s" message
            1
        | Ok fixmeByFile ->
            if not anyFeatureFileMatched then
                eprintfn
                    "Error: --features matched no .feature files across glob(s) %A — check for a path typo or directory rename (an empty declared set would otherwise make this gate always silently pass)"
                    features

                1
            else
                let fixme =
                    declaredWithPaths
                    |> List.filter (fun (featureAbs, entry) ->
                        Specs.isUnboundOrAbsent featureAbs entry.Scenario fixmeByFile)
                    |> List.map snd

                let declared = declaredWithPaths |> List.map snd

                if hasFlag [ "--update-baseline" ] rawArgs then
                    match
                        Specs.saveBaseline
                            baselinePath
                            { Project = Option.get project
                              AllowedUnbound = fixme }
                    with
                    | Error message ->
                        eprintfn "Error: %s" message
                        1
                    | Ok() ->
                        printfn "Wrote baseline manifest to %s" baselinePath
                        0
                else
                    match Specs.loadBaseline baselinePath with
                    | Error message ->
                        eprintfn "Error: %s" message
                        1
                    | Ok manifest ->
                        let report = Specs.diffGaps declared fixme manifest.AllowedUnbound

                        let output =
                            Formatters.render
                                format
                                (fun () -> Specs.formatGapText report)
                                (fun () -> Specs.formatGapJson report)
                                (fun () -> Specs.formatGapMarkdown report)

                        let err =
                            if report.Failed then
                                Some(
                                    sprintf
                                        "%d new unbound scenario(s) found beyond baseline"
                                        (List.length report.NewGaps)
                                )
                            else
                                None

                        printResultAndExitCode output err

/// Prints a validation result in the requested format and returns the exit
/// code, with `errorFor` naming the failure message shape each harness leaf
/// uses [Repo-grounded — the `harness_validate_*.rs` wrappers, which share
/// this body and differ only in that message].
let private reportValidation
    (format: OutputFormat)
    (result: Harness.ValidationResult)
    (rawArgs: string list)
    (errorFor: int -> string)
    : int =
    let verbose = hasFlag [ "--verbose"; "-v" ] rawArgs
    let quiet = hasFlag [ "--quiet"; "-q" ] rawArgs

    match format with
    | Text -> printf "%s" (Formatters.validationText result verbose quiet)
    | Json -> printfn "%s" (Formatters.validationJson result)
    | Markdown -> printf "%s" (Formatters.validationMarkdown result verbose)

    if result.FailedChecks = 0 then
        0
    else
        eprintfn "Error: %s" (errorFor result.FailedChecks)
        1

/// `harness duplication validate` [Repo-grounded —
/// `harness_validate_duplication.rs::run`].
let private runHarnessDuplicationLeaf (repoRoot: string) (format: OutputFormat) : int =
    match Harness.detectDuplication repoRoot with
    | Error message ->
        eprintfn "Error: agents detect-duplication failed: %s" message
        1
    | Ok findings ->
        let output =
            Formatters.render
                format
                (fun () -> Formatters.duplicationText findings)
                (fun () -> Formatters.duplicationJson findings)
                (fun () -> Formatters.duplicationMarkdown findings)

        let err =
            if List.isEmpty findings then
                None
            else
                Some(sprintf "%d duplication cluster(s) detected" (List.length findings))

        printResultAndExitCode output err

/// `harness claude validate` [Repo-grounded — `harness_validate_claude.rs::run`].
let private runHarnessClaudeLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let agentsOnly = hasFlag [ "--agents-only" ] rawArgs
    let skillsOnly = hasFlag [ "--skills-only" ] rawArgs

    if agentsOnly && skillsOnly then
        eprintfn "Error: cannot use --agents-only and --skills-only together"
        1
    else
        let result =
            Harness.validateClaude
                { RepoRoot = repoRoot
                  AgentsOnly = agentsOnly
                  SkillsOnly = skillsOnly }

        reportValidation format result rawArgs (sprintf "validation failed: %d checks failed")

/// `harness sync validate` [Repo-grounded — `harness_validate_sync.rs::run`].
let private runHarnessSyncValidateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    reportValidation format (Harness.validateSync repoRoot) rawArgs (sprintf "validation failed: %d checks failed")

/// `harness bindings validate` [Repo-grounded — `harness_validate_bindings.rs::run`].
let private runHarnessBindingsValidateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    reportValidation
        format
        (Harness.validateBindings repoRoot)
        rawArgs
        (sprintf "binding validation failed: %d checks failed")

/// `harness ownership validate` [Repo-grounded — `harness_validate_ownership.rs::run`].
let private runHarnessOwnershipLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    reportValidation
        format
        (Harness.validateOwnership repoRoot)
        rawArgs
        (sprintf "ownership validation failed: %d checks failed")

[<Literal>]
let private CatalogCheckName = "Harness catalog: generated region"

/// Rebuilds the single-check `ValidationResult` the catalog leaves report.
/// Both leaves render the same document once and differ only in whether a
/// divergence is repaired or reported [Repo-grounded —
/// `harness_catalog.rs::run_generate`, `run_validate`].
let private catalogValidationResult
    (outcome: Harness.HarnessCatalogOutcome)
    (relative: string)
    : Harness.ValidationResult =
    let check =
        if outcome.ExitCode = 0 then
            Harness.ValidationCheck.passed CatalogCheckName (outcome.Output.TrimEnd '\n')
        else
            Harness.ValidationCheck.failed
                CatalogCheckName
                "generated region rendered from repo-config.yml"
                (sprintf "%s diverges from the registry" relative)
                (sprintf
                    "the generated region of %s was hand-edited or the registry changed; %s"
                    relative
                    Harness.catalogRemediation)

    Harness.ValidationResult.tally check Harness.ValidationResult.empty

/// The catalog document's repo-relative path, taken from the same
/// `harness-catalog:` block the renderer reads.
let private catalogRelativePath (repoRoot: string) : string =
    match RepoConfig.load repoRoot with
    | Ok config ->
        match config.HarnessCatalog with
        | Some settings -> settings.Document
        | None -> Harness.platformBindingsCatalog
    | Error _ -> Harness.platformBindingsCatalog

/// `harness catalog generate` [Repo-grounded — `harness_catalog.rs::run_generate`].
let private runHarnessCatalogGenerateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let outcome = Harness.runHarnessCatalogGenerate repoRoot
    let relative = catalogRelativePath repoRoot
    let result = catalogValidationResult outcome relative

    reportValidation format result rawArgs (fun _ -> outcome.Output.TrimEnd '\n')
    |> ignore

    0

/// `harness catalog validate` [Repo-grounded — `harness_catalog.rs::run_validate`].
let private runHarnessCatalogValidateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let outcome = Harness.runHarnessCatalogValidate repoRoot
    let relative = catalogRelativePath repoRoot
    let result = catalogValidationResult outcome relative

    reportValidation format result rawArgs (fun _ ->
        sprintf
            "catalog validation failed: %s diverges from the harness registry; %s"
            relative
            Harness.catalogRemediation)

/// `harness sync triage` [Repo-grounded — `harness_sync_triage.rs::run`].
let private runHarnessSyncTriageLeaf (repoRoot: string) (rawArgs: string list) : int =
    match Harness.triage repoRoot with
    | Error message ->
        eprintfn "Error: %s" message
        1
    | Ok report ->
        printfn
            "harness sync triage: %d generated file(s) compared, %d divergence(s)"
            report.Compared
            (List.length report.Divergences)

        if not (hasFlag [ "--quiet"; "-q" ] rawArgs) then
            for divergence in report.Divergences do
                printf "%s" (Harness.formatDivergence divergence)

        if List.isEmpty report.Divergences then
            0
        else
            eprintfn "Error: %s" (Harness.verdictSummary report)
            1

/// `harness sync promote` [Repo-grounded — `harness_sync_promote.rs::run`].
/// `--from` is required, and clap reports its absence before anything else.
let private runHarnessSyncPromoteLeaf (repoRoot: string) (rawArgs: string list) : int =
    match stringFlag [ "--from" ] rawArgs with
    | None ->
        let flagSegment =
            if hasFlag [ "--help"; "-h" ] rawArgs then
                " --help"
            elif
                rawArgs
                |> List.exists (fun a ->
                    a = "-o"
                    || a = "--output"
                    || a.StartsWith("--output=", StringComparison.Ordinal))
            then
                " --output <OUTPUT>"
            else
                ""

        eprintfn "error: the following required arguments were not provided:"
        eprintfn "  --from <MIRROR>"
        eprintfn ""
        eprintfn "Usage: rhino-cli harness sync promote --from <MIRROR>%s" flagSegment
        2
    | Some mirror ->
        match Harness.promote repoRoot mirror with
        | Error message ->
            eprintfn "Error: %s" message
            1
        | Ok proposal ->
            printf "%s" (Harness.formatProposal proposal)
            0

/// `harness bindings generate` [Repo-grounded —
/// `harness_generate_bindings.rs::run`]. Rejects an unknown `--harness`
/// against the registry rather than a hard-coded list.
let private runHarnessBindingsGenerateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let requested = stringFlag [ "--harness" ] rawArgs

    let nameError =
        match requested with
        | None -> None
        | Some name ->
            match RepoConfig.load repoRoot with
            | Error message -> Some(sprintf "failed to load repo-config.yml: %s" message)
            | Ok config ->
                match Harness.validateHarnessName config name with
                | Ok() -> None
                | Error message -> Some message

    match nameError with
    | Some message ->
        eprintfn "Error: %s" message
        1
    | None ->
        let stopwatch = Diagnostics.Stopwatch.StartNew()

        match Harness.runHarnessBindingsGenerateDetailed repoRoot with
        | Error message ->
            eprintfn "Error: %s" message
            1
        | Ok outcome ->
            stopwatch.Stop()

            if not (hasFlag [ "--quiet"; "-q" ] rawArgs) then
                let verbose = hasFlag [ "--verbose"; "-v" ] rawArgs

                match format with
                | Text -> printf "%s" (Formatters.syncText outcome.Agents stopwatch.Elapsed verbose false)
                | Json -> printfn "%s" (Formatters.syncJson outcome.Agents stopwatch.Elapsed)
                | Markdown -> printf "%s" (Formatters.syncMarkdown outcome.Agents stopwatch.Elapsed)

                printfn "codex: %d agent(s) emitted" outcome.Codex.Result.Converted

                printfn
                    "codex: %d skill file(s) mirrored, %d stale removed"
                    outcome.Mirror.Copied
                    outcome.Mirror.Removed

            if List.isEmpty outcome.Agents.FailedFiles then
                0
            else
                eprintfn
                    "Error: generation completed with %d failure(s): %s"
                    (List.length outcome.Agents.FailedFiles)
                    (String.concat ", " outcome.Agents.FailedFiles)

                1

/// `harness audit` [Repo-grounded — `harness_audit.rs::run`]. Each member is
/// named before it runs, because the per-validator reporters print only
/// failures at this verbosity.
let private runHarnessAuditLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
    let skip = collectRepeatableFlag [ "--skip" ] rawArgs

    let members =
        [ "detect-duplication"
          "validate-claude"
          "validate-sync"
          "validate-bindings"
          "validate-catalog"
          "validate-word-budget" ]

    let failures = ResizeArray<string>()

    for name in members do
        if not (List.contains name skip) then
            printfn "harness audit: %s" name

            let exitCode =
                match name with
                | "detect-duplication" -> runHarnessDuplicationLeaf repoRoot format
                | "validate-claude" -> runHarnessClaudeLeaf repoRoot format []
                | "validate-sync" -> runHarnessSyncValidateLeaf repoRoot format []
                | "validate-bindings" -> runHarnessBindingsValidateLeaf repoRoot format []
                | "validate-catalog" -> runHarnessCatalogValidateLeaf repoRoot format []
                | _ -> runGovernanceWordBudgetValidateLeaf repoRoot format []

            if exitCode <> 0 then
                failures.Add name

    if failures.Count = 0 then
        printfn "HARNESS AUDIT PASSED: all %d validators passed" (List.length members - List.length skip)
        0
    else
        eprintfn "HARNESS AUDIT FAILED: %d validator(s) reported failures" failures.Count
        eprintfn "Error: harness audit found %d failure(s)" failures.Count
        1

let private routeTable: (string list * string) list =
    [ [ "convention"; "emoji"; "validate" ], "emoji"
      [ "convention"; "license"; "validate" ], "license"
      [ "convention"; "audit" ], "audit"
      [ "parity"; "manifest"; "generate" ], "generate"
      [ "parity"; "manifest"; "validate" ], "validate"
      [ "repo-config"; "validate" ], "repo-config-validate"
      [ "env"; "init" ], "env-init"
      [ "env"; "backup" ], "env-backup"
      [ "env"; "restore" ], "env-restore"
      [ "env"; "validate" ], "env-validate"
      [ "env"; "staged-guard"; "validate" ], "env-staged-guard-validate"
      [ "doctor" ], "doctor"
      [ "test-coverage"; "validate" ], "test-coverage-validate"
      [ "md"; "links"; "validate" ], "md-links-validate"
      [ "md"; "mermaid"; "validate" ], "md-mermaid-validate"
      [ "md"; "heading-hierarchy"; "validate" ], "md-heading-hierarchy-validate"
      [ "md"; "naming"; "validate" ], "md-naming-validate"
      [ "md"; "frontmatter"; "validate" ], "md-frontmatter-validate"
      [ "md"; "frontmatter-dates"; "validate" ], "md-frontmatter-dates-validate"
      [ "md"; "audit" ], "md-audit"
      [ "governance"; "word-budget"; "validate" ], "governance-word-budget-validate"
      [ "governance"; "readme-index"; "validate" ], "governance-readme-index-validate"
      [ "governance"; "readme-index"; "generate" ], "governance-readme-index-generate"
      [ "governance"; "readme-index"; "rewrite-paths" ], "governance-readme-index-rewrite-paths"
      [ "git"; "lockfile"; "sync" ], "git-lockfile-sync"
      [ "repo-governance"; "vendor"; "validate" ], "repo-governance-vendor-validate"
      [ "repo-governance"; "layer-coherence"; "validate" ], "repo-governance-layer-coherence-validate"
      [ "repo-governance"; "traceability"; "validate" ], "repo-governance-traceability-validate"
      [ "repo-governance"; "audit" ], "repo-governance-audit"
      [ "specs"; "counts"; "validate" ], "specs-counts-validate"
      [ "specs"; "structure"; "validate" ], "specs-structure-validate"
      [ "specs"; "gherkin-cardinality"; "validate" ], "specs-gherkin-cardinality-validate"
      [ "specs"; "scaffold"; "dart" ], "specs-scaffold-dart"
      [ "specs"; "behavior-coverage"; "validate" ], "specs-behavior-coverage-validate"
      [ "specs"; "domain-coverage"; "validate" ], "specs-domain-coverage-validate"
      [ "harness"; "duplication"; "validate" ], "harness-duplication-validate"
      [ "harness"; "claude"; "validate" ], "harness-claude-validate"
      [ "harness"; "sync"; "validate" ], "harness-sync-validate"
      [ "harness"; "sync"; "triage" ], "harness-sync-triage"
      [ "harness"; "sync"; "promote" ], "harness-sync-promote"
      [ "harness"; "bindings"; "validate" ], "harness-bindings-validate"
      [ "harness"; "bindings"; "generate" ], "harness-bindings-generate"
      [ "harness"; "ownership"; "validate" ], "harness-ownership-validate"
      [ "harness"; "catalog"; "generate" ], "harness-catalog-generate"
      [ "harness"; "catalog"; "validate" ], "harness-catalog-validate"
      [ "harness"; "audit" ], "harness-audit"
      [ "specs"; "e2e-coverage"; "validate" ], "specs-e2e-coverage-validate"
      [ "specs"; "audit" ], "specs-audit"
      [ "gate"; "list" ], "gate-list"
      [ "gate"; "emit" ], "gate-emit"
      [ "gate"; "run" ], "gate-run" ]

/// Returns the first `routeTable` entry whose prefix `argvList` starts with,
/// paired with the arguments left after that prefix — the data-driven
/// equivalent of matching each command path as its own pattern arm.
let private matchRoute (argvList: string list) : (string * string list) option =
    let rec strip (prefix: string list) (args: string list) : string list option =
        match prefix, args with
        | [], rest -> Some rest
        | ph :: pt, ah :: at when ph = ah -> strip pt at
        | _ -> None

    routeTable
    |> List.tryPick (fun (prefix, name) -> strip prefix argvList |> Option.map (fun rest -> name, rest))

/// Routes `argv` to the leaf it names, resolving the repository root via
/// `getRepoRoot` — injected so tests can point at a fixture directory
/// instead of shelling out to the real `git` in this checkout.
let route (getRepoRoot: unit -> Result<string, string>) (argv: string[]) : int =
    let argvList = List.ofArray argv

    let path, rest =
        match matchRoute argvList with
        | Some(name, rest) -> Some name, rest
        | None -> None, []

    // `test-coverage validate`, the two coverage leaves, and `governance
    // readme-index rewrite-paths` have required arguments (positional /
    // `--map`), whose absence must win over `--help` — clap reports the
    // missing argument even for `--help`, so these are checked ahead of the
    // blanket `wantsHelp` shortcut every other leaf relies on.
    if path = Some "test-coverage-validate" then
        match getRepoRoot () with
        | Error message ->
            eprintfn "Error: failed to find git repository root: %s" message
            1
        | Ok repoRoot -> runTestCoverageValidateLeaf repoRoot rest
    elif path = Some "harness-sync-promote" then
        match getRepoRoot () with
        | Error message ->
            eprintfn "Error: failed to find git repository root: %s" message
            1
        | Ok repoRoot -> runHarnessSyncPromoteLeaf repoRoot rest
    elif path = Some "specs-e2e-coverage-validate" then
        match parseOutputFormat rest with
        | Error message ->
            eprintfn "Error: %s" message
            1
        | Ok format -> runSpecsE2eCoverageLeaf format rest
    elif path = Some "specs-behavior-coverage-validate" then
        match getRepoRoot () with
        | Error message ->
            eprintfn "Error: failed to find git repository root: %s" message
            1
        | Ok repoRoot ->
            match parseOutputFormat rest with
            | Error message ->
                eprintfn "Error: %s" message
                1
            | Ok format -> runSpecsBehaviorCoverageLeaf repoRoot format rest
    elif path = Some "specs-domain-coverage-validate" then
        match getRepoRoot () with
        | Error message ->
            eprintfn "Error: failed to find git repository root: %s" message
            1
        | Ok repoRoot ->
            match parseOutputFormat rest with
            | Error message ->
                eprintfn "Error: %s" message
                1
            | Ok format -> runSpecsDomainCoverageLeaf repoRoot format rest
    elif path = Some "governance-readme-index-rewrite-paths" then
        match getRepoRoot () with
        | Error message ->
            eprintfn "Error: failed to find git repository root: %s" message
            1
        | Ok repoRoot -> runGovernanceReadmeIndexRewritePathsLeaf repoRoot rest
    elif wantsHelp argv then
        printf "%s" HelpText.Text
        0
    else
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
                    | "doctor" -> runDoctorLeaf repoRoot format rest
                    | "md-links-validate" -> runMdLinksValidateLeaf repoRoot format rest
                    | "md-mermaid-validate" -> runMdMermaidValidateLeaf repoRoot format rest
                    | "md-heading-hierarchy-validate" -> runMdHeadingHierarchyValidateLeaf repoRoot format rest
                    | "md-naming-validate" -> runMdNamingValidateLeaf repoRoot format rest
                    | "md-frontmatter-validate" -> runMdFrontmatterValidateLeaf repoRoot format rest
                    | "md-frontmatter-dates-validate" -> runMdFrontmatterDatesValidateLeaf repoRoot format rest
                    | "md-audit" -> runMdAuditLeaf repoRoot format rest
                    | "governance-word-budget-validate" -> runGovernanceWordBudgetValidateLeaf repoRoot format rest
                    | "governance-readme-index-validate" -> runGovernanceReadmeIndexValidateLeaf repoRoot format rest
                    | "governance-readme-index-generate" -> runGovernanceReadmeIndexGenerateLeaf repoRoot format rest
                    | "git-lockfile-sync" -> runGitLockfileSyncLeaf repoRoot
                    | "gate-list" -> runGateListLeaf repoRoot rest
                    | "gate-emit" -> runGateEmitLeaf repoRoot rest
                    | "gate-run" -> runGateRunLeaf repoRoot rest
                    | "repo-governance-vendor-validate" -> runRepoGovernanceVendorValidateLeaf repoRoot format rest
                    | "repo-governance-layer-coherence-validate" ->
                        runRepoGovernanceLayerCoherenceValidateLeaf repoRoot format
                    | "repo-governance-traceability-validate" ->
                        runRepoGovernanceTraceabilityValidateLeaf repoRoot format
                    | "repo-governance-audit" -> runRepoGovernanceAuditLeaf repoRoot format rest
                    | "specs-counts-validate" -> runSpecsCountsValidateLeaf repoRoot rest
                    | "specs-structure-validate" -> runSpecsStructureValidateLeaf repoRoot rest
                    | "specs-gherkin-cardinality-validate" -> runSpecsCardinalityLeaf repoRoot format rest
                    | "specs-scaffold-dart" -> runSpecsScaffoldDartLeaf format rest
                    | "harness-duplication-validate" -> runHarnessDuplicationLeaf repoRoot format
                    | "harness-claude-validate" -> runHarnessClaudeLeaf repoRoot format rest
                    | "harness-sync-validate" -> runHarnessSyncValidateLeaf repoRoot format rest
                    | "harness-sync-triage" -> runHarnessSyncTriageLeaf repoRoot rest
                    | "harness-bindings-validate" -> runHarnessBindingsValidateLeaf repoRoot format rest
                    | "harness-bindings-generate" -> runHarnessBindingsGenerateLeaf repoRoot format rest
                    | "harness-ownership-validate" -> runHarnessOwnershipLeaf repoRoot format rest
                    | "harness-catalog-generate" -> runHarnessCatalogGenerateLeaf repoRoot format rest
                    | "harness-catalog-validate" -> runHarnessCatalogValidateLeaf repoRoot format rest
                    | "harness-audit" -> runHarnessAuditLeaf repoRoot format rest
                    | "specs-behavior-coverage-validate" -> runSpecsBehaviorCoverageLeaf repoRoot format rest
                    | "specs-domain-coverage-validate" -> runSpecsDomainCoverageLeaf repoRoot format rest
                    | "specs-audit" -> runSpecsAuditLeaf repoRoot format rest
                    | _ -> 2
