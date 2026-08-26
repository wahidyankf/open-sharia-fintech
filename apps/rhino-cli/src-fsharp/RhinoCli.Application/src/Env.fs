/// Port of the slice of the Rust `env` namespace needed by
/// `env-backup.feature`'s 21 scenarios [Repo-grounded —
/// `apps/rhino-cli/src/application/env/backup.rs`,
/// `apps/rhino-cli/src/commands/env_backup.rs`].
///
/// Scope: this module ports `backup` and `env init`, plus the helpers each
/// (and their respective feature files' scenarios) needs. `restore` and
/// `env validate-app-drift` are separate later waves in this same namespace;
/// `discoverConfig`, `findExisting`, and `detectWorktree` are written here
/// because `backup` needs them, and are expected to be reused unchanged once
/// `restore` lands. `env init`'s own scan (`collectEnvExamples`) does not
/// share `backup`'s `discover`/`walkDir` machinery — it is deliberately
/// simpler: two fixed root directories, no skip-dirs list, and no file-size
/// ceiling.
///
/// Design decision — confirmation is real here, not a silent no-op: grepping
/// the Rust reference shows `Options.force` is threaded from the CLI args
/// into `Options` but never read inside `backup()`'s body, and `find_existing`
/// is only ever called from its own unit test — the Rust binary always
/// silently overwrites an existing backup file, regardless of `--force`. The
/// four `@env-backup-confirm` scenarios describe behaviour the current Rust
/// binary does not actually have, so `backup` below closes that gap rather
/// than reproducing it: it takes an explicit `confirm: unit -> bool`
/// callback and invokes it only when a real conflict exists in the
/// destination and `Force` is `false`. Whether to invoke the callback at all
/// is itself a pure function of `Options` and `findExisting`'s result — the
/// callback is the one deliberately impure seam — so tests can assert both
/// the decision made and that the callback fires exactly when (and only
/// when) a real decision is needed, without touching `Console.In`.
module RhinoCli.Application.Env

open System
open System.IO
open System.Text.Encodings.Web
open System.Text.Json
open System.Text.Json.Serialization

/// Maximum file size (in bytes) that will be backed up (1 MiB) [Repo-grounded
/// — `backup.rs::DEFAULT_MAX_SIZE`].
[<Literal>]
let DefaultMaxSize: int64 = 1024L * 1024L

/// Default name of the backup directory placed outside the repository
/// [Repo-grounded — `backup.rs::DEFAULT_BACKUP_DIR`]. This is ose-public's
/// own canonical value; ose-private's Rust constant differs and its F# port
/// must mirror whatever that repository's own constant currently is, not
/// this literal.
[<Literal>]
let DefaultBackupDir: string = "ose-public-env-backup"

/// Directory names the walker skips outright [Repo-grounded —
/// `backup.rs::default_skip_dirs`].
let defaultSkipDirs: string list =
    [ ".git"
      "node_modules"
      "bower_components"
      ".nx"
      ".next"
      ".turbo"
      ".cache"
      ".parcel-cache"
      ".nyc_output"
      "dist"
      "build"
      "coverage"
      "__pycache__"
      ".venv"
      "venv"
      "target"
      ".gradle"
      "vendor"
      "_build"
      "deps"
      ".elixir_ls"
      ".mix"
      ".dart_tool"
      ".cargo"
      "zig-cache"
      ".stack-work"
      "elm-stuff"
      "_deps"
      ".terraform"
      ".pulumi"
      "generated-contracts" ]

/// One well-known config file that `--include-config` may also back up
/// [Repo-grounded — `backup.rs::ConfigPattern`].
type ConfigPattern =
    { RelPath: string
      Description: string
      Category: string }

