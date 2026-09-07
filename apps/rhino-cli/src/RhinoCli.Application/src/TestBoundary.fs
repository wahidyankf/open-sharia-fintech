/// Integration test network boundary audit. The Integration layer is defined
/// by resource ownership rather than transport, so a loopback socket the test
/// itself starts and stops is a legitimate Integration resource — but the
/// repository denies it by default so no project can adopt one silently. A
/// project opts in through `repo-config.yml`'s `integration-loopback:` list,
/// which is never a licence to reach an external network.
///
/// Binds
/// `specs/apps/rhino/cli/behaviours/repo-governance/repo-governance-test-boundary.feature`
/// and enforces
/// `repo-governance/development/infra/nx-targets/mandatory-targets-integration-tests.md`.
module RhinoCli.Application.TestBoundary

open System
open System.IO
open System.Text
open System.Text.Json
open System.Text.RegularExpressions

/// A single finding emitted by the test-boundary audit.
type TestBoundaryFinding =
    {
        /// Nx project name the finding is scoped to.
        Project: string
        /// Repository-relative source path, or `""` for a config-only finding.
        Path: string
        /// 1-based line, or `0` when the finding is not line-scoped.
        Line: int
        Severity: string
        /// Machine-readable violation category.
        Kind: string
        Message: string
    }

/// An Integration test reaches the network in a project no allowlist entry covers.
[<Literal>]
let KindUnallowlistedNetworkUse = "unallowlisted-network-use"

/// A project is allowlisted but no Integration source of its own uses the network.
[<Literal>]
let KindStaleAllowlistEntry = "stale-allowlist-entry"

/// An allowlist entry names a project that declares no `test:integration` target.
[<Literal>]
let KindUnknownAllowlistedProject = "unknown-allowlisted-project"

/// An allowlist entry carries no reason, so the opt-in cannot be audited.
[<Literal>]
let KindAllowlistEntryMissingReason = "allowlist-entry-missing-reason"

[<Literal>]
let private SeverityBlocking = "blocking"

[<Literal>]
let private SeverityWarning = "warning"

/// Module specifiers that reach the network, matched only in import position
/// (`from "axios"`, `require("axios")`, `import "node:http"`). These names
/// legitimately live inside a string, so they are matched before string
/// literals are stripped.
let private networkImportRe =
    Regex(
        @"(?:from|import|require\s*\()\s*[""'](?:node:(?:http|https|net|dgram|tls)|axios|supertest|undici|got|msw)[""']",
        RegexOptions.Compiled
    )

/// Network-API constructs a test uses to open a socket, matched only outside
/// string literals. A name that appears inside a string is data, not a call:
/// the repository's Integration suites embed package names in JSON fixtures
/// and this audit's own tests embed `HttpClient` in a source fixture, so a
/// scan that read string contents would report every one of them.
let private networkCallRe =
    Regex(
        @"\bHttpClient\b|\bHttpListener\b|\bHttpWebRequest\b|\bTcpClient\b|\bTcpListener\b|"
        + @"\bUdpClient\b|\bWebClient\b|\bClientWebSocket\b|new\s+Socket\s*\(|"
        + @"\bXMLHttpRequest\b|(?<![\w.])fetch\s*\(|new\s+WebSocket\s*\(",
        RegexOptions.Compiled
    )

/// Triple-quoted, verbatim, and ordinary string literals, longest form first
/// so a `"""..."""` block is consumed whole rather than as three fragments.
let private stringLiteralRe =
    Regex("\"\"\"[\\s\\S]*?\"\"\"|@\"(?:[^\"]|\"\")*\"|\"(?:\\\\.|[^\"\\\\])*\"", RegexOptions.Compiled)

/// Blanks every string literal in `line`, leaving code positions intact.
let withoutStringLiterals (line: string) : string = stringLiteralRe.Replace(line, "")

/// File extensions an Integration test can be written in here.
let private testExtensions =
    set [ ".fs"; ".fsx"; ".cs"; ".ts"; ".tsx"; ".js"; ".mjs"; ".cjs" ]

/// `true` when `path` is a source file the audit reads.
let isScannableSource (path: string) : bool =
    testExtensions.Contains(Path.GetExtension(path).ToLowerInvariant())

