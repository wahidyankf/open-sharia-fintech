/// Materializes a contract document from the real repository so the rule
/// engine in `TestContractLayout.fs` can measure a project instead of a
/// hand-authored fixture.
///
/// The fixture corpus pins what each rule rejects; this module supplies the
/// other half the [Target Contract and Project
/// Matrix](../../../../../plans/in-progress/adopt-beavernest-test-automation/tech-docs/target-contract-and-project-matrix.md)
/// requires — `test:layout:validation` reads the project, not a document
/// somebody typed.
///
/// Runner discovery is deliberate: which file a runtime target selects is
/// decided by the runner's own configuration (a vitest `include` list, a
/// `.fsproj` compile list, a Playwright `testDir`), never by the directory a
/// file happens to sit in. That is what lets the layout rule catch a test in
/// `src/` that a runner still picks up, and a test under `tests/unit/` that no
/// runner picks up at all.
///
/// Reader boundary: nothing here writes a tracked byte.
module RhinoCli.Application.TestContractProject

open System
open System.IO
open System.Text
open System.Text.Json
open System.Text.RegularExpressions
open RhinoCli.Application.TestContractJson

/// Directory names a project scan never descends into: build output, package
/// caches, coverage and report artifacts, generated fixtures, and authored
/// educational content. `content` holds sample/course material (e.g.
/// `ayokoding-www`'s Python and TypeScript teaching snippets) that
/// legitimately uses executable-test-shaped filenames — `test_*.py`,
/// `*.test.ts` — without being a real project test. `.features-gen` is
/// playwright-bdd's own gitignored output directory: it emits one
/// `*.feature.spec.js` file per scenario, a real executable-suffix match,
/// purely as a local/CI build artifact that never belongs under `tests/`.
/// Location never decides classification for a genuine authored test, but
/// neither directory is ever a real test's home in this repository.
let private excludedScanDirNames: Set<string> =
    Set.ofList
        [ "node_modules"
          "obj"
          "bin"
          ".git"
          ".nx"
          ".next"
          ".turbo"
          "dist"
          "target"
          "coverage"
          "TestResults"
          "playwright-report"
          "test-results"
          "content"
          ".features-gen" ]

/// The three workspace roots that host an Nx `project.json`, matching the
/// bijection `test-contract registry validate` already compares against.
let private scanRoots = [ "apps"; "libs"; "specs" ]

/// The runtime targets whose selection decides which layer owns a file. The
/// order is the report order, so a twice-selected file always names its
/// selectors in the same sequence.
let private runtimeTargets = [ "test:unit"; "test:integration"; "test:e2e" ]

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------

let private forwardSlashes (value: string) : string = value.Replace('\\', '/')

let private relativeTo (repoRoot: string) (absolute: string) : string =
    forwardSlashes (Path.GetRelativePath(repoRoot, absolute))

let private absoluteOf (repoRoot: string) (relative: string) : string =
    Path.Combine(repoRoot, relative.Replace('/', Path.DirectorySeparatorChar))

/// Joins two repository-relative fragments, dropping a `./` prefix so the
/// result compares equal to a walked path.
let private joinRelative (left: string) (right: string) : string =
    let trimmed = (forwardSlashes right).TrimStart('.', '/')

    if String.IsNullOrEmpty left then trimmed
    else if String.IsNullOrEmpty trimmed then left
    else left.TrimEnd('/') + "/" + trimmed

// ---------------------------------------------------------------------------
// Locating the project
// ---------------------------------------------------------------------------

let rec private projectJsonFiles (dir: string) : string list =
    if not (Directory.Exists dir) then
        []
    else
        let here =
            let candidate = Path.Combine(dir, "project.json")
            if File.Exists candidate then [ candidate ] else []

        let nested =
            Directory.GetDirectories dir
            |> Array.filter (fun child -> not (Set.contains (Path.GetFileName(child: string)) excludedScanDirNames))
            |> Array.toList
            |> List.collect projectJsonFiles

        here @ nested

/// The Nx project name one `project.json` declares, falling back to the
/// containing directory exactly as Nx itself does.
let private declaredName (projectJsonPath: string) : string option =
    let inferred =
        let directory = Path.GetDirectoryName(projectJsonPath: string)

        // Coverage note: `declaredName`'s only caller, `locate` below, only
        // ever calls it with a `path` `projectJsonFiles` returned —
        // `Path.Combine(dir, "project.json")` for a `dir` that
        // `projectJsonFiles` already confirmed exists via `Directory.Exists`
        // moments earlier in the same synchronous scan. `Path.GetDirectoryName`
        // on such a path always yields that same non-empty `dir` back, so
        // this `None` arm is unreachable via the public `locate` entry point.
        if String.IsNullOrEmpty directory then
            None
        else
            Some(Path.GetFileName directory)

    try
        use document = JsonDocument.Parse(File.ReadAllText projectJsonPath)

        match tryProperty document.RootElement "name" with
        | Some element when element.ValueKind = JsonValueKind.String -> Some(element.GetString())
        | _ -> inferred
    with _ ->
        None

/// The repository-relative directory of the `project.json` that declares
/// `project`.
let locate (repoRoot: string) (project: string) : string option =
    scanRoots
    |> List.collect (fun root -> projectJsonFiles (Path.Combine(repoRoot, root)))
    |> List.tryFind (fun path -> declaredName path = Some project)
    |> Option.map (fun path -> relativeTo repoRoot (Path.GetDirectoryName(path: string)))

// ---------------------------------------------------------------------------
// Executable-test classification
// ---------------------------------------------------------------------------

/// Filename shapes that mark an executable test in each language this
/// repository ships. Location never decides, which is what lets the layout
/// rule catch one under `src/` or `tests/support/`.
let private executableSuffixes =
    [ ".test.ts"
      ".test.tsx"
      ".test.js"
      ".test.jsx"
      ".test.mjs"
      ".spec.ts"
      ".spec.tsx"
      ".spec.js"
      ".spec.jsx"
      ".steps.ts"
      ".steps.tsx"
      ".steps.js"
      "Tests.fs"
      "Test.fs"
      "Steps.fs"
      "_test.py"
      "_test.dart"
      "_test.go" ]

