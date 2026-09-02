/// Port of `rhino-cli test-coverage diff` and `rhino-cli test-coverage
/// merge` — coverage restricted to lines changed in a git diff, and
/// coverage-map merging/LCOV serialization, respectively [Repo-grounded —
/// `apps/rhino-cli/src/application/testcoverage/diff.rs`,
/// `apps/rhino-cli/src/application/testcoverage/types.rs`,
/// `apps/rhino-cli/src/application/testcoverage/exclude.rs`,
/// `apps/rhino-cli/src/application/testcoverage/merge.rs`,
/// `apps/rhino-cli/src/application/testcoverage/lcov.rs`] for
/// `specs/apps/rhino/cli/behaviors/test-coverage/test-coverage-diff.feature`'s
/// 4 scenarios and
/// `specs/apps/rhino/cli/behaviors/test-coverage/test-coverage-merge.feature`'s
/// 3 scenarios.
///
/// Scope: the first PR against the test-coverage subsystem ported only the
/// pieces `compute_diff_coverage` itself needs: the coverage-report result
/// shapes (`types.rs`'s `Format`/`FileResult`/`Result`), the
/// `CoverageMap`/`LineCoverage`/`BranchCoverage` shapes and
/// `has_missed_branch` — the slice of `merge.rs` `diff.rs` calls directly.
/// This PR adds `merge.rs`'s own map-merge (`merge_coverage_maps`) and
/// LCOV-serialization (`format_lcov_string`/`write_lcov`) functions, its
/// `result_from_coverage_map` line-based aggregator, and the LCOV-specific
/// slice of `lcov.rs`'s `parse_lcov` plus `merge.rs`'s
/// `to_coverage_map_lcov` needed to turn a real `.info` file into a
/// `CoverageMap`. The JaCoCo/Cobertura/Go format parsers/converters and
/// `lcov.rs`'s own `compute_lcov_result` stay out of scope until the
/// `test-coverage-validate.feature` PR needs them. Also ports the
/// Go-`filepath.Match`-semantics exclude matcher (`exclude.rs`) and
/// `compute_diff_coverage`'s own line-intersection algorithm.
///
/// No Rust command wrapper exists for either `test-coverage diff` or
/// `test-coverage merge` under `apps/rhino-cli/src/commands/` (only
/// `test_coverage_validate.rs` is wired to a CLI verb) to bind argument
/// shapes against, so — matching this plan's established `Doctor.fs`
/// precedent for a feature with no wired-up CLI verb yet — every scenario
/// calls [`computeDiffCoverage`]/[`mergeCoverageMaps`]/[`writeLcov`]/
/// [`resultFromCoverageMap`] directly. `get_git_diff`'s real `git diff`
/// invocation and `parse_git_diff`'s unified-diff text parsing are both
/// deferred to whichever future PR wires a real `test-coverage diff` CLI
/// verb: each scenario's changed-line set is supplied directly as a
/// [`DiffHunk`] list, and each diff scenario's coverage-report contents are
/// supplied directly as a [`CoverageMap`] rather than round-tripped through
/// a not-yet-ported file parser. The merge scenarios, in contrast, do
/// round-trip through real temp LCOV files on disk via [`toCoverageMapLcov`]
/// and [`writeLcov`], because one merge scenario itself asserts that the
/// merged output file exists in LCOV format.
module RhinoCli.Application.TestCoverage

open System
open System.IO
open System.Text.Encodings.Web
open System.Text.Json
open System.Text.Json.Nodes
open System.Text.RegularExpressions
open System.Xml.Linq

// ---------------------------------------------------------------------------
// Core types [Repo-grounded — `types.rs`]
// ---------------------------------------------------------------------------

/// Identifies the coverage-report format used by a particular file
/// [Repo-grounded — `types.rs::Format`].
[<RequireQualifiedAccess>]
type Format =
    | Go
    | Lcov
    | Jacoco
    | Cobertura
    | Diff

/// Coverage statistics for a single source file
/// [Repo-grounded — `types.rs::FileResult`].
type FileResult =
    { Path: string
      Covered: int
      Partial: int
      Missed: int
      Total: int
      Pct: float }

/// Aggregated coverage result for an entire coverage report
/// [Repo-grounded — `types.rs::Result`]. Named `CoverageResult` rather than
/// the Rust source's literal `Result` to avoid colliding with `FSharp.Core`'s
/// own `Result` type — see `RhinoCli.Domain.Types.Severity`'s doc comment for
/// the same class of rename rationale.
type CoverageResult =
    { File: string
      Format: Format
      Covered: int
      Partial: int
      Missed: int
      Total: int
      Pct: float
      Threshold: float
      Passed: bool
      Files: FileResult list }

// ---------------------------------------------------------------------------
// CoverageMap shapes [Repo-grounded — `merge.rs`'s `LineCoverage`/
// `BranchCoverage`/`CoverageMap`]
// ---------------------------------------------------------------------------

/// Coverage data for a single branch within a line
/// [Repo-grounded — `merge.rs::BranchCoverage`].
type BranchCoverage =
    { BlockId: int64
      BranchId: int64
      HitCount: int64 }

/// Coverage data for a single executable line
/// [Repo-grounded — `merge.rs::LineCoverage`].
type LineCoverage =
    { HitCount: int64
      Branches: BranchCoverage list }

/// filepath → line number → [`LineCoverage`]. An F# `Map` mirrors Rust's
/// `BTreeMap`'s sorted, deterministic iteration order [Repo-grounded —
/// `merge.rs::CoverageMap`].
type CoverageMap = Map<string, Map<int64, LineCoverage>>

/// Whether any branch in the list has `HitCount <= 0`
/// [Repo-grounded — `merge.rs::has_missed_branch`].
let hasMissedBranch (branches: BranchCoverage list) : bool =
    branches |> List.exists (fun b -> b.HitCount <= 0L)

// ---------------------------------------------------------------------------
// File exclusion [Repo-grounded — `exclude.rs`]
// ---------------------------------------------------------------------------