/// Every network-API use in `content`, as `(1-based line, matched text)`.
let findNetworkUses (content: string) : (int * string) list =
    content.Split('\n')
    |> Array.toList
    |> List.mapi (fun index line ->
        let importMatch = networkImportRe.Match(line)

        let m =
            if importMatch.Success then
                importMatch
            else
                networkCallRe.Match(withoutStringLiterals line)

        if m.Success then Some(index + 1, m.Value.Trim()) else None)
    |> List.choose id

/// A project that exposes `test:integration`, and where its sources live.
type IntegrationProject =
    {
        /// Nx project name, as `integration-loopback[].project` spells it.
        Name: string
        /// Repository-relative project directory, e.g. `apps/ose-be`.
        Directory: string
    }

/// Repository-relative directory holding `project`'s Integration sources.
let integrationRoot (project: IntegrationProject) : string =
    sprintf "%s/tests/integration" (project.Directory.TrimEnd('/'))

let private finding severity kind project path line message =
    { Project = project
      Path = path
      Line = line
      Severity = severity
      Kind = kind
      Message = message }

/// Audits `projects` against `sources` (repository-relative path -> content,
/// covering every scannable file under each project's Integration root) and
/// the `integration-loopback:` allowlist. Findings sort by project, then kind,
/// then path, then line, so the output is stable across filesystem orderings.
let audit
    (projects: IntegrationProject list)
    (sources: Map<string, string>)
    (allowlist: RepoConfig.IntegrationLoopbackEntry list)
    : TestBoundaryFinding list =
    let allowlistedNames =
        allowlist |> List.map (fun entry -> entry.Project) |> Set.ofList

    let usesByProject =
        projects
        |> List.map (fun project ->
            let root = integrationRoot project + "/"

            let uses =
                sources
                |> Map.toList
                |> List.filter (fun (path, _) ->
                    path.StartsWith(root, StringComparison.Ordinal) && isScannableSource path)
                |> List.collect (fun (path, content) ->
                    findNetworkUses content |> List.map (fun (line, token) -> path, line, token))

            project, uses)

    let networkFindings =
        usesByProject
        |> List.collect (fun (project, uses) ->
            if allowlistedNames.Contains project.Name then
                []
            else
                uses
                |> List.map (fun (path, line, token) ->
                    finding
                        SeverityBlocking
                        KindUnallowlistedNetworkUse
                        project.Name
                        path
                        line
                        (sprintf
                            "Integration test reaches the network through `%s`; Integration owns local resources only. Move the proof to E2E, or add `%s` to `integration-loopback:` in repo-config.yml when the socket is one this test starts and stops itself."
                            token
                            project.Name)))

    let projectsByName =
        projects |> List.map (fun project -> project.Name, project) |> Map.ofList

    let usesCountByName =
        usesByProject
        |> List.map (fun (project, uses) -> project.Name, List.length uses)
        |> Map.ofList

    let allowlistFindings =
        allowlist
        |> List.collect (fun entry ->
            match Map.tryFind entry.Project projectsByName with
            | None ->
                [ finding
                      SeverityBlocking
                      KindUnknownAllowlistedProject
                      entry.Project
                      ""
                      0
                      (sprintf
                          "`integration-loopback:` names \"%s\", which declares no `test:integration` target. Remove the entry or add the target."
                          entry.Project) ]
            | Some _ ->
                let missingReason =
                    if String.IsNullOrWhiteSpace entry.Reason then
                        [ finding
                              SeverityBlocking
                              KindAllowlistEntryMissingReason
                              entry.Project
                              ""
                              0
                              (sprintf
                                  "`integration-loopback:` entry for \"%s\" carries no reason. State why this project owns a loopback socket."
                                  entry.Project) ]
                    else
                        []

                let stale =
                    if Map.tryFind entry.Project usesCountByName = Some 0 then
                        [ finding
                              SeverityWarning
                              KindStaleAllowlistEntry
                              entry.Project
                              ""
                              0
                              (sprintf
                                  "`integration-loopback:` still lists \"%s\", but none of its Integration sources uses a network API. Drop the entry so the opt-in keeps meaning something."
                                  entry.Project) ]
                    else
                        []

                missingReason @ stale)

    networkFindings @ allowlistFindings
    |> List.sortWith (fun left right ->
        match String.CompareOrdinal(left.Project, right.Project) with
        | 0 ->
            match String.CompareOrdinal(left.Kind, right.Kind) with
            | 0 ->
                match String.CompareOrdinal(left.Path, right.Path) with
                | 0 -> compare left.Line right.Line
                | other -> other
            | other -> other
        | other -> other)