/// Default `--include-config` patterns [Repo-grounded —
/// `backup.rs::default_config_patterns`].
let defaultConfigPatterns: ConfigPattern list =
    [ { RelPath = ".claude/settings.local.json"
        Description = "Claude Code local settings"
        Category = "ai-tools" }
      { RelPath = ".claude/settings.local.json.bkup"
        Description = "Claude Code settings backup"
        Category = "ai-tools" }
      { RelPath = ".cursor/mcp.json"
        Description = "Cursor MCP configuration"
        Category = "ai-tools" }
      { RelPath = ".windsurfrules"
        Description = "Windsurf project rules"
        Category = "ai-tools" }
      { RelPath = ".clinerules"
        Description = "Cline project rules"
        Category = "ai-tools" }
      { RelPath = ".aider.conf.yml"
        Description = "Aider configuration"
        Category = "ai-tools" }
      { RelPath = ".aiderignore"
        Description = "Aider ignore patterns"
        Category = "ai-tools" }
      { RelPath = ".continue/config.json"
        Description = "Continue configuration"
        Category = "ai-tools" }
      { RelPath = ".gemini/settings.json"
        Description = "Gemini CLI settings"
        Category = "ai-tools" }
      { RelPath = ".amazonq/mcp.json"
        Description = "Amazon Q MCP configuration"
        Category = "ai-tools" }
      { RelPath = ".roomodes"
        Description = "Roo Code custom modes"
        Category = "ai-tools" }
      { RelPath = "docker-compose.override.yml"
        Description = "Docker Compose local overrides"
        Category = "docker" }
      { RelPath = "mise.local.toml"
        Description = "mise local overrides"
        Category = "version-mgrs" }
      { RelPath = ".envrc"
        Description = "direnv environment setup"
        Category = "environment" } ]

/// One file discovered during a scan, and its copy outcome [Repo-grounded —
/// `backup.rs::FileEntry`]. `Reason`/`Source` use `""` (rather than `option`)
/// as their unset sentinel, mirroring the Rust struct's `String` fields and
/// its `f.source.is_empty()`/`f.reason` emptiness checks in the reporters.
type EnvFileEntry =
    { RelPath: string
      AbsPath: string
      Size: int64
      Skipped: bool
      Reason: string
      Source: string }

/// Options for a [`backup`] operation [Repo-grounded — `backup.rs::Options`].
/// `Force` is threaded here (unlike the never-read Rust field it mirrors —
/// see the module doc comment) because `backup` below genuinely reads it.
type EnvOptions =
    { RepoRoot: string
      BackupDir: string
      SkipDirs: string list
      MaxSize: int64
      WorktreeAware: bool
      WorktreeName: string
      Force: bool
      IncludeConfig: bool
      DryRun: bool }

/// Outcome of a [`backup`] operation [Repo-grounded — `backup.rs::Result`].
/// Named `EnvOperationResult` rather than `Result` to avoid colliding with
/// `FSharp.Core.Result`.
type EnvOperationResult =
    { Direction: string
      Dir: string
      Files: EnvFileEntry list
      Copied: int
      Skipped: int
      Errors: string list
      WorktreeName: string
      Cancelled: bool
      DryRun: bool }

/// Expands a leading `~` in `path` to the value of the `HOME` environment
/// variable; returns `path` unchanged when it does not start with `~`
/// [Repo-grounded — `backup.rs::expand_tilde`].
///
/// # Errors
///
/// Returns an error when `path` starts with `~` but `HOME` is not set.
let expandTilde (path: string) : Result<string, string> =
    if not (path.StartsWith("~", StringComparison.Ordinal)) then
        Ok path
    else
        match Environment.GetEnvironmentVariable("HOME") with
        | null -> Error "HOME not set"
        | home ->
            let tail = path.Substring(1)

            if tail.StartsWith("/", StringComparison.Ordinal) then
                Ok(Path.Combine(home, tail.Substring(1)))
            elif tail = "" then
                Ok home
            else
                Ok(Path.Combine(home, tail))

/// Splits `path` into its non-empty components, tolerating either separator.
let private pathComponents (path: string) : string list =
    path.Split('/', '\\')
    |> Array.filter (fun segment -> segment <> "")
    |> List.ofArray

/// `true` when `backupDir` is `repoRoot` or a subdirectory of it, compared
/// component-wise on the raw (non-canonicalized) strings — mirroring Rust's
/// `Path::strip_prefix` [Repo-grounded — `backup.rs::is_inside_repo`].
let isInsideRepo (backupDir: string) (repoRoot: string) : bool =
    let backupParts = pathComponents backupDir
    let rootParts = pathComponents repoRoot

    rootParts.Length <= backupParts.Length
    && (backupParts |> List.take rootParts.Length) = rootParts