/// Port of Go's `path/filepath.Match`. Single-segment globbing; `*` does not
/// cross `/` [Repo-grounded — `exclude.rs::go_filepath_match`,
/// `exclude.rs::go_match_rec`].
///
/// Supports `?` (any single non-`/` char), `*` (any sequence of non-`/`
/// chars), `[…]` character classes with optional `^` negation and `lo-hi`
/// ranges, and `\` escaping of literal metacharacters.
let private goFilepathMatch (pattern: string) (name: string) : bool =
    let p = pattern.ToCharArray()
    let n = name.ToCharArray()

    let rec go (pi: int) (ni: int) : bool =
        if pi >= p.Length then
            ni = n.Length
        else
            match p.[pi] with
            | '*' ->
                let pi2 = pi + 1

                if pi2 = p.Length then
                    // Trailing '*' matches anything up to '/' or end.
                    let rec allNonSlash (k: int) : bool =
                        if k >= n.Length then true
                        elif n.[k] = '/' then false
                        else allNonSlash (k + 1)

                    allNonSlash ni
                else
                    let rec tryFrom (k: int) : bool =
                        if go pi2 k then true
                        elif k >= n.Length || n.[k] = '/' then false
                        else tryFrom (k + 1)

                    tryFrom ni
            | '?' ->
                if ni >= n.Length || n.[ni] = '/' then
                    false
                else
                    go (pi + 1) (ni + 1)
            | '[' ->
                if ni >= n.Length then
                    false
                else
                    let ch = n.[ni]
                    let negate = pi + 1 < p.Length && p.[pi + 1] = '^'
                    let start = if negate then pi + 2 else pi + 1

                    let rec scanClass (j: int) (matched: bool) : int * bool =
                        if j >= p.Length || p.[j] = ']' then
                            j, matched
                        else
                            let lo = p.[j]

                            let hi, next =
                                if j + 2 < p.Length && p.[j + 1] = '-' then
                                    p.[j + 2], j + 2
                                else
                                    lo, j

                            scanClass (next + 1) (matched || (ch >= lo && ch <= hi))

                    let closeIdx, matched = scanClass start false

                    if closeIdx >= p.Length then false
                    elif matched = negate then false
                    else go (closeIdx + 1) (ni + 1)
            | '\\' when pi + 1 < p.Length ->
                if ni >= n.Length || n.[ni] <> p.[pi + 1] then
                    false
                else
                    go (pi + 2) (ni + 1)
            | c ->
                if ni >= n.Length || n.[ni] <> c then
                    false
                else
                    go (pi + 1) (ni + 1)

    go 0 0

/// True if `path` matches any glob pattern using Go's `filepath.Match`
/// semantics, tried against both the full path and its basename
/// [Repo-grounded — `exclude.rs::matches_any_exclude_pattern`].
let matchesAnyExcludePattern (path: string) (patterns: string list) : bool =
    let baseName =
        match path.LastIndexOf('/') with
        | -1 -> path
        | idx -> path.Substring(idx + 1)

    patterns
    |> List.exists (fun pattern -> goFilepathMatch pattern path || goFilepathMatch pattern baseName)

// ---------------------------------------------------------------------------
// Diff coverage [Repo-grounded — `diff.rs`]
// ---------------------------------------------------------------------------

/// A single diff hunk: the set of added or modified line numbers for one
/// file [Repo-grounded — `diff.rs::DiffHunk`].
type DiffHunk =
    { FilePath: string
      ChangedLines: int64 list }

/// Computes coverage restricted to lines changed in a git diff
/// [Repo-grounded — `diff.rs::compute_diff_coverage`]. Takes `hunks` and
/// `coverageMap` directly rather than a git ref and a coverage-report
/// filename — see this file's module doc comment for why the git invocation
/// and file parsing are out of this PR's scope.
///
/// Gherkin (binds) — "No changed lines reports 100% coverage":
///   Given a coverage file and no git changes
///   When the developer runs test-coverage diff
///   Then the command exits successfully
///   And the output reports 100% coverage
///
/// Gherkin (binds) — "Changed lines with full coverage pass threshold":
///   Given a coverage file where all changed lines are covered
///   When the developer runs test-coverage diff with a threshold
///   Then the command exits successfully
///
/// Gherkin (binds) — "Changed lines with missing coverage fail threshold":
///   Given a coverage file where some changed lines are missed
///   When the developer runs test-coverage diff with a high threshold
///   Then the command exits with a failure code
///
/// Gherkin (binds) — "Excluded files are not counted in diff coverage":
///   Given a coverage file and changes in excluded files
///   When the developer runs test-coverage diff with exclusion
///   Then the excluded files do not affect the diff coverage result
let computeDiffCoverage
    (coverageFile: string)
    (coverageMap: CoverageMap)
    (hunks: DiffHunk list)
    (excludePatterns: string list)
    (threshold: float)
    : CoverageResult =
    if List.isEmpty hunks then
        { File = coverageFile
          Format = Format.Diff
          Covered = 0
          Partial = 0
          Missed = 0
          Total = 0
          Pct = 100.0
          Threshold = threshold
          Passed = true
          Files = [] }
    else
        let excluded (filePath: string) : bool =
            not (List.isEmpty excludePatterns)
            && matchesAnyExcludePattern filePath excludePatterns

        let foldHunk
            ((covered, partial, missed, files): int * int * int * FileResult list)
            (hunk: DiffHunk)
            : int * int * int * FileResult list =
            if excluded hunk.FilePath then
                covered, partial, missed, files
            else
                let fileCov = Map.tryFind hunk.FilePath coverageMap

                let fc, fp, fm =
                    hunk.ChangedLines
                    |> List.fold
                        (fun (fc, fp, fm) (lineNo: int64) ->
                            match fileCov with
                            | None -> fc, fp, fm + 1
                            | Some lines ->
                                match Map.tryFind lineNo lines with
                                | None -> fc, fp, fm
                                | Some lc ->
                                    if lc.HitCount > 0L then
                                        if hasMissedBranch lc.Branches then
                                            fc, fp + 1, fm
                                        else
                                            fc + 1, fp, fm
                                    else
                                        fc, fp, fm + 1)
                        (0, 0, 0)

                let ft = fc + fp + fm

                let files' =
                    if ft > 0 then
                        let fpct = 100.0 * float fc / float ft

                        files
                        @ [ { Path = hunk.FilePath
                              Covered = fc
                              Partial = fp
                              Missed = fm
                              Total = ft
                              Pct = fpct } ]
                    else
                        files

                covered + fc, partial + fp, missed + fm, files'

        let covered, partial, missed, files = hunks |> List.fold foldHunk (0, 0, 0, [])
        let total = covered + partial + missed

        let pct =
            if total > 0 then
                100.0 * float covered / float total
            else
                100.0

        { File = coverageFile
          Format = Format.Diff
          Covered = covered
          Partial = partial
          Missed = missed
          Total = total
          Pct = pct
          Threshold = threshold
          Passed = threshold = 0.0 || pct >= threshold
          Files = files }

