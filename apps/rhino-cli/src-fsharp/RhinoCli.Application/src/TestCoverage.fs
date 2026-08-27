/// Port of `rhino-cli test-coverage diff` — coverage restricted to lines
/// changed in a git diff [Repo-grounded —
/// `apps/rhino-cli/src/application/testcoverage/diff.rs`,
/// `apps/rhino-cli/src/application/testcoverage/types.rs`,
/// `apps/rhino-cli/src/application/testcoverage/exclude.rs`,
/// `apps/rhino-cli/src/application/testcoverage/merge.rs`] for
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/test-coverage/test-coverage-diff.feature`'s
/// 4 scenarios.
///
/// Scope: this first PR against the test-coverage subsystem ports only the
/// pieces `compute_diff_coverage` itself needs: the coverage-report result
/// shapes (`types.rs`'s `Format`/`FileResult`/`Result`), the
/// `CoverageMap`/`LineCoverage`/`BranchCoverage` shapes and
/// `has_missed_branch` — the slice of `merge.rs` `diff.rs` calls directly.
/// The LCOV/JaCoCo/Cobertura/Go format parsers and the actual
/// map-merge/LCOV-serialization functions stay out of scope until the
/// `test-coverage-merge.feature`/`test-coverage-validate.feature` PRs need
/// them (they extend this same file). Also ports the Go-`filepath.Match`
/// -semantics exclude matcher (`exclude.rs`) and `compute_diff_coverage`'s
/// own line-intersection algorithm.
///
/// No Rust command wrapper exists for `test-coverage diff` under
/// `apps/rhino-cli/src/commands/` (only `test_coverage_validate.rs` is
/// wired to a CLI verb) to bind argument shapes against, so — matching this
/// plan's established `Doctor.fs` precedent for a feature with no wired-up
/// CLI verb yet — every scenario calls [`computeDiffCoverage`] directly.
/// `get_git_diff`'s real `git diff` invocation and `parse_git_diff`'s
/// unified-diff text parsing are both deferred to whichever future PR wires
/// a real `test-coverage diff` CLI verb: each scenario's changed-line set is
/// supplied directly as a [`DiffHunk`] list, and each scenario's
/// coverage-report contents are supplied directly as a [`CoverageMap`]
/// rather than round-tripped through a not-yet-ported file parser.
module RhinoCli.Application.TestCoverage

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
