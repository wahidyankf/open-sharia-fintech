/// Plain xunit tests exercising `RhinoCli.Application.Convention` behaviour
/// that has no dedicated Gherkin scenario: guard clauses, SPDX-prose
/// classification variants, GFM table-parsing edge cases, and non-BMP
/// codepoint counting. Kept separate from `ConventionSteps.fs` (which binds
/// only real, frozen feature-file scenarios) so this file can grow test
/// cases without inflating the plan's tracked Gherkin scenario count.
///
/// Fixtures below use `\uXXXX`/`\UXXXXXXXX` escapes rather than literal
/// emoji characters so this file doesn't trip the emoji-in-source-code
/// convention it tests [mirrors `emoji_audit.rs`'s own test-fixture note].
module RhinoCli.Tests.Integration.Steps.ConventionResourceTests

open System
open System.IO
open Xunit
open RhinoCli.Application.Convention

let private newTempDir () =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-convention-unit-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private writeFile (root: string) (relativePath: string) (content: string) =
    let full = Path.Combine(root, relativePath)
    Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
    File.WriteAllText(full, content)

// ---- runEmojiValidate guard clauses ----

[<Fact>]
let ``runEmojiValidate fails with a guard message when no paths are given`` () =
    let result = runEmojiValidate []
    Assert.False(result.Success)
    Assert.Contains("at least one path is required", result.Output)
    Assert.Empty(result.Findings)

[<Fact>]
let ``runEmojiValidate passes when the only path does not exist`` () =
    let missing =
        Path.Combine(Path.GetTempPath(), "rhino-cli-does-not-exist-" + Guid.NewGuid().ToString("N"))

    let result = runEmojiValidate [ missing ]
    Assert.True(result.Success)
    Assert.Empty(result.Findings)

// ---- non-BMP codepoint counting (surrogate pairs) ----

[<Fact>]
let ``a non-BMP codepoint before a flagged emoji does not shift its column`` () =
    let root = newTempDir ()

    try
        // U+1F680 (rocket) is two UTF-16 code units but one codepoint; U+2713
        // (check mark) immediately after it must still be reported at column
        // 2, not column 3, and its own codepoint is never itself flagged
        // since 0x1F680 falls inside the audited 0x1F000-0x1FFFF block too.
        writeFile root "src/example.ts" "\U0001F680\u2713\n"
        let result = runEmojiValidate [ root ]
        Assert.False(result.Success)
        let messages = result.Findings |> List.map (fun f -> f.Message)
        Assert.Contains(messages, fun m -> m.Contains(":1:1  ") && m.Contains("U+1F680"))
        Assert.Contains(messages, fun m -> m.Contains(":1:2  ") && m.Contains("U+2713"))
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``formatCodepoint renders codepoints above U+FFFF without zero-padding`` () =
    let root = newTempDir ()

    try
        writeFile root "src/example.ts" "\U0001F680\n"
        let result = runEmojiValidate [ root ]
        Assert.False(result.Success)
        Assert.Contains(result.Findings, fun f -> f.Message.Contains("U+1F680"))
    finally
        Directory.Delete(root, true)

// ---- License.classifyLine SPDX-prose variants (Rust parity —
// license_audit.rs::classify_license_line recognises the same breadth) ----

let licenseMismatchCases: obj[] list =
    [ [| "BSD 3-Clause License"; "BSD-3-Clause" |]
      [| "BSD 2-Clause License"; "BSD-2-Clause" |]
      [| "Mozilla Public License 2.0"; "MPL-2.0" |]
      [| "GNU General Public License"; "GPL" |] ]

[<Theory>]
[<MemberData(nameof licenseMismatchCases)>]
let ``license audit identifies common SPDX prose headers`` (licenseFirstLine: string) (expectedSpdx: string) =
    let root = newTempDir ()

    try
        writeFile root "apps/sample/LICENSE" (licenseFirstLine + "\n")
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"

        writeFile
            root
            "LICENSING-NOTICE.md"
            (String.concat
                "\n"
                [ "| Path | License |"
                  "| --- | --- |"
                  "| apps/sample | MIT |"
                  "| libs/other | MIT |"
                  "| specs | MIT |" ])

        let result = runLicenseValidate root
        Assert.False(result.Success)

        Assert.Contains(result.Findings, fun f -> f.Message.Contains("apps/sample") && f.Message.Contains(expectedSpdx))
    finally
        Directory.Delete(root, true)

// ---- License.audit: normalisation, ownership scoping, GFM parsing ----

