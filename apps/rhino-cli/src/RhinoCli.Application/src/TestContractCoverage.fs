/// The 99% native-coverage floor: threshold resolution, native-target
/// validation, and integer comparison of a measured slice set, as specified by
/// [Target Contract and Project Matrix](../../../../../plans/in-progress/adopt-beavernest-test-automation/tech-docs/target-contract-and-project-matrix.md).
///
/// The gate compares integers by cross-multiplication (`covered * 100 >=
/// floor * total`), so a 989-of-1000 slice fails on arithmetic rather than on
/// a percentage that rounds up to the floor. Nothing here renders a percent
/// sign.
///
/// Reader boundary: nothing here writes a tracked byte. A fixture document is
/// read into memory only; `TestContract.fs` remains the typed registry facade
/// and carries no coverage logic.
module RhinoCli.Application.TestContractCoverage

open System
open System.IO
open System.Text.Json

/// The three adapter levels a coverage owner may declare.
type CoverageAdapter =
    | CoverageUnit
    | CoverageIntegration
    | CoverageE2e

/// A coverage profile is either measured against a native denominator or
/// governed as having none.
type CoverageProfile =
    | MeasuredProfile
    | NoDenominatorProfile

/// One declared threshold and the configuration source that declares it.
type Threshold = { Source: string; Value: int }

/// The native target that produces the coverage measurement.
type CoverageTarget = { Name: string; Command: string }

/// One measured or omitted unit of the coverage denominator.
type Slice =
    { Path: string
      Applicable: bool
      Measured: bool
      Covered: int
      Total: int
      Output: string }

/// One `ose-test-contract-coverage-fixture/v1` document.
type CoverageDocument =
    { Schema: string
      Case: string
      Project: string
      Owner: string
      Adapter: CoverageAdapter
      Profile: CoverageProfile
      Reason: string option
      Thresholds: Threshold list
      Target: CoverageTarget
      Exclusions: string list
      Slices: Slice list }

/// The measured totals for one adapter.
type CoverageReport =
    { Project: string
      Owner: string
      Adapter: CoverageAdapter
      Profile: CoverageProfile
      Reason: string option
      Threshold: int option
      Covered: int
      Total: int }

/// The exact coverage fixture schema string.
[<Literal>]
let SchemaVersion = "ose-test-contract-coverage-fixture/v1"

/// The only directory a coverage fixture is resolved from.
[<Literal>]
let FixtureRoot = "apps/rhino-cli/tests/unit/Fixtures/TestContract/Coverage"

/// The native floor every measured adapter must meet, as a whole percent.
[<Literal>]
let Floor = 99

let adapterName (adapter: CoverageAdapter) : string =
    match adapter with
    | CoverageUnit -> "unit"
    | CoverageIntegration -> "integration"
    | CoverageE2e -> "e2e"

let profileName (profile: CoverageProfile) : string =
    match profile with
    | MeasuredProfile -> "measured"
    | NoDenominatorProfile -> "no-denominator"

// ---------------------------------------------------------------------------
// JSON reading helpers
// ---------------------------------------------------------------------------

let private isBlank (value: string) : bool = String.IsNullOrWhiteSpace value

let private misuse (message: string) : Result<'a, TestContract.Failure> = Error(TestContract.Misuse message)

