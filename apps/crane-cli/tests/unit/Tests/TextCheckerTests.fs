module CraneCli.Tests.Unit.Tests.TextCheckerTests

open Xunit
open CraneCore.Domain.Finding
open CraneCore.Logic.TextChecker

[<Fact>]
let ``Finding type has category field`` () =
    let f =
        { Category = "text-completeness"
          Criticality = "HIGH"
          Confidence = "HIGH"
          LocationPdf = None
          LocationMd = None
          Description = "test"
          PdfText = None
          FixSuggestion = None
          AutoFixable = false }

    Assert.Equal("text-completeness", f.Category)

// @covers specs/apps/crane/cli/behaviors/content/text-check.feature:Complete conversion produces no findings
[<Fact>]
let ``checkText returns empty list when all chunks present in MD`` () =
    let chunks = [ "hello world this is section one content" ]
    let mdText = "hello world this is section one content"
    let result = checkText chunks mdText
    Assert.Empty(result)

// @covers specs/apps/crane/cli/behaviors/content/text-check.feature:Missing section produces a CRITICAL finding
[<Fact>]
let ``checkText returns finding for missing chunk`` () =
    let chunks = [ "Missing section here" ]
    let mdText = "completely different content with no overlap"
    let result = checkText chunks mdText
    Assert.NotEmpty(result)
    Assert.Equal("CRITICAL", result.[0].Criticality)
    Assert.Equal("text-completeness", result.[0].Category)

// @covers specs/apps/crane/cli/behaviors/content/text-check.feature:Whitespace normalization prevents false positives
[<Fact>]
let ``checkText treats multiple consecutive spaces as equivalent via normalization`` () =
    let chunks = [ "hello    world   with  extra    spaces" ]
    let mdText = "hello world with extra spaces"
    let result = checkText chunks mdText
    Assert.Empty(result)

[<Fact>]
let ``normalize collapses whitespace`` () =
    let result = normalize "hello   world   text"
    Assert.Equal("hello world text", result)

[<Fact>]
let ``segmentIsPresent returns true for exact substring`` () =
    let found = segmentIsPresent "hello world" "hello world some more text"
    Assert.True(found)

// @covers specs/apps/crane/cli/behaviors/content/text-check.feature:Fuzzy match accepts minor OCR spelling variation
[<Fact>]
let ``segmentIsPresent handles fuzzy single-word match`` () =
    let found = segmentIsPresent "Organisation" "Organization some text"
    Assert.True(found)

[<Fact>]
let ``classifyMissing returns CRITICAL for short segments`` () =
    let result = classifyMissing "short text"
    Assert.Equal("CRITICAL", result)

[<Fact>]
let ``classifyMissing returns HIGH for long segments`` () =
    let longText = System.String('a', 60)
    let result = classifyMissing longText
    Assert.Equal("HIGH", result)

[<Fact>]
let ``computeSimilarity returns 1.0 for identical strings`` () =
    let result = computeSimilarity "hello world" "hello world"
    Assert.Equal(1.0, result)

[<Fact>]
let ``computeSimilarity returns less than 1.0 for different strings`` () =
    let result = computeSimilarity "hello" "world"
    Assert.True(result < 1.0)

[<Fact>]
let ``checkText skips whitespace-only chunks`` () =
    let chunks = [ "   "; "\t\n"; "actual content not in md" ]
    let mdText = "completely different text here"
    // Only the non-whitespace chunk should produce a finding
    let result = checkText chunks mdText
    Assert.Equal(1, result.Length)