[<Fact>]
let ``a LICENSING-NOTICE.md claim path normalises backticks, ./ prefix, trailing slash and backslashes`` () =
    let root = newTempDir ()

    try
        writeFile root "apps/sample/LICENSE" "MIT License\n"
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"

        // Deliberately mismatched claim so a raw, un-normalised path would
        // fail to match `apps/sample` and silently drop the finding instead
        // of reporting the mismatch below. Two backslashes in the raw GFM
        // source survive `splitMarkdownRow`'s escape handling as a single
        // literal backslash in the parsed cell.
        writeFile
            root
            "LICENSING-NOTICE.md"
            (String.concat
                "\n"
                [ "| Path | License |"
                  "| --- | --- |"
                  "| `./apps\\\\sample/` | Apache-2.0 |"
                  "| libs/other | MIT |"
                  "| specs | MIT |" ])

        let result = runLicenseValidate root
        Assert.False(result.Success)
        Assert.Contains(result.Findings, fun f -> f.Path = Some "apps/sample")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``a LICENSING-NOTICE.md claim for a nested path outside apps or libs top level is ignored`` () =
    let root = newTempDir ()

    try
        writeFile root "apps/sample/LICENSE" "MIT License\n"
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"

        // `apps/sample/nested` is not an immediate child of `apps/`, and
        // `docs` is neither `apps/`, `libs/`, nor `specs` — both claims must
        // be silently ignored rather than reported as mismatches.
        writeFile
            root
            "LICENSING-NOTICE.md"
            (String.concat
                "\n"
                [ "| Path | License |"
                  "| --- | --- |"
                  "| apps/sample | MIT |"
                  "| apps/sample/nested | Apache-2.0 |"
                  "| docs | Apache-2.0 |"
                  "| libs/other | MIT |"
                  "| specs | MIT |" ])

        let result = runLicenseValidate root
        Assert.True(result.Success)
        Assert.Empty(result.Findings)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``a claim row with an escaped pipe in a cell is split correctly`` () =
    let root = newTempDir ()

    try
        writeFile root "apps/sample/LICENSE" "MIT License\n"
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"

        // The escaped pipe inside the license cell must not be treated as a
        // column separator; if it were, `findColumns`/row-splitting would
        // desync and this mismatch would go unreported.
        writeFile
            root
            "LICENSING-NOTICE.md"
            (String.concat
                "\n"
                [ "| Path | License |"
                  "| --- | --- |"
                  @"| apps/sample | MIT \| dual |"
                  "| libs/other | MIT |"
                  "| specs | MIT |" ])

        let result = runLicenseValidate root
        Assert.False(result.Success)
        Assert.Contains(result.Findings, fun f -> f.Path = Some "apps/sample")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``a markdown table without a Path or License column contributes no claims`` () =
    let root = newTempDir ()

    try
        writeFile root "apps/sample/LICENSE" "MIT License\n"
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"

        // First table has neither a recognised header nor a claim; second
        // (real) table follows immediately, exercising the parser's
        // reset-then-reparse path across two consecutive tables.
        writeFile
            root
            "LICENSING-NOTICE.md"
            (String.concat
                "\n"
                [ "| Name | Owner |"
                  "| --- | --- |"
                  "| unrelated | someone |"
                  ""
                  "| Path | License |"
                  "| --- | --- |"
                  "| apps/sample | MIT |"
                  "| libs/other | MIT |"
                  "| specs | MIT |" ])

        let result = runLicenseValidate root
        Assert.True(result.Success)
        Assert.Empty(result.Findings)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``an empty LICENSE file is reported as unreadable`` () =
    let root = newTempDir ()

    try
        writeFile root "apps/sample/LICENSE" ""
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"
        writeFile root "LICENSING-NOTICE.md" ""

        let result = runLicenseValidate root
        Assert.False(result.Success)

        Assert.Contains(
            result.Findings,
            fun f -> f.Message.Contains("unreadable-license") && f.Path = Some "apps/sample"
        )
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``LICENSING-NOTICE.md missing entirely yields zero claims without error`` () =
    let root = newTempDir ()

    try
        writeFile root "apps/sample/LICENSE" "MIT License\n"
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"

        let result = runLicenseValidate root
        Assert.True(result.Success)
        Assert.Empty(result.Findings)
    finally
        Directory.Delete(root, true)

// ---- runConventionAudit: aggregate success path ----

[<Fact>]
let ``runConventionAudit passes when every validator passes`` () =
    let root = newTempDir ()

    try
        writeFile root "apps/sample/LICENSE" "MIT License\n"
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"
        writeFile root "apps/sample/index.ts" "const ok = true\n"

        let result = runConventionAudit root []
        Assert.True(result.Success)
        Assert.Empty(result.Findings)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``runConventionAudit skips a named validator`` () =
    let root = newTempDir ()

    try
        // No LICENSE files at all would fail the license validator; skipping
        // it must still let the (passing) emoji validator's result through.
        writeFile root "apps/sample/index.ts" "const ok = true\n"

        let result = runConventionAudit root [ "license" ]
        Assert.True(result.Success)
    finally
        Directory.Delete(root, true)