// ---------------------------------------------------------------------------
// CoverageMap merging and LCOV serialization [Repo-grounded — `merge.rs`]
// ---------------------------------------------------------------------------

/// Merges two branch lists, taking the maximum `HitCount` per
/// `(BlockId, BranchId)` key [Repo-grounded — `merge.rs::merge_branches`].
let private mergeBranches (a: BranchCoverage list) (b: BranchCoverage list) : BranchCoverage list =
    let byKey =
        (Map.empty, a)
        ||> List.fold (fun acc br -> Map.add (br.BlockId, br.BranchId) br.HitCount acc)

    let merged =
        (byKey, b)
        ||> List.fold (fun acc br ->
            let key = br.BlockId, br.BranchId
            let current = Map.tryFind key acc |> Option.defaultValue 0L

            if br.HitCount > current then
                Map.add key br.HitCount acc
            else
                acc)

    merged
    |> Map.toList
    |> List.map (fun ((blockId, branchId), hitCount) ->
        { BlockId = blockId
          BranchId = branchId
          HitCount = hitCount })

/// Unions multiple `CoverageMap`s. Max hit count per line; branches unioned
/// by `(BlockId, BranchId)` [Repo-grounded — `merge.rs::merge_coverage_maps`].
let mergeCoverageMaps (maps: CoverageMap list) : CoverageMap =
    let mergeLine (existing: LineCoverage option) (incoming: LineCoverage) : LineCoverage =
        match existing with
        | None -> incoming
        | Some ex ->
            { HitCount = max ex.HitCount incoming.HitCount
              Branches = mergeBranches ex.Branches incoming.Branches }

    let mergeOne (acc: CoverageMap) (m: CoverageMap) : CoverageMap =
        (acc, Map.toList m)
        ||> List.fold (fun acc2 (filePath, lines) ->
            let existingLines = Map.tryFind filePath acc2 |> Option.defaultValue Map.empty

            let mergedLines =
                (existingLines, Map.toList lines)
                ||> List.fold (fun linesAcc (lineNo, lc) ->
                    let merged = mergeLine (Map.tryFind lineNo linesAcc) lc
                    Map.add lineNo merged linesAcc)

            Map.add filePath mergedLines acc2)

    (Map.empty, maps) ||> List.fold mergeOne

/// Formats a `CoverageMap` as LCOV text. Deterministic order via F#'s
/// sorted `Map` [Repo-grounded — `merge.rs::format_lcov_string`].
let formatLcovString (cm: CoverageMap) : string =
    let sb = System.Text.StringBuilder()

    for KeyValue(filePath, lines) in cm do
        sb.Append("TN:\n") |> ignore
        sb.Append(sprintf "SF:%s\n" filePath) |> ignore

        // BRDA records first.
        for KeyValue(lineNo, lc) in lines do
            for br in lc.Branches do
                sb.Append(sprintf "BRDA:%d,%d,%d,%d\n" lineNo br.BlockId br.BranchId br.HitCount)
                |> ignore

        // Then DA records.
        for KeyValue(lineNo, lc) in lines do
            sb.Append(sprintf "DA:%d,%d\n" lineNo lc.HitCount) |> ignore

        sb.Append("end_of_record\n") |> ignore

    sb.ToString()

/// Writes `cm` serialized as LCOV text to `outPath`
/// [Repo-grounded — `merge.rs::write_lcov`].
let writeLcov (outPath: string) (cm: CoverageMap) : unit =
    File.WriteAllText(outPath, formatLcovString cm)

/// Computes a [`CoverageResult`] from a `CoverageMap` using the standard
/// line-based algorithm [Repo-grounded — `merge.rs::result_from_coverage_map`].
let resultFromCoverageMap (cm: CoverageMap) (threshold: float) : CoverageResult =
    let fileResult (filePath: string) (lines: Map<int64, LineCoverage>) : int * int * int * FileResult =
        let fc, fp, fm =
            lines
            |> Map.toList
            |> List.fold
                (fun (fc, fp, fm) (_, lc: LineCoverage) ->
                    if lc.HitCount > 0L then
                        if hasMissedBranch lc.Branches then
                            fc, fp + 1, fm
                        else
                            fc + 1, fp, fm
                    else
                        fc, fp, fm + 1)
                (0, 0, 0)

        let ft = fc + fp + fm
        let fpct = if ft > 0 then 100.0 * float fc / float ft else 100.0

        fc,
        fp,
        fm,
        { Path = filePath
          Covered = fc
          Partial = fp
          Missed = fm
          Total = ft
          Pct = fpct }

    let covered, partial, missed, files =
        cm
        |> Map.toList
        |> List.fold
            (fun (c, p, m, files) (filePath, lines) ->
                let fc, fp, fm, fr = fileResult filePath lines
                c + fc, p + fp, m + fm, files @ [ fr ])
            (0, 0, 0, [])

    let total = covered + partial + missed

    let pct =
        if total > 0 then
            100.0 * float covered / float total
        else
            100.0

    { File = ""
      Format = Format.Lcov
      Covered = covered
      Partial = partial
      Missed = missed
      Total = total
      Pct = pct
      Threshold = threshold
      Passed = pct >= threshold
      Files = files }

// ---------------------------------------------------------------------------
// LCOV parsing → CoverageMap [Repo-grounded — `lcov.rs::parse_lcov`,
// `merge.rs::to_coverage_map_lcov`]
// ---------------------------------------------------------------------------

/// Parsed data for a single source file recorded in an LCOV info file
/// [Repo-grounded — `lcov.rs::LcovFile`].
type private LcovFile =
    { Path: string
      DaLines: Map<int64, int64>
      BrdaData: Map<int64, int64 list> }

let private emptyLcovFile: LcovFile =
    { Path = ""
      DaLines = Map.empty
      BrdaData = Map.empty }

