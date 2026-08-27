/// Plain xunit tests for `RhinoCli.Application.TestCoverage`'s pure helpers
/// that have no dedicated Gherkin scenario, or are exercised only
/// indirectly there — mirrors the rationale `DoctorUnitTests.fs`'s module
/// doc comment states for its own split from `DoctorSteps.fs`. Ported from
/// `apps/rhino-cli/src/application/testcoverage/exclude.rs`'s and
/// `apps/rhino-cli/src/application/testcoverage/merge.rs`'s
/// `#[cfg(test)] mod tests`.
module RhinoCli.Tests.Unit.Steps.TestCoverageUnitTests

open System.IO
open Xunit
open RhinoCli.Application.TestCoverage

// ---- hasMissedBranch ----

[<Fact>]
let ``hasMissedBranch detects a zero-hit branch`` () =
    Assert.True(
        hasMissedBranch
            [ { BlockId = 0L
                BranchId = 0L
                HitCount = 0L } ]
    )

[<Fact>]
let ``hasMissedBranch is false when every branch was hit`` () =
    Assert.False(
        hasMissedBranch
            [ { BlockId = 0L
                BranchId = 0L
                HitCount = 1L } ]
    )

[<Fact>]
let ``hasMissedBranch is false for an empty branch list`` () = Assert.False(hasMissedBranch [])

// ---- matchesAnyExcludePattern / goFilepathMatch ----

[<Fact>]
let ``matches a basename glob`` () =
    Assert.True(matchesAnyExcludePattern "src/foo_test.go" [ "*_test.go" ])

[<Fact>]
let ``matches a path glob`` () =
    Assert.True(matchesAnyExcludePattern "generated/foo.go" [ "generated/*" ])

[<Fact>]
let ``no match returns false`` () =
    Assert.False(matchesAnyExcludePattern "src/foo.go" [ "*_test.go" ])

[<Fact>]
let ``star does not cross a path separator`` () =
    Assert.False(matchesAnyExcludePattern "a/b/c" [ "a/*" ])
    Assert.True(matchesAnyExcludePattern "a/b" [ "a/*" ])

[<Fact>]
let ``question mark matches exactly one character`` () =
    Assert.True(matchesAnyExcludePattern "a.go" [ "?.go" ])
    Assert.False(matchesAnyExcludePattern "ab.go" [ "?.go" ])

[<Fact>]
let ``character class matches any listed character`` () =
    Assert.True(matchesAnyExcludePattern "a.go" [ "[ab].go" ])
    Assert.True(matchesAnyExcludePattern "b.go" [ "[ab].go" ])
    Assert.False(matchesAnyExcludePattern "c.go" [ "[ab].go" ])

[<Fact>]
let ``character class supports a range and negation`` () =
    Assert.True(matchesAnyExcludePattern "5.go" [ "[0-9].go" ])
    Assert.False(matchesAnyExcludePattern "5.go" [ "[^0-9].go" ])

[<Fact>]
let ``backslash escapes a literal metacharacter`` () =
    Assert.True(matchesAnyExcludePattern "a*b" [ @"a\*b" ])
    Assert.False(matchesAnyExcludePattern "axb" [ @"a\*b" ])

[<Fact>]
let ``empty pattern list never matches`` () =
    Assert.False(matchesAnyExcludePattern "src/foo.go" [])

// ---- computeDiffCoverage ----

[<Fact>]
let ``computeDiffCoverage reports 100 percent when there are no hunks`` () =
    let result = computeDiffCoverage "cov.info" Map.empty [] [] 0.0
    Assert.Equal(100.0, result.Pct)
    Assert.True(result.Passed)
    Assert.Equal(0, result.Total)
    Assert.Empty(result.Files)

[<Fact>]
let ``computeDiffCoverage treats every changed line as missed when the file is absent from the coverage map`` () =
    let cm: CoverageMap =
        Map.ofList [ "other.fs", Map.ofList [ 1L, { HitCount = 1L; Branches = [] } ] ]

    let hunks =
        [ { FilePath = "a.fs"
            ChangedLines = [ 1L; 2L ] } ]

    let result = computeDiffCoverage "cov.info" cm hunks [] 0.0
    Assert.Equal(0, result.Covered)
    Assert.Equal(2, result.Missed)

[<Fact>]
let ``computeDiffCoverage skips a changed line not present in the coverage report`` () =
    let cm: CoverageMap = Map.ofList [ "a.fs", Map.ofList [] ]

    let hunks =
        [ { FilePath = "a.fs"
            ChangedLines = [ 1L ] } ]

    let result = computeDiffCoverage "cov.info" cm hunks [] 0.0
    Assert.Equal(0, result.Total)
    Assert.Equal(100.0, result.Pct)

[<Fact>]
let ``computeDiffCoverage treats a covered line with a missed branch as partial`` () =
    let cm: CoverageMap =
        Map.ofList
            [ "a.fs",
              Map.ofList
                  [ 1L,
                    { HitCount = 1L
                      Branches =
                        [ { BlockId = 0L
                            BranchId = 0L
                            HitCount = 0L } ] } ] ]

    let hunks =
        [ { FilePath = "a.fs"
            ChangedLines = [ 1L ] } ]

    let result = computeDiffCoverage "cov.info" cm hunks [] 0.0
    Assert.Equal(1, result.Partial)
    Assert.Equal(0, result.Covered)