let private isExecutableTestFile (fileName: string) : bool =
    let named =
        executableSuffixes
        |> List.exists (fun suffix -> fileName.EndsWith(suffix, StringComparison.Ordinal))

    named
    || (fileName.StartsWith("test_", StringComparison.Ordinal)
        && fileName.EndsWith(".py", StringComparison.Ordinal))

// ---------------------------------------------------------------------------
// Globs
// ---------------------------------------------------------------------------

/// Translates one runner glob into an anchored regex. `**` crosses directory
/// separators, `*` and `?` do not, and a brace list becomes an alternation —
/// the subset every runner configuration in this repository uses.
let private globToRegex (glob: string) : Regex =
    let builder = StringBuilder()
    builder.Append('^') |> ignore
    let text = forwardSlashes glob
    let mutable index = 0

    while index < text.Length do
        let current = text.[index]

        if current = '*' then
            if index + 1 < text.Length && text.[index + 1] = '*' then
                if index + 2 < text.Length && text.[index + 2] = '/' then
                    builder.Append("(?:.*/)?") |> ignore
                    index <- index + 3
                else
                    builder.Append(".*") |> ignore
                    index <- index + 2
            else
                builder.Append("[^/]*") |> ignore
                index <- index + 1
        elif current = '?' then
            builder.Append("[^/]") |> ignore
            index <- index + 1
        elif current = '{' then
            let close = text.IndexOf('}', index)

            if close < 0 then
                builder.Append(Regex.Escape(string<char> current)) |> ignore
                index <- index + 1
            else
                let options = text.Substring(index + 1, close - index - 1).Split(',')

                let rendered = options |> Array.map Regex.Escape |> String.concat "|"

                builder.Append("(?:").Append(rendered).Append(')') |> ignore
                index <- close + 1
        else
            builder.Append(Regex.Escape(string<char> current)) |> ignore
            index <- index + 1

    builder.Append('$') |> ignore
    Regex(builder.ToString(), RegexOptions.None)

// ---------------------------------------------------------------------------
// Walking the project
// ---------------------------------------------------------------------------

let rec private filesUnder (dir: string) : string list =
    if not (Directory.Exists dir) then
        []
    else
        let here = Directory.GetFiles dir |> Array.toList

        let nested =
            Directory.GetDirectories dir
            |> Array.filter (fun child -> not (Set.contains (Path.GetFileName(child: string)) excludedScanDirNames))
            |> Array.toList
            |> List.collect filesUnder

        here @ nested

// ---------------------------------------------------------------------------
// Runner discovery
// ---------------------------------------------------------------------------

/// Splits a shell command into bare tokens, dropping the quoting a command
/// string carries so a path argument compares as a path.
let private tokenize (command: string) : string list =
    command.Split([| ' '; '\t'; '\n' |], StringSplitOptions.RemoveEmptyEntries)
    |> Array.map (fun token -> token.Trim([| '"'; '\''; ';'; ',' |]))
    |> Array.filter (fun token -> token.Length > 0)
    |> Array.toList

/// Strips `//`-to-end-of-line comments from TypeScript source text, tracking
/// single/double/backtick-quoted strings so a comment marker or quote
/// character inside prose never corrupts a real string literal. This
/// repository's own config comments are prose-heavy enough that a bare
/// apostrophe ("project's") or a backtick-quoted mention of a pattern
/// (`` `tests/unit/app/**` ``) each look, to a naive quote-delimited scan of
/// the raw file, like the start or end of a glob string — silently
/// misresolving or dropping the real glob that follows. Stripping comments
/// first removes the prose entirely, so only real code is ever scanned.
let private stripLineComments (text: string) : string =
    let builder = StringBuilder(text.Length)
    let mutable quoteChar: char option = None
    let mutable index = 0

    while index < text.Length do
        let current = text.[index]

        match quoteChar with
        | Some quote ->
            builder.Append(current) |> ignore

            if current = '\\' && index + 1 < text.Length then
                builder.Append(text.[index + 1]) |> ignore
                index <- index + 2
            else
                if current = quote then
                    quoteChar <- None

                index <- index + 1
        | None ->
            if current = '"' || current = '\'' || current = '`' then
                quoteChar <- Some current
                builder.Append(current) |> ignore
                index <- index + 1
            elif current = '/' && index + 1 < text.Length && text.[index + 1] = '/' then
                while index < text.Length && text.[index] <> '\n' do
                    index <- index + 1
            else
                builder.Append(current) |> ignore
                index <- index + 1

    builder.ToString()

/// The string literals inside every `include: [ ... ]` array of a runner
/// configuration, unioned. A vitest multi-project config
/// (`test.projects[]`) repeats `include` once per named project, and
/// `test.coverage.include` is itself a same-named key that can appear
/// anywhere in the file — reading only the first occurrence silently
/// resolves the wrong array (or only one of several) the moment more than
/// one `include:` key exists, which is the ordinary shape once a project
/// splits into named vitest projects.
let private includeGlobs (configText: string) : string list =
    let text = stripLineComments configText

    Regex.Matches(text, @"include\s*:\s*\[(?<body>[^\]]*)\]", RegexOptions.Singleline)
    |> Seq.collect (fun arrayMatch ->
        Regex.Matches(arrayMatch.Groups.["body"].Value, "[\"'`](?<value>[^\"'`]+)[\"'`]")
        |> Seq.map (fun m -> m.Groups.["value"].Value))
    |> Seq.toList

