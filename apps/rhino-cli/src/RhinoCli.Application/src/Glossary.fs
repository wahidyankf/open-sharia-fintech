/// Glossary validator for bounded-context glossary markdown files
/// [1:1 port of `apps/rhino-cli/src/application/glossary.rs`].
///
/// A glossary file has three sections:
/// - **Frontmatter** — bold key-value pairs (`**Key**: value`) at the top.
/// - **Terms table** — a markdown table under `## Terms` or `## Term index`.
/// - **Forbidden synonyms** — a bullet list under `## Forbidden synonyms`.
///
/// The validator parses every glossary declared in the bounded-context
/// registry, then checks required frontmatter keys, terms-table header shape,
/// code-identifier liveness, feature-reference resolution, forbidden-synonym
/// self-use, and cross-context term collisions.
module RhinoCli.Application.Glossary

open System
open System.Collections.Generic
open System.IO
open System.Text
open System.Text.RegularExpressions
open RhinoCli.Domain.Types
open RhinoCli.Application.Ddd

/// One term entry from the glossary terms table.
type Term =
    { Term: string
      Definition: string
      CodeIdentifiers: string list
      UsedInFeatures: string list
      SourceLine: int }

/// One entry from the `## Forbidden synonyms` bullet list.
type Forbidden =
    { Term: string
      Reason: string
      SourceLine: int }

/// A structural parse error that prevented a glossary element from being read.
type ParseError = { Line: int; Message: string }

/// In-memory representation of a parsed glossary file.
type Glossary =
    { Path: string
      Frontmatter: Map<string, string>
      Terms: Term list
      ForbiddenSynonyms: Forbidden list
      ParseErrors: ParseError list }

/// A validation finding produced by the glossary checker.
type GlossaryFinding =
    { File: string
      Message: string
      Severity: Severity }

/// Inputs for one `validateAll` run.
type GlossaryValidateOptions =
    {
        RepoRoot: string
        App: string
        /// `None` defaults to blocking.
        Severity: Severity option
    }

let private reFrontmatter =
    Regex(@"^\*\*([^*]+)\*\*:\s*(.+)$", RegexOptions.Compiled)

let private reBacktickIdents = Regex(@"`([^`]+)`", RegexOptions.Compiled)

/// Keys every glossary frontmatter block must contain.
let requiredFrontmatterKeys = [ "Bounded context"; "Maintainer"; "Last reviewed" ]

/// Expected column headers for the terms table.
let expectedTableColumns = [ "Term"; "Code identifier(s)"; "Used in features" ]

/// Removes backticks and trims surrounding whitespace from a markdown cell.
let stripMarkup (s: string) : string = s.Trim().Replace("`", "")

/// Splits a markdown table row on `|`, trimming the outer pipes.
let splitTableRow (line: string) : string list =
    let line = line.Trim()

    let line =
        if line.StartsWith("|", StringComparison.Ordinal) then
            line.Substring 1
        else
            line

    let line =
        if line.EndsWith("|", StringComparison.Ordinal) then
            line.Substring(0, line.Length - 1)
        else
            line

    line.Split('|') |> Array.map (fun p -> p.Trim()) |> List.ofArray

/// True when every cell holds only dashes and optional alignment colons.
let isSeparatorRow (cells: string list) : bool =
    match cells with
    | [] -> false
    | _ ->
        cells
        |> List.forall (fun c ->
            let s = c.Replace("-", "").Trim()
            s = "" || s = ":")

/// Extracts all backtick-delimited identifiers from a table cell.
let parseBacktickList (cell: string) : string list =
    reBacktickIdents.Matches cell
    |> Seq.map (fun m -> m.Groups.[1].Value.Trim())
    |> Seq.filter (fun s -> s <> "")
    |> List.ofSeq

/// Parses feature references from a cell, handling `<br>` separators,
/// comma-separated lists, and trailing parenthetical annotations.
let parseFeatureRefs (cell: string) : string list =
    cell.Replace("<br>", ",").Split(',')
    |> Array.map (fun p ->
        let s = p.Trim().Replace("`", "")

        match s.IndexOf '(' with
        | -1 -> s
        | idx -> s.Substring(0, idx).Trim())
    |> Array.filter (fun s -> s <> "")
    |> List.ofArray