[<Fact>]
let ``computeDiffCoverage passes at exactly the threshold`` () =
    let cm: CoverageMap =
        Map.ofList [ "a.fs", Map.ofList [ 1L, { HitCount = 1L; Branches = [] } ] ]

    let hunks =
        [ { FilePath = "a.fs"
            ChangedLines = [ 1L ] } ]

    let result = computeDiffCoverage "cov.info" cm hunks [] 100.0
    Assert.True(result.Passed)

[<Fact>]
let ``computeDiffCoverage a zero threshold always passes`` () =
    let cm: CoverageMap =
        Map.ofList [ "a.fs", Map.ofList [ 1L, { HitCount = 0L; Branches = [] } ] ]

    let hunks =
        [ { FilePath = "a.fs"
            ChangedLines = [ 1L ] } ]

    let result = computeDiffCoverage "cov.info" cm hunks [] 0.0
    Assert.True(result.Passed)

[<Fact>]
let ``computeDiffCoverage populates per-file results only for files with executable lines`` () =
    let cm: CoverageMap =
        Map.ofList
            [ "a.fs", Map.ofList [ 1L, { HitCount = 1L; Branches = [] } ]
              "b.fs", Map.ofList [] ]

    let hunks =
        [ { FilePath = "a.fs"
            ChangedLines = [ 1L ] }
          { FilePath = "b.fs"
            ChangedLines = [ 1L ] } ]

    let result = computeDiffCoverage "cov.info" cm hunks [] 0.0
    Assert.Equal(1, List.length result.Files)
    Assert.Equal("a.fs", result.Files.[0].Path)

// ---- mergeCoverageMaps ----

[<Fact>]
let ``mergeCoverageMaps takes the max hit count per line`` () =
    let a: CoverageMap =
        Map.ofList [ "a.go", Map.ofList [ 10L, { HitCount = 1L; Branches = [] } ] ]

    let b: CoverageMap =
        Map.ofList [ "a.go", Map.ofList [ 10L, { HitCount = 5L; Branches = [] } ] ]

    let merged = mergeCoverageMaps [ a; b ]
    Assert.Equal(5L, merged.["a.go"].[10L].HitCount)

[<Fact>]
let ``mergeCoverageMaps unions files across maps`` () =
    let a: CoverageMap =
        Map.ofList [ "a.go", Map.ofList [ 1L, { HitCount = 1L; Branches = [] } ] ]

    let b: CoverageMap =
        Map.ofList [ "b.go", Map.ofList [ 2L, { HitCount = 1L; Branches = [] } ] ]

    let merged = mergeCoverageMaps [ a; b ]
    Assert.Equal(2, merged.Count)

[<Fact>]
let ``mergeCoverageMaps merges branches taking the max per block-branch key`` () =
    let a: CoverageMap =
        Map.ofList
            [ "a.go",
              Map.ofList
                  [ 1L,
                    { HitCount = 1L
                      Branches =
                        [ { BlockId = 0L
                            BranchId = 0L
                            HitCount = 1L } ] } ] ]

    let b: CoverageMap =
        Map.ofList
            [ "a.go",
              Map.ofList
                  [ 1L,
                    { HitCount = 1L
                      Branches =
                        [ { BlockId = 0L
                            BranchId = 0L
                            HitCount = 3L } ] } ] ]

    let merged = mergeCoverageMaps [ a; b ]
    let branches = merged.["a.go"].[1L].Branches
    Assert.Equal(1, List.length branches)
    Assert.Equal(3L, branches.[0].HitCount)

[<Fact>]
let ``mergeCoverageMaps of an empty list produces an empty map`` () = Assert.Empty(mergeCoverageMaps [])

// ---- formatLcovString ----

[<Fact>]
let ``formatLcovString includes TN, SF, DA, and end_of_record`` () =
    let cm: CoverageMap =
        Map.ofList [ "a.go", Map.ofList [ 10L, { HitCount = 2L; Branches = [] } ] ]

    let s = formatLcovString cm
    Assert.Contains("TN:\n", s)
    Assert.Contains("SF:a.go", s)
    Assert.Contains("DA:10,2", s)
    Assert.Contains("end_of_record", s)

[<Fact>]
let ``formatLcovString emits a BRDA record for each branch`` () =
    let cm: CoverageMap =
        Map.ofList
            [ "a.go",
              Map.ofList
                  [ 10L,
                    { HitCount = 2L
                      Branches =
                        [ { BlockId = 1L
                            BranchId = 2L
                            HitCount = 3L } ] } ] ]

    let s = formatLcovString cm
    Assert.Contains("BRDA:10,1,2,3", s)

// ---- writeLcov ----

