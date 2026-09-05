module CraneCli.Tests.Unit.Tests.MermaidValidatorTests

open Xunit
open CraneCore.Logic.MermaidValidator

[<Fact>]
let ``validateBlock returns Ok for valid graph block`` () =
    let result = validateBlock "graph TD\n A-->B\n"
    Assert.Equal(Ok(), result)

[<Fact>]
let ``validateBlock returns Error for empty block`` () =
    match validateBlock "" with
    | Error _ -> ()
    | Ok() -> Assert.Fail("expected error")

[<Fact>]
let ``validateBlock returns Error for unknown diagram type`` () =
    match validateBlock "unknownType\n A-->B\n" with
    | Error msg -> Assert.Contains("unknown diagram type", msg)
    | Ok() -> Assert.Fail("expected error")

[<Fact>]
let ``validateBlock returns Error for unmatched brackets`` () =
    match validateBlock "graph TD\n A[ unclosed\n" with
    | Error msg -> Assert.Contains("unmatched brackets", msg)
    | Ok() -> Assert.Fail("expected error")

[<Fact>]
let ``extractBlocks returns empty for text without mermaid`` () =
    let result = extractBlocks "# Heading\n\nSome text"
    Assert.Empty(result)

[<Fact>]
let ``extractBlocks finds mermaid block`` () =
    let mdText = "```mermaid\ngraph TD\n A-->B\n```"
    let result = extractBlocks mdText
    Assert.Equal(1, result.Length)

[<Fact>]
let ``validateMd returns empty for valid mermaid`` () =
    let mdText = "```mermaid\ngraph TD\n A-->B\n```"
    let result = validateMd mdText
    Assert.Empty(result)

[<Fact>]
let ``validateMd returns finding for invalid mermaid`` () =
    let mdText = "```mermaid\nunknownType\n A-->B\n```"
    let result = validateMd mdText
    Assert.NotEmpty(result)
    Assert.Equal("HIGH", result.[0].Criticality)
    Assert.Equal("mermaid-syntax", result.[0].Category)

[<Fact>]
let ``validateMd returns HIGH finding mentioning bracket for unmatched bracket block`` () =
    let mdText = "```mermaid\ngraph TD\n A[ unclosed\n```"
    let result = validateMd mdText
    Assert.NotEmpty(result)
    Assert.Equal("HIGH", result.[0].Criticality)
    Assert.Contains("bracket", result.[0].Description)

[<Fact>]
let ``validateMd returns empty for all known diagram type keywords`` () =
    let types =
        [ "graph"
          "flowchart"
          "sequenceDiagram"
          "stateDiagram"
          "stateDiagram-v2"
          "classDiagram"
          "gantt"
          "pie"
          "erDiagram"
          "journey"
          "gitGraph"
          "mindmap"
          "timeline"
          "quadrantChart"
          "xychart-beta"
          "sankey-beta"
          "block-beta"
          "architecture-beta" ]

    let mdText =
        types
        |> List.map (fun t -> sprintf "```mermaid\n%s\n note text\n```" t)
        |> String.concat "\n\n"

    let result = validateMd mdText
    Assert.Empty(result)

[<Fact>]
let ``validateBlock returns Error for unmatched parentheses`` () =
    match validateBlock "graph TD\n A(unclosed\n" with
    | Error msg -> Assert.Contains("unmatched parentheses", msg)
    | Ok() -> Assert.Fail("expected error for unmatched parentheses")