/// Canonicalizes `path`, falling back to the nearest existing ancestor when
/// `path` itself (or its trailing components) does not yet exist on disk
/// [Repo-grounded — `backup.rs::canonicalize_best_effort`].
///
/// A user-supplied `--dir` for `env backup` is frequently a directory that
/// has not been created yet, so a plain "canonicalize or fall back to the
/// raw path" approach would silently compare a non-canonical `backup_dir`
/// against a canonical `repo_root` in [`isInsideRepo`], defeating the safety
/// guard that check exists for (the same physical-vs-logical-path reasoning
/// `GitRoot.fs`'s module doc comment describes for macOS's `/private/var`).
/// This walks up to the nearest existing ancestor, resolves that ancestor's
/// full path, and rejoins the missing trailing components.
///
/// Scope note: unlike Rust's `fs::canonicalize`, this uses `Path.GetFullPath`
/// (lexical normalization), since the .NET base class library has no public
/// equivalent that also resolves symlinks — the same disclosed limitation as
/// `RepoConfig.fs::confinedRepoPath`. The two-step existing-ancestor fallback
/// control flow is otherwise identical.
///
/// # Errors
///
/// Returns an error when no ancestor of `path` exists, which should not
/// happen for any path derived from an absolute filesystem location.
let canonicalizeBestEffort (path: string) : Result<string, string> =
    if Directory.Exists path || File.Exists path then
        Ok(Path.GetFullPath path)
    else
        let rec walk (cursor: string) (tail: string list) : Result<string, string> =
            match Path.GetDirectoryName cursor with
            | null
            | "" -> Error(sprintf "no existing ancestor found while canonicalizing %s" path)
            | parent ->
                let name = Path.GetFileName cursor
                let tail = if name = "" then tail else name :: tail

                if Directory.Exists parent || File.Exists parent then
                    let canonicalParent = Path.GetFullPath parent

                    Ok(
                        tail
                        |> List.fold (fun acc segment -> Path.Combine(acc, segment)) canonicalParent
                    )
                else
                    walk parent tail

        walk path []

/// `true` for files that belong in a secret backup [Repo-grounded —
/// `backup.rs::is_secret_file`]: `.env`/`.env.*`, `secrets.json`, anything
/// under `.secrets/`, or a `.pem`/`.key`/`.crt`/`.pfx` file.
let isSecretFile (rel: string) (baseName: string) : bool =
    if
        baseName.StartsWith(".env", StringComparison.Ordinal)
        || baseName = "secrets.json"
        || rel.StartsWith(".secrets/", StringComparison.Ordinal)
    then
        true
    else
        let rawExt = Path.GetExtension baseName

        let ext =
            if rawExt.StartsWith(".", StringComparison.Ordinal) then
                rawExt.Substring(1)
            else
                rawExt

        match ext with
        | "pem"
        | "key"
        | "crt"
        | "pfx" -> true
        | _ -> false

/// `true` when a symlink is present at `path` [Repo-grounded —
/// `backup.rs::discover`'s `meta.file_type().is_symlink()` check].
let private isSymlink (path: string) : bool =
    match FileInfo(path).LinkTarget with
    | null -> false
    | _ -> true