/// Parses one forbidden-synonym bullet into a `(term, reason)` pair, accepting
/// either an em-dash or an ASCII hyphen as the separator.
let parseForbiddenEntry (line: string) : string * string =
    let emDash = "—"

    let idx =
        match line.IndexOf(emDash, StringComparison.Ordinal) with
        | -1 ->
            match line.IndexOf '-' with
            | -1 -> None
            | i -> Some(i, 1)
        | i -> Some(i, emDash.Length)

    match idx with
    | Some(i, len) -> line.Substring(0, i).Trim().Trim('"'), line.Substring(i + len).Trim()
    | None -> line.Trim().Trim('"'), ""

/// Validates that the terms-table header row carries the expected columns.
let validateTableHeader (cells: string list) (lineNum: int) : ParseError list =
    if List.length cells < List.length expectedTableColumns then
        [ { Line = lineNum
            Message = "malformed terms table header: too few columns" } ]
    else
        expectedTableColumns
        |> List.indexed
        |> List.tryPick (fun (i, expected) ->
            let got = stripMarkup cells.[i]

            if got <> expected then
                Some
                    { Line = lineNum
                      Message = sprintf "malformed terms table header: column %s expected %s" got expected }
            else
                None)
        |> Option.toList

/// Parses `content` line by line into frontmatter, terms, and forbidden
/// synonyms — collecting structural problems rather than failing fast, so the
/// caller can still validate a partially-parsed glossary.
let parseContent (path: string) (content: string) : Glossary =
    let frontmatter = Dictionary<string, string>()
    let terms = ResizeArray<Term>()
    let forbidden = ResizeArray<Forbidden>()
    let parseErrors = ResizeArray<ParseError>()
    let mutable lineNum = 0
    let mutable inTerms = false
    let mutable headerParsed = false
    let mutable inForbidden = false

    for line in content.Split('\n') do
        lineNum <- lineNum + 1
        let fm = reFrontmatter.Match line

        if fm.Success then
            frontmatter.[fm.Groups.[1].Value.Trim()] <- fm.Groups.[2].Value.Trim()
        elif line = "## Terms" || line = "## Term index" then
            inTerms <- true
            inForbidden <- false
            headerParsed <- false
        elif line.StartsWith("## Forbidden synonyms", StringComparison.Ordinal) then
            inTerms <- false
            inForbidden <- true
        elif line.StartsWith("## ", StringComparison.Ordinal) then
            inTerms <- false
            inForbidden <- false
        else
            if inTerms && line.StartsWith("|", StringComparison.Ordinal) then
                let cells = splitTableRow line

                if not headerParsed then
                    headerParsed <- true
                    parseErrors.AddRange(validateTableHeader cells lineNum)
                elif not (isSeparatorRow cells) && List.length cells >= 3 then
                    terms.Add
                        { Term = stripMarkup cells.[0]
                          Definition = ""
                          CodeIdentifiers = parseBacktickList cells.[1]
                          UsedInFeatures = parseFeatureRefs cells.[2]
                          SourceLine = lineNum }

            if inForbidden then
                let trimmed =
                    let t = line.Trim()

                    if t.StartsWith("- ", StringComparison.Ordinal) then
                        t.Substring 2
                    else
                        t

                // A line that survives both trims unchanged is not a bullet.
                if trimmed <> "" && trimmed <> line then
                    let term, reason = parseForbiddenEntry trimmed

                    if term <> "" then
                        forbidden.Add
                            { Term = term
                              Reason = reason
                              SourceLine = lineNum }

    { Path = path
      Frontmatter = frontmatter |> Seq.map (fun kv -> kv.Key, kv.Value) |> Map.ofSeq
      Terms = List.ofSeq terms
      ForbiddenSynonyms = List.ofSeq forbidden
      ParseErrors = List.ofSeq parseErrors }

/// Reads and parses the glossary file at `path`; an unreadable file becomes a
/// file-level parse error rather than a thrown exception.
let parse (path: string) : Glossary =
    try
        parseContent path (File.ReadAllText path)
    with ex ->
        { Path = path
          Frontmatter = Map.empty
          Terms = []
          ForbiddenSynonyms = []
          ParseErrors = [ { Line = 0; Message = ex.Message } ] }

let private glossaryFinding (file: string) (message: string) (severity: Severity) : GlossaryFinding =
    { File = file
      Message = message
      Severity = severity }

