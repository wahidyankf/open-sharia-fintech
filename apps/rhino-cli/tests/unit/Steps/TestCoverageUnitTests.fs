/// Plain xunit tests for `RhinoCli.Application.TestCoverage`'s pure helpers
/// that have no dedicated Gherkin scenario, or are exercised only
/// indirectly there — mirrors the rationale `DoctorUnitTests.fs`'s module
/// doc comment states for its own split from `DoctorSteps.fs`. Ported from
/// `apps/rhino-cli/src/application/testcoverage/exclude.rs`'s,
/// `apps/rhino-cli/src/application/testcoverage/merge.rs`'s,
/// `apps/rhino-cli/src/application/testcoverage/detect.rs`'s,
/// `apps/rhino-cli/src/application/testcoverage/go_coverage.rs`'s,
/// `apps/rhino-cli/src/application/testcoverage/cobertura.rs`'s, and
/// `apps/rhino-cli/src/application/testcoverage/reporter.rs`'s
/// `#[cfg(test)] mod tests`.
module RhinoCli.Tests.Unit.Steps.TestCoverageUnitTests

open System
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

// ---- formatCode ----

[<Fact>]
let ``formatCode returns the lowercase code for every format`` () =
    Assert.Equal("go", formatCode Format.Go)
    Assert.Equal("lcov", formatCode Format.Lcov)
    Assert.Equal("jacoco", formatCode Format.Jacoco)
    Assert.Equal("cobertura", formatCode Format.Cobertura)
    Assert.Equal("diff", formatCode Format.Diff)

// ---- detectFormat ----

[<Fact>]
let ``detectFormat recognizes lcov by filename`` () =
    Assert.Equal(Format.Lcov, detectFormat "/tmp/coverage.info")
    Assert.Equal(Format.Lcov, detectFormat "/tmp/lcov-report.dat")

[<Fact>]
let ``detectFormat recognizes jacoco and cobertura xml by filename`` () =
    Assert.Equal(Format.Jacoco, detectFormat "/tmp/jacoco.xml")
    Assert.Equal(Format.Cobertura, detectFormat "/tmp/cobertura.xml")

[<Fact>]
let ``detectFormat falls back to Go when the file is missing`` () =
    Assert.Equal(Format.Go, detectFormat "/nonexistent/file")

[<Fact>]
let ``detectFormat detects go by mode preamble`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "mode: set\nfoo.go:1.1,2.2 1 1\n")
    Assert.Equal(Format.Go, detectFormat path)

[<Fact>]
let ``detectFormat detects lcov by SF or TN preamble`` () =
    let sfPath = Path.GetTempFileName()
    File.WriteAllText(sfPath, "SF:src/foo.rs\nDA:1,1\nend_of_record\n")
    Assert.Equal(Format.Lcov, detectFormat sfPath)

    let tnPath = Path.GetTempFileName()
    File.WriteAllText(tnPath, "TN:foo\nSF:bar.rs\n")
    Assert.Equal(Format.Lcov, detectFormat tnPath)

[<Fact>]
let ``detectFormat detects jacoco and cobertura by xml root element`` () =
    let jacocoPath = Path.GetTempFileName()
    File.WriteAllText(jacocoPath, "<?xml version=\"1.0\"?>\n<report>\n</report>")
    Assert.Equal(Format.Jacoco, detectFormat jacocoPath)

    let cobPath = Path.GetTempFileName()
    File.WriteAllText(cobPath, "<?xml version=\"1.0\"?>\n<coverage>\n</coverage>")
    Assert.Equal(Format.Cobertura, detectFormat cobPath)

[<Fact>]
let ``detectFormat detects the root element on the same line as the xml declaration`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "<?xml version=\"1.0\"?><report></report>")
    Assert.Equal(Format.Jacoco, detectFormat path)

[<Fact>]
let ``detectFormat skips DOCTYPE and blank lines before deciding`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "\n<!DOCTYPE html>\n<coverage>\n</coverage>")
    Assert.Equal(Format.Cobertura, detectFormat path)

[<Fact>]
let ``detectFormat falls back to Go for unrecognized content`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "unknown content\n")
    Assert.Equal(Format.Go, detectFormat path)

// ---- computeGoResult ----

[<Fact>]
let ``computeGoResult reports file not found for a missing cover.out`` () =
    match computeGoResult "/nonexistent/cover.out" 50.0 with
    | Error message -> Assert.Contains("file not found", message)
    | Ok _ -> failwith "expected an error"

