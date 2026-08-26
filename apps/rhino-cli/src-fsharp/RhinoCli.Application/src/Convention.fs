/// Port of the Rust `convention` namespace's two file-system validators
/// (emoji, license) and their aggregate runner
/// [Repo-grounded —
/// `apps/rhino-cli/src/application/repo_governance/emoji_audit.rs`,
/// `apps/rhino-cli/src/application/repo_governance/license_audit.rs`,
/// `apps/rhino-cli/src/commands/convention_audit.rs`]. Wave A's first
/// namespace: findings from both validators are represented with the shared
/// `RhinoCli.Domain.Types.Finding` record rather than bespoke per-validator
/// types, since `Severity` / `Message` / `Path` already cover everything
/// either validator needs to report.
module RhinoCli.Application.Convention

open System
open System.IO
open RhinoCli.Domain.Types

// Grants RhinoCli.Tests.Unit direct access to `internal` members below, so
// `runAuditMember`'s unreachable-via-`runConventionAudit` branch can be unit
// tested the same way Rust tests the equivalent `run_member` directly
// [Repo-grounded — `convention_audit.rs::tests::run_member_unknown_returns_error`].
[<assembly: System.Runtime.CompilerServices.InternalsVisibleTo("RhinoCli.UnitTests")>]
do ()

/// The outcome of running one convention validator: whether it passed, the
/// human-readable text a CLI invocation would print, and the structured
/// findings behind that text.
type ValidatorResult =
    { Success: bool
      Output: string
      Findings: Finding list }

/// Emoji-codepoint scanning over forbidden file types
/// [Repo-grounded — `emoji_audit.rs`].
module private Emoji =

    /// File extensions for which emoji are forbidden.
    let forbiddenExtensions: string list =
        [ ".json"
          ".yaml"
          ".yml"
          ".toml"
          ".go"
          ".ts"
          ".tsx"
          ".js"
          ".jsx"
          ".py"
          ".java"
          ".kt"
          ".rs"
          ".fs"
          ".cs"
          ".dart"
          ".exs"
          ".ex"
          ".clj" ]

    /// Returns `true` when `name` ends with one of `forbiddenExtensions`
    /// (case-insensitive).
    let hasForbiddenExtension (name: string) : bool =
        let lower = name.ToLowerInvariant()

        forbiddenExtensions
        |> List.exists (fun ext -> lower.EndsWith(ext, StringComparison.Ordinal))

    /// Directory names to skip during the walk.
    let skipDirs: Set<string> =
        set
            [ "node_modules"
              ".agents"
              ".git"
              ".next"
              "dist"
              "build"
              "target"
              "generated"
              "generated-contracts"
              "generated-sources"
              "generated-test-sources"
              "generated-reports"
              "archived"
              "test-results"
              "playwright-report"
              "coverage"
              ".venv"
              "__pycache__"
              ".pytest_cache"
              ".dart_tool"
              "out"
              ".cache"
              "storybook-static"
              ".playwright-mcp"
              "raw" ]

    /// Recursively walks `path` and returns every file found, skipping
    /// directories named in `skipDirs`. A `path` that is itself a file is
    /// returned as a single-element list, mirroring `WalkDir::new(root)`
    /// accepting a file root.
    let rec walk (path: string) : string list =
        if File.Exists path then
            [ path ]
        elif Directory.Exists path then
            Directory.GetFileSystemEntries path
            |> Array.toList
            |> List.collect (fun entry ->
                if Directory.Exists entry then
                    let name = Path.GetFileName entry
                    if skipDirs.Contains name then [] else walk entry
                else
                    [ entry ])
        else
            []

    /// Returns `true` when `codepoint` falls within one of the emoji
    /// Unicode blocks checked by this audit
    /// [Repo-grounded — `emoji_audit.rs::is_emoji_rune`].
    let isEmojiCodepoint (codepoint: int) : bool =
        (codepoint >= 0x2300 && codepoint <= 0x23FF)
        || (codepoint >= 0x2600 && codepoint <= 0x27BF)
        || codepoint = 0x200D
        || codepoint = 0xFE0F
        || (codepoint >= 0x1F000 && codepoint <= 0x1FFFF)

    /// Formats `codepoint` as a Unicode codepoint string (e.g. `U+1F680`).
    let formatCodepoint (codepoint: int) : string =
        if codepoint <= 0xFFFF then
            sprintf "U+%04X" codepoint
        else
            sprintf "U+%X" codepoint

    /// Splits `line` into Unicode scalar values (matching Rust's
    /// `str::chars`), combining UTF-16 surrogate pairs into a single
    /// codepoint so multi-byte emoji beyond the BMP are counted once.
    let codepointsOf (line: string) : int list =
        let rec loop (i: int) (acc: int list) : int list =
            if i >= line.Length then
                List.rev acc
            elif
                i + 1 < line.Length
                && Char.IsHighSurrogate(line.[i])
                && Char.IsLowSurrogate(line.[i + 1])
            then
                loop (i + 2) (Char.ConvertToUtf32(line.[i], line.[i + 1]) :: acc)
            else
                loop (i + 1) (int line.[i] :: acc)

        loop 0 []

    /// Scans a single file for emoji codepoints line by line, returning raw
    /// `(file, line, column, codepoint)` tuples so callers can sort before
    /// rendering into `Finding`s.
    let scanFileRaw (path: string) : (string * int * int * string) list =
        File.ReadAllLines(path)
        |> Array.toList
        |> List.mapi (fun lineIdx line -> (lineIdx + 1, line))
        |> List.collect (fun (lineNumber, line) ->
            codepointsOf line
            |> List.mapi (fun colIdx codepoint -> (colIdx + 1, codepoint))
            |> List.filter (fun (_, codepoint) -> isEmojiCodepoint codepoint)
            |> List.map (fun (column, codepoint) -> (path, lineNumber, column, formatCodepoint codepoint)))

    /// Walks each root in `paths` and reports any emoji codepoints found in
    /// files with a forbidden extension. Findings are sorted by file, then
    /// line, then column.
    let audit (paths: string list) : Result<Finding list, string> =
        if List.isEmpty paths then
            Error "at least one path is required"
        else
            paths
            |> List.collect walk
            |> List.filter (fun p -> hasForbiddenExtension (Path.GetFileName p))
            |> List.sort
            |> List.collect scanFileRaw
            |> List.sortBy (fun (file, line, column, _) -> (file, line, column))
            |> List.map (fun (file, line, column, codepoint) ->
                { Severity = Severity.Blocking
                  Message = sprintf "%s:%d:%d  [high]  %s" file line column codepoint
                  Path = Some file })
            |> Ok

    /// Renders emoji findings as human-readable text.
    let formatText (findings: Finding list) : string =
        if List.isEmpty findings then
            "EMOJI AUDIT PASSED: no emoji codepoints found in forbidden file types\n"
        else
            let header =
                sprintf "EMOJI AUDIT FAILED: %d emoji codepoint(s) found\n" (List.length findings)

            let body =
                findings |> List.map (fun f -> sprintf "  %s\n" f.Message) |> String.concat ""

            header + body