/// The `testDir` a Playwright configuration declares as a string literal.
/// Every `playwright-bdd` project in this repository instead assigns
/// `testDir` from `defineBddConfig({ ... })`'s return value — a bare
/// variable reference, never a literal this can read — so this only ever
/// resolves a plain (non-BDD) Playwright config.
let private playwrightTestDir (configText: string) : string option =
    let found =
        Regex.Match(configText, "testDir\\s*:\\s*[\"'`](?<value>[^\"'`]+)[\"'`]")

    if found.Success then
        Some(found.Groups.["value"].Value)
    else
        None

/// The `steps` glob a `defineBddConfig({ ... })` call declares. This is
/// `playwright-bdd`'s real, authored test surface — the `.steps.ts` files a
/// project owns — as opposed to `testDir`, which names its *generated*
/// output directory (already excluded from scanning via `.features-gen`)
/// and is never a literal in this repository's configs to begin with.
let private playwrightBddStepsGlob (configText: string) : string option =
    let found =
        Regex.Match(stripLineComments configText, "steps\\s*:\\s*[\"'`](?<value>[^\"'`]+)[\"'`]")

    if found.Success then
        Some(found.Groups.["value"].Value)
    else
        None

let private readTextOrEmpty (path: string) : string =
    if File.Exists path then File.ReadAllText path else ""

/// The configuration file a `--config` flag names, else the first default
/// name that exists beside the working directory.
let private resolveConfig
    (repoRoot: string)
    (cwd: string)
    (tokens: string list)
    (defaults: string list)
    : string option =
    let flagged =
        let rec find (remaining: string list) : string option =
            match remaining with
            | flag :: value :: _ when flag = "--config" || flag = "-c" -> Some value
            | token :: rest ->
                if token.StartsWith("--config=", StringComparison.Ordinal) then
                    Some(token.Substring("--config=".Length))
                else
                    find rest
            | [] -> None

        find tokens

    let candidates =
        match flagged with
        | Some value -> [ value ]
        | None -> defaults

    candidates
    |> List.map (fun candidate -> joinRelative cwd candidate)
    |> List.tryFind (fun candidate -> File.Exists(absoluteOf repoRoot candidate))

/// The compile list of one MSBuild test project, resolved against the
/// directory that holds it.
let private compileList (repoRoot: string) (projectFile: string) : string list =
    let directory =
        let raw =
            Path.GetDirectoryName(projectFile.Replace('/', Path.DirectorySeparatorChar))

        forwardSlashes raw

    let text = readTextOrEmpty (absoluteOf repoRoot projectFile)

    Regex.Matches(text, "<Compile\\s+Include=\"(?<value>[^\"]+)\"")
    |> Seq.map (fun m -> joinRelative directory (forwardSlashes m.Groups.["value"].Value))
    |> Seq.toList

/// The `.fsproj`/`.csproj` tokens one `dotnet test` command line names,
/// resolved against `cwd`. Shared by the direct `dotnet test` command shape
/// and the wrapper-script shape below, which apply this to different text
/// (the command itself, versus a script the command invokes).
let private dotnetProjectTokens (repoRoot: string) (cwd: string) (tokens: string list) : string list =
    tokens
    |> List.filter (fun token ->
        token.EndsWith(".fsproj", StringComparison.Ordinal)
        || token.EndsWith(".csproj", StringComparison.Ordinal))
    |> List.map (fun token ->
        if File.Exists(absoluteOf repoRoot token) then
            token
        else
            joinRelative cwd token)

/// Strips this repository's own `${ROOT}/` (or `$ROOT/`) prefix convention —
/// every `scripts/run-integration.sh` wrapper computes `ROOT` as the absolute
/// repository root via `$(dirname "${BASH_SOURCE[0]}")/../../..` and then
/// addresses every path from it, so a `.fsproj` token carrying that prefix is
/// already repository-root-relative once the prefix itself is removed.
let private stripRepoRootPrefix (token: string) : string =
    [ "${ROOT}/"; "$ROOT/" ]
    |> List.tryPick (fun prefix ->
        if token.StartsWith(prefix, StringComparison.Ordinal) then
            Some(token.Substring(prefix.Length))
        else
            None)
    |> Option.defaultValue token

/// Every repository-relative file one command selects.
let private selectionOfCommand (repoRoot: string) (projectRoot: string) (cwd: string) (command: string) : string list =
    let tokens = tokenize command

    if command.Contains "vitest" then
        match resolveConfig repoRoot cwd tokens [ "vitest.config.ts"; "vitest.config.mts"; "vitest.config.js" ] with
        | None -> []
        | Some config ->
            let configDirectory =
                forwardSlashes (Path.GetDirectoryName(config.Replace('/', Path.DirectorySeparatorChar)))

            let patterns =
                includeGlobs (readTextOrEmpty (absoluteOf repoRoot config))
                |> List.map (fun glob -> globToRegex (joinRelative configDirectory glob))

            filesUnder (absoluteOf repoRoot projectRoot)
            |> List.map (relativeTo repoRoot)
            |> List.filter (fun path -> patterns |> List.exists (fun pattern -> pattern.IsMatch path))
    elif command.Contains "playwright" then
        match resolveConfig repoRoot cwd tokens [ "playwright.config.ts"; "playwright.config.js" ] with
        | None -> []
        | Some config ->
            let configDirectory =
                forwardSlashes (Path.GetDirectoryName(config.Replace('/', Path.DirectorySeparatorChar)))

            let configText = readTextOrEmpty (absoluteOf repoRoot config)

            let fromTestDir =
                match playwrightTestDir configText with
                | None -> []
                | Some testDir ->
                    let root = joinRelative configDirectory testDir
                    filesUnder (absoluteOf repoRoot root) |> List.map (relativeTo repoRoot)

            let fromStepsGlob =
                match playwrightBddStepsGlob configText with
                | None -> []
                | Some glob ->
                    let pattern = globToRegex (joinRelative configDirectory glob)

                    filesUnder (absoluteOf repoRoot projectRoot)
                    |> List.map (relativeTo repoRoot)
                    |> List.filter (fun path -> pattern.IsMatch path)

            fromTestDir @ fromStepsGlob |> List.distinct
    elif command.Contains "dotnet test" then
        dotnetProjectTokens repoRoot cwd tokens |> List.collect (compileList repoRoot)
    elif
        tokens
        |> List.exists (fun token -> token.EndsWith(".sh", StringComparison.Ordinal))
    then
        // A docker-compose-orchestrated integration suite (bring up
        // dependencies, export env, run, tear down even on failure) commonly
        // lives behind a wrapper script rather than a direct `dotnet test`
        // command — `apps/organiclever-be/scripts/run-integration.sh` and
        // `apps/ose-be/scripts/run-integration.sh` both do this. The command
        // string itself then names no `.fsproj`, so without reading into the
        // script every file the suite it runs owns is reported unselected.
        // Read the script the same way a `.fsproj`/`.csproj` compile list is
        // read, and apply the identical `dotnet test` token scan to its
        // content — the same rule, just against different text.
        match
            tokens
            |> List.tryFind (fun token -> token.EndsWith(".sh", StringComparison.Ordinal))
        with
        | None -> []
        | Some scriptToken ->
            let scriptPath =
                if File.Exists(absoluteOf repoRoot scriptToken) then
                    scriptToken
                else
                    joinRelative cwd scriptToken

            let scriptText = readTextOrEmpty (absoluteOf repoRoot scriptPath)

            if scriptText.Contains "dotnet test" then
                dotnetProjectTokens repoRoot cwd (tokenize scriptText |> List.map stripRepoRootPrefix)
                |> List.collect (compileList repoRoot)
            else
                []
    else
        []