// ---- Additional coverage-gap-closing tests: classifyLine's
// SPDX-License-Identifier header form, splitMarkdownRow's missing-trailing-
// pipe tolerance, parseLicensingNotice's header-at-EOF/empty-cell/short-row
// skip branches, License.audit's mismatch computation for a claimed
// directory with no identified LICENSE at all, and runAuditMember's
// emoji-failure error branch. ----

[<Fact>]
let ``license audit strips the SPDX-License-Identifier prefix when classifying a LICENSE file`` () =
    let root = newTempDir ()

    try
        writeFile root "apps/sample/LICENSE" "SPDX-License-Identifier: MIT\n"
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"

        writeFile
            root
            "LICENSING-NOTICE.md"
            (String.concat
                "\n"
                [ "| Path | License |"
                  "| --- | --- |"
                  "| apps/sample | Apache-2.0 |"
                  "| libs/other | MIT |"
                  "| specs | MIT |" ])

        let result = runLicenseValidate root
        Assert.False(result.Success)

        Assert.Contains(
            result.Findings,
            fun f -> f.Path = Some "apps/sample" && f.Message.Contains("LICENSE identifies \"MIT\"")
        )
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``a claim row missing its closing pipe is still parsed`` () =
    let root = newTempDir ()

    try
        writeFile root "apps/sample/LICENSE" "MIT License\n"
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"

        writeFile
            root
            "LICENSING-NOTICE.md"
            (String.concat
                "\n"
                [ "| Path | License |"
                  "| --- | --- |"
                  "| apps/sample | Apache-2.0"
                  "| libs/other | MIT |"
                  "| specs | MIT |" ])

        let result = runLicenseValidate root
        Assert.False(result.Success)
        Assert.Contains(result.Findings, fun f -> f.Path = Some "apps/sample")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``a pipe-prefixed line at the very end of LICENSING-NOTICE.md with no room for a separator row is ignored`` () =
    let root = newTempDir ()

    try
        writeFile root "apps/sample/LICENSE" "MIT License\n"
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"
        writeFile root "LICENSING-NOTICE.md" "some prose\n\n| Path | License |"

        let result = runLicenseValidate root
        Assert.True(result.Success)
        Assert.Empty(result.Findings)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``a claim row with an empty license cell contributes no claim`` () =
    let root = newTempDir ()

    try
        writeFile root "apps/sample/LICENSE" "MIT License\n"
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"

        writeFile
            root
            "LICENSING-NOTICE.md"
            (String.concat
                "\n"
                [ "| Path | License |"
                  "| --- | --- |"
                  "| apps/sample |  |"
                  "| libs/other | MIT |"
                  "| specs | MIT |" ])

        let result = runLicenseValidate root
        Assert.True(result.Success)
        Assert.Empty(result.Findings)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``a claim row with fewer cells than the license column index contributes no claim`` () =
    let root = newTempDir ()

    try
        writeFile root "apps/sample/LICENSE" "MIT License\n"
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"

        writeFile
            root
            "LICENSING-NOTICE.md"
            (String.concat
                "\n"
                [ "| Path | License |"
                  "| --- | --- |"
                  "| apps/sample |"
                  "| libs/other | MIT |"
                  "| specs | MIT |" ])

        let result = runLicenseValidate root
        Assert.True(result.Success)
        Assert.Empty(result.Findings)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``a claim for a directory with no LICENSE file at all produces no mismatch finding`` () =
    let root = newTempDir ()

    try
        writeFile root "libs/other/LICENSE" "MIT License\n"
        writeFile root "specs/LICENSE" "MIT License\n"
        Directory.CreateDirectory(Path.Combine(root, "apps", "nolicense")) |> ignore

        writeFile
            root
            "LICENSING-NOTICE.md"
            (String.concat
                "\n"
                [ "| Path | License |"
                  "| --- | --- |"
                  "| apps/nolicense | MIT |"
                  "| libs/other | MIT |"
                  "| specs | MIT |" ])

        let result = runLicenseValidate root
        Assert.False(result.Success)
        // Exactly the missing-license finding — no additional spdx-mismatch
        // finding, since there is no identified license to compare against.
        Assert.Equal(1, List.length result.Findings)
        Assert.Contains(result.Findings, fun f -> f.Message.Contains("missing-license"))
    finally
        Directory.Delete(root, true)