/// Per-directory `LICENSE` presence and SPDX-consistency audit
/// [Repo-grounded — `license_audit.rs`].
module private License =

    /// App directories that are intentionally exempt from the LICENSE
    /// requirement.
    let exemptApps: Set<string> = set [ "rhino-cli" ]

    /// A single row parsed from the `LICENSING-NOTICE.md` table.
    type private Claim =
        { ClaimPath: string
          ClaimLicense: string }

    /// Returns the sorted names of non-hidden subdirectories inside `dir`.
    /// Returns an empty list when `dir` does not exist.
    let readNonHiddenDirs (dir: string) : string list =
        if not (Directory.Exists dir) then
            []
        else
            Directory.GetDirectories dir
            |> Array.map Path.GetFileName
            |> Array.filter (fun name -> not (name.StartsWith(".", StringComparison.Ordinal)))
            |> Array.sort
            |> Array.toList

    /// Returns a sorted list of relative directory paths that must contain a
    /// `LICENSE` file: non-exempt, non-`-e2e` subdirectories of `apps/`, all
    /// subdirectories of `libs/`, and `specs/` when it exists.
    let requiredDirs (repoRoot: string) : string list =
        let apps =
            readNonHiddenDirs (Path.Combine(repoRoot, "apps"))
            |> List.filter (fun name ->
                not (exemptApps.Contains name)
                && not (name.EndsWith("-e2e", StringComparison.Ordinal)))
            |> List.map (fun name -> sprintf "apps/%s" name)

        let libs =
            readNonHiddenDirs (Path.Combine(repoRoot, "libs"))
            |> List.map (fun name -> sprintf "libs/%s" name)

        let specs =
            if Directory.Exists(Path.Combine(repoRoot, "specs")) then
                [ "specs" ]
            else
                []

        apps @ libs @ specs |> List.sort

    /// The result of reading a directory's `LICENSE` file for its SPDX
    /// identifier.
    type private SpdxOutcome =
        | Found of string
        | Missing
        | Unreadable of string

    /// Maps the first line of a `LICENSE` file to a canonical SPDX
    /// identifier, recognising `SPDX-License-Identifier:` headers and common
    /// prose patterns. Returns `line` unchanged when no pattern matches.
    let classifyLine (line: string) : string =
        let spdxPrefix = "SPDX-License-Identifier:"

        if
            line.Length >= spdxPrefix.Length
            && line.Substring(0, spdxPrefix.Length).Equals(spdxPrefix, StringComparison.OrdinalIgnoreCase)
        then
            line.Substring(spdxPrefix.Length).Trim()
        else
            let lower = line.ToLowerInvariant()

            if lower.Contains("mit license") || lower = "mit" then
                "MIT"
            elif
                lower.Contains("apache license, version 2.0")
                || lower.Contains("apache license 2.0")
                || lower.Contains("apache-2.0")
            then
                "Apache-2.0"
            elif lower.Contains("bsd 3-clause") || lower.Contains("bsd-3-clause") then
                "BSD-3-Clause"
            elif lower.Contains("bsd 2-clause") || lower.Contains("bsd-2-clause") then
                "BSD-2-Clause"
            elif lower.Contains("mozilla public license") || lower.Contains("mpl-2.0") then
                "MPL-2.0"
            elif lower.Contains("gnu general public license") then
                "GPL"
            else
                line

    /// Reads the first non-blank line of the `LICENSE` file at `path` and
    /// classifies it as an SPDX identifier.
    let private extractSpdx (path: string) : SpdxOutcome =
        if not (File.Exists path) then
            Missing
        else
            let firstNonBlank =
                File.ReadAllLines(path) |> Array.tryFind (fun l -> l.Trim() <> "")

            match firstNonBlank with
            | Some line -> Found(classifyLine (line.Trim()))
            | None -> Unreadable(sprintf "LICENSE file \"%s\" is empty" path)

    /// Returns `true` when `identified` and `claim` refer to the same SPDX
    /// license, either by direct case-insensitive comparison or after
    /// normalising both through `classifyLine`.
    let licensesEqual (identified: string) (claim: string) : bool =
        String.Equals(identified, claim, StringComparison.OrdinalIgnoreCase)
        || String.Equals(classifyLine identified, classifyLine claim, StringComparison.OrdinalIgnoreCase)

    /// Normalises a raw path value from `LICENSING-NOTICE.md` by stripping
    /// surrounding whitespace, backticks, leading `./`, trailing `/`, and
    /// converting backslashes to forward slashes.
    let normaliseClaimPath (raw: string) : string =
        let trimmed = raw.Trim().Trim('`').Trim()

        let withoutPrefix =
            if trimmed.StartsWith("./", StringComparison.Ordinal) then
                trimmed.Substring(2)
            else
                trimmed

        let withoutSuffix =
            if withoutPrefix.EndsWith("/", StringComparison.Ordinal) then
                withoutPrefix.Substring(0, withoutPrefix.Length - 1)
            else
                withoutPrefix

        withoutSuffix.Replace('\\', '/')

    /// Returns `true` when `path` falls within the scope of this audit
    /// (immediate children of `apps/` or `libs/`, or the `specs` root).
    let ownedByLicenseAudit (path: string) : bool =
        if path = "specs" then
            true
        elif
            path.StartsWith("apps/", StringComparison.Ordinal)
            || path.StartsWith("libs/", StringComparison.Ordinal)
        then
            let rest = path.Substring(5)
            not (String.IsNullOrEmpty rest) && not (rest.Contains("/"))
        else
            false

    /// Splits a GFM table row `line` into individual cell strings,
    /// respecting backslash-escaped pipe characters.
    let splitMarkdownRow (line: string) : string list =
        let trimmed = line.Trim()

        let trimmed =
            if trimmed.StartsWith("|", StringComparison.Ordinal) then
                trimmed.Substring(1)
            else
                trimmed

        let trimmed =
            if trimmed.EndsWith("|", StringComparison.Ordinal) then
                trimmed.Substring(0, trimmed.Length - 1)
            else
                trimmed

        let rec loop (chars: char list) (current: char list) (escaped: bool) (cells: string list) : string list =
            match chars with
            | [] -> List.rev (String(current |> List.rev |> Array.ofList) :: cells)
            | c :: rest when escaped -> loop rest (c :: current) false cells
            | '\\' :: rest -> loop rest current true cells
            | '|' :: rest -> loop rest [] false (String(current |> List.rev |> Array.ofList) :: cells)
            | c :: rest -> loop rest (c :: current) false cells

        loop (trimmed |> List.ofSeq) [] false []

    /// Returns `true` when `line` is a GFM table separator row (e.g.
    /// `| --- | :---: |`).
    let isMarkdownTableSeparator (line: string) : bool =
        if not (line.StartsWith("|", StringComparison.Ordinal)) then
            false
        else
            let cells = splitMarkdownRow line

            not (List.isEmpty cells)
            && cells
               |> List.forall (fun cell ->
                   let core = cell.Trim().Trim(':')
                   core.Length > 0 && core |> Seq.forall (fun ch -> ch = '-'))

    /// Finds the column indices for the `path`/`directory` and `license`
    /// headers in a GFM table header row.
    let findColumns (cells: string list) : int option * int option =
        cells
        |> List.indexed
        |> List.fold
            (fun (pathCol, licenseCol) (i, cell) ->
                match cell.Trim().ToLowerInvariant() with
                | "path"
                | "directory" when pathCol = None -> (Some i, licenseCol)
                | "license" when licenseCol = None -> (pathCol, Some i)
                | _ -> (pathCol, licenseCol))
            (None, None)

    /// Parses `LICENSING-NOTICE.md` at `path` and extracts every claim row
    /// from GFM tables that have both a `Path`/`Directory` column and a
    /// `License` column. Returns an empty list when the file does not
    /// exist.
    let private parseLicensingNotice (path: string) : Claim list =
        if not (File.Exists path) then
            []
        else
            let lines = File.ReadAllLines path

            let rec loop
                (i: int)
                (pathCol: int option)
                (licenseCol: int option)
                (inTable: bool)
                (acc: Claim list)
                : Claim list =
                if i >= lines.Length then
                    List.rev acc
                else
                    let line = lines.[i].Trim()

                    if not (line.StartsWith("|", StringComparison.Ordinal)) then
                        loop (i + 1) None None false acc
                    else
                        let cells = splitMarkdownRow line

                        if not inTable then
                            if i + 1 >= lines.Length then
                                loop (i + 1) pathCol licenseCol inTable acc
                            else
                                let separator = lines.[i + 1].Trim()

                                if not (isMarkdownTableSeparator separator) then
                                    loop (i + 1) pathCol licenseCol inTable acc
                                else
                                    let pc, lc = findColumns cells
                                    loop (i + 2) pc lc (pc.IsSome && lc.IsSome) acc
                        else
                            match pathCol, licenseCol with
                            | Some pc, Some lc when pc < List.length cells && lc < List.length cells ->
                                let rawPath = cells.[pc].Trim()
                                let rawLicense = cells.[lc].Trim()

                                if rawPath <> "" && rawLicense <> "" then
                                    loop
                                        (i + 1)
                                        pathCol
                                        licenseCol
                                        inTable
                                        ({ ClaimPath = rawPath
                                           ClaimLicense = rawLicense }
                                         :: acc)
                                else
                                    loop (i + 1) pathCol licenseCol inTable acc
                            | _ -> loop (i + 1) pathCol licenseCol inTable acc

            loop 0 None None false []

    /// Audits every required `apps/` and `libs/` subdirectory (plus
    /// `specs/`) for a `LICENSE` file and cross-checks identified SPDX
    /// identifiers against `LICENSING-NOTICE.md`. Findings are sorted by
    /// path.
    let audit (repoRoot: string) : Finding list =
        let dirs = requiredDirs repoRoot

        let outcomes =
            dirs
            |> List.map (fun rel -> rel, extractSpdx (Path.Combine(repoRoot, rel, "LICENSE")))

        let licenseByDir =
            outcomes
            |> List.choose (fun (rel, outcome) ->
                match outcome with
                | Found spdx -> Some(rel, spdx)
                | Missing
                | Unreadable _ -> None)
            |> Map.ofList

        let missingOrUnreadable =
            outcomes
            |> List.choose (fun (rel, outcome) ->
                match outcome with
                | Found _ -> None
                | Missing ->
                    Some
                        { Severity = Severity.Blocking
                          Message =
                            sprintf "[missing-license] %s — required directory \"%s\" has no LICENSE file" rel rel
                          Path = Some rel }
                | Unreadable message ->
                    Some
                        { Severity = Severity.Blocking
                          Message = sprintf "[unreadable-license] %s — read LICENSE in \"%s\": %s" rel rel message
                          Path = Some rel })

        let claims = parseLicensingNotice (Path.Combine(repoRoot, "LICENSING-NOTICE.md"))

        let mismatches =
            claims
            |> List.choose (fun claim ->
                let normalised = normaliseClaimPath claim.ClaimPath

                if not (ownedByLicenseAudit normalised) then
                    None
                else
                    match Map.tryFind normalised licenseByDir with
                    | None -> None
                    | Some identified ->
                        if licensesEqual identified claim.ClaimLicense then
                            None
                        else
                            Some
                                { Severity = Severity.Blocking
                                  Message =
                                    sprintf
                                        "[spdx-mismatch] %s — LICENSING-NOTICE.md claims \"%s\" for \"%s\" but LICENSE identifies \"%s\""
                                        normalised
                                        claim.ClaimLicense
                                        normalised
                                        identified
                                  Path = Some normalised })

        missingOrUnreadable @ mismatches |> List.sortBy (fun f -> f.Path)

    /// Renders license findings as human-readable text.
    let formatText (findings: Finding list) : string =
        if List.isEmpty findings then
            "LICENSE AUDIT PASSED: no findings\n"
        else
            let header = sprintf "LICENSE AUDIT FAILED: %d finding(s)\n" (List.length findings)

            let body =
                findings |> List.map (fun f -> sprintf "  %s\n" f.Message) |> String.concat ""

            header + body