/// Parses the portion of a `DA:` record after the prefix and updates
/// `current`. Expected format: `<lineNo>,<count>[,<checksum>]`. Silently
/// ignores malformed records. When the same line number appears more than
/// once, keeps only the maximum count (matching the Rust/Go implementation)
/// [Repo-grounded — `lcov.rs::parse_da`].
let private parseDa (rest: string) (current: LcovFile) : LcovFile =
    let parts = rest.Split(',', 3)

    if parts.Length < 2 then
        current
    else
        match System.Int64.TryParse(parts.[0]), System.Int64.TryParse(parts.[1]) with
        | (true, lineNo), (true, count) ->
            match Map.tryFind lineNo current.DaLines with
            | Some existing when count <= existing -> current
            | _ ->
                { current with
                    DaLines = Map.add lineNo count current.DaLines }
        | _ -> current

/// Parses the portion of a `BRDA:` record after the prefix and updates
/// `current`. Expected format: `<lineNo>,<block>,<branch>,<taken>` where
/// `<taken>` may be `"-"` (never executed). Silently ignores malformed
/// records [Repo-grounded — `lcov.rs::parse_brda`].
let private parseBrda (rest: string) (current: LcovFile) : LcovFile =
    let parts = rest.Split(',', 4)

    if parts.Length < 4 then
        current
    else
        match System.Int64.TryParse(parts.[0]) with
        | false, _ -> current
        | true, lineNo ->
            let countStr = parts.[3]

            let count =
                if countStr = "-" || countStr = "" then
                    0L
                else
                    match System.Int64.TryParse(countStr) with
                    | true, v -> v
                    | false, _ -> 0L

            let existing = Map.tryFind lineNo current.BrdaData |> Option.defaultValue []

            { current with
                BrdaData = Map.add lineNo (existing @ [ count ]) current.BrdaData }

/// Reads and parses an LCOV info file from `filename`, one [`LcovFile`] per
/// `end_of_record` section [Repo-grounded — `lcov.rs::parse_lcov`].
let private parseLcov (filename: string) : LcovFile list =
    let lines = File.ReadAllLines(filename)

    let files, _ =
        ((List.empty, emptyLcovFile), lines)
        ||> Array.fold (fun (files, current) line ->
            let trimmed = line.Trim()

            if trimmed.StartsWith("SF:", StringComparison.Ordinal) then
                files,
                { current with
                    Path = trimmed.Substring(3) }
            elif trimmed.StartsWith("DA:", StringComparison.Ordinal) then
                files, parseDa (trimmed.Substring(3)) current
            elif trimmed.StartsWith("BRDA:", StringComparison.Ordinal) then
                files, parseBrda (trimmed.Substring(5)) current
            elif trimmed = "end_of_record" then
                files @ [ current ], emptyLcovFile
            else
                files, current)

    files

/// Converts an LCOV info file into a [`CoverageMap`]
/// [Repo-grounded — `merge.rs::to_coverage_map_lcov`].
let toCoverageMapLcov (filename: string) : CoverageMap =
    let convertFile (f: LcovFile) : Map<int64, LineCoverage> =
        let daEntries =
            f.DaLines
            |> Map.toList
            |> List.map (fun (lineNo, count) ->
                let branches =
                    Map.tryFind lineNo f.BrdaData
                    |> Option.defaultValue []
                    |> List.mapi (fun i hits ->
                        { BlockId = 0L
                          BranchId = int64 i
                          HitCount = hits })

                lineNo,
                { HitCount = count
                  Branches = branches })

        // BRDA-only lines: no DA record recorded this line, so classify and
        // derive the hit count from the branch data alone.
        let brdaOnlyEntries =
            f.BrdaData
            |> Map.toList
            |> List.filter (fun (lineNo, _) -> not (Map.containsKey lineNo f.DaLines))
            |> List.map (fun (lineNo, branchHits) ->
                let branches =
                    branchHits
                    |> List.mapi (fun i hits ->
                        { BlockId = 0L
                          BranchId = int64 i
                          HitCount = hits })

                let hitCount =
                    branchHits |> List.tryFind (fun h -> h > 0L) |> Option.defaultValue 0L

                lineNo,
                { HitCount = hitCount
                  Branches = branches })

        (daEntries @ brdaOnlyEntries) |> Map.ofList

    parseLcov filename
    |> List.fold (fun (acc: CoverageMap) f -> Map.add f.Path (convertFile f) acc) Map.empty

// ---------------------------------------------------------------------------
// Format code + detection [Repo-grounded — `types.rs::Format::code`,
// `detect.rs::detect_format`]
// ---------------------------------------------------------------------------

/// Lowercase string code for a [`Format`], used in JSON output
/// [Repo-grounded — `types.rs::Format::code`].
let formatCode (fmt: Format) : string =
    match fmt with
    | Format.Go -> "go"
    | Format.Lcov -> "lcov"
    | Format.Jacoco -> "jacoco"
    | Format.Cobertura -> "cobertura"
    | Format.Diff -> "diff"

/// Detects the coverage format of `filename` from its name, then — when the
/// name gives no answer — its content. Falls back to [`Format.Go`]
/// [Repo-grounded — `detect.rs::detect_format`].
let detectFormat (filename: string) : Format =
    let lower = filename.ToLowerInvariant()

    if lower.EndsWith(".info", StringComparison.Ordinal) || lower.Contains("lcov") then
        Format.Lcov
    elif lower.EndsWith(".xml", StringComparison.Ordinal) && lower.Contains("jacoco") then
        Format.Jacoco
    elif lower.EndsWith(".xml", StringComparison.Ordinal) && lower.Contains("cobertura") then
        Format.Cobertura
    elif not (File.Exists filename) then
        Format.Go
    else
        let rec scan (lines: string list) : Format =
            match lines with
            | [] -> Format.Go
            | line :: rest ->
                let s = line.Trim()

                if s = "" then
                    scan rest
                elif s.StartsWith("mode:", StringComparison.Ordinal) then
                    Format.Go
                elif
                    s.StartsWith("SF:", StringComparison.Ordinal)
                    || s.StartsWith("TN:", StringComparison.Ordinal)
                then
                    Format.Lcov
                elif s.StartsWith("<!DOCTYPE", StringComparison.Ordinal) then
                    scan rest
                elif s.StartsWith("<?xml", StringComparison.Ordinal) then
                    match s.IndexOf("?>", StringComparison.Ordinal) with
                    | -1 -> scan rest
                    | idx ->
                        let restOfLine = s.Substring(idx + 2).Trim()

                        if restOfLine = "" then
                            scan rest
                        elif restOfLine.StartsWith("<report", StringComparison.Ordinal) then
                            Format.Jacoco
                        elif restOfLine.StartsWith("<coverage", StringComparison.Ordinal) then
                            Format.Cobertura
                        else
                            Format.Go
                elif s.StartsWith("<report", StringComparison.Ordinal) then
                    Format.Jacoco
                elif s.StartsWith("<coverage", StringComparison.Ordinal) then
                    Format.Cobertura
                else
                    Format.Go

        File.ReadAllLines(filename) |> List.ofArray |> scan

