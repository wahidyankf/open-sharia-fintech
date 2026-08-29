/// Bounded-context registry parsing and structural-parity validation: checks
/// that `specs/apps/<app>/ddd/bounded-contexts.yaml` and the filesystem agree
/// on code layers, glossaries, Gherkin folders, and relationship symmetry
/// [Repo-grounded — `apps/rhino-cli/src/application/bcregistry.rs`,
/// `apps/rhino-cli/src/application/severity.rs`], binding
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/ddd/ddd-bc.feature`.
module RhinoCli.Application.Ddd

open System
open System.Collections.Generic
open System.IO
open System.Text
open YamlDotNet.Serialization
open RhinoCli.Domain.Types

/// The only schema version this tool understands.
[<Literal>]
let SchemaVersion = 2

/// Canonical lowercase code for a severity, as the CLI prints it.
let severityCode (severity: Severity) : string =
    match severity with
    | Severity.Blocking -> "error"
    | Severity.Advisory -> "warn"

/// Parses a severity string; `"warn"`/`"warning"` (case-insensitive) are
/// advisory, everything else — including empty — is blocking.
let parseSeverity (s: string) : Severity =
    match s.Trim().ToLowerInvariant() with
    | "warn"
    | "warning" -> Severity.Advisory
    | _ -> Severity.Blocking

/// Resolves the effective severity: a non-empty flag wins, then a non-empty
/// env value, then blocking. Returns the resolved severity alongside the audit
/// line the CLI writes to stderr when the env var downgrades it.
let resolveSeverity (flagVal: string) (envVal: string) : Severity * string option =
    if flagVal <> "" then
        parseSeverity flagVal, None
    elif envVal <> "" then
        let severity = parseSeverity envVal

        severity,
        (if severity = Severity.Advisory then
             Some "WARN: severity downgraded to \"warn\" via OSE_RHINO_DDD_SEVERITY env var"
         else
             None)
    else
        Severity.Blocking, None

/// A directional relationship between two bounded contexts.
type Relationship =
    { To: string
      Kind: string
      Role: string }

/// One bounded context entry in the registry.
type BcContext =
    { Name: string
      Summary: string
      Layers: string list
      Code: string list
      CodeLang: string list
      Glossary: string
      Gherkin: string list
      Relationships: Relationship list }

/// A parsed `bounded-contexts.yaml` registry.
type Registry =
    { Version: int
      App: string
      Contexts: BcContext list }

/// One validation finding.
type BcFinding =
    { File: string
      Message: string
      Severity: Severity }

/// Inputs for one validation run.
type BcValidateOptions =
    {
        RepoRoot: string
        App: string
        /// `None` defaults to blocking.
        Severity: Severity option
    }

/// Language identifier to source-file globs.
let supportedLangGlobs: Map<string, string list> =
    Map.ofList
        [ "ts", [ "*.ts" ]
          "tsx", [ "*.tsx" ]
          "fs", [ "*.fs" ]
          "go", [ "*.go" ]
          "py", [ "*.py" ]
          "java", [ "*.java" ]
          "kt", [ "*.kt" ]
          "rs", [ "*.rs" ]
          "ex", [ "*.ex"; "*.exs" ]
          "exs", [ "*.exs" ]
          "cs", [ "*.cs" ]
          "clj", [ "*.clj"; "*.cljc" ]
          "dart", [ "*.dart" ] ]

/// `Some true` — the kind needs a reciprocal declaration; `Some false` — it is
/// unidirectional; `None` — the kind is unrecognised.
let relationshipKindIsAsymmetric (kind: string) : bool option =
    match kind with
    | "customer-supplier"
    | "conformist"
    | "partnership"
    | "shared-kernel" -> Some true
    | "anticorruption-layer"
    | "open-host-service" -> Some false
    | _ -> None

let private yamlDeserializer = DeserializerBuilder().Build()

let private asMap (v: obj) : IDictionary<obj, obj> option =
    match v with
    | :? IDictionary<obj, obj> as d -> Some d
    | _ -> None

let private asList (v: obj) : obj list option =
    match v with
    | :? IList<obj> as l -> Some(List.ofSeq l)
    | _ -> None

let private asString (v: obj) : string =
    match v with
    | null -> ""
    | :? string as s -> s
    | other -> string other

let private lookup (m: IDictionary<obj, obj>) (key: string) : obj option =
    match m.TryGetValue(box key) with
    | true, value -> Some value
    | _ -> None

let private stringSeq (v: obj) : string list =
    asList v |> Option.map (List.map asString) |> Option.defaultValue []

/// The `gherkin` field is either a scalar path or a sequence of them.
let private parseGherkin (v: obj) : string list =
    match v with
    | :? string as s -> [ s ]
    | other -> stringSeq other

let private parseRelationship (v: obj) : Relationship =
    match asMap v with
    | None -> { To = ""; Kind = ""; Role = "" }
    | Some m ->
        { To = lookup m "to" |> Option.map asString |> Option.defaultValue ""
          Kind = lookup m "kind" |> Option.map asString |> Option.defaultValue ""
          Role = lookup m "role" |> Option.map asString |> Option.defaultValue "" }

let private parseContext (v: obj) : BcContext =
    let empty =
        { Name = ""
          Summary = ""
          Layers = []
          Code = []
          CodeLang = []
          Glossary = ""
          Gherkin = []
          Relationships = [] }

    match asMap v with
    | None -> empty
    | Some m ->
        let str key =
            lookup m key |> Option.map asString |> Option.defaultValue ""

        { empty with
            Name = str "name"
            Summary = str "summary"
            Glossary = str "glossary"
            Layers = lookup m "layers" |> Option.map stringSeq |> Option.defaultValue []
            Code = lookup m "code" |> Option.map stringSeq |> Option.defaultValue []
            CodeLang = lookup m "code_lang" |> Option.map stringSeq |> Option.defaultValue []
            Gherkin = lookup m "gherkin" |> Option.map parseGherkin |> Option.defaultValue []
            Relationships =
                lookup m "relationships"
                |> Option.bind asList
                |> Option.map (List.map parseRelationship)
                |> Option.defaultValue [] }

let private parseRegistry (v: obj) : Registry =
    match asMap v with
    | None -> { Version = 0; App = ""; Contexts = [] }
    | Some m ->
        { Version =
            lookup m "version"
            |> Option.map asString
            |> Option.bind (fun s ->
                match Int32.TryParse s with
                | true, n -> Some n
                | _ -> None)
            |> Option.defaultValue 0
          App = lookup m "app" |> Option.map asString |> Option.defaultValue ""
          Contexts =
            lookup m "contexts"
            |> Option.bind asList
            |> Option.map (List.map parseContext)
            |> Option.defaultValue [] }

/// Loads and validates the registry for `app`: the schema version must match,
/// every context needs non-empty `code` and `gherkin` lists, and `code_lang`
/// defaults to `["ts"; "tsx"]`.
let loadRegistry (repoRoot: string) (app: string) : Result<Registry, string> =
    let path =
        Path.Combine(repoRoot, "specs", "apps", app, "ddd", "bounded-contexts.yaml")

    if not (File.Exists path) then
        Error(sprintf "registry not found for app \"%s\" at %s" app path)
    else
        try
            let registry =
                parseRegistry (yamlDeserializer.Deserialize<obj>(File.ReadAllText path))

            if registry.Version <> SchemaVersion then
                Error(
                    sprintf
                        "registry for app \"%s\" has unsupported version %d (expected %d) at %s"
                        app
                        registry.Version
                        SchemaVersion
                        path
                )
            else
                let invalid =
                    registry.Contexts
                    |> List.tryPick (fun ctx ->
                        if List.isEmpty ctx.Code then
                            Some(
                                sprintf
                                    "registry for app \"%s\" context \"%s\" has empty code list at %s"
                                    app
                                    ctx.Name
                                    path
                            )
                        elif List.isEmpty ctx.Gherkin then
                            Some(
                                sprintf
                                    "registry for app \"%s\" context \"%s\" has empty gherkin list at %s"
                                    app
                                    ctx.Name
                                    path
                            )
                        else
                            let langs =
                                if List.isEmpty ctx.CodeLang then
                                    [ "ts"; "tsx" ]
                                else
                                    ctx.CodeLang

                            langs
                            |> List.tryFind (fun l -> not (supportedLangGlobs.ContainsKey l))
                            |> Option.map (fun l ->
                                sprintf
                                    "registry context \"%s\": unsupported code_lang \"%s\" (supported: ts, tsx, fs, go, py, java, kt, rs, ex, exs, cs, clj, dart)"
                                    ctx.Name
                                    l))

                match invalid with
                | Some message -> Error message
                | None ->
                    Ok
                        { registry with
                            Contexts =
                                registry.Contexts
                                |> List.map (fun ctx ->
                                    if List.isEmpty ctx.CodeLang then
                                        { ctx with CodeLang = [ "ts"; "tsx" ] }
                                    else
                                        ctx) }
        with ex ->
            Error(sprintf "failed to parse registry for app \"%s\": %s" app ex.Message)

let private finding (file: string) (message: string) (severity: Severity) : BcFinding =
    { File = file
      Message = message
      Severity = severity }

let private subdirectoryNames (dir: string) : string list =
    Directory.GetDirectories dir |> Array.map Path.GetFileName |> List.ofArray

/// Checks that every declared layer exists under `codeRel`, and that no
/// undeclared layer directory sits there.
let private checkLayersAtPath
    (repoRoot: string)
    (ctx: BcContext)
    (codeRel: string)
    (severity: Severity)
    : BcFinding list =
    let codePath = Path.Combine(repoRoot, codeRel)

    try
        let actual = subdirectoryNames codePath |> Set.ofList

        let missing =
            ctx.Layers
            |> List.filter (fun l -> not (Set.contains l actual))
            |> List.map (fun l ->
                finding
                    (sprintf "%s/%s" codeRel l)
                    (sprintf "missing layer \"%s\" for context \"%s\"" l ctx.Name)
                    severity)

        let declared = Set.ofList ctx.Layers

        let extras =
            actual
            |> Set.toList
            |> List.filter (fun n -> not (Set.contains n declared))
            |> List.sortWith (fun a b -> String.CompareOrdinal(a, b))
            |> List.map (fun name ->
                finding
                    (sprintf "%s/%s" codeRel name)
                    (sprintf
                        "extra layer \"%s\" found on filesystem but not declared in registry for context \"%s\""
                        name
                        ctx.Name)
                    severity)

        missing @ extras
    with ex ->
        [ finding codeRel (sprintf "cannot read code directory for context \"%s\": %s" ctx.Name ex.Message) severity ]

/// Verifies every Gherkin directory exists and holds at least one `.feature`
/// file.
let private checkGherkin (repoRoot: string) (ctx: BcContext) (severity: Severity) : BcFinding list =
    ctx.Gherkin
    |> List.collect (fun gh ->
        let gpath = Path.Combine(repoRoot, gh)

        if not (Directory.Exists gpath) then
            [ finding gh (sprintf "missing gherkin directory for context \"%s\"" ctx.Name) severity ]
        elif
            Directory.GetFiles gpath
            |> Array.exists (fun f -> f.EndsWith(".feature", StringComparison.Ordinal))
        then
            []
        else
            [ finding gh (sprintf "no feature files found in gherkin directory for context \"%s\"" ctx.Name) severity ])

let private checkContext (repoRoot: string) (ctx: BcContext) (severity: Severity) : BcFinding list =
    let codeFindings =
        ctx.Code
        |> List.collect (fun codeRel ->
            let codePath = Path.Combine(repoRoot, codeRel)

            if not (Directory.Exists codePath || File.Exists codePath) then
                [ finding codeRel (sprintf "missing code directory for context \"%s\"" ctx.Name) severity ]
            else
                checkLayersAtPath repoRoot ctx codeRel severity)

    let glossaryFindings =
        let glossaryPath = Path.Combine(repoRoot, ctx.Glossary)

        if File.Exists glossaryPath || Directory.Exists glossaryPath then
            []
        else
            [ finding ctx.Glossary (sprintf "missing glossary for context \"%s\"" ctx.Name) severity ]

    codeFindings @ glossaryFindings @ checkGherkin repoRoot ctx severity

/// Reports every subdirectory of `root` that no context registered.
let private detectOrphanDirs
    (root: string)
    (registered: Set<string>)
    (kind: string)
    (notReason: string)
    (severity: Severity)
    : BcFinding list =
    if not (Directory.Exists root) then
        []
    else
        Directory.GetDirectories root
        |> Array.map (fun p -> Path.GetFileName p, p)
        |> Array.sortWith (fun (a, _) (b, _) -> String.CompareOrdinal(a, b))
        |> Array.toList
        |> List.filter (fun (_, full) -> not (Set.contains full registered))
        |> List.map (fun (name, full) -> finding full (sprintf "%s \"%s\" not %s" kind name notReason) severity)

/// Reports every non-README `.md` file in `root` that no context registered.
let private detectOrphanFiles
    (root: string)
    (registered: Set<string>)
    (kind: string)
    (notReason: string)
    (severity: Severity)
    : BcFinding list =
    if not (Directory.Exists root) then
        []
    else
        Directory.GetFiles root
        |> Array.map (fun p -> Path.GetFileName p, p)
        |> Array.filter (fun (name, _) -> name.EndsWith(".md", StringComparison.Ordinal) && name <> "README.md")
        |> Array.sortWith (fun (a, _) (b, _) -> String.CompareOrdinal(a, b))
        |> Array.toList
        |> List.filter (fun (_, full) -> not (Set.contains full registered))
        |> List.map (fun (name, full) -> finding full (sprintf "%s \"%s\" not %s" kind name notReason) severity)

let private parentsOf (paths: string seq) : string list =
    paths
    |> Seq.choose (fun p ->
        match Path.GetDirectoryName p with
        | null
        | "" -> None
        | parent -> Some parent)
    |> Seq.distinct
    |> Seq.sortWith (fun a b -> String.CompareOrdinal(a, b))
    |> List.ofSeq

/// Scans the registered parents for code, glossary, and Gherkin entries that
/// exist on disk but appear in no context.
let private detectOrphans
    (repoRoot: string)
    (reg: Registry)
    (registeredCode: Set<string>)
    (registeredGlossary: Set<string>)
    (registeredGherkin: Set<string>)
    (severity: Severity)
    : BcFinding list =
    let notReason = "registered in bounded-contexts.yaml"

    let codeRoots =
        parentsOf (
            reg.Contexts
            |> List.collect (fun c -> c.Code)
            |> List.map (fun c -> Path.Combine(repoRoot, c))
        )

    let glossaryRoots =
        parentsOf (reg.Contexts |> List.map (fun c -> Path.Combine(repoRoot, c.Glossary)))

    let gherkinRoots =
        parentsOf (
            reg.Contexts
            |> List.collect (fun c -> c.Gherkin)
            |> List.map (fun g -> Path.Combine(repoRoot, g))
        )

    (codeRoots
     |> List.collect (fun r -> detectOrphanDirs r registeredCode "orphan code directory" notReason severity))
    @ (glossaryRoots
       |> List.collect (fun r -> detectOrphanFiles r registeredGlossary "orphan glossary file" notReason severity))
    @ (gherkinRoots
       |> List.collect (fun r -> detectOrphanDirs r registeredGherkin "orphan gherkin directory" notReason severity))

let private hasReciprocal (ctx: BcContext) (source: string) (kind: string) : bool =
    ctx.Relationships |> List.exists (fun r -> r.To = source && r.Kind = kind)

/// Checks that every symmetric relationship has a reciprocal declaration in
/// its target context.
let private checkRelationshipSymmetry
    (reg: Registry)
    (byName: Map<string, BcContext>)
    (severity: Severity)
    : BcFinding list =
    let yamlPath = sprintf "specs/apps/%s/ddd/bounded-contexts.yaml" reg.App

    reg.Contexts
    |> List.collect (fun ctx ->
        ctx.Relationships
        |> List.choose (fun rel ->
            match relationshipKindIsAsymmetric rel.Kind with
            | None
            | Some false -> None
            | Some true ->
                match Map.tryFind rel.To byName with
                | None ->
                    Some(
                        finding
                            yamlPath
                            (sprintf
                                "relationship target \"%s\" declared by \"%s\" does not exist in registry"
                                rel.To
                                ctx.Name)
                            severity
                    )
                | Some target when not (hasReciprocal target ctx.Name rel.Kind) ->
                    Some(
                        finding
                            yamlPath
                            (sprintf
                                "relationship asymmetry: \"%s\" → \"%s\" (%s) but \"%s\" has no reciprocal entry"
                                ctx.Name
                                rel.To
                                rel.Kind
                                rel.To)
                            severity
                    )
                | Some _ -> None))

let private checkRelationshipKinds (reg: Registry) (severity: Severity) : BcFinding list =
    let yamlPath = sprintf "specs/apps/%s/ddd/bounded-contexts.yaml" reg.App

    reg.Contexts
    |> List.collect (fun ctx ->
        ctx.Relationships
        |> List.filter (fun rel -> (relationshipKindIsAsymmetric rel.Kind).IsNone)
        |> List.map (fun rel ->
            finding
                yamlPath
                (sprintf "unknown relationship kind \"%s\" in \"%s\" → \"%s\"" rel.Kind ctx.Name rel.To)
                severity))

/// Runs every registry check and returns the findings, sorted by file.
let validateRegistry (repoRoot: string) (reg: Registry) (severity: Severity) : BcFinding list =
    let absolute (rel: string) = Path.Combine(repoRoot, rel)

    let registeredCode =
        reg.Contexts
        |> List.collect (fun c -> c.Code)
        |> List.map absolute
        |> Set.ofList

    let registeredGlossary =
        reg.Contexts |> List.map (fun c -> absolute c.Glossary) |> Set.ofList

    let registeredGherkin =
        reg.Contexts
        |> List.collect (fun c -> c.Gherkin)
        |> List.map absolute
        |> Set.ofList

    let byName = reg.Contexts |> List.map (fun c -> c.Name, c) |> Map.ofList

    let contextFindings =
        reg.Contexts |> List.collect (fun ctx -> checkContext repoRoot ctx severity)

    let orphanFindings =
        if List.isEmpty reg.Contexts then
            []
        else
            detectOrphans repoRoot reg registeredCode registeredGlossary registeredGherkin severity

    contextFindings
    @ orphanFindings
    @ checkRelationshipSymmetry reg byName severity
    @ checkRelationshipKinds reg severity
    |> List.sortWith (fun a b -> String.CompareOrdinal(a.File, b.File))

/// Loads the registry for `opts.App` and validates it against the filesystem.
let validateBoundedContexts (opts: BcValidateOptions) : Result<BcFinding list, string> =
    let severity = opts.Severity |> Option.defaultValue Severity.Blocking

    loadRegistry opts.RepoRoot opts.App
    |> Result.map (fun reg -> validateRegistry opts.RepoRoot reg severity)

/// Renders findings as the CLI's `"{file}: {severity}: {message}"` lines, and
/// reports whether the run exits successfully — any blocking finding fails it.
let renderDddFindings (findings: BcFinding list) : string * bool =
    let sb = StringBuilder()

    for f in findings do
        sb.Append(sprintf "%s: %s: %s\n" f.File (severityCode f.Severity) f.Message)
        |> ignore

    sb.ToString(), not (findings |> List.exists (fun f -> f.Severity = Severity.Blocking))