/// Every command string one target runs, in declaration order.
let private commandsOf (target: JsonElement) : string list =
    match tryProperty target "options" with
    | None -> []
    | Some options ->
        let single =
            match tryProperty options "command" with
            | Some element when element.ValueKind = JsonValueKind.String -> [ element.GetString() ]
            | _ -> []

        let many =
            match tryProperty options "commands" with
            | Some element when element.ValueKind = JsonValueKind.Array ->
                element.EnumerateArray()
                |> Seq.choose (fun entry ->
                    if entry.ValueKind = JsonValueKind.String then
                        Some(entry.GetString())
                    else
                        match tryProperty entry "command" with
                        | Some inner when inner.ValueKind = JsonValueKind.String -> Some(inner.GetString())
                        | _ -> None)
                |> Seq.toList
            | _ -> []

        single @ many

let private cwdOf (projectRoot: string) (target: JsonElement) : string =
    match tryProperty target "options" with
    | None -> projectRoot
    | Some options ->
        match tryProperty options "cwd" with
        | Some element when element.ValueKind = JsonValueKind.String -> forwardSlashes (element.GetString())
        | _ -> projectRoot

/// Which runtime target selects which file, keyed by target in report order.
let private selections
    (repoRoot: string)
    (projectRoot: string)
    (targets: JsonElement option)
    : (string * Set<string>) list =
    match targets with
    | None -> []
    | Some targetsElement ->
        runtimeTargets
        |> List.choose (fun name ->
            match tryProperty targetsElement name with
            | None -> None
            | Some target ->
                let cwd = cwdOf projectRoot target

                let selected =
                    commandsOf target
                    |> List.collect (selectionOfCommand repoRoot projectRoot cwd)
                    |> Set.ofList

                Some(name, selected))

// ---------------------------------------------------------------------------
// Materializing
// ---------------------------------------------------------------------------

/// The layers this project hosts executable tests for: exactly those whose
/// registry adapter is `required` and names this project.
let ownedLayers (row: TestContract.ProjectRow) : TestContractLayout.Layer list =
    let adapters = row.Behavior.Adapters

    [ TestContractLayout.LayerUnit, adapters.Unit
      TestContractLayout.LayerIntegration, adapters.Integration
      TestContractLayout.LayerE2e, adapters.E2e ]
    |> List.filter (fun (_, entry) -> entry.Disposition = TestContract.Required && entry.Project = Some row.Project)
    |> List.map fst

/// The immediate subdirectories of the project's `tests/` root, which is where
/// an unowned-layer placeholder shows up.
let private testsDirectories (repoRoot: string) (projectRoot: string) : string list =
    let tests = absoluteOf repoRoot (projectRoot + "/tests")

    if not (Directory.Exists tests) then
        []
    else
        Directory.GetDirectories tests
        |> Array.map (fun child -> Path.GetFileName(child: string))
        |> Array.filter (fun name -> not (Set.contains name excludedScanDirNames))
        |> Array.toList
        |> List.sort
        |> List.map (fun name -> projectRoot + "/tests/" + name)

/// Builds this project's layout document from its `project.json`, its runner
/// configuration, and the files it ships.
let materialize
    (repoRoot: string)
    (project: string)
    (layers: TestContractLayout.Layer list)
    : Result<TestContractLayout.LayoutDocument, TestContract.Failure> =
    match locate repoRoot project with
    | None -> misuse (sprintf "no project.json under apps/, libs/, or specs/ declares the project \"%s\"" project)
    | Some projectRoot ->
        let projectJson = absoluteOf repoRoot (projectRoot + "/project.json")

        // Coverage note: `locate` (called two lines above to produce
        // `projectRoot`) only matches a project via `declaredName`, which
        // already parses this exact `project.json` with
        // `JsonDocument.Parse` and returns `None` — never `Some project` —
        // on a `JsonException`. Reaching `Some projectRoot` here therefore
        // already proves this file parsed as valid JSON once; re-parsing it
        // synchronously, with no intervening mutation possible in a single
        // test run, cannot then throw. The `with`/`Error failure` arms
        // below are unreachable via the public `materialize` entry point.
        let parsed =
            try
                Ok(JsonDocument.Parse(File.ReadAllText projectJson))
            with :? JsonException as error ->
                Error(TestContract.Misuse(sprintf "%s/project.json is not valid JSON: %s" projectRoot error.Message))

        match parsed with
        | Error failure -> Error failure
        | Ok document ->
            use document = document

            let selectors =
                selections repoRoot projectRoot (tryProperty document.RootElement "targets")

            let files =
                filesUnder (absoluteOf repoRoot projectRoot)
                |> List.map (relativeTo repoRoot)
                |> List.sort
                |> List.map (fun path ->
                    { TestContractLayout.Path = path
                      TestContractLayout.Executable = isExecutableTestFile (Path.GetFileName path)
                      TestContractLayout.SelectedBy =
                        selectors
                        |> List.filter (fun (_, selected) -> Set.contains path selected)
                        |> List.map fst })

            Ok
                { Schema = TestContractLayout.SchemaVersion
                  Case = sprintf "materialized from %s" projectRoot
                  Project = project
                  Owner = project
                  Root = projectRoot
                  OwnedLayers = layers
                  Directories = testsDirectories repoRoot projectRoot
                  Files = files }