// ---------------------------------------------------------------------------
// Go cover.out parsing and result computation [Repo-grounded —
// `go_coverage.rs`]
// ---------------------------------------------------------------------------

/// One coverage block parsed from a `cover.out` line
/// [Repo-grounded — `go_coverage.rs::CoverBlock`].
type private CoverBlock =
    { Filepath: string
      StartLine: int
      EndLine: int
      Count: int }

/// Mirrors Go's `coverBlockRe` — capture groups: filepath, start line, end
/// line, count [Repo-grounded — `go_coverage.rs::cover_block_re`].
let private coverBlockRegex = Regex(@"^(.+):(\d+)\.\d+,(\d+)\.\d+ \d+ (\d+)$")

/// Returns `true` when `content` is executable Go code: not blank, not a
/// `//`-comment line, and not a brace-only line. `(`/`)` are NOT excluded
/// [Repo-grounded — `go_coverage.rs::is_go_code_line`].
let private isGoCodeLine (content: string) : bool =
    let s = content.Trim()

    if s = "" then false
    elif s.StartsWith("//", StringComparison.Ordinal) then false
    elif s = "{" || s = "}" then false
    else true

/// Reads `go.mod` in `dir` and returns the module path, or `""` when absent
/// [Repo-grounded — `go_coverage.rs::get_module_name_from`].
let private getModuleNameFrom (dir: string) : string =
    let path = Path.Combine(dir, "go.mod")

    if not (File.Exists path) then
        ""
    else
        File.ReadAllLines(path)
        |> Array.tryPick (fun line ->
            let parts = line.Split([| ' '; '\t' |], StringSplitOptions.RemoveEmptyEntries)

            if parts.Length >= 2 && parts.[0] = "module" then
                Some parts.[1]
            else
                None)
        |> Option.defaultValue ""

/// Returns line number (1-based) → content for a source file resolved
/// relative to `baseDir`, or `None` when the file cannot be opened
/// [Repo-grounded — `go_coverage.rs::get_source_lines_from`].
let private getSourceLinesFrom (baseDir: string) (relPath: string) : Map<int, string> option =
    let path = Path.Combine(baseDir, relPath)

    if not (File.Exists path) then
        None
    else
        File.ReadAllLines(path)
        |> Array.mapi (fun idx line -> idx + 1, line)
        |> Map.ofArray
        |> Some

/// Parses a Go `cover.out` file into its coverage blocks
/// [Repo-grounded — `go_coverage.rs::parse_cover_out`].
let private parseCoverOut (filename: string) : Result<CoverBlock list, string> =
    if not (File.Exists filename) then
        Error(sprintf "file not found: %s" filename)
    else
        File.ReadAllLines(filename)
        |> Array.choose (fun line ->
            let trimmed = line.Trim()

            if trimmed.StartsWith("mode:", StringComparison.Ordinal) || trimmed = "" then
                None
            else
                let m = coverBlockRegex.Match(trimmed)

                if not m.Success then
                    None
                else
                    Some
                        { Filepath = m.Groups.[1].Value
                          StartLine = int m.Groups.[2].Value
                          EndLine = int m.Groups.[3].Value
                          Count = int m.Groups.[4].Value })
        |> List.ofArray
        |> Ok

/// Computes line coverage from a Go `cover.out` file using the standard
/// line-based algorithm. Source files are resolved relative to the
/// `cover.out`'s directory; when a source file cannot be found, every line
/// recorded for it is counted without the non-code-line skip
/// [Repo-grounded — `go_coverage.rs::compute_go_result`].
///
/// Gherkin (binds) — see [`validate`]'s doc comment for the scenarios this
/// function jointly satisfies.
let computeGoResult (filename: string) (threshold: float) : Result<CoverageResult, string> =
    parseCoverOut filename
    |> Result.map (fun blocks ->
        let projectDir =
            match Path.GetDirectoryName(filename) with
            | null
            | "" -> "."
            | d -> d

        let moduleName = getModuleNameFrom projectDir

        let perFile =
            blocks
            |> List.groupBy (fun b -> b.Filepath)
            |> List.map (fun (fp, fblocks) ->
                let relPath =
                    if moduleName <> "" && fp.StartsWith(moduleName + "/", StringComparison.Ordinal) then
                        fp.Substring(moduleName.Length + 1)
                    else
                        fp

                let source = getSourceLinesFrom projectDir relPath

                let lineCounts =
                    (Map.empty, fblocks)
                    ||> List.fold (fun acc b ->
                        ([ b.StartLine .. b.EndLine ], acc)
                        ||> List.foldBack (fun lineNo acc2 ->
                            let existing = Map.tryFind lineNo acc2 |> Option.defaultValue []
                            Map.add lineNo (b.Count :: existing) acc2))

                let fc, fp2, fm =
                    lineCounts
                    |> Map.toList
                    |> List.fold
                        (fun (fc, fp2, fm) (lineNo, counts) ->
                            let skip =
                                match source with
                                | None -> false
                                | Some src ->
                                    match Map.tryFind lineNo src with
                                    | None -> true
                                    | Some content -> not (isGoCodeLine content)

                            if skip then
                                fc, fp2, fm
                            else
                                let hasCovered = counts |> List.exists (fun c -> c > 0)
                                let hasMissed = counts |> List.exists (fun c -> c = 0)

                                if hasCovered && not hasMissed then fc + 1, fp2, fm
                                elif hasCovered && hasMissed then fc, fp2 + 1, fm
                                else fc, fp2, fm + 1)
                        (0, 0, 0)

                let ft = fc + fp2 + fm
                let fpct = if ft > 0 then 100.0 * float fc / float ft else 100.0

                fc,
                fp2,
                fm,
                { Path = fp
                  Covered = fc
                  Partial = fp2
                  Missed = fm
                  Total = ft
                  Pct = fpct })

        let covered, partial, missed, files =
            (perFile, (0, 0, 0, []))
            ||> List.foldBack (fun (fc, fp2, fm, fr) (c, p, m, files) -> c + fc, p + fp2, m + fm, fr :: files)

        let total = covered + partial + missed

        let pct =
            if total > 0 then
                100.0 * float covered / float total
            else
                100.0

        { File = filename
          Format = Format.Go
          Covered = covered
          Partial = partial
          Missed = missed
          Total = total
          Pct = pct
          Threshold = threshold
          Passed = pct >= threshold
          Files = files })