/// Threads `Result` through the field-by-field parse without a nested match
/// per field.
type private ResultBuilder() =
    member _.Bind(value: Result<'a, 'e>, binder: 'a -> Result<'b, 'e>) = Result.bind binder value
    member _.Return(value: 'a) : Result<'a, 'e> = Ok value
    member _.ReturnFrom(value: Result<'a, 'e>) = value

let private result = ResultBuilder()

let private tryProperty (element: JsonElement) (name: string) : JsonElement option =
    match element.TryGetProperty name with
    | true, value -> Some value
    | _ -> None

/// Rejects any key the schema does not declare. Closed keys are what make an
/// unnoticed fixture typo a failure rather than a silent no-op.
let private closedKeys
    (element: JsonElement)
    (allowed: string list)
    (scope: string)
    : Result<unit, TestContract.Failure> =
    let unknown =
        element.EnumerateObject()
        |> Seq.map (fun property -> property.Name)
        |> Seq.filter (fun name -> not (List.contains name allowed))
        |> Seq.sort
        |> List.ofSeq

    match unknown with
    | [] -> Ok()
    | names -> misuse (sprintf "%s rejects the unknown key %s" scope (String.concat ", " names))

let private requiredString (element: JsonElement) (name: string) : Result<string, TestContract.Failure> =
    match tryProperty element name with
    | None -> misuse (sprintf "\"%s\" is required" name)
    | Some value when value.ValueKind <> JsonValueKind.String -> misuse (sprintf "\"%s\" must be a string" name)
    | Some value ->
        let raw = value.GetString()

        if isBlank raw then
            misuse (sprintf "\"%s\" must not be blank" name)
        else
            Ok raw

/// A key that must be present but whose value may be JSON `null`.
let private nullableString (element: JsonElement) (name: string) : Result<string option, TestContract.Failure> =
    match tryProperty element name with
    | None -> misuse (sprintf "\"%s\" is required" name)
    | Some value when value.ValueKind = JsonValueKind.Null -> Ok None
    | Some value when value.ValueKind <> JsonValueKind.String -> misuse (sprintf "\"%s\" must be a string or null" name)
    | Some value ->
        let raw = value.GetString()

        if isBlank raw then
            misuse (sprintf "\"%s\" must not be blank" name)
        else
            Ok(Some raw)

let private requiredInt (element: JsonElement) (name: string) : Result<int, TestContract.Failure> =
    match tryProperty element name with
    | None -> misuse (sprintf "\"%s\" is required" name)
    | Some value when value.ValueKind <> JsonValueKind.Number -> misuse (sprintf "\"%s\" must be an integer" name)
    | Some value ->
        match value.TryGetInt32() with
        | true, parsed -> Ok parsed
        | _ -> misuse (sprintf "\"%s\" must be an integer" name)

let private requiredBool (element: JsonElement) (name: string) : Result<bool, TestContract.Failure> =
    match tryProperty element name with
    | None -> misuse (sprintf "\"%s\" is required" name)
    | Some value when value.ValueKind = JsonValueKind.True -> Ok true
    | Some value when value.ValueKind = JsonValueKind.False -> Ok false
    | Some _ -> misuse (sprintf "\"%s\" must be a boolean" name)

let private requiredArray (element: JsonElement) (name: string) : Result<JsonElement list, TestContract.Failure> =
    match tryProperty element name with
    | None -> misuse (sprintf "\"%s\" is required" name)
    | Some value when value.ValueKind <> JsonValueKind.Array -> misuse (sprintf "\"%s\" must be an array" name)
    | Some value -> Ok(value.EnumerateArray() |> List.ofSeq)

let private requiredObject (element: JsonElement) (name: string) : Result<JsonElement, TestContract.Failure> =
    match tryProperty element name with
    | None -> misuse (sprintf "\"%s\" is required" name)
    | Some value when value.ValueKind <> JsonValueKind.Object -> misuse (sprintf "\"%s\" must be an object" name)
    | Some value -> Ok value

/// Folds a `Result`-returning mapper over a list, stopping at the first error
/// and preserving input order.
let private traverse
    (mapper: 'a -> Result<'b, TestContract.Failure>)
    (items: 'a list)
    : Result<'b list, TestContract.Failure> =
    let rec loop (remaining: 'a list) (accumulated: 'b list) =
        match remaining with
        | [] -> Ok(List.rev accumulated)
        | head :: tail ->
            match mapper head with
            | Error failure -> Error failure
            | Ok mapped -> loop tail (mapped :: accumulated)

    loop items []

let private stringArray (element: JsonElement) (name: string) : Result<string list, TestContract.Failure> =
    result {
        let! items = requiredArray element name

        return!
            items
            |> traverse (fun item ->
                if item.ValueKind <> JsonValueKind.String then
                    misuse (sprintf "\"%s\" must contain only strings" name)
                else
                    let raw = item.GetString()

                    if isBlank raw then
                        misuse (sprintf "\"%s\" must not contain a blank entry" name)
                    else
                        Ok raw)
    }

// ---------------------------------------------------------------------------
// Path rules, mirrored from the registry validator
// ---------------------------------------------------------------------------

let private isAbsolutePath (value: string) : bool =
    value.StartsWith("/", StringComparison.Ordinal)
    || (value.Length > 1 && value.[1] = ':')

let private hasTraversal (value: string) : bool =
    value.Replace('\\', '/').Split('/')
    |> Array.exists (fun segment -> segment = "..")

let private checkedRelativePath (label: string) (value: string) : Result<string, TestContract.Failure> =
    if isAbsolutePath value then
        misuse (sprintf "%s \"%s\" must not be an absolute path" label value)
    elif hasTraversal value then
        misuse (sprintf "%s \"%s\" must not contain a traversal segment" label value)
    else
        Ok value

// ---------------------------------------------------------------------------
// Parsing
// ---------------------------------------------------------------------------

let private parseAdapter (raw: string) : Result<CoverageAdapter, TestContract.Failure> =
    match raw with
    | "unit" -> Ok CoverageUnit
    | "integration" -> Ok CoverageIntegration
    | "e2e" -> Ok CoverageE2e
    | other -> misuse (sprintf "\"adapter\" \"%s\" must be unit, integration, or e2e" other)

let private parseProfile (raw: string) : Result<CoverageProfile, TestContract.Failure> =
    match raw with
    | "measured" -> Ok MeasuredProfile
    | "no-denominator" -> Ok NoDenominatorProfile
    | other -> misuse (sprintf "\"profile\" \"%s\" must be measured or no-denominator" other)

let private parseThreshold (element: JsonElement) : Result<Threshold, TestContract.Failure> =
    result {
        do! closedKeys element [ "source"; "value" ] "a threshold"
        let! source = requiredString element "source"
        let! value = requiredInt element "value"

        if value < 0 || value > 100 then
            return! misuse (sprintf "threshold \"value\" %d must be between 0 and 100" value)
        else
            return { Source = source; Value = value }
    }

let private parseTarget (element: JsonElement) : Result<CoverageTarget, TestContract.Failure> =
    result {
        do! closedKeys element [ "name"; "command" ] "a target"
        let! name = requiredString element "name"
        let! command = requiredString element "command"
        return { Name = name; Command = command }
    }

let private parseSlice (element: JsonElement) : Result<Slice, TestContract.Failure> =
    result {
        do! closedKeys element [ "path"; "applicable"; "measured"; "covered"; "total"; "output" ] "a slice"
        let! rawPath = requiredString element "path"
        let! path = checkedRelativePath "slice path" rawPath
        let! applicable = requiredBool element "applicable"
        let! measured = requiredBool element "measured"
        let! covered = requiredInt element "covered"
        let! total = requiredInt element "total"
        let! rawOutput = requiredString element "output"
        let! output = checkedRelativePath "slice output" rawOutput

        if covered < 0 then
            return! misuse (sprintf "slice \"%s\" \"covered\" %d must not be negative" path covered)
        elif total < 0 then
            return! misuse (sprintf "slice \"%s\" \"total\" %d must not be negative" path total)
        elif covered > total then
            return! misuse (sprintf "slice \"%s\" \"covered\" %d must not exceed \"total\" %d" path covered total)
        else
            return
                { Path = path
                  Applicable = applicable
                  Measured = measured
                  Covered = covered
                  Total = total
                  Output = output }
    }

/// Reads one fixture document. Every rule enforced here is a fixture-authoring
/// rule; a contract verdict is `validateDocument`'s job.
let parseDocument (text: string) : Result<CoverageDocument, TestContract.Failure> =
    let parsed =
        try
            Ok(JsonDocument.Parse text)
        with :? JsonException as error ->
            misuse (sprintf "the fixture is not valid JSON: %s" error.Message)

    match parsed with
    | Error failure -> Error failure
    | Ok json ->
        use json = json
        let root = json.RootElement

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
                          "adapter"
                          "profile"
                          "reason"
                          "thresholds"
                          "target"
                          "exclusions"
                          "slices" ]
                        "the fixture"

                let! schema = requiredString root "schema"

                if schema <> SchemaVersion then
                    return! misuse (sprintf "\"schema\" must be \"%s\", not \"%s\"" SchemaVersion schema)
                else

                    let! case = requiredString root "case"
                    let! project = requiredString root "project"
                    let! owner = requiredString root "owner"
                    let! rawAdapter = requiredString root "adapter"
                    let! adapter = parseAdapter rawAdapter
                    let! rawProfile = requiredString root "profile"
                    let! profile = parseProfile rawProfile
                    let! reason = nullableString root "reason"
                    let! thresholdElements = requiredArray root "thresholds"
                    let! thresholds = traverse parseThreshold thresholdElements
                    let! targetElement = requiredObject root "target"
                    let! target = parseTarget targetElement
                    let! exclusions = stringArray root "exclusions"
                    let! sliceElements = requiredArray root "slices"
                    let! slices = traverse parseSlice sliceElements

                    let duplicateSlice =
                        slices
                        |> List.countBy (fun slice -> slice.Path)
                        |> List.tryFind (fun (_, count) -> count > 1)

                    match profile, reason, duplicateSlice with
                    | _, _, Some(path, count) ->
                        return! misuse (sprintf "slice path \"%s\" is declared %d times" path count)
                    | NoDenominatorProfile, None, _ -> return! misuse "a no-denominator profile requires a \"reason\""
                    | MeasuredProfile, Some _, _ -> return! misuse "a measured profile must leave \"reason\" null"
                    | NoDenominatorProfile, Some _, _ when not (List.isEmpty slices) ->
                        return! misuse "a no-denominator profile must declare no \"slices\""
                    | MeasuredProfile, None, _ when List.isEmpty slices ->
                        return! misuse "a measured profile must declare at least one entry in \"slices\""
                    | _ ->
                        return
                            { Schema = schema
                              Case = case
                              Project = project
                              Owner = owner
                              Adapter = adapter
                              Profile = profile
                              Reason = reason
                              Thresholds = thresholds
                              Target = target
                              Exclusions = exclusions
                              Slices = slices }
            }

/// Resolves a fixture beneath `FixtureRoot` and reads it.
let loadDocument (repoRoot: string) (fixturePath: string) : Result<CoverageDocument, TestContract.Failure> =
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

/// A target that reports success without measuring anything. An echo stub is
/// the exact shape this leaf exists to reject.
let private isPlaceholderCommand (command: string) : bool =
    let trimmed = command.Trim()

    trimmed.StartsWith("echo ", StringComparison.Ordinal)
    || trimmed.StartsWith("echo'", StringComparison.Ordinal)
    || trimmed.StartsWith("echo\"", StringComparison.Ordinal)
    || trimmed = "echo"
    || trimmed.StartsWith("true", StringComparison.Ordinal)
    || trimmed.StartsWith(":", StringComparison.Ordinal)

/// Whether an exclusion pattern covers a slice path. Only the prefix form the
/// fixtures use is honoured; anything else is treated as non-matching so a
/// pattern can never silently widen the exclusion.
let private excludes (pattern: string) (path: string) : bool =
    let normalized = pattern.Replace("\\", "/")

    if normalized.EndsWith("/**", StringComparison.Ordinal) then
        let prefix = normalized.Substring(0, normalized.Length - 3)
        path = prefix || path.StartsWith(prefix + "/", StringComparison.Ordinal)
    elif normalized.EndsWith("**", StringComparison.Ordinal) then
        let prefix = normalized.Substring(0, normalized.Length - 2)
        path.StartsWith(prefix, StringComparison.Ordinal)
    else
        path = normalized

/// The one place a slice is tested against the declared exclusion patterns, so
/// the "which slices were excluded" and "which slices are measured" views can
/// never disagree.
let private isExcluded (document: CoverageDocument) (slice: Slice) : bool =
    document.Exclusions |> List.exists (fun pattern -> excludes pattern slice.Path)

let private finding
    (code: string)
    (document: CoverageDocument)
    (item: string)
    (actual: int)
    (extra: string)
    (remediation: string)
    : string =
    sprintf
        "%s project=%s owner=%s adapter=%s item=%s expected=%d actual=%d%s remediation=%s"
        code
        document.Project
        document.Owner
        (adapterName document.Adapter)
        item
        Floor
        actual
        extra
        remediation

/// The one rendering of the measured pair, shared by the failure summary and
/// the success line so the two can never drift.
let private renderPair (threshold: int option) (covered: int) (total: int) : string =
    let declared =
        match threshold with
        | Some value -> string<int> value
        | None -> "none"

    sprintf "threshold=%s covered=%d/%d floor=%d" declared covered total Floor

/// The owner/adapter identity used when a finding has no narrower subject.
let private ownerItem (document: CoverageDocument) : string =
    sprintf "%s@%s" document.Owner (adapterName document.Adapter)

/// Resolves the single governing threshold, or the finding that explains why
/// there is not exactly one at or above the floor.
let private resolveThreshold (document: CoverageDocument) : Result<int, string> =
    match document.Thresholds with
    | [] ->
        Error(
            finding
                "coverage-threshold-missing"
                document
                (ownerItem document)
                0
                ""
                (sprintf "declare a %d threshold for this adapter" Floor)
        )
    | thresholds ->
        let distinct =
            thresholds |> List.map (fun threshold -> threshold.Value) |> List.distinct

        match distinct with
        | [ single ] when single >= Floor -> Ok single
        | [ single ] ->
            let source =
                thresholds
                |> List.tryFind (fun threshold -> threshold.Value = single)
                |> Option.map (fun threshold -> threshold.Source)
                |> Option.defaultValue (ownerItem document)

            Error(
                finding
                    "coverage-threshold-below-floor"
                    document
                    source
                    single
                    ""
                    (sprintf "raise the declared threshold to %d" Floor)
            )
        | values ->
            Error(
                finding
                    "coverage-threshold-conflict"
                    document
                    (ownerItem document)
                    (List.min values)
                    (sprintf " sources=%d" (List.length thresholds))
                    (sprintf "declare one %d threshold for this adapter" Floor)
            )

/// Measures a `measured` profile and returns every finding, in a fixed order
/// so a fixture pins exactly one code.
let private validateMeasured (document: CoverageDocument) : Result<CoverageReport, TestContract.Failure> =
    let thresholdOutcome = resolveThreshold document

    let thresholdValue =
        match thresholdOutcome with
        | Ok value -> Some value
        | Error _ -> None

    let thresholdFindings =
        match thresholdOutcome with
        | Ok _ -> []
        | Error message -> [ message ]

    let targetFindings =
        if isPlaceholderCommand document.Target.Command then
            [ finding
                  "coverage-target-not-executable"
                  document
                  document.Target.Name
                  0
                  ""
                  "run the native coverage runner instead of a placeholder command" ]
        else
            []

    let applicable = document.Slices |> List.filter (fun slice -> slice.Applicable)

    let excludedApplicable = applicable |> List.filter (isExcluded document)

    let exclusionFindings =
        if
            not (List.isEmpty applicable)
            && List.length excludedApplicable = List.length applicable
        then
            document.Exclusions
            |> List.filter (fun pattern -> applicable |> List.exists (fun slice -> excludes pattern slice.Path))
            |> List.map (fun pattern ->
                finding
                    "coverage-exclusion-too-broad"
                    document
                    pattern
                    0
                    ""
                    "narrow the exclusion so an applicable slice remains measured")
        else
            []

    let omittedFindings =
        applicable
        |> List.filter (fun slice -> not slice.Measured)
        |> List.map (fun slice ->
            finding
                "coverage-slice-omitted"
                document
                slice.Path
                0
                ""
                "measure this applicable slice or mark it inapplicable with a reason")

    let measured =
        applicable
        |> List.filter (fun slice -> slice.Measured)
        |> List.filter (fun slice -> not (isExcluded document slice))

    let overlapFindings =
        measured
        |> List.countBy (fun slice -> slice.Output)
        |> List.filter (fun (_, count) -> count > 1)
        |> List.sortBy fst
        |> List.map (fun (output, count) ->
            finding
                "coverage-output-overlap"
                document
                output
                0
                (sprintf " candidates=%d" count)
                "give each measured slice its own coverage output path")

    let covered = measured |> List.sumBy (fun slice -> slice.Covered)
    let total = measured |> List.sumBy (fun slice -> slice.Total)

    let belowFloorFindings =
        measured
        |> List.filter (fun slice -> slice.Total > 0 && slice.Covered * 100 < Floor * slice.Total)
        |> List.map (fun slice ->
            finding
                "coverage-below-floor"
                document
                slice.Path
                (slice.Covered * 100 / slice.Total)
                ""
                (sprintf "cover at least %d of every 100 measured lines in this slice" Floor))

    let findings =
        thresholdFindings
        @ targetFindings
        @ exclusionFindings
        @ omittedFindings
        @ overlapFindings
        @ belowFloorFindings

    if List.isEmpty findings then
        Ok
            { Project = document.Project
              Owner = document.Owner
              Adapter = document.Adapter
              Profile = document.Profile
              Reason = document.Reason
              Threshold = thresholdValue
              Covered = covered
              Total = total }
    else
        let summary =
            sprintf
                "native-coverage-failed project=%s owner=%s adapter=%s profile=%s %s"
                document.Project
                document.Owner
                (adapterName document.Adapter)
                (profileName document.Profile)
                (renderPair thresholdValue covered total)

        Error(TestContract.ContractFailure(String.concat "\n" (findings @ [ summary ])))

/// Dispatches a parsed document to its profile's rules.
let validateDocument (document: CoverageDocument) : Result<CoverageReport, TestContract.Failure> =
    match document.Profile with
    | NoDenominatorProfile ->
        Ok
            { Project = document.Project
              Owner = document.Owner
              Adapter = document.Adapter
              Profile = document.Profile
              Reason = document.Reason
              Threshold = None
              Covered = 0
              Total = 0 }
    | MeasuredProfile -> validateMeasured document

/// Renders a passing report. A governed no-denominator adapter states its
/// reason instead of a pair.
let formatReport (report: CoverageReport) : string =
    match report.Profile with
    | NoDenominatorProfile ->
        sprintf
            "native-coverage-no-denominator project=%s owner=%s adapter=%s reason=%s"
            report.Project
            report.Owner
            (adapterName report.Adapter)
            (Option.defaultValue "unstated" report.Reason)
    | MeasuredProfile ->
        sprintf
            "native-coverage-valid project=%s owner=%s adapter=%s profile=%s %s"
            report.Project
            report.Owner
            (adapterName report.Adapter)
            (profileName report.Profile)
            (renderPair report.Threshold report.Covered report.Total)