/// Findings for every required frontmatter key absent from `g`.
let checkFrontmatter (file: string) (g: Glossary) (sev: Severity) : GlossaryFinding list =
    requiredFrontmatterKeys
    |> List.filter (fun k -> not (g.Frontmatter.ContainsKey k))
    |> List.map (fun k -> glossaryFinding file (sprintf "missing frontmatter key: %s" k) sev)

/// Findings for every malformed-header parse error stored in `g`.
let checkTableHeader (file: string) (g: Glossary) (sev: Severity) : GlossaryFinding list =
    g.ParseErrors
    |> List.filter (fun pe -> pe.Message.Contains "malformed terms table header")
    |> List.map (fun pe -> glossaryFinding file pe.Message sev)

/// Counts lines under `root` (filtered by `exts`) holding a whole-word match.
let grepFiles (pattern: string) (root: string) (exts: string list) : int =
    let re = Regex(sprintf @"\b%s\b" (Regex.Escape pattern))

    if not (Directory.Exists root) then
        0
    else
        let suffixes =
            exts
            |> List.map (fun e ->
                "."
                + (if e.StartsWith("*.", StringComparison.Ordinal) then
                       e.Substring 2
                   else
                       e))

        Directory.EnumerateFiles(root, "*", SearchOption.AllDirectories)
        |> Seq.filter (fun f ->
            let name = Path.GetFileName f
            suffixes |> List.exists (fun s -> name.EndsWith(s, StringComparison.Ordinal)))
        |> Seq.sumBy (fun f ->
            try
                File.ReadAllLines f |> Array.filter re.IsMatch |> Array.length
            with _ ->
                0)

/// Formats a list of paths as a bracketed, space-separated string.
let formatPaths (paths: string list) : string =
    sprintf "[%s]" (String.Join(" ", paths))

/// True when `reference` resolves to an existing file inside one of the
/// `gherkinPaths` directories — accepting bare filenames, `sub/dir` paths, and
/// glob patterns.
let featureRefResolves (reference: string) (gherkinPaths: string list) : bool =
    gherkinPaths
    |> List.exists (fun gh ->
        let featurePath =
            if reference.Contains "/" then
                let parts = reference.Split([| '/' |], 2)
                let parent = Path.GetDirectoryName(gh.TrimEnd(Path.DirectorySeparatorChar, '/'))

                if String.IsNullOrEmpty parent then
                    Path.Combine(gh, Path.GetFileName reference)
                else
                    Path.Combine(parent, parts.[0], parts.[1])
            else
                Path.Combine(gh, Path.GetFileName reference)

        if featurePath.Contains "*" then
            let dir = Path.GetDirectoryName featurePath
            let pattern = Path.GetFileName featurePath

            Directory.Exists dir
            && Directory.EnumerateFiles(dir, pattern) |> Seq.isEmpty |> not
        else
            File.Exists featurePath || Directory.Exists featurePath)

/// Validates every term's code identifiers and feature references.
let checkTerms
    (file: string)
    (g: Glossary)
    (codePaths: string list)
    (codeExts: string list)
    (gherkinPaths: string list)
    (sev: Severity)
    : GlossaryFinding list =
    [ for term in g.Terms do
          for id in term.CodeIdentifiers do
              if codePaths |> List.sumBy (fun cp -> grepFiles id cp codeExts) = 0 then
                  yield
                      glossaryFinding
                          file
                          (sprintf
                              "stale identifier: `%s` (term \"%s\", not found in %s)"
                              id
                              term.Term
                              (formatPaths codePaths))
                          sev

          for r in term.UsedInFeatures do
              if not (featureRefResolves r gherkinPaths) then
                  yield glossaryFinding file (sprintf "missing feature reference: %s" r) sev ]

/// Findings for forbidden synonyms used in the context's own code or Gherkin.
let checkForbiddenSynonyms
    (file: string)
    (g: Glossary)
    (codePaths: string list)
    (codeExts: string list)
    (gherkinPaths: string list)
    (sev: Severity)
    : GlossaryFinding list =
    [ for fb in g.ForbiddenSynonyms do
          let inCode = codePaths |> List.sumBy (fun cp -> grepFiles fb.Term cp codeExts)

          let inGherkin =
              gherkinPaths |> List.sumBy (fun gh -> grepFiles fb.Term gh [ "*.feature" ])

          if inCode + inGherkin > 0 then
              yield glossaryFinding file (sprintf "forbidden synonym used in own context: \"%s\"" fb.Term) sev ]