// ---------------------------------------------------------------------------
// Cobertura XML parsing and result computation [Repo-grounded —
// `cobertura.rs`]
// ---------------------------------------------------------------------------

/// Extracts `(covered, total)` from a `condition-coverage` attribute such as
/// `"50% (1/2)"` [Repo-grounded — `cobertura.rs::parse_branch_coverage`].
let parseBranchCoverage (condCov: string) : int * int =
    let openIdx = condCov.IndexOf('(')
    let closeIdx = condCov.IndexOf(')')

    if openIdx = -1 || closeIdx = -1 || closeIdx <= openIdx then
        0, 0
    else
        let fraction = condCov.Substring(openIdx + 1, closeIdx - openIdx - 1)
        let parts = fraction.Split([| '/' |], 2)

        if parts.Length <> 2 then
            0, 0
        else
            match Int32.TryParse(parts.[0]), Int32.TryParse(parts.[1]) with
            | (true, c), (true, t) -> c, t
            | _ -> 0, 0

/// Reads and parses a Cobertura XML file [Repo-grounded —
/// `cobertura.rs::parse_cobertura`].
let private parseCobertura (filename: string) : Result<XDocument, string> =
    if not (File.Exists filename) then
        Error(sprintf "file not found: %s" filename)
    else
        try
            Ok(XDocument.Load(filename))
        with ex ->
            Error(sprintf "invalid Cobertura XML: %s" ex.Message)

/// Parses `filename` as a Cobertura XML report and computes aggregated
/// coverage [Repo-grounded — `cobertura.rs::compute_cobertura_result`].
///
/// Gherkin (binds) — see [`validate`]'s doc comment for the scenarios this
/// function jointly satisfies.
let computeCoberturaResult (filename: string) (threshold: float) : Result<CoverageResult, string> =
    parseCobertura filename
    |> Result.map (fun doc ->
        let name (n: string) = XName.Get(n)

        let attrString (el: XElement) (n: string) : string =
            match el.Attribute(name n) with
            | null -> ""
            | a -> a.Value

        let attrInt64 (el: XElement) (n: string) : int64 =
            match el.Attribute(name n) with
            | null -> 0L
            | a ->
                match Int64.TryParse(a.Value) with
                | true, v -> v
                | false, _ -> 0L

        let attrBool (el: XElement) (n: string) : bool = attrString el n = "true"

        let lineRows =
            doc.Descendants(name "class")
            |> Seq.collect (fun cls ->
                let path = attrString cls "filename"

                cls.Descendants(name "line")
                |> Seq.map (fun line ->
                    path, attrInt64 line "hits", attrBool line "branch", attrString line "condition-coverage"))
            |> List.ofSeq

        let perFile =
            lineRows
            |> List.groupBy (fun (path, _, _, _) -> path)
            |> List.sortBy fst
            |> List.map (fun (path, lines) ->
                let fc, fp2, fm =
                    lines
                    |> List.fold
                        (fun (c, p, m) (_, hits, branch, condCov) ->
                            if hits > 0L then
                                if branch then
                                    let brCov, brTotal = parseBranchCoverage condCov

                                    if brTotal > 0 && brCov < brTotal then
                                        c, p + 1, m
                                    else
                                        c + 1, p, m
                                else
                                    c + 1, p, m
                            else
                                c, p, m + 1)
                        (0, 0, 0)

                let ft = fc + fp2 + fm
                let fpct = if ft > 0 then 100.0 * float fc / float ft else 100.0

                fc,
                fp2,
                fm,
                { Path = path
                  Covered = fc
                  Partial = fp2
                  Missed = fm
                  Total = ft
                  Pct = fpct })

        let covered, partial, missed, files =
            (perFile, (0, 0, 0, []))
            ||> List.foldBack (fun (fc, fp2, fm, fr) (c, p, m, files) -> c + fc, p + fp2, m + fm, fr :: files)

        let total = covered + partial + missed

        let pct =
            if total > 0 then
                100.0 * float covered / float total
            else
                100.0

        { File = filename
          Format = Format.Cobertura
          Covered = covered
          Partial = partial
          Missed = missed
          Total = total
          Pct = pct
          Threshold = threshold
          Passed = pct >= threshold
          Files = files })

// ---------------------------------------------------------------------------
// Exclude-pattern application [Repo-grounded —
// `test_coverage_validate.rs::apply_exclude`]
// ---------------------------------------------------------------------------

/// Drops `FileResult` entries whose path matches any of `patterns` and
/// recomputes the aggregate counts. Reuses [`matchesAnyExcludePattern`]'s
/// Go-`filepath.Match` semantics rather than porting the `glob` crate
/// separately — the scope this function serves (a handful of
/// exact-name/simple-wildcard exclusions) does not need the two matchers'
/// differing edge-case behavior to diverge [Repo-grounded —
/// `test_coverage_validate.rs::apply_exclude`].
let applyExclude (patterns: string list) (result: CoverageResult) : CoverageResult =
    if List.isEmpty patterns then
        result
    else
        let files =
            result.Files
            |> List.filter (fun f -> not (matchesAnyExcludePattern f.Path patterns))

        let covered, partial, missed =
            (files, (0, 0, 0))
            ||> List.foldBack (fun f (c, p, m) -> c + f.Covered, p + f.Partial, m + f.Missed)

        let total = covered + partial + missed

        let pct =
            if total > 0 then
                100.0 * float covered / float total
            else
                100.0

        { result with
            Files = files
            Covered = covered
            Partial = partial
            Missed = missed
            Total = total
            Pct = pct
            Passed = pct >= result.Threshold }

// ---------------------------------------------------------------------------
// Text/JSON reporting [Repo-grounded — `reporter.rs`]
// ---------------------------------------------------------------------------

