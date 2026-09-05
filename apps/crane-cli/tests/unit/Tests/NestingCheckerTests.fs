module CraneCli.Tests.Unit.Tests.NestingCheckerTests

open Xunit
open CraneCore.Logic.NestingChecker

[<Fact>]
let ``extractNestingLevels returns empty for plain text`` () =
    let result = extractNestingLevels "plain text no bullets"
    Assert.Empty(result)

[<Fact>]
let ``extractNestingLevels extracts level-1 bullets`` () =
    let result = extractNestingLevels "- item one\n- item two"
    Assert.Equal(2, result.Length)
    Assert.Equal(1, result.[0].Level)

[<Fact>]
let ``checkNesting returns empty for matching single-level lists`` () =
    let pdfText = "- item one\n- item two"
    let mdText = "- item one\n- item two"
    let result = checkNesting pdfText mdText
    Assert.Empty(result)

[<Fact>]
let ``checkNesting detects inverted nesting as HIGH`` () =
    let pdfText = "- parent\n  - child"
    let mdText = "- child\n- parent"
    let result = checkNesting pdfText mdText
    Assert.NotEmpty(result)
    let finding = result |> List.head
    Assert.Equal("HIGH", finding.Criticality)

[<Fact>]
let ``checkNesting returns MEDIUM finding for off-by-one deeper nesting`` () =
    // PDF has two-level nesting (parent at level 1, child at level 2);
    // MD has the same child pushed one level deeper (level 3 instead of 2).
    let pdfText = "- parent\n  - child"
    let mdText = "- parent\n    - child"
    let result = checkNesting pdfText mdText
    Assert.NotEmpty(result)
    Assert.Equal("MEDIUM", result.[0].Criticality)

[<Fact>]
let ``checkNesting returns empty when items match at same level`` () =
    // PDF has nested item; MD has same item at same level -> no finding
    let pdfText = "  - nested item"
    let mdText = "  - nested item"
    let result = checkNesting pdfText mdText
    Assert.Empty(result)

[<Fact>]
let ``checkNesting returns empty when pdf item not found in md`` () =
    let pdfText = "- unique item not in markdown"
    let mdText = "- completely different content"
    let result = checkNesting pdfText mdText
    Assert.Empty(result)
