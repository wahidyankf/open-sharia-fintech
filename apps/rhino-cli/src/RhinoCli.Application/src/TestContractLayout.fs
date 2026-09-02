/// The physical test-layout rule: an executable test lives in exactly one
/// layer directory of the project that owns it, and exactly one runtime target
/// selects it, as specified by [Target Contract and Project
/// Matrix](../../../../../plans/in-progress/adopt-beavernest-test-automation/tech-docs/target-contract-and-project-matrix.md).
///
/// A layer directory exists only when the project owns that layer, so a
/// dedicated E2E project has `tests/e2e/` and no empty unit/integration
/// placeholders. `src/**`, a generic `test/`, `__tests__/`, `tests/support/`,
/// and `tests/fixtures/` never hold an executable test.
///
/// Reader boundary: nothing here writes a tracked byte. A fixture document is
/// read into memory only; `TestContract.fs` remains the typed registry facade
/// and carries no layout logic.
module RhinoCli.Application.TestContractLayout

open System
open System.IO
open System.Text.Json
open RhinoCli.Application.TestContractJson

/// The three layers a project may own. Anything else in `tests/` is
/// non-executable support material.
type Layer =
    | LayerUnit
    | LayerIntegration
    | LayerE2e

/// One file the project ships, and every runtime target that selects it.
/// `Executable` distinguishes a test from fixture data or a shared helper.
type LayoutFile =
    { Path: string
      Executable: bool
      SelectedBy: string list }

type LayoutDocument =
    { Schema: string
      Case: string
      Project: string
      Owner: string
      Root: string
      OwnedLayers: Layer list
      Directories: string list
      Files: LayoutFile list }

type LayoutReport =
    { Project: string
      Owner: string
      OwnedLayers: Layer list
      ExecutableFiles: int }

[<Literal>]
let SchemaVersion = "ose-test-contract-layout-fixture/v1"

[<Literal>]
let FixtureRoot = "apps/rhino-cli/tests/unit/Fixtures/TestContract/Layout"

let layerName (layer: Layer) : string =
    match layer with
    | LayerUnit -> "unit"
    | LayerIntegration -> "integration"
    | LayerE2e -> "e2e"

/// Directories that may exist under `tests/` but must never hold an executable
/// test.
let private nonExecutableDirectories = [ "support"; "fixtures" ]

/// Directory names that are never a valid home for an executable test,
/// wherever they appear in the project.
let private forbiddenRoots = [ "src"; "test"; "__tests__" ]

// ---------------------------------------------------------------------------
// Parsing
// ---------------------------------------------------------------------------

let private parseLayer (raw: string) : Result<Layer, TestContract.Failure> =
    match raw with
    | "unit" -> Ok LayerUnit
    | "integration" -> Ok LayerIntegration
    | "e2e" -> Ok LayerE2e
    | other -> misuse (sprintf "the layer \"%s\" must be unit, integration, or e2e" other)

let private parseFile (element: JsonElement) : Result<LayoutFile, TestContract.Failure> =
    result {
        do! closedKeys element [ "path"; "executable"; "selectedBy" ] "a layout file"
        let! path = requiredString element "path"
        let! path = checkedRelativePath "the file path" path
        let! executable = requiredBool element "executable"
        let! selectedBy = stringArray element "selectedBy"

        match duplicates selectedBy with
        | [] ->
            return
                { Path = path
                  Executable = executable
                  SelectedBy = selectedBy }
        | repeated ->
            return! misuse (sprintf "the file \"%s\" repeats the target %s" path (String.concat ", " repeated))
    }

