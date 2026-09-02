/// The project-local `package.json` policy: a manifest is either a real direct
/// boundary with a named consumer, or it is absent and `project.json` owns the
/// commands, as specified by [Target Contract and Project
/// Matrix](../../../../../plans/in-progress/adopt-beavernest-test-automation/tech-docs/target-contract-and-project-matrix.md).
///
/// "Nx project discovery", "convenient npm script", and "compatibility proxy"
/// are named in the contract as *not* valid consumers, so they are rejected by
/// exact phrase rather than by judgment. A retained manifest whose only script
/// forwards to the same project's Nx target is the proxy the policy exists to
/// remove.
///
/// Reader boundary: nothing here writes a tracked byte. A fixture document is
/// read into memory only; `TestContract.fs` remains the typed registry facade
/// and carries no manifest logic.
module RhinoCli.Application.TestContractManifest

open System
open System.IO
open System.Text.Json
open RhinoCli.Application.TestContractJson

/// The three bounded groups Phase 0 inventoried. A project outside them is
/// unclassified, which is itself a failure.
type ManifestGroup =
    | WebApplication
    | DedicatedE2e
    | TypeScriptLibrary

type Disposition =
    | Retained
    | Removed

type ManifestScript = { Name: string; Command: string }

type ManifestDocument =
    { Schema: string
      Case: string
      Project: string
      Owner: string
      Group: ManifestGroup
      Disposition: Disposition
      ManifestPath: string option
      Consumer: string option
      RequiredFields: string list
      Verification: string option
      Scripts: ManifestScript list
      Commands: string list }

type ManifestReport =
    { Project: string
      Owner: string
      Group: ManifestGroup
      Disposition: Disposition
      Consumer: string option }

[<Literal>]
let SchemaVersion = "ose-test-contract-manifest-fixture/v1"

[<Literal>]
let FixtureRoot = "apps/rhino-cli/tests/unit/Fixtures/TestContract/Manifest"

let groupName (group: ManifestGroup) : string =
    match group with
    | WebApplication -> "web-application"
    | DedicatedE2e -> "dedicated-e2e"
    | TypeScriptLibrary -> "typescript-library"

let dispositionName (disposition: Disposition) : string =
    match disposition with
    | Retained -> "retained"
    | Removed -> "removed"

/// Consumers the contract names as invalid, matched case-insensitively so a
/// capitalisation change cannot slip one through.
let private invalidConsumers =
    [ "nx project discovery"; "convenient npm script"; "compatibility proxy" ]

// ---------------------------------------------------------------------------
// Parsing
// ---------------------------------------------------------------------------

let private parseGroup (raw: string) : Result<ManifestGroup, TestContract.Failure> =
    match raw with
    | "web-application" -> Ok WebApplication
    | "dedicated-e2e" -> Ok DedicatedE2e
    | "typescript-library" -> Ok TypeScriptLibrary
    | other -> misuse (sprintf "the group \"%s\" must be web-application, dedicated-e2e, or typescript-library" other)

let private parseDisposition (raw: string) : Result<Disposition, TestContract.Failure> =
    match raw with
    | "retained" -> Ok Retained
    | "removed" -> Ok Removed
    | other -> misuse (sprintf "the disposition \"%s\" must be retained or removed" other)

let private parseScript (element: JsonElement) : Result<ManifestScript, TestContract.Failure> =
    result {
        do! closedKeys element [ "name"; "command" ] "a manifest script"
        let! name = requiredString element "name"
        let! command = requiredString element "command"
        return { Name = name; Command = command }
    }

let parseDocument (text: string) : Result<ManifestDocument, TestContract.Failure> =
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
                          "group"
                          "disposition"
                          "manifestPath"
                          "consumer"
                          "requiredFields"
                          "verification"
                          "scripts"
                          "commands" ]
                        "the manifest fixture"

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
                let! groupRaw = requiredString root "group"
                let! group = parseGroup groupRaw
                let! dispositionRaw = requiredString root "disposition"
                let! disposition = parseDisposition dispositionRaw
                let! manifestPath = nullableString root "manifestPath"

                let! manifestPath =
                    match manifestPath with
                    | None -> Ok None
                    | Some path -> checkedRelativePath "the manifest path" path |> Result.map Some

                let! consumer = nullableString root "consumer"
                let! requiredFields = stringArray root "requiredFields"
                let! verification = nullableString root "verification"
                let! scriptElements = requiredArray root "scripts"
                let! scripts = scriptElements |> traverse parseScript
                let! commands = stringArray root "commands"

                do!
                    match duplicates (scripts |> List.map (fun script -> script.Name)) with
                    | [] -> Ok()
                    | repeated -> misuse (sprintf "\"scripts\" repeats %s" (String.concat ", " repeated))

                return
                    { Schema = schema
                      Case = case
                      Project = project
                      Owner = owner
                      Group = group
                      Disposition = disposition
                      ManifestPath = manifestPath
                      Consumer = consumer
                      RequiredFields = requiredFields
                      Verification = verification
                      Scripts = scripts
                      Commands = commands }
            }

