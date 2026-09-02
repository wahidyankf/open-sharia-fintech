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
/// caches, coverage and report artifacts.
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
          "test-results" ]

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

/// The string literals inside the first `include: [ ... ]` array of a runner
/// configuration.
let private includeGlobs (configText: string) : string list =
    let arrayMatch =
        Regex.Match(configText, @"include\s*:\s*\[(?<body>[^\]]*)\]", RegexOptions.Singleline)

    if not arrayMatch.Success then
        []
    else
        Regex.Matches(arrayMatch.Groups.["body"].Value, "[\"'`](?<value>[^\"'`]+)[\"'`]")
        |> Seq.map (fun m -> m.Groups.["value"].Value)
        |> Seq.toList

/// The `testDir` a Playwright configuration declares.
let private playwrightTestDir (configText: string) : string option =
    let found =
        Regex.Match(configText, "testDir\\s*:\\s*[\"'`](?<value>[^\"'`]+)[\"'`]")

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

            match playwrightTestDir (readTextOrEmpty (absoluteOf repoRoot config)) with
            | None -> []
            | Some testDir ->
                let root = joinRelative configDirectory testDir

                filesUnder (absoluteOf repoRoot root) |> List.map (relativeTo repoRoot)
    elif command.Contains "dotnet test" then
        tokens
        |> List.filter (fun token ->
            token.EndsWith(".fsproj", StringComparison.Ordinal)
            || token.EndsWith(".csproj", StringComparison.Ordinal))
        |> List.map (fun token ->
            if File.Exists(absoluteOf repoRoot token) then
                token
            else
                joinRelative cwd token)
        |> List.collect (compileList repoRoot)
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