let parseDocument (text: string) : Result<LayoutDocument, TestContract.Failure> =
    let parsed =
        try
            Ok(JsonDocument.Parse(text))
        with :? JsonException as error ->
            Error(TestContract.Misuse(sprintf "the fixture is not valid JSON: %s" error.Message))

    match parsed with
    | Error failure -> Error failure
    | Ok document ->
        use document = document
        let root = document.RootElement

        if root.ValueKind <> JsonValueKind.Object then
            misuse "the fixture must be a JSON object"
        else
            result {
                do!
                    closedKeys
                        root
                        [ "schema"
                          "case"
                          "project"
                          "owner"
                          "root"
                          "ownedLayers"
                          "directories"
                          "files" ]
                        "the layout fixture"

                let! schema = requiredString root "schema"

                do!
                    if schema = SchemaVersion then
                        Ok()
                    else
                        Error(
                            TestContract.Misuse(sprintf "\"schema\" must be \"%s\", found \"%s\"" SchemaVersion schema)
                        )

                let! case = requiredString root "case"
                let! project = requiredString root "project"
                let! owner = requiredString root "owner"
                let! projectRoot = requiredString root "root"
                let! projectRoot = checkedRelativePath "the project root" projectRoot
                let! layerNames = stringArray root "ownedLayers"

                do!
                    match duplicates layerNames with
                    | [] -> Ok()
                    | repeated -> misuse (sprintf "\"ownedLayers\" repeats %s" (String.concat ", " repeated))

                let! ownedLayers = layerNames |> traverse parseLayer

                do!
                    if List.isEmpty ownedLayers then
                        misuse "\"ownedLayers\" must declare at least one layer"
                    else
                        Ok()

                let! directories = stringArray root "directories"
                let! directories = directories |> traverse (checkedRelativePath "a directory")
                let! fileElements = requiredArray root "files"
                let! files = fileElements |> traverse parseFile

                do!
                    match duplicates (files |> List.map (fun file -> file.Path)) with
                    | [] -> Ok()
                    | repeated -> misuse (sprintf "\"files\" repeats %s" (String.concat ", " repeated))

                return
                    { Schema = schema
                      Case = case
                      Project = project
                      Owner = owner
                      Root = projectRoot
                      OwnedLayers = ownedLayers
                      Directories = directories
                      Files = files }
            }

let loadDocument (repoRoot: string) (fixturePath: string) : Result<LayoutDocument, TestContract.Failure> =
    if isAbsolutePath fixturePath then
        misuse (sprintf "the fixture path \"%s\" must not be an absolute path" fixturePath)
    elif hasTraversal fixturePath then
        misuse (sprintf "the fixture path \"%s\" must not contain a traversal segment" fixturePath)
    else
        let full = Path.Combine(repoRoot, FixtureRoot, fixturePath)

        if not (File.Exists full) then
            misuse (sprintf "the fixture \"%s\" was not found under %s" fixturePath FixtureRoot)
        else
            parseDocument (File.ReadAllText full)

// ---------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------

let private segments (path: string) : string list =
    path.Replace('\\', '/').Split('/') |> List.ofArray

/// The path a file must sit under to belong to `layer` of this project.
let private layerPrefix (document: LayoutDocument) (layer: Layer) : string =
    sprintf "%s/tests/%s/" (document.Root.TrimEnd('/')) (layerName layer)

let private testsPrefix (document: LayoutDocument) : string =
    sprintf "%s/tests/" (document.Root.TrimEnd('/'))

let private finding (code: string) (document: LayoutDocument) (item: string) (detail: string) : string =
    sprintf "%s project=%s owner=%s item=%s %s" code document.Project document.Owner item detail

/// The one place a file is tested against the project's owned layers.
let private owningLayer (document: LayoutDocument) (file: LayoutFile) : Layer option =
    document.OwnedLayers
    |> List.tryFind (fun layer -> file.Path.StartsWith(layerPrefix document layer, StringComparison.Ordinal))

let private forbiddenSegment (document: LayoutDocument) (file: LayoutFile) : string option =
    let relative =
        let root = document.Root.TrimEnd('/') + "/"

        if file.Path.StartsWith(root, StringComparison.Ordinal) then
            file.Path.Substring(root.Length)
        else
            file.Path

    let parts = segments relative

    match parts |> List.tryFind (fun part -> List.contains part forbiddenRoots) with
    | Some part -> Some part
    | None ->
        // `tests/support/` and `tests/fixtures/` are legal directories but never
        // hold an executable test.
        match parts with
        | "tests" :: second :: _ when List.contains second nonExecutableDirectories -> Some(sprintf "tests/%s" second)
        | _ -> None