/// Filters `files` to those below `belowThreshold` (all files when
/// `belowThreshold` is `0.0`), then sorts ascending by `Pct`
/// [Repo-grounded — `reporter.rs::filter_and_sort_files`].
let filterAndSortFiles (files: FileResult list) (belowThreshold: float) : FileResult list =
    files
    |> List.filter (fun f -> not (belowThreshold > 0.0 && f.Pct >= belowThreshold))
    |> List.sortBy (fun f -> f.Pct)

/// Human-readable coverage summary — byte-for-byte match of Go/Rust's
/// output shape [Repo-grounded — `reporter.rs::format_text`].
let formatText (r: CoverageResult) : string =
    let statusLine =
        if r.Passed then
            sprintf "PASS: %.2f%% >= %.0f%% threshold\n" r.Pct r.Threshold
        else
            sprintf "FAIL: %.2f%% < %.0f%% threshold\n" r.Pct r.Threshold

    sprintf
        "Line coverage: %.2f%% (%d covered, %d partial, %d missed, %d total)\n"
        r.Pct
        r.Covered
        r.Partial
        r.Missed
        r.Total
    + statusLine

/// Per-file coverage table as plain text [Repo-grounded —
/// `reporter.rs::format_text_per_file`].
let formatTextPerFile (r: CoverageResult) (belowThreshold: float) : string =
    let files = filterAndSortFiles r.Files belowThreshold

    if List.isEmpty files then
        "No files to report.\n"
    else
        let header = sprintf "\nPer-file coverage (%d files):\n" (List.length files)

        let rows =
            files
            |> List.map (fun f ->
                sprintf "  %6.2f%%  %s (%d covered, %d partial, %d missed)\n" f.Pct f.Path f.Covered f.Partial f.Missed)
            |> String.concat ""

        header + rows

/// Serialises a `float` the way Go's `encoding/json` does: whole-number
/// floats render without a trailing `.0` [Repo-grounded —
/// `reporter.rs::serialize_f64_gostyle`].
let private jsonFloat (v: float) : JsonNode =
    if Double.IsFinite v && v = Math.Truncate v && Math.Abs v < 1e15 then
        JsonValue.Create(int64 v) :> JsonNode
    else
        JsonValue.Create(v) :> JsonNode

let private fileResultNode (f: FileResult) : JsonNode =
    let node = JsonObject()
    node.["path"] <- JsonValue.Create(f.Path)
    node.["covered"] <- JsonValue.Create(f.Covered)
    node.["partial"] <- JsonValue.Create(f.Partial)
    node.["missed"] <- JsonValue.Create(f.Missed)
    node.["total"] <- JsonValue.Create(f.Total)
    node.["pct"] <- jsonFloat f.Pct
    node :> JsonNode

/// Formats `r` as a pretty-printed JSON string. Includes a per-file
/// breakdown, filtered to files below `belowThreshold`, only when `perFile`
/// is `true` and `r.Files` is non-empty [Repo-grounded —
/// `reporter.rs::format_json`].
let formatJson (r: CoverageResult) (perFile: bool) (belowThreshold: float) : string =
    let status = if r.Passed then "success" else "failure"

    let files =
        if perFile && not (List.isEmpty r.Files) then
            filterAndSortFiles r.Files belowThreshold
            |> List.map fileResultNode
            |> Array.ofList
        else
            [||]

    let root = JsonObject()
    root.["status"] <- JsonValue.Create(status)
    root.["timestamp"] <- JsonValue.Create(DateTimeOffset.Now.ToString("yyyy-MM-ddTHH:mm:sszzz"))
    root.["file"] <- JsonValue.Create(r.File)
    root.["format"] <- JsonValue.Create(formatCode r.Format)
    root.["covered"] <- JsonValue.Create(r.Covered)
    root.["partial"] <- JsonValue.Create(r.Partial)
    root.["missed"] <- JsonValue.Create(r.Missed)
    root.["total"] <- JsonValue.Create(r.Total)
    root.["pct"] <- jsonFloat r.Pct
    root.["threshold"] <- jsonFloat r.Threshold
    root.["passed"] <- JsonValue.Create(r.Passed)

    if files.Length > 0 then
        root.["files"] <- JsonArray(files)

    let options = JsonSerializerOptions()
    options.WriteIndented <- true
    options.Encoder <- JavaScriptEncoder.UnsafeRelaxedJsonEscaping
    root.ToJsonString(options)

/// Formats `r` as a Markdown coverage report: a summary metric table always,
/// plus a per-file breakdown table when `perFile` is `true` and `r.Files` is
/// non-empty [Repo-grounded — `reporter.rs::format_markdown`].
let formatMarkdown (r: CoverageResult) (perFile: bool) (belowThreshold: float) : string =
    let status = if r.Passed then "PASS" else "FAIL"

    let sb = Text.StringBuilder()

    sb.Append("## Coverage Report\n\n") |> ignore
    sb.Append("| Metric | Value |\n") |> ignore
    sb.Append("| --- | --- |\n") |> ignore
    sb.Append(sprintf "| File | %s |\n" r.File) |> ignore
    sb.Append(sprintf "| Format | %s |\n" (formatCode r.Format)) |> ignore
    sb.Append(sprintf "| Line Coverage | %.2f%% |\n" r.Pct) |> ignore
    sb.Append(sprintf "| Threshold | %.0f%% |\n" r.Threshold) |> ignore
    sb.Append(sprintf "| Covered | %d |\n" r.Covered) |> ignore
    sb.Append(sprintf "| Partial | %d |\n" r.Partial) |> ignore
    sb.Append(sprintf "| Missed | %d |\n" r.Missed) |> ignore
    sb.Append(sprintf "| Total | %d |\n" r.Total) |> ignore
    sb.Append(sprintf "| Status | **%s** |\n" status) |> ignore

    if perFile && not (List.isEmpty r.Files) then
        let files = filterAndSortFiles r.Files belowThreshold

        if not (List.isEmpty files) then
            sb.Append("\n### Per-File Breakdown\n\n") |> ignore
            sb.Append("| Coverage | File | Covered | Partial | Missed |\n") |> ignore
            sb.Append("| --- | --- | --- | --- | --- |\n") |> ignore

            for f in files do
                sb.Append(sprintf "| %.2f%% | %s | %d | %d | %d |\n" f.Pct f.Path f.Covered f.Partial f.Missed)
                |> ignore

    sb.ToString()

