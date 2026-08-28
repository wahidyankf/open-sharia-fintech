/// Renders `RhinoCli.Application.Convention` results into the exact
/// text/JSON/markdown shapes the Rust CLI layer emits
/// [Repo-grounded — `apps/rhino-cli/src/commands/convention_validate_emoji.rs`,
/// `.../convention_validate_license.rs`]. Kept in `RhinoCli.Cli` rather than
/// `RhinoCli.Application` because the Rust source draws the same line: the
/// shared `Finding` record covers what the *application* layer needs
/// (severity, message, path), while these three per-field JSON envelopes are
/// a CLI-output concern specific to each validator, mirroring Rust's
/// distinct `EmojiFinding`/`LicenseFinding` structs.
module RhinoCli.Cli.Formatters

open System
open System.Text.Json
open System.Text.Json.Serialization
open System.Text.Encodings.Web
open System.Text.RegularExpressions
open RhinoCli.Domain.Types
open RhinoCli.Application

let private jsonOptions =
    let opts = JsonSerializerOptions()
    opts.WriteIndented <- true
    opts.Encoder <- JavaScriptEncoder.UnsafeRelaxedJsonEscaping
    opts

/// One emoji finding shaped for JSON, mirroring Rust's `FindingJson`.
type EmojiFindingJson =
    { file: string
      line: int
      column: int
      codepoint: string
      severity: string }

type EmojiEnvelope =
    { schema: string
      status: string
      result: EmojiFindingJson list }

type LicenseFindingJson =
    { path: string
      kind: string
      message: string }

type LicenseInnerResult =
    { total_findings: int
      findings: LicenseFindingJson list }

type LicenseEnvelope =
    { schema: string
      status: string
      result: LicenseInnerResult }

let private emojiMessageRe =
    Regex(@"^(.*):(\d+):(\d+)  \[(\w+)\]  (.+)$", RegexOptions.Compiled)

/// Recovers `RhinoCli.Application.Convention.Emoji`'s per-finding fields
/// (file/line/column/severity/codepoint) from its combined `Finding.Message`
/// string, which `Emoji.scanFileRaw` builds as
/// `"{file}:{line}:{column}  [{severity}]  {codepoint}"`.
let toEmojiFindingJson (f: Finding) : EmojiFindingJson =
    let m = emojiMessageRe.Match(f.Message)

    if not m.Success then
        failwithf "malformed emoji finding message: %s" f.Message

    { file = m.Groups.[1].Value
      line = int m.Groups.[2].Value
      column = int m.Groups.[3].Value
      severity = m.Groups.[4].Value
      codepoint = m.Groups.[5].Value }

/// Recovers `RhinoCli.Application.Convention.License`'s per-finding
/// `kind`/`message` fields from its combined `Finding.Message` string, which
/// `License.audit` builds as `"[{kind}] {path} — {message}"`. `path` is read
/// from `Finding.Path` directly rather than re-parsed from the message.
let toLicenseFindingJson (f: Finding) : LicenseFindingJson =
    let msg = f.Message
    let closeBracket = msg.IndexOf("] ", StringComparison.Ordinal)

    if not (msg.StartsWith("[", StringComparison.Ordinal)) || closeBracket < 0 then
        failwithf "malformed license finding message: %s" msg

    let kind = msg.Substring(1, closeBracket - 1)
    let afterKind = msg.Substring(closeBracket + 2)
    let sepIdx = afterKind.IndexOf(" — ", StringComparison.Ordinal)

    if sepIdx < 0 then
        failwithf "malformed license finding message: %s" msg

    { path = f.Path |> Option.defaultValue ""
      kind = kind
      message = afterKind.Substring(sepIdx + 3) }

/// `EMOJI AUDIT PASSED/FAILED` text, byte-identical to
/// `convention_validate_emoji.rs::format_text`.
let emojiText (findings: Finding list) : string =
    if List.isEmpty findings then
        "EMOJI AUDIT PASSED: no emoji codepoints found in forbidden file types\n"
    else
        let header =
            sprintf "EMOJI AUDIT FAILED: %d emoji codepoint(s) found\n" (List.length findings)

        let body =
            findings |> List.map (fun f -> sprintf "  %s\n" f.Message) |> String.concat ""

        header + body