/// Recursively walks `dir`, returning every secret-shaped file under it.
/// Hidden directories are skipped entirely except `.secrets/`, which is
/// descended; directories named in `skipDirs` are likewise skipped
/// [Repo-grounded — `backup.rs::discover`].
let rec private walkDir (repoRoot: string) (skipDirs: Set<string>) (maxSize: int64) (dir: string) : EnvFileEntry list =
    let fileEntries =
        Directory.EnumerateFiles dir
        |> Seq.choose (fun filePath ->
            let baseName = Path.GetFileName filePath
            let rel = Path.GetRelativePath(repoRoot, filePath).Replace('\\', '/')

            if not (isSecretFile rel baseName) then
                None
            elif isSymlink filePath then
                Some
                    { RelPath = rel
                      AbsPath = filePath
                      Size = 0L
                      Skipped = true
                      Reason = "symlink"
                      Source = "" }
            else
                let size = FileInfo(filePath).Length

                if size > maxSize then
                    Some
                        { RelPath = rel
                          AbsPath = filePath
                          Size = size
                          Skipped = true
                          Reason = "exceeds 1 MB"
                          Source = "" }
                else
                    Some
                        { RelPath = rel
                          AbsPath = filePath
                          Size = size
                          Skipped = false
                          Reason = ""
                          Source = "" })
        |> List.ofSeq

    let dirEntries =
        Directory.EnumerateDirectories dir
        |> Seq.collect (fun subDir ->
            let baseName = Path.GetFileName subDir

            if baseName.StartsWith(".", StringComparison.Ordinal) then
                let relDir = Path.GetRelativePath(repoRoot, subDir).Replace('\\', '/')

                if relDir = ".secrets" then
                    walkDir repoRoot skipDirs maxSize subDir
                else
                    []
            elif Set.contains baseName skipDirs then
                []
            else
                walkDir repoRoot skipDirs maxSize subDir)
        |> List.ofSeq

    fileEntries @ dirEntries

/// Walks `opts.RepoRoot` and returns every `.env*`/secret-shaped file found,
/// sorted by relative path [Repo-grounded — `backup.rs::discover`].
let discover (opts: EnvOptions) : EnvFileEntry list =
    let maxSize = if opts.MaxSize <= 0L then DefaultMaxSize else opts.MaxSize

    let skipDirs =
        if List.isEmpty opts.SkipDirs then
            Set.ofList defaultSkipDirs
        else
            Set.ofList opts.SkipDirs

    walkDir opts.RepoRoot skipDirs maxSize opts.RepoRoot
    |> List.sortWith (fun a b -> String.CompareOrdinal(a.RelPath, b.RelPath))

/// Checks each `ConfigPattern` relative to `repoRoot` and returns entries for
/// any that exist on disk, sorted by relative path [Repo-grounded —
/// `backup.rs::discover_config`].
let discoverConfig (repoRoot: string) (patterns: ConfigPattern list) (maxSize: int64) : EnvFileEntry list =
    let effectiveMax = if maxSize <= 0L then DefaultMaxSize else maxSize

    patterns
    |> List.choose (fun pattern ->
        let abs = Path.Combine(repoRoot, pattern.RelPath)

        if Directory.Exists abs || not (File.Exists abs) then
            None
        elif isSymlink abs then
            Some
                { RelPath = pattern.RelPath
                  AbsPath = abs
                  Size = 0L
                  Skipped = true
                  Reason = "symlink"
                  Source = "config" }
        else
            let size = FileInfo(abs).Length

            if size > effectiveMax then
                Some
                    { RelPath = pattern.RelPath
                      AbsPath = abs
                      Size = size
                      Skipped = true
                      Reason = sprintf "file too large (%d bytes > %d)" size effectiveMax
                      Source = "config" }
            else
                Some
                    { RelPath = pattern.RelPath
                      AbsPath = abs
                      Size = size
                      Skipped = false
                      Reason = ""
                      Source = "config" })
    |> List.sortWith (fun a b -> String.CompareOrdinal(a.RelPath, b.RelPath))

/// Returns the relative paths of the non-skipped `entries` that already
/// exist under `destRoot` [Repo-grounded — `backup.rs::find_existing`].
let findExisting (entries: EnvFileEntry list) (destRoot: string) : string list =
    entries
    |> List.filter (fun e -> not e.Skipped)
    |> List.choose (fun e ->
        let dst = Path.Combine(destRoot, e.RelPath)

        if File.Exists dst || Directory.Exists dst then
            Some e.RelPath
        else
            None)

/// Whether a repository root is a linked Git worktree [Repo-grounded —
/// `backup.rs::WorktreeInfo`].
type WorktreeInfo =
    { IsWorktree: bool
      WorktreeName: string }