[<Fact>]
let ``writeLcov writes the formatted LCOV text to disk`` () =
    let path = Path.GetTempFileName()

    let cm: CoverageMap =
        Map.ofList [ "a.go", Map.ofList [ 1L, { HitCount = 3L; Branches = [] } ] ]

    writeLcov path cm
    let content = File.ReadAllText(path)
    Assert.Contains("DA:1,3", content)

// ---- resultFromCoverageMap ----

[<Fact>]
let ``resultFromCoverageMap computes covered, missed, and pct`` () =
    let cm: CoverageMap =
        Map.ofList [ "a.go", Map.ofList [ 1L, { HitCount = 1L; Branches = [] }; 2L, { HitCount = 0L; Branches = [] } ] ]

    let result = resultFromCoverageMap cm 50.0
    Assert.Equal(1, result.Covered)
    Assert.Equal(1, result.Missed)
    Assert.True(abs (result.Pct - 50.0) < 1e-9)
    Assert.True(result.Passed)

[<Fact>]
let ``resultFromCoverageMap treats a covered line with a missed branch as partial`` () =
    let cm: CoverageMap =
        Map.ofList
            [ "a.go",
              Map.ofList
                  [ 1L,
                    { HitCount = 1L
                      Branches =
                        [ { BlockId = 0L
                            BranchId = 0L
                            HitCount = 0L } ] } ] ]

    let result = resultFromCoverageMap cm 50.0
    Assert.Equal(1, result.Partial)
    Assert.Equal(0, result.Covered)

[<Fact>]
let ``resultFromCoverageMap fails when pct is below threshold`` () =
    let cm: CoverageMap =
        Map.ofList [ "a.go", Map.ofList [ 1L, { HitCount = 0L; Branches = [] } ] ]

    let result = resultFromCoverageMap cm 90.0
    Assert.False(result.Passed)

[<Fact>]
let ``resultFromCoverageMap of an empty map reports 100 percent`` () =
    let result = resultFromCoverageMap Map.empty 100.0
    Assert.Equal(100.0, result.Pct)
    Assert.Equal(0, result.Total)
    Assert.True(result.Passed)

// ---- toCoverageMapLcov ----

[<Fact>]
let ``toCoverageMapLcov reads DA lines into the coverage map`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "SF:src/foo.fs\nDA:10,5\nDA:11,0\nend_of_record\n")
    let cm = toCoverageMapLcov path
    Assert.Equal(5L, cm.["src/foo.fs"].[10L].HitCount)
    Assert.Equal(0L, cm.["src/foo.fs"].[11L].HitCount)

[<Fact>]
let ``toCoverageMapLcov keeps the max count for a duplicate DA line`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "SF:src/foo.fs\nDA:10,3\nDA:10,7\nDA:10,5\nend_of_record\n")
    let cm = toCoverageMapLcov path
    Assert.Equal(7L, cm.["src/foo.fs"].[10L].HitCount)

[<Fact>]
let ``toCoverageMapLcov attaches BRDA branches to their DA line`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "SF:src/foo.fs\nDA:10,3\nBRDA:10,0,0,3\nBRDA:10,0,1,-\nend_of_record\n")
    let cm = toCoverageMapLcov path
    let branches = cm.["src/foo.fs"].[10L].Branches
    Assert.Equal(2, List.length branches)
    Assert.Equal(3L, branches.[0].HitCount)
    Assert.Equal(0L, branches.[1].HitCount) // "-" parses to 0

[<Fact>]
let ``toCoverageMapLcov derives the hit count of a BRDA-only line from its branches`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "SF:src/foo.fs\nBRDA:10,0,0,3\nBRDA:10,0,1,7\nend_of_record\n")
    let cm = toCoverageMapLcov path
    Assert.Equal(3L, cm.["src/foo.fs"].[10L].HitCount)
    Assert.Equal(2, List.length cm.["src/foo.fs"].[10L].Branches)

[<Fact>]
let ``toCoverageMapLcov handles multiple end_of_record sections`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "SF:a.fs\nDA:1,1\nend_of_record\nSF:b.fs\nDA:1,0\nend_of_record\n")
    let cm = toCoverageMapLcov path
    Assert.Equal(2, cm.Count)
    Assert.Equal(1L, cm.["a.fs"].[1L].HitCount)
    Assert.Equal(0L, cm.["b.fs"].[1L].HitCount)

[<Fact>]
let ``toCoverageMapLcov round-trips through mergeCoverageMaps and writeLcov`` () =
    let pathA = Path.GetTempFileName()
    let pathB = Path.GetTempFileName()
    let outPath = Path.GetTempFileName()
    File.WriteAllText(pathA, "SF:a.fs\nDA:1,1\nend_of_record\n")
    File.WriteAllText(pathB, "SF:b.fs\nDA:1,0\nend_of_record\n")
    let merged = mergeCoverageMaps [ toCoverageMapLcov pathA; toCoverageMapLcov pathB ]
    writeLcov outPath merged
    let content = File.ReadAllText(outPath)
    Assert.Contains("SF:a.fs", content)
    Assert.Contains("SF:b.fs", content)
    Assert.Contains("end_of_record", content)