/// `materialize` with the owned layers and the behavior owner resolved from
/// the canonical registry.
let materializeLayout
    (repoRoot: string)
    (project: string)
    : Result<TestContractLayout.LayoutDocument, TestContract.Failure> =
    match TestContract.parseRegistry repoRoot with
    | Error failure -> Error failure
    | Ok registry ->
        match registry.Testing with
        | None -> misuse "testing: is absent; the canonical registry must exist before a project is measured"
        | Some testing ->
            match testing.Projects |> List.tryFind (fun row -> row.Project = project) with
            | None -> misuse (sprintf "testing.projects[] declares no row for \"%s\"" project)
            | Some row ->
                materialize repoRoot project (ownedLayers row)
                |> Result.map (fun document ->
                    { document with
                        Owner = defaultArg row.Behavior.Owner project })

// ---------------------------------------------------------------------------
// Manifest policy: does a project-local package.json have a real consumer?
// ---------------------------------------------------------------------------

/// Every other `package.json` under `apps/` or `libs/` that declares `name`
/// as a `dependencies`/`devDependencies` entry, or whose source imports it by
/// name — a real direct consumer, as opposed to Nx project discovery alone.
let private hasDirectConsumer (repoRoot: string) (projectRoot: string) (packageName: string) : bool =
    let otherPackageJsons =
        [ "apps"; "libs" ]
        |> List.collect (fun root -> projectJsonFiles (Path.Combine(repoRoot, root)))
        |> List.map (fun path -> Path.Combine(Path.GetDirectoryName(path: string), "package.json"))
        |> List.filter (fun path ->
            File.Exists path
            && relativeTo repoRoot (Path.GetDirectoryName(path: string)) <> projectRoot)

    let declaredAsDependency =
        otherPackageJsons
        |> List.exists (fun path ->
            try
                use document = JsonDocument.Parse(File.ReadAllText path)

                [ "dependencies"; "devDependencies" ]
                |> List.exists (fun section ->
                    match tryProperty document.RootElement section with
                    | Some element when element.ValueKind = JsonValueKind.Object ->
                        element.EnumerateObject() |> Seq.exists (fun prop -> prop.Name = packageName)
                    | _ -> false)
            with _ ->
                false)

    let importedBySource =
        [ "apps"; "libs" ]
        |> List.collect (fun root -> filesUnder (Path.Combine(repoRoot, root)))
        |> List.filter (fun path ->
            let ext = Path.GetExtension(path: string)

            [ ".ts"; ".tsx"; ".js"; ".jsx" ] |> List.contains ext
            && relativeTo repoRoot path
               |> fun rel -> not (rel.StartsWith(projectRoot + "/", StringComparison.Ordinal)))
        |> List.exists (fun path ->
            try
                (File.ReadAllText path).Contains(packageName)
            with _ ->
                false)

    declaredAsDependency || importedBySource

/// `package-manifest:policy:validation` measured against the real project: no
/// manifest is trivially compliant (native runner owns every command); a
/// present manifest is compliant only when some other project genuinely
/// consumes it.
let validateManifestForProject (repoRoot: string) (project: string) : Result<string, TestContract.Failure> =
    match locate repoRoot project with
    | None -> misuse (sprintf "no project.json under apps/, libs/, or specs/ declares the project \"%s\"" project)
    | Some projectRoot ->
        let manifestPath = absoluteOf repoRoot (projectRoot + "/package.json")

        if not (File.Exists manifestPath) then
            Ok(sprintf "manifest-not-present project=%s owner=%s" project project)
        else
            try
                use document = JsonDocument.Parse(File.ReadAllText manifestPath)

                match tryProperty document.RootElement "name" with
                | None -> misuse (sprintf "%s/package.json has no \"name\"" projectRoot)
                | Some nameElement ->
                    let packageName = nameElement.GetString()

                    if hasDirectConsumer repoRoot projectRoot packageName then
                        Ok(
                            sprintf
                                "manifest-consumer-verified project=%s owner=%s manifest=%s"
                                project
                                project
                                packageName
                        )
                    else
                        Error(
                            TestContract.ContractFailure(
                                sprintf
                                    "manifest-no-direct-consumer project=%s owner=%s manifest=%s"
                                    project
                                    project
                                    packageName
                            )
                        )
            with :? JsonException as error ->
                misuse (sprintf "%s/package.json is not valid JSON: %s" projectRoot error.Message)

// ---------------------------------------------------------------------------
// Coverage policy: does test:coverage enforce a real >= 99% native threshold?
// ---------------------------------------------------------------------------

/// The first `Threshold=<n>`/`--coverage.thresholds.lines=<n>`/`Threshold <n>`
/// style native coverage floor a command string declares.
let private nativeThreshold (command: string) : int option =
    let patterns =
        [ @"[Tt]hreshold=(?<value>\d+)"
          @"thresholds\.lines=(?<value>\d+)"
          @"--Threshold\s+(?<value>\d+)" ]

    patterns
    |> List.tryPick (fun pattern ->
        let found = Regex.Match(command, pattern)

        if found.Success then
            Some(int found.Groups.["value"].Value)
        else
            None)