/// JSON envelope, byte-identical to
/// `convention_validate_emoji.rs::format_json`.
let emojiJson (findings: Finding list) : string =
    let status = if List.isEmpty findings then "passed" else "failed"

    let env: EmojiEnvelope =
        { schema = "rhino-cli/emoji-audit/v1"
          status = status
          result = findings |> List.map toEmojiFindingJson }

    JsonSerializer.Serialize(env, jsonOptions) + "\n"

/// GFM table, byte-identical to
/// `convention_validate_emoji.rs::format_markdown`.
let emojiMarkdown (findings: Finding list) : string =
    if List.isEmpty findings then
        "## Governance Emoji Audit\n\n**PASSED**: no emoji codepoints found in forbidden file types\n"
    else
        let header =
            sprintf "## Governance Emoji Audit\n\n**FAILED**: %d emoji codepoint(s) found\n\n" (List.length findings)

        let tableHeader =
            "| File | Line | Column | Codepoint | Severity |\n|------|------|--------|-----------|----------|\n"

        let rows =
            findings
            |> List.map toEmojiFindingJson
            |> List.map (fun f -> sprintf "| %s | %d | %d | %s | %s |\n" f.file f.line f.column f.codepoint f.severity)
            |> String.concat ""

        header + tableHeader + rows

/// `LICENSE AUDIT PASSED/FAILED` text, byte-identical to
/// `convention_validate_license.rs::format_text`.
let licenseText (findings: Finding list) : string =
    if List.isEmpty findings then
        "LICENSE AUDIT PASSED: no findings\n"
    else
        let header = sprintf "LICENSE AUDIT FAILED: %d finding(s)\n" (List.length findings)

        let body =
            findings |> List.map (fun f -> sprintf "  %s\n" f.Message) |> String.concat ""

        header + body

/// JSON envelope, byte-identical to
/// `convention_validate_license.rs::format_json`.
let licenseJson (findings: Finding list) : string =
    let status = if List.isEmpty findings then "passed" else "failed"
    let jf = findings |> List.map toLicenseFindingJson

    let inner: LicenseInnerResult =
        { total_findings = List.length findings
          findings = jf }

    let env: LicenseEnvelope =
        { schema = "rhino-cli/license-audit/v1"
          status = status
          result = inner }

    JsonSerializer.Serialize(env, jsonOptions) + "\n"

/// GFM table, byte-identical to
/// `convention_validate_license.rs::format_markdown`.
let licenseMarkdown (findings: Finding list) : string =
    let header = "## License Audit\n\n"

    if List.isEmpty findings then
        header + "**PASSED**: no findings\n"
    else
        let sub = sprintf "**FAILED**: %d finding(s)\n\n" (List.length findings)
        let tableHeader = "| Kind | Path | Message |\n| --- | --- | --- |\n"

        let rows =
            findings
            |> List.map toLicenseFindingJson
            |> List.map (fun f -> sprintf "| %s | `%s` | %s |\n" f.kind f.path f.message)
            |> String.concat ""

        header + sub + tableHeader + rows

/// Renders one validator's result in the requested `OutputFormat`, given its
/// per-format renderers — shared by the emoji and license leaf commands.
let render (format: OutputFormat) (asText: unit -> string) (asJson: unit -> string) (asMarkdown: unit -> string) =
    match format with
    | Text -> asText ()
    | Json -> asJson ()
    | Markdown -> asMarkdown ()

// ---------------------------------------------------------------------------
// md naming
// ---------------------------------------------------------------------------

type NamingFindingJson =
    { file: string
      severity: string
      message: string }

type NamingEnvelope =
    { schema: string
      status: string
      result: NamingFindingJson list }

let private toNamingJson (f: Finding) : NamingFindingJson =
    { file = f.Path |> Option.defaultValue ""
      severity = "high"
      message = f.Message }

