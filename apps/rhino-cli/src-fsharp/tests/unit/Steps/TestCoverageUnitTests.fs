/// Plain xunit tests for `RhinoCli.Application.TestCoverage`'s pure helpers
/// that have no dedicated Gherkin scenario, or are exercised only
/// indirectly there — mirrors the rationale `DoctorUnitTests.fs`'s module
/// doc comment states for its own split from `DoctorSteps.fs`. Ported from
/// `apps/rhino-cli/src/application/testcoverage/exclude.rs`'s and
/// `apps/rhino-cli/src/application/testcoverage/merge.rs`'s
/// `#[cfg(test)] mod tests`.
module RhinoCli.Tests.Unit.Steps.TestCoverageUnitTests

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
