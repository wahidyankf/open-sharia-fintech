/// Port of `rhino-cli test-coverage diff` and `rhino-cli test-coverage
/// merge` — coverage restricted to lines changed in a git diff, and
/// coverage-map merging/LCOV serialization, respectively [Repo-grounded —
/// `apps/rhino-cli/src/application/testcoverage/diff.rs`,
/// `apps/rhino-cli/src/application/testcoverage/types.rs`,
/// `apps/rhino-cli/src/application/testcoverage/exclude.rs`,
/// `apps/rhino-cli/src/application/testcoverage/merge.rs`,
/// `apps/rhino-cli/src/application/testcoverage/lcov.rs`] for
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/test-coverage/test-coverage-diff.feature`'s
/// 4 scenarios and
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/test-coverage/test-coverage-merge.feature`'s
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

open System.IO

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

            if trimmed.StartsWith("SF:") then
                files,
                { current with
                    Path = trimmed.Substring(3) }
            elif trimmed.StartsWith("DA:") then
                files, parseDa (trimmed.Substring(3)) current
            elif trimmed.StartsWith("BRDA:") then
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