/// `true` when `findings` contains at least one blocking entry — the audit's
/// exit-code predicate. A stale allowlist entry is a warning and passes.
let hasBlocking (findings: TestBoundaryFinding list) : bool =
    findings |> List.exists (fun f -> f.Severity = SeverityBlocking)

/// Renders findings the way the CLI's text output does.
let formatText (findings: TestBoundaryFinding list) : string =
    if List.isEmpty findings then
        "TEST BOUNDARY AUDIT PASSED: zero findings\n"
    else
        let blocking =
            findings |> List.filter (fun f -> f.Severity = SeverityBlocking) |> List.length

        let sb = StringBuilder()

        let headline =
            if blocking > 0 then
                sprintf "TEST BOUNDARY AUDIT FAILED: %d finding(s) reported\n" (List.length findings)
            else
                sprintf "TEST BOUNDARY AUDIT PASSED: %d warning(s) reported\n" (List.length findings)

        sb.Append(headline) |> ignore

        for f in findings do
            let location =
                if String.IsNullOrEmpty f.Path then f.Project
                elif f.Line > 0 then sprintf "%s:%d" f.Path f.Line
                else f.Path

            sb.Append(sprintf "  %s  [%s]  %s — %s\n" location f.Severity f.Kind f.Message)
            |> ignore

        sb.ToString()

/// Reads one `project.json` and returns its Nx name when it declares a
/// `test:integration` target.
let readIntegrationProject (directory: string) (projectJson: string) : IntegrationProject option =
    try
        use document = JsonDocument.Parse(projectJson)
        let root = document.RootElement

        let hasTarget =
            match root.TryGetProperty("targets") with
            | true, targets -> fst (targets.TryGetProperty("test:integration"))
            | _ -> false

        if not hasTarget then
            None
        else
            match root.TryGetProperty("name") with
            // `JsonElement.ToString()` on a `String` element yields the value
            // itself, and never null — unlike `GetString()`, whose nullable
            // return would add a branch no JSON document can reach.
            | true, name when name.ValueKind = JsonValueKind.String ->
                Some
                    { Name = name.ToString()
                      Directory = directory }
            | _ -> None
    with :? JsonException ->
        None

/// Expresses `absolute` relative to `repoRoot` with forward slashes, the form
/// every finding path takes regardless of host separator.
let toRelativePath (repoRoot: string) (absolute: string) : string =
    Path.GetRelativePath(repoRoot, absolute).Replace(Path.DirectorySeparatorChar, '/')

/// Audits the repository at `repoRoot` from disk.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let auditRepository (repoRoot: string) : TestBoundaryFinding list =
    let relative = toRelativePath repoRoot

    let projects =
        [ "apps"; "libs" ]
        |> List.map (fun top -> Path.Combine(repoRoot, top))
        |> List.filter Directory.Exists
        |> List.collect (fun top -> Directory.EnumerateDirectories(top) |> List.ofSeq)
        |> List.choose (fun directory ->
            let projectJson = Path.Combine(directory, "project.json")

            if File.Exists projectJson then
                readIntegrationProject (relative directory) (File.ReadAllText projectJson)
            else
                None)

    let sources =
        projects
        |> List.collect (fun project ->
            let root = Path.Combine(repoRoot, integrationRoot project)

            if Directory.Exists root then
                Directory.EnumerateFiles(root, "*", SearchOption.AllDirectories)
                |> Seq.filter isScannableSource
                |> Seq.map (fun file -> relative file, File.ReadAllText file)
                |> List.ofSeq
            else
                [])
        |> Map.ofList

    let allowlist = (RepoConfig.loadOrDefault repoRoot).IntegrationLoopback

    audit projects sources allowlist