let loadDocument (repoRoot: string) (fixturePath: string) : Result<ManifestDocument, TestContract.Failure> =
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

let private finding (code: string) (document: ManifestDocument) (item: string) (detail: string) : string =
    sprintf
        "%s project=%s owner=%s group=%s item=%s %s"
        code
        document.Project
        document.Owner
        (groupName document.Group)
        item
        detail

/// A script that only re-enters Nx for its own project adds a second way to run
/// one target. Matched on the project name appearing in an `nx` invocation.
let private proxiesOwnNxTarget (document: ManifestDocument) (script: ManifestScript) : bool =
    let command = script.Command.Trim()

    let mentionsNx =
        command.Contains("nx run", StringComparison.Ordinal)
        || command.Contains("nx ", StringComparison.Ordinal)

    mentionsNx && command.Contains(document.Project, StringComparison.Ordinal)

let private validateRetained (document: ManifestDocument) : Result<unit, TestContract.Failure> =
    result {
        do!
            match document.ManifestPath with
            | Some _ -> Ok()
            | None ->
                Error(
                    TestContract.ContractFailure(
                        finding "manifest-retained-without-path" document document.Project "manifestPath=null"
                    )
                )

        do!
            match document.Consumer with
            | None ->
                Error(
                    TestContract.ContractFailure(
                        finding "manifest-retained-without-consumer" document document.Project "consumer=null"
                    )
                )
            | Some consumer when List.contains (consumer.Trim().ToLowerInvariant()) invalidConsumers ->
                Error(
                    TestContract.ContractFailure(
                        finding "manifest-invalid-consumer" document document.Project (sprintf "consumer=%s" consumer)
                    )
                )
            | Some _ -> Ok()

        do!
            match document.Verification with
            | Some _ -> Ok()
            | None ->
                Error(
                    TestContract.ContractFailure(
                        finding "manifest-missing-verification" document document.Project "verification=null"
                    )
                )

        do!
            if List.isEmpty document.RequiredFields then
                Error(
                    TestContract.ContractFailure(
                        finding "manifest-missing-required-fields" document document.Project "requiredFields=0"
                    )
                )
            else
                Ok()

        return ()
    }

let private validateRemoved (document: ManifestDocument) : Result<unit, TestContract.Failure> =
    result {
        do!
            match document.ManifestPath with
            | None -> Ok()
            | Some path ->
                Error(TestContract.ContractFailure(finding "manifest-removed-with-path" document path "expected=null"))

        do!
            match
                document.Commands
                |> List.tryFind (fun command -> command.Contains("npm --prefix", StringComparison.Ordinal))
            with
            | None -> Ok()
            | Some command ->
                Error(
                    TestContract.ContractFailure(
                        finding
                            "manifest-removed-still-prefixed"
                            document
                            document.Project
                            (sprintf "command=%s" command)
                    )
                )

        do!
            if List.isEmpty document.Scripts then
                Ok()
            else
                Error(
                    TestContract.ContractFailure(
                        finding
                            "manifest-removed-with-scripts"
                            document
                            document.Project
                            (sprintf "scripts=%d" (List.length document.Scripts))
                    )
                )

        return ()
    }

let validateDocument (document: ManifestDocument) : Result<ManifestReport, TestContract.Failure> =
    result {
        do!
            match document.Scripts |> List.tryFind (proxiesOwnNxTarget document) with
            | None -> Ok()
            | Some script ->
                Error(
                    TestContract.ContractFailure(
                        finding
                            "manifest-script-proxies-nx-target"
                            document
                            script.Name
                            (sprintf "command=%s" script.Command)
                    )
                )

        do!
            match document.Disposition with
            | Retained -> validateRetained document
            | Removed -> validateRemoved document

        return
            { Project = document.Project
              Owner = document.Owner
              Group = document.Group
              Disposition = document.Disposition
              Consumer = document.Consumer }
    }

let formatReport (report: ManifestReport) : string =
    sprintf
        "native-manifest-valid project=%s owner=%s group=%s disposition=%s consumer=%s"
        report.Project
        report.Owner
        (groupName report.Group)
        (dispositionName report.Disposition)
        (defaultArg report.Consumer "none")