[<Fact>]
let ``computeGoResult classifies a partial line as neither covered nor missed`` () =
    let path = Path.GetTempFileName()

    File.WriteAllText(path, "mode: set\nexample.com/proj/foo.go:3.1,3.2 1 1\nexample.com/proj/foo.go:3.1,3.2 1 0\n")

    let result = computeGoResult path 50.0 |> Result.defaultWith (fun e -> failwith e)
    Assert.Equal(1, result.Partial)
    Assert.Equal(0, result.Covered)

[<Fact>]
let ``computeGoResult skips non-code lines when the source file is available`` () =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-testcoverage-go-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    File.WriteAllText(Path.Combine(dir, "foo.go"), "package foo\n}\nfunc Foo() {}\n")
    let coverPath = Path.Combine(dir, "cover.out")
    File.WriteAllText(coverPath, "mode: set\nfoo.go:2.1,2.2 1 0\n")

    let result =
        computeGoResult coverPath 50.0 |> Result.defaultWith (fun e -> failwith e)

    Assert.Equal(0, result.Total)
    Assert.True(result.Passed)

// ---- computeCoberturaResult / parseBranchCoverage ----

[<Fact>]
let ``computeCoberturaResult reports file not found for a missing file`` () =
    match computeCoberturaResult "/nonexistent/cob.xml" 50.0 with
    | Error message -> Assert.Contains("file not found", message)
    | Ok _ -> failwith "expected an error"