/// Detects whether `repoRoot` is a linked Git worktree by inspecting its
/// `.git` entry: a regular checkout has `.git` as a directory, a linked
/// worktree has `.git` as a file starting with `"gitdir:"` [Repo-grounded —
/// `backup.rs::detect_worktree`].
///
/// # Errors
///
/// Returns an error when `.git` does not exist at `repoRoot`, or when it
/// exists as a file that does not start with `"gitdir:"`.
let detectWorktree (repoRoot: string) : Result<WorktreeInfo, string> =
    let gitPath = Path.Combine(repoRoot, ".git")
    let name = Path.GetFileName(repoRoot.TrimEnd('/', '\\'))

    if Directory.Exists gitPath then
        Ok
            { IsWorktree = false
              WorktreeName = name }
    elif File.Exists gitPath then
        let line = (File.ReadAllText gitPath).Trim()

        if line.StartsWith("gitdir:", StringComparison.Ordinal) then
            Ok
                { IsWorktree = true
                  WorktreeName = name }
        else
            Error(sprintf ".git file does not start with 'gitdir:' (got: %s)" line)
    else
        Error(sprintf "no .git found at %s" repoRoot)

/// Running total kept while copying `backup`'s discovered entries.
type private CopyAcc =
    { Copied: int
      Skipped: int
      Errors: string list }

/// Copies one entry into `destRoot`, folding its outcome into `acc`
/// [Repo-grounded — `backup.rs::backup`'s per-entry copy loop].
let private copyOne (destRoot: string) (acc: CopyAcc) (e: EnvFileEntry) : CopyAcc =
    if e.Skipped then
        { acc with Skipped = acc.Skipped + 1 }
    else
        let dst = Path.Combine(destRoot, e.RelPath)

        try
            match Path.GetDirectoryName dst with
            | null
            | "" -> ()
            | parent -> Directory.CreateDirectory parent |> ignore

            File.Copy(e.AbsPath, dst, true)
            { acc with Copied = acc.Copied + 1 }
        with ex ->
            { acc with
                Skipped = acc.Skipped + 1
                Errors = acc.Errors @ [ sprintf "copy %s: %s" e.RelPath ex.Message ] }

/// Copies `.env*` files (and optionally config files) from
/// `opts.RepoRoot` to `opts.BackupDir` [Repo-grounded — `backup.rs::backup`].
///
/// `confirm` is invoked at most once, and only when the destination already
/// contains at least one of the non-skipped discovered files and
/// `opts.Force` is `false` — see the module doc comment for why this is a
/// real decision here rather than the dead `force` field it is ported from.
///
/// # Errors
///
/// Returns an error when `opts.BackupDir` (after tilde expansion) is inside
/// `opts.RepoRoot`.
let backup (opts: EnvOptions) (confirm: unit -> bool) : Result<EnvOperationResult, string> =
    match expandTilde opts.BackupDir with
    | Error message -> Error message
    | Ok expandedBackupDir ->
        if isInsideRepo expandedBackupDir opts.RepoRoot then
            Error(
                sprintf
                    "backup dir %s is inside repo root %s; choose a directory outside the repo"
                    expandedBackupDir
                    opts.RepoRoot
            )
        else
            let maxSize = if opts.MaxSize <= 0L then DefaultMaxSize else opts.MaxSize

            let discoverOpts =
                { opts with
                    BackupDir = expandedBackupDir
                    MaxSize = maxSize }

            let envEntries = discover discoverOpts

            let entries =
                if opts.IncludeConfig then
                    let tagged =
                        envEntries
                        |> List.map (fun e -> if e.Source = "" then { e with Source = "env" } else e)

                    let configEntries = discoverConfig opts.RepoRoot defaultConfigPatterns maxSize

                    tagged @ configEntries
                    |> List.sortWith (fun a b -> String.CompareOrdinal(a.RelPath, b.RelPath))
                else
                    envEntries

            let destRoot =
                if opts.WorktreeAware && opts.WorktreeName <> "" then
                    Path.Combine(expandedBackupDir, opts.WorktreeName)
                else
                    expandedBackupDir

            if opts.DryRun then
                Ok
                    { Direction = "backup"
                      Dir = expandedBackupDir
                      Files = entries
                      Copied = 0
                      Skipped = 0
                      Errors = []
                      WorktreeName = opts.WorktreeName
                      Cancelled = false
                      DryRun = true }
            else
                let existing = findExisting entries destRoot
                let proceed = opts.Force || List.isEmpty existing || confirm ()

                if not proceed then
                    Ok
                        { Direction = "backup"
                          Dir = expandedBackupDir
                          Files = entries
                          Copied = 0
                          Skipped = 0
                          Errors = []
                          WorktreeName = opts.WorktreeName
                          Cancelled = true
                          DryRun = false }
                else
                    Directory.CreateDirectory destRoot |> ignore

                    let finalAcc =
                        entries |> List.fold (copyOne destRoot) { Copied = 0; Skipped = 0; Errors = [] }

                    Ok
                        { Direction = "backup"
                          Dir = expandedBackupDir
                          Files = entries
                          Copied = finalAcc.Copied
                          Skipped = finalAcc.Skipped
                          Errors = finalAcc.Errors
                          WorktreeName = opts.WorktreeName
                          Cancelled = false
                          DryRun = false }