/// `coverage:policy:validation` measured against the real project: every
/// `test:coverage` command must declare a native line threshold no lower than
/// the repository floor, and the target must not be an echo placeholder.
let validateCoveragePolicyForProject (repoRoot: string) (project: string) : Result<string, TestContract.Failure> =
    match locate repoRoot project with
    | None -> misuse (sprintf "no project.json under apps/, libs/, or specs/ declares the project \"%s\"" project)
    | Some projectRoot ->
        let projectJson = absoluteOf repoRoot (projectRoot + "/project.json")

        // Coverage note: same reasoning as `materialize` above — `locate`
        // already proved this exact `project.json` parses as valid JSON via
        // `declaredName`'s own `JsonDocument.Parse`, so this re-parse cannot
        // throw in a single synchronous call. The `with :? JsonException`
        // arm at the bottom of this function is unreachable via the public
        // `validateCoveragePolicyForProject` entry point.
        try
            use document = JsonDocument.Parse(File.ReadAllText projectJson)

            match tryProperty document.RootElement "targets" with
            | None -> misuse (sprintf "%s/project.json has no targets" projectRoot)
            | Some targets ->
                match tryProperty targets "test:coverage" with
                | None ->
                    Error(
                        TestContract.ContractFailure(
                            sprintf "coverage-target-missing project=%s owner=%s" project project
                        )
                    )
                | Some target ->
                    let commands = commandsOf target

                    if
                        commands
                        |> List.exists (fun c -> c.TrimStart().StartsWith("echo", StringComparison.Ordinal))
                    then
                        Error(
                            TestContract.ContractFailure(
                                sprintf "coverage-echo-placeholder project=%s owner=%s" project project
                            )
                        )
                    else
                        match commands |> List.tryPick nativeThreshold with
                        | None ->
                            Error(
                                TestContract.ContractFailure(
                                    sprintf "coverage-threshold-undeclared project=%s owner=%s" project project
                                )
                            )
                        | Some found when found < TestContract.MinimumLine ->
                            Error(
                                TestContract.ContractFailure(
                                    sprintf
                                        "coverage-below-floor project=%s owner=%s threshold=%d floor=%d"
                                        project
                                        project
                                        found
                                        TestContract.MinimumLine
                                )
                            )
                        | Some found ->
                            Ok(sprintf "coverage-policy-valid project=%s owner=%s threshold=%d" project project found)
        with :? JsonException as error ->
            misuse (sprintf "%s/project.json is not valid JSON: %s" projectRoot error.Message)

/// `test-contract layout validate --project=<project>` end to end: materialize
/// against the canonical registry, run the same rule engine a fixture
/// document runs through, then render the report the fixture path renders.
let validateLayoutForProject (repoRoot: string) (project: string) : Result<string, TestContract.Failure> =
    materializeLayout repoRoot project
    |> Result.bind TestContractLayout.validateDocument
    |> Result.map TestContractLayout.formatReport

// ---------------------------------------------------------------------------
// BDD coverage: does test:behavior:coverage:<adapter> prove the real project?
// ---------------------------------------------------------------------------

let private adapterEntryOf
    (adapters: TestContract.Adapters)
    (adapter: TestContractBdd.Adapter)
    : TestContract.AdapterEntry =
    match adapter with
    | TestContractBdd.AdapterUnit -> adapters.Unit
    | TestContractBdd.AdapterIntegration -> adapters.Integration
    | TestContractBdd.AdapterE2e -> adapters.E2e

let private bddDisposition (disposition: TestContract.Disposition) : TestContractBdd.BddDisposition =
    match disposition with
    | TestContract.Required -> TestContractBdd.BddRequired
    | TestContract.Delegated -> TestContractBdd.BddDelegated
    | TestContract.Inapplicable -> TestContractBdd.BddInapplicable

/// A non-owner row may leave `behavior.corpus` empty and inherit the
/// glob(s) its `behavior.owner` resolves — the same inheritance
/// `behaviorFindings` already permits in `TestContract.fs`.
let private resolveCorpus (testing: TestContract.TestingRegistry) (row: TestContract.ProjectRow) : string list =
    if not (List.isEmpty row.Behavior.Corpus) then
        row.Behavior.Corpus
    else
        match row.Behavior.Owner with
        | Some owner when owner <> row.Project ->
            testing.Projects
            |> List.tryFind (fun candidate -> candidate.Project = owner)
            |> Option.map (fun ownerRow -> ownerRow.Behavior.Corpus)
            |> Option.defaultValue []
        | _ -> []

/// Strips every trailing wildcard path segment from a corpus glob, leaving
/// the base directory `Specs.coverageWalkFeatureFiles` can walk. A glob with
/// no wildcard segment names a directory outright and is returned unchanged.
let private corpusBaseDir (glob: string) : string =
    let isWildcard (segment: string) : bool =
        segment.Contains '*' || segment.Contains '?' || segment.Contains '{'

    let kept =
        (forwardSlashes glob).Split('/')
        |> Array.rev
        |> Array.skipWhile isWildcard
        |> Array.rev

    String.concat "/" kept

/// Drops the synthetic `(Background)` scenario `Specs.parseFeatureContent`
/// prepends, folding its steps onto every real scenario's own steps instead.
/// A Background has no `When`/`Then` of its own, so leaving it as a
/// freestanding scenario would always fail the keyword-structure check below,
/// and its steps still need a binding exactly once per real scenario they
/// run ahead of.
let private foldBackground (scenarios: Specs.ParsedScenario list) : Specs.ParsedScenario list =
    match scenarios with
    | background :: rest when background.Title = "(Background)" ->
        rest
        |> List.map (fun scenario ->
            { scenario with
                Steps = background.Steps @ scenario.Steps })
    | _ -> scenarios

/// One step rendered `<Keyword> <text>`, the exact shape
/// `TestContractBdd.BddScenario.Steps` and its fixture corpus already use as
/// a step's display identity.
let private stepLine (step: Specs.ParsedStep) : string = sprintf "%s %s" step.Keyword step.Text

