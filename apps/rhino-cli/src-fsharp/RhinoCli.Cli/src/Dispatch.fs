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
let private runMdLinksValidateLeaf (repoRoot: string) (format: OutputFormat) (rawArgs: string list) : int =
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

/// Routes `argv` to the leaf it names, resolving the repository root via
/// `getRepoRoot` — injected so tests can point at a fixture directory
/// instead of shelling out to the real `git` in this checkout.
let route (getRepoRoot: unit -> Result<string, string>) (argv: string[]) : int =
    let argvList = List.ofArray argv

    let path, rest =
        match argvList with
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
        | "doctor" :: rest -> Some "doctor", rest
        | "test-coverage" :: "validate" :: rest -> Some "test-coverage-validate", rest
        | "md" :: "links" :: "validate" :: rest -> Some "md-links-validate", rest
        | "md" :: "mermaid" :: "validate" :: rest -> Some "md-mermaid-validate", rest
        | "md" :: "heading-hierarchy" :: "validate" :: rest -> Some "md-heading-hierarchy-validate", rest
        | "md" :: "naming" :: "validate" :: rest -> Some "md-naming-validate", rest
        | "md" :: "frontmatter" :: "validate" :: rest -> Some "md-frontmatter-validate", rest
        | "md" :: "frontmatter-dates" :: "validate" :: rest -> Some "md-frontmatter-dates-validate", rest
        | "md" :: "audit" :: rest -> Some "md-audit", rest
        | "governance" :: "word-budget" :: "validate" :: rest -> Some "governance-word-budget-validate", rest
        | "governance" :: "readme-index" :: "validate" :: rest -> Some "governance-readme-index-validate", rest
        | "governance" :: "readme-index" :: "generate" :: rest -> Some "governance-readme-index-generate", rest
        | "governance" :: "readme-index" :: "rewrite-paths" :: rest ->
            Some "governance-readme-index-rewrite-paths", rest
        | "git" :: "lockfile" :: "sync" :: rest -> Some "git-lockfile-sync", rest
        | _ -> None, []

    // `test-coverage validate` and `governance readme-index rewrite-paths`
    // have required arguments (positional / `--map` respectively), whose
    // absence must win over `--help` (see `runTestCoverageValidateLeaf`'s and
    // `runGovernanceReadmeIndexRewritePathsLeaf`'s doc comments) — checked
    // ahead of the blanket `wantsHelp` shortcut every other leaf relies on.
    if path = Some "test-coverage-validate" then
        match getRepoRoot () with
        | Error message ->
            eprintfn "Error: failed to find git repository root: %s" message
            1
        | Ok repoRoot -> runTestCoverageValidateLeaf repoRoot rest
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
                    | _ -> 2
