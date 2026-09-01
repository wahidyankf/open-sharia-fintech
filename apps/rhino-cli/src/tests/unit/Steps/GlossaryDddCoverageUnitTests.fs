/// Plain xunit tests calling `RhinoCli.Application.Glossary`/`Ddd`'s public
/// helper functions directly with synthetic content. These fixtures cover
/// content-dependent parser branches without altering either repository's
/// real glossary or bounded-context registry.
module RhinoCli.Tests.Unit.Steps.GlossaryDddCoverageUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Domain.Types
open RhinoCli.Application

let private newTempDir () =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-glossary-ddd-cov-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private writeFile (root: string) (relativePath: string) (content: string) =
    let full = Path.Combine(root, relativePath)
    Directory.CreateDirectory(Path.GetDirectoryName full) |> ignore
    File.WriteAllText(full, content)

// ---------------------------------------------------------------------------
// Glossary.parseContent — forbidden-synonyms bullet parsing (both separator
// forms) and the generic "## " section close
// ---------------------------------------------------------------------------

[<Fact>]
let ``parseContent parses forbidden synonyms with both em-dash and hyphen separators and closes the section on the next heading``
    ()
    =
    let content =
        "**Bounded context**: sample\n"
        + "**Maintainer**: me\n"
        + "**Last reviewed**: 2026-01-01\n"
        + "\n"
        + "## Term index\n"
        + "\n"
        + "| Term | Code identifier(s) | Used in features |\n"
        + "| --- | --- | --- |\n"
        + "| Widget | `Widget` | sub/dir/widget.feature |\n"
        + "\n"
        + "## Forbidden synonyms\n"
        + "\n"
        + "- \"Thingy\" — use Widget instead\n"
        + "- \"Doohickey\" - use Gadget instead\n"
        + "\n"
        + "## Notes\n"
        + "\n"
        + "Some other content that must not be parsed as a bullet.\n"

    let g = Glossary.parseContent "fixture.md" content

    Assert.Equal(2, g.ForbiddenSynonyms.Length)

    Assert.Contains(
        g.ForbiddenSynonyms,
        (fun (f: Glossary.Forbidden) -> f.Term = "Thingy" && f.Reason = "use Widget instead")
    )

    Assert.Contains(
        g.ForbiddenSynonyms,
        (fun (f: Glossary.Forbidden) -> f.Term = "Doohickey" && f.Reason = "use Gadget instead")
    )

// ---------------------------------------------------------------------------
// Glossary.featureRefResolves — slash-qualified and glob-qualified branches
// ---------------------------------------------------------------------------

[<Fact>]
let ``featureRefResolves resolves a slash-qualified reference against the gherkin path's parent directory`` () =
    let root = newTempDir ()
    let gherkinPath = Path.Combine(root, "specs", "apps", "foo", "gherkin")
    Directory.CreateDirectory gherkinPath |> ignore
    writeFile root "specs/apps/foo/sub/dir/thing.feature" "Feature: thing\n"

    let resolved = Glossary.featureRefResolves "sub/dir/thing.feature" [ gherkinPath ]

    Assert.True resolved

[<Fact>]
let ``featureRefResolves resolves a glob-qualified reference against files in the gherkin path`` () =
    let root = newTempDir ()
    let gherkinPath = Path.Combine(root, "gherkin")
    writeFile root "gherkin/foo.feature" "Feature: foo\n"

    let resolved = Glossary.featureRefResolves "*.feature" [ gherkinPath ]

    Assert.True resolved

// ---------------------------------------------------------------------------
// Glossary.checkForbiddenSynonyms — the forbidden-synonym self-use loop
// ---------------------------------------------------------------------------

[<Fact>]
let ``checkForbiddenSynonyms flags a forbidden term still used in the context's own code`` () =
    let root = newTempDir ()
    writeFile root "code/sample.fs" "let thingy = 1\n"

    let glossary: Glossary.Glossary =
        { Path = "fixture.md"
          Frontmatter = Map.empty
          Terms = []
          ForbiddenSynonyms =
            [ { Glossary.Forbidden.Term = "thingy"
                Reason = "use Widget instead"
                SourceLine = 1 } ]
          ParseErrors = [] }

    let findings =
        Glossary.checkForbiddenSynonyms
            "fixture.md"
            glossary
            [ Path.Combine(root, "code") ]
            [ "*.fs" ]
            []
            Severity.Blocking

    Assert.Single(findings) |> ignore
    Assert.Contains("thingy", findings.[0].Message)

// ---------------------------------------------------------------------------
// Ddd.loadRegistry — default code_lang assignment and malformed-YAML branch
// ---------------------------------------------------------------------------

[<Fact>]
let ``loadRegistry defaults an empty code_lang to ts and tsx`` () =
    let root = newTempDir ()

    writeFile
        root
        "specs/apps/fixture/ddd/bounded-contexts.yaml"
        ("version: 2\n"
         + "app: fixture\n"
         + "contexts:\n"
         + "  - name: sample\n"
         + "    code: [apps/fixture]\n"
         + "    gherkin: [specs/fixture]\n")

    let result = Ddd.loadRegistry root "fixture"

    match result with
    | Ok registry -> Assert.Equal<string list>([ "ts"; "tsx" ], registry.Contexts.[0].CodeLang)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``loadRegistry reports an error for malformed YAML`` () =
    let root = newTempDir ()
    writeFile root "specs/apps/fixture/ddd/bounded-contexts.yaml" "version: [unterminated\n"

    let result = Ddd.loadRegistry root "fixture"

    match result with
    | Error _ -> ()
    | Ok _ -> Assert.Fail "expected Error for malformed YAML"