// ---- Reporters ----

/// Capitalises the first character of `s`, leaving the rest unchanged
/// [Repo-grounded — `backup.rs::capitalize`].
let capitalize (s: string) : string =
    if s = "" then
        ""
    else
        (Char.ToUpperInvariant s.[0]).ToString() + s.Substring(1)

/// Formats an [`EnvOperationResult`] as human-readable text [Repo-grounded —
/// `backup.rs::format_text`]. When `quiet` is `true`, per-file lines are
/// suppressed; when `verbose` is `true`, skipped files are also listed.
let formatText (r: EnvOperationResult) (verbose: bool) (quiet: bool) : string =
    if r.Cancelled then
        let label = if r.Direction = "" then "operation" else r.Direction
        sprintf "%s cancelled.\n" (capitalize label)
    else
        let sb = Text.StringBuilder()

        if not quiet then
            let action = if r.DryRun then "WOULD" else r.Direction.ToUpperInvariant()

            for f in r.Files do
                if f.Skipped then
                    if verbose then
                        sb.Append(sprintf "  SKIPPED  %s  (%s)\n" f.RelPath f.Reason) |> ignore
                else
                    let tag = if f.Source = "config" then " [config]" else ""
                    sb.Append(sprintf "  %s  %s%s\n" action f.RelPath tag) |> ignore

            for e in r.Errors do
                sb.Append(sprintf "  WARNING  %s\n" e) |> ignore

        let label = if r.Direction = "" then "processed" else r.Direction

        if r.DryRun then
            let wouldCount = r.Files |> List.filter (fun f -> not f.Skipped) |> List.length

            sb.Append(sprintf "Dry-run %s: %d file(s) would be %sd, %d skipped" label wouldCount label r.Skipped)
            |> ignore
        else
            sb.Append(sprintf "%s complete: %d file(s) %sd, %d skipped" (capitalize label) r.Copied label r.Skipped)
            |> ignore

        let configCount =
            r.Files
            |> List.filter (fun f -> f.Source = "config" && not f.Skipped)
            |> List.length

        if configCount > 0 then
            sb.Append(sprintf " (%d config)" configCount) |> ignore

        if r.WorktreeName <> "" then
            sb.Append(sprintf "  [worktree: %s]" r.WorktreeName) |> ignore

        sb.Append('\n') |> ignore
        sb.ToString()

/// JSON shape of one file entry [Repo-grounded — `backup.rs::JsonEntry`].
/// Scope note: unlike Rust's `#[serde(skip_serializing_if = ...)]`, every
/// field is always emitted here (no omission of zero/empty values) — this
/// port's `formatJson` only needs to satisfy "the JSON includes ..."
/// (env-backup.feature), not byte-identical CLI JSON output; that
/// byte-identical requirement belongs to the later CLI-wiring wave.
///
/// Not `private`: `System.Text.Json`'s default reflection-based resolver
/// silently reflects into zero members of a non-visible (`private`) type —
/// it neither throws nor logs, it just serializes `{}` — the same pitfall
/// `RepoConfig.fs`'s module doc comment warns about for a `private` YamlDotNet
/// DTO, reproduced here for `System.Text.Json` instead. This type is still
/// excluded from this module's public surface indirectly: nothing outside
/// `formatJson` ever constructs or returns one.
type JsonFileEntry =
    { relPath: string
      size: int64
      skipped: bool
      reason: string
      source: string }