/// Runs the emoji-codepoint validator over `paths`
/// [Repo-grounded — `convention_validate_emoji.rs::run`].
let runEmojiValidate (paths: string list) : ValidatorResult =
    match Emoji.audit paths with
    | Error message ->
        { Success = false
          Output = sprintf "EMOJI AUDIT FAILED: %s\n" message
          Findings = [] }
    | Ok findings ->
        { Success = List.isEmpty findings
          Output = Emoji.formatText findings
          Findings = findings }

/// Runs the per-directory LICENSE validator over `repoRoot`
/// [Repo-grounded — `convention_validate_license.rs::run`].
let runLicenseValidate (repoRoot: string) : ValidatorResult =
    let findings = License.audit repoRoot

    { Success = List.isEmpty findings
      Output = License.formatText findings
      Findings = findings }

/// The convention validators `convention audit` runs, in order
/// [Repo-grounded — `convention_audit.rs::MEMBERS`].
let private auditMembers: string list = [ "emoji"; "license" ]

/// Runs one named convention validator against `repoRoot` with its default
/// arguments, returning `Error` with a short reason when it reports
/// findings.
let internal runAuditMember (repoRoot: string) (name: string) : Result<unit, string> =
    match name with
    | "emoji" ->
        let result = runEmojiValidate [ repoRoot ]

        if result.Success then
            Ok()
        else
            Error(sprintf "%d emoji finding(s) found" (List.length result.Findings))
    | "license" ->
        let result = runLicenseValidate repoRoot

        if result.Success then
            Ok()
        else
            Error(sprintf "%d license finding(s) found" (List.length result.Findings))
    | other -> Error(sprintf "unknown convention validator: %s" other)

/// Runs every convention validator in sequence against `repoRoot`, skipping
/// any name listed in `skip`
/// [Repo-grounded — `convention_audit.rs::run`].
let runConventionAudit (repoRoot: string) (skip: string list) : ValidatorResult =
    let failures =
        auditMembers
        |> List.filter (fun name -> not (List.contains name skip))
        |> List.choose (fun name ->
            match runAuditMember repoRoot name with
            | Ok() -> None
            | Error message -> Some(sprintf "%s: %s" name message))

    if List.isEmpty failures then
        let passedCount = List.length auditMembers - List.length skip

        { Success = true
          Output = sprintf "CONVENTION AUDIT PASSED: all %d validators passed\n" passedCount
          Findings = [] }
    else
        let header =
            sprintf "CONVENTION AUDIT FAILED: %d validator(s) reported failures\n" (List.length failures)

        let body =
            failures
            |> List.map (fun failure -> sprintf "  %s\n" failure)
            |> String.concat ""

        { Success = false
          Output = header + body
          Findings = [] }