/// `DOCS NAMING VALIDATION PASSED/FAILED` text, byte-identical to
/// `md_validate_naming.rs::format_text`.
let namingText (findings: Finding list) : string =
    if List.isEmpty findings then
        "DOCS NAMING VALIDATION PASSED: no naming violations found\n"
    else
        let header =
            sprintf "DOCS NAMING VALIDATION FAILED: %d violation(s) found\n" (List.length findings)

        let body =
            findings
            |> List.map (fun f -> sprintf "  %s  [high]  %s\n" (f.Path |> Option.defaultValue "") f.Message)
            |> String.concat ""

        header + body

let namingJson (findings: Finding list) : string =
    let status = if List.isEmpty findings then "passed" else "failed"

    let env: NamingEnvelope =
        { schema = "rhino-cli/docs-validate-naming/v1"
          status = status
          result = findings |> List.map toNamingJson }

    JsonSerializer.Serialize(env, jsonOptions) + "\n"

let namingMarkdown (findings: Finding list) : string =
    if List.isEmpty findings then
        "## Docs Filename Naming Validation\n\n**PASSED**: no naming violations found\n"
    else
        let header =
            sprintf "## Docs Filename Naming Validation\n\n**FAILED**: %d violation(s) found\n\n" (List.length findings)

        let tableHeader = "| File | Severity | Message |\n|------|----------|---------|\n"

        let rows =
            findings
            |> List.map (fun f -> sprintf "| %s | high | %s |\n" (f.Path |> Option.defaultValue "") f.Message)
            |> String.concat ""

        header + tableHeader + rows

// ---------------------------------------------------------------------------
// md heading-hierarchy
// ---------------------------------------------------------------------------

type HeadingFindingJson =
    { file: string
      line: int
      severity: string
      kind: string
      message: string }

type HeadingEnvelope =
    { schema: string
      status: string
      result: HeadingFindingJson list }

let private toHeadingJson (f: Md.HeadingFinding) : HeadingFindingJson =
    { file = f.File
      line = f.Line
      severity = f.Severity
      kind = f.Kind
      message = f.Message }

/// `DOCS HEADING HIERARCHY VALIDATION PASSED/FAILED` text, byte-identical to
/// `md_validate_heading_hierarchy.rs::format_text`.
let headingHierarchyText (findings: Md.HeadingFinding list) : string =
    if List.isEmpty findings then
        "DOCS HEADING HIERARCHY VALIDATION PASSED: no heading hierarchy violations found\n"
    else
        let header =
            sprintf "DOCS HEADING HIERARCHY VALIDATION FAILED: %d violation(s) found\n" (List.length findings)

        let body =
            findings
            |> List.map (fun f -> sprintf "  %s:%d  [%s]  [%s]  %s\n" f.File f.Line f.Severity f.Kind f.Message)
            |> String.concat ""

        header + body

let headingHierarchyJson (findings: Md.HeadingFinding list) : string =
    let status = if List.isEmpty findings then "passed" else "failed"

    let env: HeadingEnvelope =
        { schema = "rhino-cli/docs-validate-heading-hierarchy/v1"
          status = status
          result = findings |> List.map toHeadingJson }

    JsonSerializer.Serialize(env, jsonOptions) + "\n"

let headingHierarchyMarkdown (findings: Md.HeadingFinding list) : string =
    if List.isEmpty findings then
        "## Docs Heading Hierarchy Validation\n\n**PASSED**: no heading hierarchy violations found\n"
    else
        let header =
            sprintf
                "## Docs Heading Hierarchy Validation\n\n**FAILED**: %d violation(s) found\n\n"
                (List.length findings)

        let tableHeader =
            "| File | Line | Severity | Kind | Message |\n|------|------|----------|------|---------|\n"

        let rows =
            findings
            |> List.map (fun f -> sprintf "| %s | %d | %s | %s | %s |\n" f.File f.Line f.Severity f.Kind f.Message)
            |> String.concat ""

        header + tableHeader + rows

// ---------------------------------------------------------------------------
// md frontmatter (docs validate-frontmatter)
// ---------------------------------------------------------------------------

type FrontmatterFindingJson =
    { file: string
      severity: string
      kind: string
      message: string }

type FrontmatterInnerResult =
    { status: string
      count: int
      fail_count: int
      warn_count: int
      findings: FrontmatterFindingJson list }

type FrontmatterEnvelope =
    { schema: string
      status: string
      result: FrontmatterInnerResult }