let private validateFile (document: LayoutDocument) (file: LayoutFile) : Result<unit, TestContract.Failure> =
    if not file.Executable then
        Ok()
    else
        match forbiddenSegment document file with
        | Some part ->
            Error(
                TestContract.ContractFailure(
                    finding "layout-test-in-forbidden-directory" document file.Path (sprintf "directory=%s" part)
                )
            )
        | None ->
            if not (file.Path.StartsWith(testsPrefix document, StringComparison.Ordinal)) then
                Error(
                    TestContract.ContractFailure(
                        finding
                            "layout-test-outside-tests-root"
                            document
                            file.Path
                            (sprintf "expected=%s*" (testsPrefix document))
                    )
                )
            else
                match owningLayer document file with
                | None ->
                    Error(
                        TestContract.ContractFailure(
                            finding
                                "layout-layer-not-owned"
                                document
                                file.Path
                                (sprintf "owned=%s" (document.OwnedLayers |> List.map layerName |> String.concat ","))
                        )
                    )
                | Some _ ->
                    match file.SelectedBy with
                    | [] ->
                        Error(
                            TestContract.ContractFailure(
                                finding "layout-file-unselected" document file.Path "selectors=0"
                            )
                        )
                    | [ _ ] -> Ok()
                    | many ->
                        Error(
                            TestContract.ContractFailure(
                                finding
                                    "layout-file-selected-twice"
                                    document
                                    file.Path
                                    (sprintf "selectors=%d targets=%s" (List.length many) (String.concat "," many))
                            )
                        )

/// A `tests/<layer>/` directory for a layer the project does not own is the
/// empty placeholder the contract forbids.
let private validateDirectory (document: LayoutDocument) (directory: string) : Result<unit, TestContract.Failure> =
    let prefix = testsPrefix document

    if not (directory.StartsWith(prefix, StringComparison.Ordinal)) then
        Ok()
    else
        let tail = directory.Substring(prefix.Length).TrimEnd('/')

        match segments tail with
        | [ name ] when List.contains name nonExecutableDirectories -> Ok()
        | [ name ] ->
            match parseLayer name with
            | Error _ -> Ok()
            | Ok layer when List.contains layer document.OwnedLayers -> Ok()
            | Ok _ ->
                Error(
                    TestContract.ContractFailure(
                        finding
                            "layout-placeholder-directory"
                            document
                            directory
                            (sprintf "owned=%s" (document.OwnedLayers |> List.map layerName |> String.concat ","))
                    )
                )
        | _ -> Ok()

/// An owned layer with no executable test is a claim the project does not keep.
let private validateOwnedLayer (document: LayoutDocument) (layer: Layer) : Result<unit, TestContract.Failure> =
    let prefix = layerPrefix document layer

    let populated =
        document.Files
        |> List.exists (fun file -> file.Executable && file.Path.StartsWith(prefix, StringComparison.Ordinal))

    if populated then
        Ok()
    else
        Error(
            TestContract.ContractFailure(
                finding "layout-owned-layer-empty" document (layerName layer) (sprintf "expected=%s*" prefix)
            )
        )

let validateDocument (document: LayoutDocument) : Result<LayoutReport, TestContract.Failure> =
    result {
        do! document.Files |> traverse (validateFile document) |> Result.map ignore

        do!
            document.Directories
            |> traverse (validateDirectory document)
            |> Result.map ignore

        do!
            document.OwnedLayers
            |> traverse (validateOwnedLayer document)
            |> Result.map ignore

        return
            { Project = document.Project
              Owner = document.Owner
              OwnedLayers = document.OwnedLayers
              ExecutableFiles = document.Files |> List.filter (fun file -> file.Executable) |> List.length }
    }

let formatReport (report: LayoutReport) : string =
    sprintf
        "native-layout-valid project=%s owner=%s layers=%s executable=%d"
        report.Project
        report.Owner
        (report.OwnedLayers |> List.map layerName |> String.concat ",")
        report.ExecutableFiles