/// JSON shape of the top-level envelope [Repo-grounded —
/// `backup.rs::JsonOut`]. See `JsonFileEntry`'s scope note for why this is
/// not `private`.
type JsonEnvelope =
    { direction: string
      dir: string
      files: JsonFileEntry list
      copied: int
      skipped: int
      errors: string list
      worktreeName: string
      cancelled: bool }

let private jsonOptions: JsonSerializerOptions =
    let opts = JsonSerializerOptions()
    opts.WriteIndented <- true
    opts.Encoder <- JavaScriptEncoder.UnsafeRelaxedJsonEscaping
    opts

/// Serialises an [`EnvOperationResult`] to a pretty-printed JSON string
/// [Repo-grounded — `backup.rs::format_json`].
let formatJson (r: EnvOperationResult) : string =
    let toJsonEntry (f: EnvFileEntry) : JsonFileEntry =
        { relPath = f.RelPath
          size = f.Size
          skipped = f.Skipped
          reason = f.Reason
          source = f.Source }

    let env: JsonEnvelope =
        { direction = r.Direction
          dir = r.Dir
          files = r.Files |> List.map toJsonEntry
          copied = r.Copied
          skipped = r.Skipped
          errors = r.Errors
          worktreeName = r.WorktreeName
          cancelled = r.Cancelled }

    JsonSerializer.Serialize(env, jsonOptions)

/// Formats an [`EnvOperationResult`] as a Markdown report [Repo-grounded —
/// `backup.rs::format_markdown`].
let formatMarkdown (r: EnvOperationResult) : string =
    let sb = Text.StringBuilder()
    let action = capitalize r.Direction
    sb.Append(sprintf "## %s Report\n\n" action) |> ignore
    sb.Append(sprintf "**Directory**: `%s`\n\n" r.Dir) |> ignore

    sb.Append(sprintf "**Copied**: %d | **Skipped**: %d\n\n" r.Copied r.Skipped)
    |> ignore

    if r.WorktreeName <> "" then
        sb.Append(sprintf "**Worktree**: `%s`\n\n" r.WorktreeName) |> ignore

    if r.Cancelled then
        let label = if r.Direction = "" then "operation" else r.Direction
        sb.Append(sprintf "_%s cancelled._\n" (capitalize label)) |> ignore
        sb.ToString()
    elif List.isEmpty r.Files then
        sb.Append("_No .env files found._\n") |> ignore
        sb.ToString()
    else
        let hasConfig = r.Files |> List.exists (fun f -> f.Source = "config")

        if hasConfig then
            sb.Append("| File | Size (bytes) | Source | Status | Reason |\n") |> ignore
            sb.Append("|------|-------------|--------|--------|--------|\n") |> ignore
        else
            sb.Append("| File | Size (bytes) | Status | Reason |\n") |> ignore
            sb.Append("|------|-------------|--------|--------|\n") |> ignore

        for f in r.Files do
            let status = if f.Skipped then "skipped" else "copied"
            let reason = if f.Skipped then f.Reason else ""
            let display = f.RelPath.Replace('\\', '/')

            if hasConfig then
                let source = if f.Source = "" then "env" else f.Source

                sb.Append(sprintf "| `%s` | %d | %s | %s | %s |\n" display f.Size source status reason)
                |> ignore
            else
                sb.Append(sprintf "| `%s` | %d | %s | %s |\n" display f.Size status reason)
                |> ignore

        if not (List.isEmpty r.Errors) then
            sb.Append("\n### Warnings\n") |> ignore

            for e in r.Errors do
                sb.Append(sprintf "- %s\n" e) |> ignore

        sb.ToString()

// ---- env init ----

/// Directories under a repo root that `env init` scans for `.env.example`
/// files [Repo-grounded — `env_init.rs::SCAN_ROOTS`]. Deliberately not
/// `backup`'s `discover`/`walkDir`: this scan is two fixed roots, with no
/// skip-dirs list and no file-size ceiling — see the module doc comment.
let envInitScanRoots: string list = [ "infra/dev"; "apps" ]