/// Best-effort projection from the generic `Finding` this validator's
/// application layer returns: `Severity.Blocking`/`Advisory` map to Rust's
/// `"fail"`/`"warn"` severity strings; `kind` has no generic-`Finding`
/// counterpart and is left empty (this repository's own tree passes this
/// validator with zero findings, so the empty-envelope path below — which
/// carries no such approximation — is what shadow-diff actually exercises).
let private toFrontmatterJson (f: Finding) : FrontmatterFindingJson =
    { file = f.Path |> Option.defaultValue ""
      severity = (if f.Severity = Severity.Blocking then "fail" else "warn")
      kind = ""
      message = f.Message }

let private frontmatterFailWarnCounts (findings: Finding list) : int * int =
    let fail =
        findings |> List.filter (fun f -> f.Severity = Severity.Blocking) |> List.length

    let warn =
        findings |> List.filter (fun f -> f.Severity = Severity.Advisory) |> List.length

    fail, warn

let frontmatterText (findings: Finding list) : string =
    if List.isEmpty findings then
        "DOCS FRONTMATTER VALIDATION PASSED: no findings\n"
    else
        let failN, warnN = frontmatterFailWarnCounts findings

        let header =
            if failN > 0 then
                if warnN > 0 then
                    sprintf "DOCS FRONTMATTER VALIDATION FAILED: %d fail finding(s), %d warn finding(s)\n" failN warnN
                else
                    sprintf "DOCS FRONTMATTER VALIDATION FAILED: %d fail finding(s)\n" failN
            else
                sprintf "DOCS FRONTMATTER VALIDATION PASSED with %d warn finding(s)\n" warnN

        let body =
            findings
            |> List.map toFrontmatterJson
            |> List.map (fun f -> sprintf "  %s  [%s]  %s — %s\n" f.file f.severity f.kind f.message)
            |> String.concat ""

        header + body

let frontmatterJson (findings: Finding list) : string =
    let failN, warnN = frontmatterFailWarnCounts findings
    let status = if failN > 0 then "failed" else "passed"

    let env: FrontmatterEnvelope =
        { schema = "rhino-cli/docs-validate-frontmatter/v1"
          status = status
          result =
            { status = status
              count = List.length findings
              fail_count = failN
              warn_count = warnN
              findings = findings |> List.map toFrontmatterJson } }

    JsonSerializer.Serialize(env, jsonOptions) + "\n"

let frontmatterMarkdown (findings: Finding list) : string =
    if List.isEmpty findings then
        "## Docs Frontmatter Validation\n\n**PASSED**: no findings\n"
    else
        let failN, warnN = frontmatterFailWarnCounts findings

        let header =
            if failN > 0 then
                sprintf
                    "## Docs Frontmatter Validation\n\n**FAILED**: %d fail finding(s), %d warn finding(s)\n\n"
                    failN
                    warnN
            else
                sprintf "## Docs Frontmatter Validation\n\n**PASSED** with %d warn finding(s)\n\n" warnN

        let tableHeader =
            "| File | Severity | Kind | Message |\n|------|----------|------|---------|\n"

        let rows =
            findings
            |> List.map toFrontmatterJson
            |> List.map (fun f -> sprintf "| %s | %s | %s | %s |\n" f.file f.severity f.kind f.message)
            |> String.concat ""

        header + tableHeader + rows

// ---------------------------------------------------------------------------
// md frontmatter-dates
// ---------------------------------------------------------------------------

type FrontmatterDatesFindingJson =
    { file: string
      line: int
      severity: string
      message: string }

type FrontmatterDatesEnvelope =
    { schema: string
      status: string
      result: FrontmatterDatesFindingJson list }

let private toFrontmatterDatesJson (f: Md.FrontmatterDatesFinding) : FrontmatterDatesFindingJson =
    { file = f.File
      line = f.Line
      severity = f.Severity
      message = f.Message }

let frontmatterDatesText (findings: Md.FrontmatterDatesFinding list) : string =
    if List.isEmpty findings then
        "FRONTMATTER AUDIT PASSED: no date-metadata violations found\n"
    else
        let header =
            sprintf "FRONTMATTER AUDIT FAILED: %d violation(s) found\n" (List.length findings)

        let body =
            findings
            |> List.map (fun f -> sprintf "  %s:%d  [%s]  %s\n" f.File f.Line f.Severity f.Message)
            |> String.concat ""

        header + body