// ---------------------------------------------------------------------------
// `test-coverage validate` entry point [Repo-grounded —
// `test_coverage_validate.rs::run`] for
// `specs/apps/rhino/cli/behaviors/test-coverage/test-coverage-validate.feature`'s
// 10 scenarios
// ---------------------------------------------------------------------------

/// CLI-argument-shaped options for `test-coverage validate`
/// [Repo-grounded — `test_coverage_validate.rs::ValidateArgs`].
type ValidateOptions =
    { CoverageFile: string
      Threshold: float
      PerFile: bool
      BelowThreshold: float
      Exclude: string list
      Json: bool
      Markdown: bool }

/// The rendered report plus whether coverage met the threshold. Unlike the
/// Rust command wrapper — which prints the report and then separately
/// returns a threshold-failure `Err` — [`validate`] always returns `Ok` once
/// the coverage file parses, carrying `Passed` for the caller to translate
/// into an exit code; `Result.Error` is reserved for cases where no report
/// could be produced at all (missing file, invalid XML, unsupported format)
/// [Repo-grounded — `test_coverage_validate.rs::run`]. `Pct`/`Threshold`
/// (the filtered, post-exclude values) let the CLI-wiring layer reconstruct
/// Rust's `"coverage {pct:.2}% is below threshold {threshold:.0}%"` failure
/// message without recomputing anything itself.
type ValidateOutcome =
    { Output: string
      Passed: bool
      Pct: float
      Threshold: float }

/// Validates a coverage report file against `opts.Threshold`, auto-detecting
/// its format (Go, LCOV, or Cobertura — `JaCoCo` and `Diff` are rejected,
/// matching this port's declared scope) and rendering it as text or JSON.
///
/// Gherkin (binds) — "A Go coverage file above the threshold reports success":
///   Given a Go coverage file recording 90% line coverage
///   When the developer runs test-coverage validate with an 85% threshold
///   Then the command exits successfully
///   And the output reports the measured coverage percentage
///   And the output indicates the coverage passes the threshold
///
/// Gherkin (binds) — "A Go coverage file below the threshold reports failure":
///   Given a Go coverage file recording 70% line coverage
///   When the developer runs test-coverage validate with an 85% threshold
///   Then the command exits with a failure code
///   And the output indicates the coverage fails the threshold
///
/// Gherkin (binds) — "An LCOV file above the threshold reports success":
///   Given an LCOV coverage file recording 90% line coverage
///   When the developer runs test-coverage validate with an 85% threshold
///   Then the command exits successfully
///   And the output indicates the coverage passes the threshold
///
/// Gherkin (binds) — "Coverage at exactly the threshold passes":
///   Given a Go coverage file recording 85% line coverage
///   When the developer runs test-coverage validate with an 85% threshold
///   Then the command exits successfully
///
/// Gherkin (binds) — "JSON output includes structured coverage metrics":
///   Given a Go coverage file recording 90% line coverage
///   When the developer runs test-coverage validate with an 85% threshold requesting JSON output
///   Then the command exits successfully
///   And the output is valid JSON
///   And the JSON includes the coverage percentage and pass/fail status
///
/// Gherkin (binds) — "Per-file flag shows individual file coverage":
///   Given an LCOV coverage file with multiple source files
///   When the developer runs test-coverage validate with an 85% threshold and per-file flag
///   Then the command exits successfully
///   And the output contains per-file coverage breakdown
///
/// Gherkin (binds) — "A Cobertura XML file above the threshold reports success":
///   Given a Cobertura XML coverage file recording 90% line coverage
///   When the developer runs test-coverage validate with an 85% threshold
///   Then the command exits successfully
///   And the output indicates the coverage passes the threshold
///
/// Gherkin (binds) — "A Cobertura XML file with partial branches classifies correctly":
///   Given a Cobertura XML coverage file with partial branch coverage
///   When the developer runs test-coverage validate with an 85% threshold
///   Then the command exits with a failure code
///   And the output indicates the coverage fails the threshold
///
/// Gherkin (binds) — "Exclude flag removes files from coverage calculation":
///   Given an LCOV coverage file with multiple source files
///   When the developer runs test-coverage validate with exclusion of a source file
///   Then the command exits successfully
///   And the output does not contain the excluded file
///
/// Gherkin (binds) — "A non-existent coverage file reports an error":
///   Given no coverage file exists at the specified path
///   When the developer runs test-coverage validate with an 85% threshold
///   Then the command exits with a failure code
///   And the output describes the missing file
let validate (opts: ValidateOptions) : Result<ValidateOutcome, string> =
    let format = detectFormat opts.CoverageFile

    let computed =
        match format with
        | Format.Lcov ->
            if not (File.Exists opts.CoverageFile) then
                Error(sprintf "file not found: %s" opts.CoverageFile)
            else
                Ok
                    { resultFromCoverageMap (toCoverageMapLcov opts.CoverageFile) opts.Threshold with
                        File = opts.CoverageFile }
        | Format.Go -> computeGoResult opts.CoverageFile opts.Threshold
        | Format.Cobertura -> computeCoberturaResult opts.CoverageFile opts.Threshold
        | Format.Jacoco -> Error "jacoco coverage files are not supported by this command"
        // Coverage note: unreachable. `format` above is always the result of
        // `detectFormat opts.CoverageFile`, and every branch of `detectFormat`
        // returns `Format.Lcov`, `Format.Jacoco`, `Format.Cobertura`, or
        // `Format.Go` — never `Format.Diff`. `Format.Diff` is constructed
        // only inside `computeDiffCoverage`, the unrelated `diff` command's
        // own result builder, whose output never flows into this match.
        | Format.Diff -> Error "diff format is not a valid input format for validate"

    computed
    |> Result.mapError (sprintf "coverage check failed: %s")
    |> Result.map (fun result ->
        let filtered =
            if List.isEmpty opts.Exclude then
                result
            else
                applyExclude opts.Exclude result

        let output =
            if opts.Json then
                formatJson filtered opts.PerFile opts.BelowThreshold
            elif opts.Markdown then
                formatMarkdown filtered opts.PerFile opts.BelowThreshold
            else
                let perFileText =
                    if opts.PerFile then
                        formatTextPerFile filtered opts.BelowThreshold
                    else
                        ""

                formatText filtered + perFileText

        { Output = output
          Passed = filtered.Passed
          Pct = filtered.Pct
          Threshold = filtered.Threshold })