/// The example count a scenario declares: 1 for a plain scenario, the
/// expanded `Examples:` row count for a scenario outline.
let private examplesOf (scenario: Specs.ParsedScenario) : int =
    match scenario.Steps with
    | [] -> 1
    | steps ->
        let widest = steps |> List.map (fun step -> List.length step.Variants) |> List.max
        max 1 widest

/// The real, substituted step text a given 1-based example actually
/// exercises: a scenario outline's `example`th expansion, or the plain step
/// text when the scenario declares no variants of its own (an ordinary
/// scenario, or an index a malformed outline never expanded).
let private expandedTextOf (step: Specs.ParsedStep) (example: int) : string =
    if List.isEmpty step.Variants || example < 1 || example > List.length step.Variants then
        step.Text
    else
        step.Variants.[example - 1]

/// The real candidate count a step's *expanded* text resolves against the
/// driver's step matcher — 0 for `bdd-undefined-binding`, 1 for a bound step.
/// This is capped at a boolean rather than counting every matching entry:
/// TickSpec is invoked per scenario against one explicit step-definition
/// class (`StepDefinitions([| typeof<XSteps> |])`, never a process-wide
/// registry), so this repository's own convention is many classes
/// independently, legitimately defining the identical generic step text
/// (`` `Then the command exits successfully` `` alone is real in 16 files) —
/// counting every entry globally would report each as `bdd-ambiguous-binding`
/// though none of them can ever collide at runtime. `StepMatcher.Matches`
/// already answers the question this reader needs: is the text bound
/// *somewhere* in the driver's own project tree.
///
/// Tried against `expandedText` (the example's substituted value) first, then
/// `rawText` (the step's own un-substituted `<placeholder>` template text) —
/// the same OR-fallback `Specs.stepCovered` already applies elsewhere. A
/// Scenario Outline driver can bind either form: TickSpec-style drivers bind
/// per substituted value, while `@amiceli/vitest-cucumber`'s `ScenarioOutline`
/// API binds only the raw template text and never sees any one example's
/// substitution.
let private candidateCount (matcher: Specs.StepMatcher) (expandedText: string) (rawText: string) : int =
    if matcher.Matches expandedText || matcher.Matches rawText then
        1
    else
        0

/// The sentinel prefix a synthesized orphan-binding key carries. No real
/// corpus key can ever start with it — a feature path is always
/// repository-relative under the corpus root, never this literal token — so
/// `TestContractBdd`'s own unused-binding pass reports every orphan step
/// implementation as `bdd-unused-binding` with no change to that module.
[<Literal>]
let private OrphanKeyPrefix = "unbound-driver-entry"

let private orphanBindingKey (orphan: Specs.OrphanStepImpl) : string =
    sprintf "%s|%s|%s|%s" OrphanKeyPrefix orphan.File orphan.MatcherKind orphan.MatcherText

/// The `Specs.TestLevel` a BDD adapter measures against a scenario's own
/// `@unit`/`@integration`/`@e2e` tags.
let private testLevelOfAdapter (adapter: TestContractBdd.Adapter) : Specs.TestLevel =
    match adapter with
    | TestContractBdd.AdapterUnit -> Specs.Unit
    | TestContractBdd.AdapterIntegration -> Specs.Integration
    | TestContractBdd.AdapterE2e -> Specs.E2e

/// Whether a scenario's own level tags (looked up by title from
/// `Specs.extractScenarioSpecs`) obligate the given adapter to bind it. A
/// scenario absent from the lookup, or carrying no level tags at all, is
/// measured by every adapter — the conservative default matching today's
/// untagged-corpus behavior, never silently narrowing what counts.
let private scenarioAppliesToLevel
    (levelTagsByTitle: Map<string, Set<Specs.TestLevel>>)
    (level: Specs.TestLevel)
    (scenario: Specs.ParsedScenario)
    : bool =
    match Map.tryFind scenario.Title levelTagsByTitle with
    | None -> true
    | Some tags when Set.isEmpty tags -> true
    | Some tags -> Set.contains level tags

/// Builds the `BddFeature` list and the synthesized `bindings` a real
/// project's corpus and driver resolve to. Each real step instance
/// contributes its own binding key exactly as many times as it has real
/// candidates, so `TestContractBdd.validateDocument` reproduces every one of
/// the Static Adapter Contract's findings — undefined, ambiguous, unused,
/// uncovered example/scenario/feature, and the exact-integer counts — with no
/// change to that module's own rule engine.
let private materializeCorpus
    (repoRoot: string)
    (corpusGlobs: string list)
    (matcher: Specs.StepMatcher)
    (level: Specs.TestLevel)
    : TestContractBdd.BddFeature list * string list =
    let featureScenariosAll =
        corpusGlobs
        |> List.collect (fun glob -> Specs.coverageWalkFeatureFiles (absoluteOf repoRoot (corpusBaseDir glob)) [])
        |> List.map (relativeTo repoRoot)
        |> List.distinct
        |> List.sort
        |> List.map (fun relativePath ->
            let scenarios =
                Specs.parseFeatureFile (absoluteOf repoRoot relativePath)
                |> foldBackground
                |> List.filter (fun scenario -> not scenario.IsWip)

            relativePath, scenarios)

    // The level-filtered view drives what this adapter is required to cover
    // (`features`/`bindings`); orphan-binding detection stays against the
    // unfiltered `featureScenariosAll` below, since a driver binding a step
    // text that a sibling adapter's scenarios also use is not orphaned.
    let featureScenarios =
        featureScenariosAll
        |> List.map (fun (relativePath, scenarios) ->
            let levelTagsByTitle =
                Specs.extractScenarioSpecs (absoluteOf repoRoot relativePath) relativePath
                |> List.map (fun spec -> spec.Title, spec.LevelTags)
                |> Map.ofList

            relativePath, scenarios |> List.filter (scenarioAppliesToLevel levelTagsByTitle level))

    let features =
        featureScenarios
        |> List.choose (fun (relativePath, scenarios) ->
            if List.isEmpty scenarios then
                None
            else
                Some
                    { TestContractBdd.Path = relativePath
                      TestContractBdd.Scenarios =
                        scenarios
                        |> List.map (fun scenario ->
                            { TestContractBdd.Name = scenario.Title
                              TestContractBdd.Examples = examplesOf scenario
                              TestContractBdd.Steps = scenario.Steps |> List.map stepLine }) })

    let bindings =
        [ for relativePath, scenarios in featureScenarios do
              for scenario in scenarios do
                  for example in 1 .. examplesOf scenario do
                      for step in scenario.Steps do
                          let candidates = candidateCount matcher (expandedTextOf step example) step.Text
                          let key = sprintf "%s|%s|%d|%s" relativePath scenario.Title example (stepLine step)

                          for _ in 1..candidates do
                              yield key ]

    let allGherkinTexts =
        [ for _, scenarios in featureScenariosAll do
              for scenario in scenarios do
                  for step in scenario.Steps do
                      yield step.Text
                      yield! step.Variants ]

    let orphanBindings =
        Specs.checkOrphanStepImpls matcher allGherkinTexts repoRoot
        |> List.map orphanBindingKey

    features, bindings @ orphanBindings