let frontmatterDatesJson (findings: Md.FrontmatterDatesFinding list) : string =
    let status = if List.isEmpty findings then "passed" else "failed"

    let env: FrontmatterDatesEnvelope =
        { schema = "rhino-cli/frontmatter-audit/v1"
          status = status
          result = findings |> List.map toFrontmatterDatesJson }

    JsonSerializer.Serialize(env, jsonOptions) + "\n"

let frontmatterDatesMarkdown (findings: Md.FrontmatterDatesFinding list) : string =
    if List.isEmpty findings then
        "## Governance Frontmatter Audit\n\n**PASSED**: no date-metadata violations found\n"
    else
        let header =
            sprintf "## Governance Frontmatter Audit\n\n**FAILED**: %d violation(s) found\n\n" (List.length findings)

        let tableHeader =
            "| File | Line | Severity | Message |\n|------|------|----------|---------|\n"

        let rows =
            findings
            |> List.map (fun f -> sprintf "| %s | %d | %s | %s |\n" f.File f.Line f.Severity f.Message)
            |> String.concat ""

        header + tableHeader + rows

// ---------------------------------------------------------------------------
// md links
// ---------------------------------------------------------------------------

let private linkCategoryOrder: string list =
    [ "Legacy prefixed paths"
      "Missing files"
      "General/other paths"
      "workflows/ paths"
      "vision/ paths"
      "conventions README"
      "broken-anchor" ]

/// `# Broken Links Report` text, byte-identical to `links.rs::format_link_text`.
let linksText (result: Md.LinkValidationResult) : string =
    if List.isEmpty result.BrokenLinks then
        "All links valid! No broken links found.\n"
    else
        let sb = Text.StringBuilder()
        sb.Append("# Broken Links Report\n\n") |> ignore

        sb.Append(sprintf "**Total broken links**: %d\n" (List.length result.BrokenLinks))
        |> ignore

        for category in linkCategoryOrder do
            match result.BrokenByCategory |> Map.tryFind category with
            | None -> ()
            | Some links when List.isEmpty links -> ()
            | Some links ->
                sb.Append(sprintf "\n## %s (%d links)\n" category (List.length links)) |> ignore

                let byFile = links |> List.groupBy (fun l -> l.SourceFile) |> List.sortBy fst

                for file, fileLinks in byFile do
                    sb.Append(sprintf "\n### %s\n\n" file) |> ignore

                    fileLinks
                    |> List.sortBy (fun l -> l.LineNumber)
                    |> List.iter (fun l -> sb.Append(sprintf "- Line %d: `%s`\n" l.LineNumber l.LinkText) |> ignore)

        sb.ToString()

type JsonBrokenLink =
    { source_file: string
      line_number: int
      link_text: string
      target_path: string }

type LinksJsonOutput =
    { status: string
      timestamp: string
      total_files: int
      total_links: int
      broken_count: int
      duration_ms: int64
      categories: Map<string, JsonBrokenLink list> }

let private toJsonBrokenLink (b: Md.BrokenLink) : JsonBrokenLink =
    { source_file = b.SourceFile
      line_number = b.LineNumber
      link_text = b.LinkText
      target_path = b.TargetPath }

/// JSON envelope byte-identical to `links.rs::format_link_json` modulo the
/// `timestamp`/`duration_ms` fields shadow-diff.sh's `mask_volatile_fields`
/// already strips before comparison.
let linksJson (result: Md.LinkValidationResult) : string =
    let status =
        if List.isEmpty result.BrokenLinks then
            "success"
        else
            "failure"

    let categories =
        result.BrokenByCategory
        |> Map.toList
        |> List.map (fun (k, v) -> k, v |> List.map toJsonBrokenLink)
        |> Map.ofList

    let out: LinksJsonOutput =
        { status = status
          timestamp = DateTimeOffset.Now.ToString("yyyy-MM-ddTHH:mm:sszzz")
          total_files = result.TotalFiles
          total_links = result.TotalLinks
          broken_count = List.length result.BrokenLinks
          duration_ms = 0L
          categories = categories }

    JsonSerializer.Serialize(out, jsonOptions)