/// The tier `env init` bootstraps: local development, never committed
/// [Repo-grounded — `env_init.rs::ENV_TIER_DEFAULT`].
[<Literal>]
let EnvInitTargetTier: string = ".env.local"

/// Recursively finds every `.env.example` file under `dir`.
let rec private walkForExamples (dir: string) : string list =
    let here =
        Directory.EnumerateFiles dir
        |> Seq.filter (fun f -> Path.GetFileName f = ".env.example")
        |> List.ofSeq

    let nested =
        Directory.EnumerateDirectories dir |> Seq.collect walkForExamples |> List.ofSeq

    here @ nested

/// Collects every `.env.example` file found under `envInitScanRoots` inside
/// `repoRoot` [Repo-grounded — `env_init.rs::collect_examples`].
let collectEnvExamples (repoRoot: string) : string list =
    envInitScanRoots
    |> List.collect (fun root ->
        let scanDir = Path.Combine(repoRoot, root)

        if Directory.Exists scanDir then
            walkForExamples scanDir
        else
            [])

/// Computes the `.env.local` path that sits alongside `examplePath`, in the
/// same directory [Repo-grounded — `env_init.rs::target_env_path`]. Unlike
/// the Rust original this returns a plain `string` rather than an `Option`:
/// every `examplePath` this module passes in comes from `collectEnvExamples`
/// walking real files on disk, so it always has a parent directory.
let targetEnvPath (examplePath: string) : string =
    Path.Combine(Path.GetDirectoryName examplePath, EnvInitTargetTier)

/// One discovered `.env.example` file's copy outcome [Repo-grounded —
/// `env_init.rs::run`'s per-file `println!` branches].
type EnvInitFileOutcome =
    | EnvInitCreated of relPath: string * exampleFileName: string
    | EnvInitSkipped of relPath: string

/// Outcome of an `env init` operation [Repo-grounded — `env_init.rs::run`].
type EnvInitResult =
    { Files: EnvInitFileOutcome list
      Created: int
      Skipped: int }

/// Copies every `.env.example` file found under `repoRoot` to its sibling
/// `.env.local`, skipping files that already exist unless `force` is `true`
/// [Repo-grounded — `env_init.rs::run`]. Unlike `backup`, this has no
/// `Result` wrapper: `env_init.rs::run`'s only failure mode is git-root
/// discovery, which this port's callers (mirroring `backup`'s `EnvOptions`)
/// handle by passing `repoRoot` in directly rather than looking it up here.
let runEnvInit (repoRoot: string) (force: bool) : EnvInitResult =
    let outcomes =
        collectEnvExamples repoRoot
        |> List.map (fun examplePath ->
            let envPath = targetEnvPath examplePath
            let rel = Path.GetRelativePath(repoRoot, envPath).Replace('\\', '/')

            if not force && (File.Exists envPath || Directory.Exists envPath) then
                EnvInitSkipped rel
            else
                File.Copy(examplePath, envPath, true)
                EnvInitCreated(rel, Path.GetFileName examplePath))

    let created =
        outcomes
        |> List.filter (function
            | EnvInitCreated _ -> true
            | EnvInitSkipped _ -> false)
        |> List.length

    let skipped = List.length outcomes - created

    { Files = outcomes
      Created = created
      Skipped = skipped }

/// Formats an [`EnvInitResult`] as human-readable text [Repo-grounded —
/// `env_init.rs::run`'s `println!` calls]. `env init` has no JSON/Markdown
/// Gherkin scenario, so unlike `backup`'s `formatText`/`formatJson`/
/// `formatMarkdown` trio this is the only formatter it needs.
let formatEnvInitText (r: EnvInitResult) : string =
    let sb = Text.StringBuilder()

    for f in r.Files do
        match f with
        | EnvInitCreated(rel, exampleFileName) ->
            sb.Append(sprintf "Created: %s (from %s)\n" rel exampleFileName) |> ignore
        | EnvInitSkipped rel ->
            sb.Append(sprintf "Skipped: %s (already exists, use --force to overwrite)\n" rel)
            |> ignore

    sb.Append(sprintf "\nSummary: %d created, %d skipped\n" r.Created r.Skipped)
    |> ignore

    sb.ToString()