[<Fact>]
let ``computeCoberturaResult reports invalid xml for malformed content`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "not xml at all <<<")

    match computeCoberturaResult path 50.0 with
    | Error message -> Assert.Contains("invalid Cobertura XML", message)
    | Ok _ -> failwith "expected an error"

[<Fact>]
let ``computeCoberturaResult treats full branch coverage as covered`` () =
    let path = Path.GetTempFileName()

    File.WriteAllText(
        path,
        "<?xml version=\"1.0\"?><coverage><packages><package name=\"pkg\"><classes><class filename=\"src/foo.py\"><lines><line number=\"10\" hits=\"5\" branch=\"true\" condition-coverage=\"100% (2/2)\"/></lines></class></classes></package></packages></coverage>"
    )

    let result =
        computeCoberturaResult path 50.0 |> Result.defaultWith (fun e -> failwith e)

    Assert.Equal(1, result.Covered)
    Assert.Equal(0, result.Partial)

[<Fact>]
let ``parseBranchCoverage parses a typical condition-coverage attribute`` () =
    Assert.Equal((1, 2), parseBranchCoverage "50% (1/2)")
    Assert.Equal((4, 4), parseBranchCoverage "100% (4/4)")
    Assert.Equal((0, 3), parseBranchCoverage "0% (0/3)")

[<Fact>]
let ``parseBranchCoverage returns zero for malformed input`` () =
    Assert.Equal((0, 0), parseBranchCoverage "")
    Assert.Equal((0, 0), parseBranchCoverage "50%")
    Assert.Equal((0, 0), parseBranchCoverage "(invalid)")

// ---- applyExclude ----

let private sampleCoverageResult: CoverageResult =
    { File = "x"
      Format = Format.Go
      Covered = 10
      Partial = 0
      Missed = 5
      Total = 15
      Pct = 66.67
      Threshold = 80.0
      Passed = false
      Files =
        [ { Path = "src/test_mock.rs"
            Covered = 0
            Partial = 0
            Missed = 5
            Total = 5
            Pct = 0.0 }
          { Path = "src/real.rs"
            Covered = 10
            Partial = 0
            Missed = 0
            Total = 10
            Pct = 100.0 } ] }

[<Fact>]
let ``applyExclude drops matching files and recomputes aggregate counts`` () =
    let result = applyExclude [ "src/test_*.rs" ] sampleCoverageResult
    Assert.Equal(1, List.length result.Files)
    Assert.Equal("src/real.rs", result.Files.[0].Path)
    Assert.Equal(10, result.Covered)
    Assert.Equal(0, result.Missed)
    Assert.Equal(10, result.Total)
    Assert.True(abs (result.Pct - 100.0) < 0.001)
    Assert.True(result.Passed)

[<Fact>]
let ``applyExclude with no patterns returns the result unchanged`` () =
    let unchanged = applyExclude [] sampleCoverageResult
    Assert.Equal(sampleCoverageResult.Covered, unchanged.Covered)
    Assert.Equal(sampleCoverageResult.Total, unchanged.Total)
    Assert.Equal(2, List.length unchanged.Files)

// ---- reporter: filterAndSortFiles / formatText / formatTextPerFile / formatJson ----

[<Fact>]
let ``filterAndSortFiles sorts ascending by percentage`` () =
    let files =
        [ { Path = "a.rs"
            Covered = 0
            Partial = 0
            Missed = 0
            Total = 0
            Pct = 80.0 }
          { Path = "b.rs"
            Covered = 0
            Partial = 0
            Missed = 0
            Total = 0
            Pct = 50.0 }
          { Path = "c.rs"
            Covered = 0
            Partial = 0
            Missed = 0
            Total = 0
            Pct = 95.0 } ]

    let sorted = filterAndSortFiles files 0.0
    Assert.Equal("b.rs", sorted.[0].Path)
    Assert.Equal("a.rs", sorted.[1].Path)
    Assert.Equal("c.rs", sorted.[2].Path)

[<Fact>]
let ``filterAndSortFiles excludes files at or above belowThreshold`` () =
    let files =
        [ { Path = "low.rs"
            Covered = 0
            Partial = 0
            Missed = 0
            Total = 0
            Pct = 70.0 }
          { Path = "high.rs"
            Covered = 0
            Partial = 0
            Missed = 0
            Total = 0
            Pct = 95.0 } ]

    let filtered = filterAndSortFiles files 80.0
    Assert.Equal(1, List.length filtered)
    Assert.Equal("low.rs", filtered.[0].Path)

[<Fact>]
let ``formatText matches the exact Go-style pass string`` () =
    let r =
        { File = "apps/rhino-cli/cover.out"
          Format = Format.Go
          Covered = 2411
          Partial = 141
          Missed = 249
          Total = 2801
          Pct = 86.08
          Threshold = 85.0
          Passed = true
          Files = [] }

    Assert.Equal(
        "Line coverage: 86.08% (2411 covered, 141 partial, 249 missed, 2801 total)\nPASS: 86.08% >= 85% threshold\n",
        formatText r
    )

[<Fact>]
let ``formatText renders FAIL when the result did not pass`` () =
    let r =
        { File = "x"
          Format = Format.Go
          Covered = 0
          Partial = 0
          Missed = 1
          Total = 1
          Pct = 0.0
          Threshold = 85.0
          Passed = false
          Files = [] }

    Assert.Contains("FAIL: 0.00% < 85% threshold", formatText r)

[<Fact>]
let ``formatTextPerFile reports no files when the list is empty`` () =
    let r =
        { File = "x"
          Format = Format.Go
          Covered = 0
          Partial = 0
          Missed = 0
          Total = 0
          Pct = 100.0
          Threshold = 0.0
          Passed = true
          Files = [] }

    Assert.Equal("No files to report.\n", formatTextPerFile r 0.0)

[<Fact>]
let ``formatJson reports success status and omits empty files`` () =
    let r =
        { File = "cover.out"
          Format = Format.Go
          Covered = 1
          Partial = 0
          Missed = 0
          Total = 1
          Pct = 100.0
          Threshold = 85.0
          Passed = true
          Files = [] }

    let json = formatJson r false 0.0
    use doc = System.Text.Json.JsonDocument.Parse(json)
    let root = doc.RootElement
    let mutable filesElement = Unchecked.defaultof<System.Text.Json.JsonElement>
    Assert.Equal("success", root.GetProperty("status").GetString())
    Assert.Equal("go", root.GetProperty("format").GetString())
    Assert.Equal(100, root.GetProperty("pct").GetInt32())
    Assert.False(root.TryGetProperty("files", &filesElement))

// ---- validate ----

[<Fact>]
let ``validate rejects jacoco coverage files`` () =
    let path = Path.GetTempFileName() + ".xml"
    File.WriteAllText(path, "<?xml version=\"1.0\"?><report jacoco=\"true\"></report>")

    let opts: ValidateOptions =
        { CoverageFile = path
          Threshold = 50.0
          PerFile = false
          BelowThreshold = 0.0
          Exclude = []
          Json = false
          Markdown = false }

    match validate opts with
    | Error message -> Assert.Contains("jacoco", message)
    | Ok _ -> failwith "expected jacoco to be rejected"

[<Fact>]
let ``validate reports file not found for a missing lcov file`` () =
    let opts: ValidateOptions =
        { CoverageFile = "/nonexistent/coverage.info"
          Threshold = 50.0
          PerFile = false
          BelowThreshold = 0.0
          Exclude = []
          Json = false
          Markdown = false }

    match validate opts with
    | Error message -> Assert.Contains("not found", message)
    | Ok _ -> failwith "expected an error"

// ---- goFilepathMatch: name-exhausted edge cases ----

[<Fact>]
let ``goFilepathMatch fails a question-mark pattern when the name is exhausted`` () =
    Assert.False(matchesAnyExcludePattern "a" [ "a?" ])

[<Fact>]
let ``goFilepathMatch fails a character-class pattern when the name is exhausted`` () =
    Assert.False(matchesAnyExcludePattern "a" [ "a[bc]" ])

// ---- toCoverageMapLcov: malformed DA/BRDA records ----

[<Fact>]
let ``toCoverageMapLcov ignores malformed DA and BRDA records`` () =
    let path = Path.GetTempFileName()

    File.WriteAllText(
        path,
        "SF:src/foo.fs\nDA:5\nDA:abc,5\nDA:10,5\nBRDA:10,0,0\nBRDA:xyz,0,0,1\nBRDA:10,0,0,weird\nend_of_record\n"
    )

    let cm = toCoverageMapLcov path

    Assert.Equal(5L, cm.["src/foo.fs"].[10L].HitCount)
    Assert.Equal(1, List.length cm.["src/foo.fs"].[10L].Branches)
    Assert.Equal(0L, cm.["src/foo.fs"].[10L].Branches.[0].HitCount)
    Assert.False(cm.["src/foo.fs"] |> Map.containsKey 5L)

// ---- detectFormat: xml-declaration and blank-content edge cases ----

[<Fact>]
let ``detectFormat falls back to Go for a completely empty file`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "")
    Assert.Equal(Format.Go, detectFormat path)