let linksMarkdown (result: Md.LinkValidationResult) : string = linksText result

// ---------------------------------------------------------------------------
// governance word-budget
// ---------------------------------------------------------------------------

type WordBudgetFindingJson =
    { path: string
      size: uint64
      target: uint64
      warn: uint64
      fail: uint64
      severity: string
      message: string }

type WordBudgetEnvelope =
    { schema: string
      status: string
      total_findings: int
      findings: WordBudgetFindingJson list }

let private toWordBudgetJson (f: Governance.WordBudgetFinding) : WordBudgetFindingJson =
    { path = f.Path
      size = f.Size
      target = f.Target
      warn = f.Warn
      fail = f.Fail
      severity = Governance.wordBudgetSeverityLabel f.Severity
      message = f.Message }

let wordBudgetText (findings: Governance.WordBudgetFinding list) : string =
    if List.isEmpty findings then
        "WORD BUDGET: PASSED — all surfaces within budget\n"
    else
        let header = sprintf "WORD BUDGET: %d finding(s)\n" (List.length findings)

        let body =
            findings
            |> List.map (fun f ->
                let label =
                    match f.Severity with
                    | Governance.WordBudgetSeverity.Within -> "PASS"
                    | Governance.WordBudgetSeverity.Warn -> "WARN"
                    | Governance.WordBudgetSeverity.Fail -> "FAIL"

                sprintf "  [%s] %s — %s\n" label f.Path f.Message)
            |> String.concat ""

        header + body

let wordBudgetJson (findings: Governance.WordBudgetFinding list) : string =
    let hasFail =
        findings
        |> List.exists (fun f -> f.Severity = Governance.WordBudgetSeverity.Fail)

    let status = if hasFail then "failed" else "passed"

    let env: WordBudgetEnvelope =
        { schema = "rhino-cli/governance-word-budget/v1"
          status = status
          total_findings = List.length findings
          findings = findings |> List.map toWordBudgetJson }

    JsonSerializer.Serialize(env, jsonOptions) + "\n"

let wordBudgetMarkdown (findings: Governance.WordBudgetFinding list) : string =
    if List.isEmpty findings then
        "## Word Budget Audit\n\n**PASSED**: all surfaces within budget\n"
    else
        let hasFail =
            findings
            |> List.exists (fun f -> f.Severity = Governance.WordBudgetSeverity.Fail)

        let label = if hasFail then "FAILED" else "WARN"

        let header =
            sprintf "## Word Budget Audit\n\n**%s**: %d finding(s)\n\n" label (List.length findings)

        let tableHeader =
            "| Path | Size (words) | Severity | Message |\n| --- | --- | --- | --- |\n"

        let rows =
            findings
            |> List.map toWordBudgetJson
            |> List.map (fun f -> sprintf "| `%s` | %d | %s | %s |\n" f.path f.size f.severity f.message)
            |> String.concat ""

        header + tableHeader + rows

// ---------------------------------------------------------------------------
// governance readme-index
// ---------------------------------------------------------------------------

type ReadmeIndexFindingJson =
    { file: string
      severity: string
      kind: string
      message: string }

type ReadmeIndexInnerResult =
    { findings: ReadmeIndexFindingJson list }

type ReadmeIndexEnvelope =
    { schema: string
      status: string
      result: ReadmeIndexInnerResult }

let private toReadmeIndexJson (f: Governance.ReadmeIndexFinding) : ReadmeIndexFindingJson =
    { file = f.File
      severity = f.Severity
      kind = f.Kind.Name
      message = f.Message }

/// `true` when at least one finding's kind is in `failKinds` (or, when
/// `failKinds` is empty, any kind except `unannotated`) — FR-1.11
/// [Repo-grounded — `governance_validate_readme_index.rs::has_failing_finding`].
let readmeIndexHasFailingFinding (findings: Governance.ReadmeIndexFinding list) (failKinds: string list) : bool =
    if List.isEmpty failKinds then
        findings |> List.exists (fun f -> f.Kind.Name <> "unannotated")
    else
        findings
        |> List.exists (fun f -> failKinds |> List.exists (fun k -> k = f.Kind.Name))