/// Materializes one adapter's BDD document from the canonical registry and
/// the real repository. `Inapplicable` builds no denominator — the
/// registry's own governed reason is the evidence, mirroring how the fixture
/// reader treats it. `Required` measures the named project's own tree;
/// `Delegated` measures the reciprocal project's tree that
/// `adapterFindings`'s own registry-validation rule already requires to
/// `Required`-host this same adapter level.
let private materializeBdd
    (repoRoot: string)
    (project: string)
    (adapter: TestContractBdd.Adapter)
    : Result<TestContractBdd.BddDocument, TestContract.Failure> =
    match TestContract.parseRegistry repoRoot with
    | Error failure -> Error failure
    | Ok registry ->
        match registry.Testing with
        | None -> misuse "testing: is absent; the canonical registry must exist before a project is measured"
        | Some testing ->
            match testing.Projects |> List.tryFind (fun row -> row.Project = project) with
            | None -> misuse (sprintf "testing.projects[] declares no row for \"%s\"" project)
            | Some row ->
                let entry = adapterEntryOf row.Behavior.Adapters adapter
                let disposition = bddDisposition entry.Disposition
                let owner = defaultArg row.Behavior.Owner project

                let baseDocument =
                    { TestContractBdd.Schema = TestContractBdd.SchemaVersion
                      TestContractBdd.Case = sprintf "materialized from %s" project
                      TestContractBdd.Project = project
                      TestContractBdd.Owner = owner
                      TestContractBdd.Adapter = adapter
                      TestContractBdd.Disposition = disposition
                      TestContractBdd.Driver = entry.Driver
                      TestContractBdd.Reason = entry.Reason
                      TestContractBdd.Corpus = TestContractBdd.ExplicitCorpus([], []) }

                match disposition with
                | TestContractBdd.BddInapplicable -> Ok { baseDocument with Driver = None }
                | TestContractBdd.BddRequired
                | TestContractBdd.BddDelegated ->
                    match entry.Driver with
                    | None ->
                        Error(
                            TestContract.ContractFailure(
                                sprintf
                                    "bdd-driver-undeclared project=%s owner=%s adapter=%s"
                                    project
                                    owner
                                    (TestContractBdd.adapterName adapter)
                            )
                        )
                    | Some _ ->
                        let hostProject = defaultArg entry.Project project

                        match locate repoRoot hostProject with
                        | None ->
                            misuse (
                                sprintf
                                    "no project.json under apps/, libs/, or specs/ declares the project \"%s\""
                                    hostProject
                            )
                        | Some hostRoot ->
                            // Resolved against `hostProject`'s own row, not the originally
                            // requested `row` — for a delegated adapter these differ, and the
                            // delegate's own row is free to declare a broader corpus than its
                            // owner (e.g. a second, in-situ binding of another project's Gherkin).
                            // `resolveCorpus`'s owner-inherit branch already makes this a no-op
                            // for every project whose delegate row leaves `corpus` empty (the
                            // repo-wide default), so this only changes behavior where a delegate
                            // row's own corpus genuinely diverges from its owner's.
                            let corpusRow =
                                if hostProject = row.Project then
                                    row
                                else
                                    testing.Projects
                                    |> List.tryFind (fun candidate -> candidate.Project = hostProject)
                                    |> Option.defaultValue row

                            let corpusGlobs = resolveCorpus testing corpusRow

                            if List.isEmpty corpusGlobs then
                                Error(
                                    TestContract.ContractFailure(
                                        sprintf
                                            "bdd-corpus-empty project=%s owner=%s adapter=%s"
                                            project
                                            owner
                                            (TestContractBdd.adapterName adapter)
                                    )
                                )
                            else
                                let matcher = Specs.extractAllStepTexts (absoluteOf repoRoot hostRoot) []

                                let features, bindings =
                                    materializeCorpus repoRoot corpusGlobs matcher (testLevelOfAdapter adapter)

                                Ok
                                    { baseDocument with
                                        Corpus = TestContractBdd.ExplicitCorpus(features, bindings) }

/// `test-contract bdd validate --project=<project> --adapter=<adapter>` end
/// to end: materialize against the canonical registry and the real corpus
/// and driver it names, run the same rule engine a fixture document runs
/// through, then render the report the fixture path renders.
let validateBehaviorCoverageForProject
    (repoRoot: string)
    (project: string)
    (adapter: TestContractBdd.Adapter)
    : Result<string, TestContract.Failure> =
    materializeBdd repoRoot project adapter
    |> Result.bind TestContractBdd.validateDocument
    |> Result.map TestContractBdd.formatReport