[<Fact>]
let ``detectFormat resumes scanning when the xml declaration is split across lines`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "<?xml\n<coverage></coverage>")
    Assert.Equal(Format.Cobertura, detectFormat path)

[<Fact>]
let ``detectFormat detects a coverage root on the same line as the xml declaration`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "<?xml version=\"1.0\"?><coverage></coverage>")
    Assert.Equal(Format.Cobertura, detectFormat path)

[<Fact>]
let ``detectFormat falls back to Go when the same-line xml declaration names neither root element`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "<?xml version=\"1.0\"?><foo/>")
    Assert.Equal(Format.Go, detectFormat path)

// ---- computeGoResult: module-prefix stripping, cwd resolution, real vs
// brace-only lines, malformed lines, out-of-range lines ----

[<Fact>]
let ``computeGoResult resolves a relative cover.out path against the current directory`` () =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-testcoverage-cwd-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory dir |> ignore
    File.WriteAllText(Path.Combine(dir, "cover.out"), "mode: set\nfoo.go:1.1,1.2 1 1\n")

    let original = Directory.GetCurrentDirectory()

    try
        Directory.SetCurrentDirectory dir

        let result =
            computeGoResult "cover.out" 50.0 |> Result.defaultWith (fun e -> failwith e)

        Assert.Equal(1, result.Total)
        Assert.Equal(1, result.Covered)
    finally
        Directory.SetCurrentDirectory original

[<Fact>]
let ``computeGoResult strips a matching go.mod module prefix, classifies a real code line, and ignores a malformed cover.out line``
    ()
    =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-testcoverage-modprefix-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory dir |> ignore
    File.WriteAllText(Path.Combine(dir, "go.mod"), "module example.com/proj\n\ngo 1.21\n")

    File.WriteAllText(
        Path.Combine(dir, "foo.go"),
        String.Join("\n", [ "package foo"; "func Foo() {"; "\treturn"; "}"; "" ])
    )

    let coverPath = Path.Combine(dir, "cover.out")

    File.WriteAllText(
        coverPath,
        String.Join(
            "\n",
            [ "mode: set"
              "not a valid cover.out line at all"
              "example.com/proj/foo.go:3.1,3.2 1 1"
              "example.com/proj/foo.go:4.1,4.2 1 1"
              "" ]
        )
    )

    let result =
        computeGoResult coverPath 50.0 |> Result.defaultWith (fun e -> failwith e)

    // Line 3 ("return") is real code and gets counted; line 4 ("}") is
    // brace-only and skipped — proving the module prefix was correctly
    // stripped so the real source file was found at all, and the malformed
    // line above did not derail parsing.
    Assert.Equal(1, result.Total)
    Assert.Equal(1, result.Covered)

[<Fact>]
let ``computeGoResult skips a covered block whose line number is beyond the resolved source file`` () =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-testcoverage-outofrange-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory dir |> ignore
    File.WriteAllText(Path.Combine(dir, "foo.go"), "package foo\n")

    let coverPath = Path.Combine(dir, "cover.out")
    File.WriteAllText(coverPath, "mode: set\nfoo.go:5.1,5.2 1 1\n")

    let result =
        computeGoResult coverPath 50.0 |> Result.defaultWith (fun e -> failwith e)

    Assert.Equal(0, result.Total)

// ---- parseBranchCoverage: numeric-but-unparsable fraction parts ----

[<Fact>]
let ``parseBranchCoverage returns zero when the fraction has a slash but non-numeric parts`` () =
    Assert.Equal((0, 0), parseBranchCoverage "50% (a/b)")

// ---- computeCoberturaResult: missing/non-numeric hits, empty report ----

[<Fact>]
let ``computeCoberturaResult treats a missing or non-numeric hits attribute as zero`` () =
    let path = Path.GetTempFileName()

    File.WriteAllText(
        path,
        "<?xml version=\"1.0\"?><coverage><packages><package name=\"pkg\"><classes>"
        + "<class filename=\"src/a.py\"><lines><line number=\"1\"/></lines></class>"
        + "<class filename=\"src/b.py\"><lines><line number=\"1\" hits=\"notanumber\"/></lines></class>"
        + "</classes></package></packages></coverage>"
    )

    let result =
        computeCoberturaResult path 50.0 |> Result.defaultWith (fun e -> failwith e)

    Assert.Equal(0, result.Covered)
    Assert.Equal(2, result.Missed)

[<Fact>]
let ``computeCoberturaResult of a report with no line entries reports 100 percent`` () =
    let path = Path.GetTempFileName()
    File.WriteAllText(path, "<?xml version=\"1.0\"?><coverage><packages></packages></coverage>")

    let result =
        computeCoberturaResult path 50.0 |> Result.defaultWith (fun e -> failwith e)

    Assert.Equal(100.0, result.Pct)
    Assert.Equal(0, result.Total)

// ---- applyExclude: fully-excluded result ----

[<Fact>]
let ``applyExclude of a fully-excluded result reports 100 percent`` () =
    let result = applyExclude [ "*" ] sampleCoverageResult
    Assert.Empty(result.Files)
    Assert.Equal(0, result.Total)
    Assert.Equal(100.0, result.Pct)

// ---- formatJson / formatMarkdown: fractional percentage, per-file breakdown ----

[<Fact>]
let ``formatJson renders a fractional percentage and a per-file breakdown`` () =
    let r =
        { File = "cover.out"
          Format = Format.Go
          Covered = 5
          Partial = 0
          Missed = 1
          Total = 6
          Pct = 83.33
          Threshold = 50.0
          Passed = true
          Files =
            [ { Path = "a.go"
                Covered = 5
                Partial = 0
                Missed = 1
                Total = 6
                Pct = 83.33 } ] }

    let json = formatJson r true 0.0
    use doc = System.Text.Json.JsonDocument.Parse(json)
    let root = doc.RootElement

    Assert.Equal(83.33, root.GetProperty("pct").GetDouble())
    let files = root.GetProperty("files")
    Assert.Equal(1, files.GetArrayLength())
    let firstFile = files.EnumerateArray() |> Seq.head
    Assert.Equal("a.go", firstFile.GetProperty("path").GetString())

[<Fact>]
let ``formatMarkdown includes a per-file breakdown table`` () =
    let r =
        { File = "cover.out"
          Format = Format.Go
          Covered = 5
          Partial = 0
          Missed = 1
          Total = 6
          Pct = 83.33
          Threshold = 50.0
          Passed = true
          Files =
            [ { Path = "a.go"
                Covered = 5
                Partial = 0
                Missed = 1
                Total = 6
                Pct = 83.33 } ] }

    let markdown = formatMarkdown r true 0.0

    Assert.Contains("### Per-File Breakdown", markdown)
    Assert.Contains("a.go", markdown)