let readmeIndexText (findings: Governance.ReadmeIndexFinding list) : string =
    if List.isEmpty findings then
        "README INDEX AUDIT PASSED: no orphan or ghost references found\n"
    else
        let header =
            sprintf "README INDEX AUDIT FAILED: %d finding(s)\n" (List.length findings)

        let body =
            findings
            |> List.map (fun f -> sprintf "  %s  [%s/%s]  %s\n" f.File f.Severity f.Kind.Name f.Message)
            |> String.concat ""

        header + body

let readmeIndexJson (findings: Governance.ReadmeIndexFinding list) : string =
    let status = if List.isEmpty findings then "passed" else "failed"

    let env: ReadmeIndexEnvelope =
        { schema = "rhino-cli/readme-index-audit/v1"
          status = status
          result = { findings = findings |> List.map toReadmeIndexJson } }

    JsonSerializer.Serialize(env, jsonOptions) + "\n"

let readmeIndexMarkdown (findings: Governance.ReadmeIndexFinding list) : string =
    if List.isEmpty findings then
        "## README Index Audit\n\n**PASSED**: no orphan or ghost references found\n"
    else
        let header =
            sprintf "## README Index Audit\n\n**FAILED**: %d finding(s)\n\n" (List.length findings)

        let tableHeader =
            "| File | Severity | Kind | Message |\n|------|----------|------|---------|\n"

        let rows =
            findings
            |> List.map (fun f -> sprintf "| %s | %s | %s | %s |\n" f.File f.Severity f.Kind.Name f.Message)
            |> String.concat ""

        header + tableHeader + rows

// ---------------------------------------------------------------------------
// governance readme-index generate
// ---------------------------------------------------------------------------

type ReadmeIndexGenerateEnvelope =
    { schema: string
      status: string
      written: string list }

let readmeIndexGenerateText (written: string list) : string =
    if List.isEmpty written then
        "README INDEX GENERATE: no directory needed a new or updated index\n"
    else
        let header =
            sprintf "README INDEX GENERATE: wrote %d index(es)\n" (List.length written)

        let body = written |> List.map (sprintf "  %s\n") |> String.concat ""
        header + body

let readmeIndexGenerateJson (written: string list) : string =
    let env: ReadmeIndexGenerateEnvelope =
        { schema = "rhino-cli/readme-index-generate/v1"
          status = "passed"
          written = written }

    JsonSerializer.Serialize(env, jsonOptions) + "\n"

let readmeIndexGenerateMarkdown (written: string list) : string =
    if List.isEmpty written then
        "## README Index Generate\n\nNo directory needed a new or updated index.\n"
    else
        let header =
            sprintf "## README Index Generate\n\nWrote %d index(es):\n\n" (List.length written)

        let body = written |> List.map (sprintf "- %s\n") |> String.concat ""
        header + body

// ---------------------------------------------------------------------------
// governance readme-index rewrite-paths
// ---------------------------------------------------------------------------

type ReadmeIndexRewritePathsEnvelope =
    { schema: string
      status: string
      rewritten: string list }

/// [Repo-grounded — `governance_rewrite_readme_index_paths.rs::run`'s
/// `OutputFormat::Text | OutputFormat::Markdown` arm — text and markdown are
/// byte-identical for this command, unlike every other Wave D leaf].
let readmeIndexRewritePathsText (rewritten: string list) : string =
    let header =
        sprintf "readme-index rewrite-paths: %d file(s) updated\n" (List.length rewritten)

    let body = rewritten |> List.map (sprintf "  %s\n") |> String.concat ""
    header + body

let readmeIndexRewritePathsJson (rewritten: string list) : string =
    let env: ReadmeIndexRewritePathsEnvelope =
        { schema = "rhino-cli/readme-index-rewrite-paths/v1"
          status = "passed"
          rewritten = rewritten }

    JsonSerializer.Serialize(env, jsonOptions) + "\n"

let readmeIndexRewritePathsMarkdown (rewritten: string list) : string = readmeIndexRewritePathsText rewritten