/// True when `g` forbids `term` (case-insensitively). `_other` is reserved for
/// future directional cross-link checking, matching the Rust signature.
let hasForbiddenFor (g: Glossary) (term: string) (_other: string) : bool =
    g.ForbiddenSynonyms
    |> List.exists (fun fb -> String.Equals(fb.Term, term, StringComparison.OrdinalIgnoreCase))

/// Detects terms defined in several contexts without mutual
/// `Forbidden synonyms` cross-links.
let checkTermCollisions (reg: Registry) (glossaries: Map<string, Glossary>) (sev: Severity) : GlossaryFinding list =
    let termContexts = Dictionary<string, ResizeArray<string>>()

    for ctx in reg.Contexts do
        match glossaries.TryFind ctx.Name with
        | None -> ()
        | Some g ->
            for t in g.Terms do
                if not (termContexts.ContainsKey t.Term) then
                    termContexts.[t.Term] <- ResizeArray<string>()

                termContexts.[t.Term].Add ctx.Name

    termContexts
    |> Seq.map (fun kv -> kv.Key, List.ofSeq kv.Value)
    |> Seq.sortWith (fun (a, _) (b, _) -> String.CompareOrdinal(a, b))
    |> Seq.filter (fun (_, contexts) -> List.length contexts >= 2)
    |> Seq.filter (fun (term, contexts) ->
        let allCovered =
            contexts
            |> List.forall (fun ctxName ->
                match glossaries.TryFind ctxName with
                | None -> true
                | Some g ->
                    contexts
                    |> List.filter (fun c -> c <> ctxName)
                    |> List.forall (fun other -> hasForbiddenFor g term other))

        not allCovered)
    |> Seq.map (fun (term, contexts) ->
        glossaryFinding
            (sprintf "specs/apps/%s/ddd/bounded-contexts.yaml" reg.App)
            (sprintf
                "term collision: \"%s\" defined in %s without mutual Forbidden-synonyms cross-link"
                term
                (formatPaths contexts))
            sev)
    |> List.ofSeq

/// Loads the bounded-context registry for `opts.App` and validates every
/// declared glossary file, returning findings sorted by file.
let validateAll (opts: GlossaryValidateOptions) : Result<GlossaryFinding list, string> =
    let sev = defaultArg opts.Severity Severity.Blocking

    match loadRegistry opts.RepoRoot opts.App with
    | Error message -> Error message
    | Ok reg ->
        let findings = ResizeArray<GlossaryFinding>()
        let glossaries = Dictionary<string, Glossary>()

        for ctx in reg.Contexts do
            let g = parse (Path.Combine(opts.RepoRoot, ctx.Glossary))

            for pe in g.ParseErrors do
                findings.Add(glossaryFinding ctx.Glossary pe.Message sev)

            findings.AddRange(checkFrontmatter ctx.Glossary g sev)
            findings.AddRange(checkTableHeader ctx.Glossary g sev)

            let codePaths = ctx.Code |> List.map (fun c -> Path.Combine(opts.RepoRoot, c))

            let codeExts =
                ctx.CodeLang
                |> List.collect (fun lang -> supportedLangGlobs.TryFind lang |> Option.defaultValue [])

            let gherkinPaths = ctx.Gherkin |> List.map (fun g -> Path.Combine(opts.RepoRoot, g))

            findings.AddRange(checkTerms ctx.Glossary g codePaths codeExts gherkinPaths sev)
            findings.AddRange(checkForbiddenSynonyms ctx.Glossary g codePaths codeExts gherkinPaths sev)
            glossaries.[ctx.Name] <- g

        findings.AddRange(checkTermCollisions reg (glossaries |> Seq.map (fun kv -> kv.Key, kv.Value) |> Map.ofSeq) sev)

        findings
        |> Seq.sortWith (fun a b -> String.CompareOrdinal(a.File, b.File))
        |> List.ofSeq
        |> Ok

/// Renders findings as `"{file}: {severity}: {message}"` lines plus a success
/// flag that is false once any finding is blocking.
let renderGlossaryFindings (findings: GlossaryFinding list) : string * bool =
    let sb = StringBuilder()
    let mutable ok = true

    for f in findings do
        sb.Append(f.File).Append(": ").Append(severityCode f.Severity).Append(": ").Append(f.Message).Append('\n')
        |> ignore

        if f.Severity = Severity.Blocking then
            ok <- false

    sb.ToString(), ok
