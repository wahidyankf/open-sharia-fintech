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

    if not (msg.StartsWith("[")) || closeBracket < 0 then
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
