/// The exact Gherkin/BDD adapter contract: recursive corpus enumeration,
/// binding resolution, and integer equality in all five categories, as
/// specified by
/// [Static Adapter Contract](../../../../../plans/in-progress/adopt-beavernest-test-automation/tech-docs/gherkin-coverage-and-adapter-design.md)
/// and
/// [Exact 100% Gherkin/BDD Enforcement](../../../../../plans/in-progress/adopt-beavernest-test-automation/tech-docs/target-contract-and-project-matrix.md).
///
/// The gate compares integers. It never renders a rounded percentage, so a
/// 999-of-1000 corpus fails rather than displaying `100%`.
///
/// Reader boundary: nothing here writes a tracked byte. A fixture document is
/// read into memory only; `TestContract.fs` remains the typed registry facade
/// and carries no BDD logic.
module RhinoCli.Application.TestContractBdd

open System
open System.IO
open System.Text.Json

/// The three adapter levels a behavior owner may declare.
type Adapter =
    | AdapterUnit
    | AdapterIntegration
    | AdapterE2e

/// The three adapter dispositions, restated locally so the validator does not
/// depend on the registry's parse order.
type BddDisposition =
    | BddRequired
    | BddDelegated
    | BddInapplicable

/// One declared scenario. `Examples` is 1 for a plain scenario and the
/// expanded example count for a scenario outline.
type BddScenario =
    { Name: string
      Examples: int
      Steps: string list }

/// One feature file and its declared scenarios.
type BddFeature =
    { Path: string
      Scenarios: BddScenario list }

/// A generated corpus descriptor. It exists so the rounding fixture can
/// declare 1,000 scenarios without 1,000 literal entries.
type Synthetic =
    { Path: string
      Scenarios: int
      Bound: int }

/// A fixture declares exactly one corpus form.
type BddCorpus =
    | ExplicitCorpus of features: BddFeature list * bindings: string list
    | GeneratedCorpus of Synthetic

/// One `ose-test-contract-bdd-fixture/v1` document.
type BddDocument =
    { Schema: string
      Case: string
      Project: string
      Owner: string
      Adapter: Adapter
      Disposition: BddDisposition
      Driver: string option
      Reason: string option
      Corpus: BddCorpus }

/// The five categories the contract requires to be exactly equal.
type Counts =
    { Files: int
      Examples: int
      Scenarios: int
      Steps: int
      Pairs: int }

/// One adapter's covered and total counts.
type BddReport =
    { Project: string
      Owner: string
      Adapter: Adapter
      Disposition: BddDisposition
      Reason: string option
      Covered: Counts
      Total: Counts }

/// The exact BDD fixture schema string.
[<Literal>]
let SchemaVersion = "ose-test-contract-bdd-fixture/v1"

/// The only directory a BDD fixture is resolved from.
[<Literal>]
let FixtureRoot = "apps/rhino-cli/src/tests/unit/Fixtures/TestContract/Bdd"

let adapterName (adapter: Adapter) : string =
    match adapter with
    | AdapterUnit -> "unit"
    | AdapterIntegration -> "integration"
    | AdapterE2e -> "e2e"

let dispositionName (disposition: BddDisposition) : string =
    match disposition with
    | BddRequired -> "required"
    | BddDelegated -> "delegated"
    | BddInapplicable -> "inapplicable"

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

/// A key that may be absent entirely.
let private optionalString (element: JsonElement) (name: string) : Result<string option, TestContract.Failure> =
    match tryProperty element name with
    | None -> Ok None
    | Some _ -> nullableString element name

let private requiredInt (element: JsonElement) (name: string) : Result<int, TestContract.Failure> =
    match tryProperty element name with
    | None -> misuse (sprintf "\"%s\" is required" name)
    | Some value when value.ValueKind <> JsonValueKind.Number -> misuse (sprintf "\"%s\" must be an integer" name)
    | Some value ->
        match value.TryGetInt32() with
        | true, parsed -> Ok parsed
        | _ -> misuse (sprintf "\"%s\" must be an integer" name)

let private requiredArray (element: JsonElement) (name: string) : Result<JsonElement list, TestContract.Failure> =
    match tryProperty element name with
    | None -> misuse (sprintf "\"%s\" is required" name)
    | Some value when value.ValueKind <> JsonValueKind.Array -> misuse (sprintf "\"%s\" must be an array" name)
    | Some value -> Ok(value.EnumerateArray() |> List.ofSeq)

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
// Path and identity rules
// ---------------------------------------------------------------------------

let private isAbsolutePath (value: string) : bool =
    value.StartsWith("/", StringComparison.Ordinal)
    || (value.Length > 1 && value.[1] = ':')

let private hasTraversal (value: string) : bool =
    value.Replace('\\', '/').Split('/')
    |> Array.exists (fun segment -> segment = "..")

let private corpusPath (value: string) : Result<string, TestContract.Failure> =
    if isAbsolutePath value then
        misuse (sprintf "a corpus path must be repository-relative, found \"%s\"" value)
    elif hasTraversal value then
        misuse (sprintf "a corpus path must not traverse, found \"%s\"" value)
    else
        Ok value

let private duplicates (values: string list) : string list =
    values
    |> List.countBy id
    |> List.filter (fun (_, count) -> count > 1)
    |> List.map fst
    |> List.sort

// ---------------------------------------------------------------------------
// Document parsing
// ---------------------------------------------------------------------------

let private parseAdapter (raw: string) : Result<Adapter, TestContract.Failure> =
    match raw with
    | "unit" -> Ok AdapterUnit
    | "integration" -> Ok AdapterIntegration
    | "e2e" -> Ok AdapterE2e
    | other -> misuse (sprintf "\"adapter\" must be unit, integration, or e2e, found \"%s\"" other)

let private parseDisposition (raw: string) : Result<BddDisposition, TestContract.Failure> =
    match raw with
    | "required" -> Ok BddRequired
    | "delegated" -> Ok BddDelegated
    | "inapplicable" -> Ok BddInapplicable
    | other -> misuse (sprintf "\"disposition\" must be required, delegated, or inapplicable, found \"%s\"" other)

let private parseScenario (element: JsonElement) : Result<BddScenario, TestContract.Failure> =
    result {
        do! closedKeys element [ "name"; "examples"; "steps" ] "a scenario"
        let! name = requiredString element "name"
        let! examples = requiredInt element "examples"
        let! steps = stringArray element "steps"

        if examples < 1 then
            return! misuse (sprintf "\"examples\" must be at least 1 for scenario \"%s\"" name)
        elif List.isEmpty steps then
            return! misuse (sprintf "\"steps\" must not be empty for scenario \"%s\"" name)
        else
            return
                { Name = name
                  Examples = examples
                  Steps = steps }
    }

let private parseFeature (element: JsonElement) : Result<BddFeature, TestContract.Failure> =
    result {
        do! closedKeys element [ "path"; "scenarios" ] "a feature"
        let! rawPath = requiredString element "path"
        let! path = corpusPath rawPath
        let! entries = requiredArray element "scenarios"

        if List.isEmpty entries then
            return! misuse (sprintf "\"scenarios\" must not be empty for feature \"%s\"" path)
        else
            let! scenarios = traverse parseScenario entries

            match duplicates (scenarios |> List.map (fun scenario -> scenario.Name)) with
            | [] -> return { Path = path; Scenarios = scenarios }
            | names ->
                return!
                    misuse (sprintf "feature \"%s\" declares the duplicate scenario %s" path (String.concat ", " names))
    }

let private parseSynthetic (element: JsonElement) : Result<Synthetic, TestContract.Failure> =
    result {
        do! closedKeys element [ "path"; "scenarios"; "bound" ] "a synthetic corpus"
        let! rawPath = requiredString element "path"
        let! path = corpusPath rawPath
        let! scenarios = requiredInt element "scenarios"
        let! bound = requiredInt element "bound"

        if scenarios < 1 then
            return! misuse "a synthetic corpus must declare at least 1 entry in \"scenarios\""
        elif bound < 0 || bound > scenarios then
            return! misuse (sprintf "\"bound\" must be between 0 and %d, found %d" scenarios bound)
        else
            return
                { Path = path
                  Scenarios = scenarios
                  Bound = bound }
    }

let private parseBindings (element: JsonElement) : Result<string list, TestContract.Failure> =
    result {
        let! bindings = stringArray element "bindings"

        return!
            bindings
            |> traverse (fun binding ->
                if binding.Split('|').Length <> 4 then
                    misuse (
                        sprintf "a binding must be \"<feature>|<scenario>|<example>|<step>\", found \"%s\"" binding
                    )
                else
                    Ok binding)
    }

let private parseCorpus (element: JsonElement) : Result<BddCorpus, TestContract.Failure> =
    match tryProperty element "corpus", tryProperty element "synthetic" with
    | Some _, Some _ -> misuse "a fixture declares either \"corpus\" or \"synthetic\", never both"
    | None, None -> misuse "a fixture must declare \"corpus\" with \"bindings\", or \"synthetic\""
    | None, Some synthetic ->
        if synthetic.ValueKind <> JsonValueKind.Object then
            misuse "\"synthetic\" must be an object"
        else
            parseSynthetic synthetic |> Result.map GeneratedCorpus
    | Some _, None ->
        result {
            let! entries = requiredArray element "corpus"

            if List.isEmpty entries then
                return! misuse "\"corpus\" must declare at least one feature"
            else
                let! features = traverse parseFeature entries
                let! bindings = parseBindings element

                match duplicates (features |> List.map (fun feature -> feature.Path)) with
                | [] -> return ExplicitCorpus(features, bindings)
                | paths ->
                    return! misuse (sprintf "\"corpus\" declares the duplicate feature %s" (String.concat ", " paths))
        }

/// Parses one fixture document from its JSON text.
let parseDocument (text: string) : Result<BddDocument, TestContract.Failure> =
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
            misuse "a fixture must be a JSON object"
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
                          "disposition"
                          "driver"
                          "reason"
                          "corpus"
                          "bindings"
                          "synthetic" ]
                        "a fixture"

                let! schema = requiredString root "schema"

                if schema <> SchemaVersion then
                    return! misuse (sprintf "\"schema\" must be \"%s\", found \"%s\"" SchemaVersion schema)
                else
                    let! case = requiredString root "case"
                    let! project = requiredString root "project"
                    let! owner = requiredString root "owner"
                    let! rawAdapter = requiredString root "adapter"
                    let! adapter = parseAdapter rawAdapter
                    let! rawDisposition = requiredString root "disposition"
                    let! disposition = parseDisposition rawDisposition
                    let! driver = nullableString root "driver"
                    let! reason = optionalString root "reason"
                    let! corpus = parseCorpus root

                    match disposition, driver, reason with
                    | BddInapplicable, Some path, _ ->
                        return! misuse (sprintf "an inapplicable adapter declares no \"driver\", found \"%s\"" path)
                    | BddInapplicable, None, None ->
                        return! misuse "an inapplicable adapter requires a non-blank \"reason\""
                    | (BddRequired | BddDelegated), _, Some text ->
                        return!
                            misuse (
                                sprintf
                                    "a %s adapter declares no \"reason\", found \"%s\""
                                    (dispositionName disposition)
                                    text
                            )
                    | _ ->
                        return
                            { Schema = schema
                              Case = case
                              Project = project
                              Owner = owner
                              Adapter = adapter
                              Disposition = disposition
                              Driver = driver
                              Reason = reason
                              Corpus = corpus }
            }

/// Resolves a repository-relative fixture below `FixtureRoot` and parses it.
let loadDocument (repoRoot: string) (fixturePath: string) : Result<BddDocument, TestContract.Failure> =
    if isBlank fixturePath then
        misuse "--fixture requires a repository-relative path"
    elif isAbsolutePath fixturePath then
        misuse (sprintf "--fixture rejects the absolute path \"%s\"" fixturePath)
    elif hasTraversal fixturePath then
        misuse (sprintf "--fixture rejects the traversal path \"%s\"" fixturePath)
    elif not (fixturePath.StartsWith(FixtureRoot + "/", StringComparison.Ordinal)) then
        misuse (sprintf "--fixture must resolve below \"%s\", found \"%s\"" FixtureRoot fixturePath)
    else
        let absolute =
            Path.Combine(repoRoot, fixturePath.Replace('/', Path.DirectorySeparatorChar))

        if not (File.Exists absolute) then
            misuse (sprintf "--fixture \"%s\" does not exist" fixturePath)
        else
            parseDocument (File.ReadAllText absolute)

// ---------------------------------------------------------------------------
// Enumeration and binding resolution
// ---------------------------------------------------------------------------

let private syntheticSteps =
    [ "Given a generated precondition"
      "When the generated action runs"
      "Then the generated outcome holds" ]

/// Materializes a generated corpus so both corpus forms share one validator.
let private expand (corpus: BddCorpus) : BddFeature list * string list =
    match corpus with
    | ExplicitCorpus(features, bindings) -> features, bindings
    | GeneratedCorpus synthetic ->
        let scenarios =
            [ for index in 1 .. synthetic.Scenarios ->
                  { Name = sprintf "Scenario %d" index
                    Examples = 1
                    Steps = syntheticSteps } ]

        let bindings =
            [ for index in 1 .. synthetic.Bound do
                  for step in syntheticSteps -> sprintf "%s|Scenario %d|1|%s" synthetic.Path index step ]

        [ { Path = synthetic.Path
            Scenarios = scenarios } ],
        bindings

/// The three normalized item identities every diagnostic and every count is
/// keyed on. A scenario identity extends its feature path, an example identity
/// extends its scenario, and a step identity extends its example, so a binding
/// string and a finding's `item=` field are always the same rendering.
let private scenarioIdentity (feature: string) (scenario: string) : string = sprintf "%s|%s" feature scenario

let private exampleIdentity (feature: string) (scenario: string) (example: int) : string =
    sprintf "%s|%d" (scenarioIdentity feature scenario) example

let private stepKey (feature: string) (scenario: string) (example: int) (step: string) : string =
    sprintf "%s|%s" (exampleIdentity feature scenario example) step

/// The one rendering of the five categories, shared by the failure summary and
/// the success line so the two can never drift.
let private renderCounts (covered: Counts) (total: Counts) : string =
    sprintf
        "files=%d/%d examples=%d/%d scenarios=%d/%d steps=%d/%d pairs=%d/%d"
        covered.Files
        total.Files
        covered.Examples
        total.Examples
        covered.Scenarios
        total.Scenarios
        covered.Steps
        total.Steps
        covered.Pairs
        total.Pairs

let private startsWithKeyword (keyword: string) (step: string) : bool =
    step.StartsWith(keyword + " ", StringComparison.Ordinal)

/// The two keywords the repository's Gherkin rules require in every scenario.
let private requiredKeywords = [ "When"; "Then" ]

let private finding
    (code: string)
    (document: BddDocument)
    (item: string)
    (covered: int)
    (total: int)
    (extra: string)
    (remediation: string)
    : string =
    sprintf
        "%s project=%s owner=%s adapter=%s item=%s covered=%d total=%d%s remediation=%s"
        code
        document.Project
        document.Owner
        (adapterName document.Adapter)
        item
        covered
        total
        extra
        remediation

/// Enumerates the corpus, resolves every step instance against the adapter's
/// bindings, and requires integer equality in all five categories.
let private validateApplicable (document: BddDocument) : Result<BddReport, TestContract.Failure> =
    let features, bindings = expand document.Corpus

    let bindingCounts =
        bindings
        |> List.countBy id
        |> List.fold (fun map (key, count) -> Map.add key count map) Map.empty

    // Structural keyword findings, then the scenarios they invalidate.
    let keywordFindings =
        [ for feature in features do
              for scenario in feature.Scenarios do
                  for keyword in requiredKeywords do
                      if not (scenario.Steps |> List.exists (startsWithKeyword keyword)) then
                          yield
                              finding
                                  "bdd-missing-required-keyword"
                                  document
                                  (scenarioIdentity feature.Path scenario.Name)
                                  (requiredKeywords
                                   |> List.filter (fun candidate ->
                                       scenario.Steps |> List.exists (startsWithKeyword candidate))
                                   |> List.length)
                                  requiredKeywords.Length
                                  (sprintf " keyword=%s" keyword)
                                  "add-missing-keyword" ]

    let scenarioIsStructural (scenario: BddScenario) : bool =
        requiredKeywords
        |> List.forall (fun keyword -> scenario.Steps |> List.exists (startsWithKeyword keyword))

    let instances =
        [ for feature in features do
              for scenario in feature.Scenarios do
                  for example in 1 .. scenario.Examples do
                      for step in scenario.Steps -> feature.Path, scenario, example, step ]

    let candidatesFor (feature: string) (scenario: BddScenario) (example: int) (step: string) : int =
        match Map.tryFind (stepKey feature scenario.Name example step) bindingCounts with
        | Some count -> count
        | None -> 0

    let totalSteps = List.length instances

    let coveredSteps =
        instances
        |> List.filter (fun (path, scenario, example, step) -> candidatesFor path scenario example step = 1)
        |> List.length

    let bindingFindings =
        [ for path, scenario, example, step in instances do
              let candidates = candidatesFor path scenario example step

              if candidates = 0 then
                  yield
                      finding
                          "bdd-undefined-binding"
                          document
                          (stepKey path scenario.Name example step)
                          coveredSteps
                          totalSteps
                          " candidates=0"
                          "bind-step"
              elif candidates > 1 then
                  yield
                      finding
                          "bdd-ambiguous-binding"
                          document
                          (stepKey path scenario.Name example step)
                          coveredSteps
                          totalSteps
                          (sprintf " candidates=%d" candidates)
                          "deduplicate-binding" ]

    let enumeratedKeys =
        instances
        |> List.map (fun (path, scenario, example, step) -> stepKey path scenario.Name example step)
        |> Set.ofList

    let declaredBindings = bindings |> List.distinct

    let unusedKeys =
        declaredBindings
        |> List.filter (fun key -> not (Set.contains key enumeratedKeys))
        |> List.sort

    let unusedFindings =
        [ for key in unusedKeys ->
              finding
                  "bdd-unused-binding"
                  document
                  key
                  (List.length declaredBindings - List.length unusedKeys)
                  (List.length declaredBindings)
                  ""
                  "remove-binding" ]

    let exampleIsCovered (path: string) (scenario: BddScenario) (example: int) : bool =
        scenarioIsStructural scenario
        && scenario.Steps
           |> List.forall (fun step -> candidatesFor path scenario example step = 1)

    let expandedExamples =
        [ for feature in features do
              for scenario in feature.Scenarios do
                  for example in 1 .. scenario.Examples -> feature.Path, scenario, example ]

    let totalExamples = List.length expandedExamples

    let coveredExamples =
        expandedExamples
        |> List.filter (fun (path, scenario, example) -> exampleIsCovered path scenario example)
        |> List.length

    let scenarioIsCovered (path: string) (scenario: BddScenario) : bool =
        [ 1 .. scenario.Examples ] |> List.forall (exampleIsCovered path scenario)

    let allScenarios =
        [ for feature in features do
              for scenario in feature.Scenarios -> feature.Path, scenario ]

    let totalScenarios = List.length allScenarios

    let coveredScenarios =
        allScenarios
        |> List.filter (fun (path, scenario) -> scenarioIsCovered path scenario)
        |> List.length

    let featureIsCovered (feature: BddFeature) : bool =
        feature.Scenarios |> List.forall (scenarioIsCovered feature.Path)

    let totalFiles = List.length features
    let coveredFiles = features |> List.filter featureIsCovered |> List.length

    let exampleFindings =
        [ for path, scenario, example in expandedExamples do
              if not (exampleIsCovered path scenario example) then
                  yield
                      finding
                          "bdd-uncovered-example"
                          document
                          (exampleIdentity path scenario.Name example)
                          coveredExamples
                          totalExamples
                          ""
                          "bind-example" ]

    let scenarioFindings =
        [ for path, scenario in allScenarios do
              if not (scenarioIsCovered path scenario) then
                  yield
                      finding
                          "bdd-uncovered-scenario"
                          document
                          (scenarioIdentity path scenario.Name)
                          coveredScenarios
                          totalScenarios
                          ""
                          "bind-scenario" ]

    let featureFindings =
        [ for feature in features do
              if not (featureIsCovered feature) then
                  yield finding "bdd-uncovered-feature" document feature.Path coveredFiles totalFiles "" "bind-feature" ]

    let pairIsCovered =
        Option.isSome document.Driver
        && coveredFiles = totalFiles
        && List.isEmpty unusedKeys
        && List.isEmpty bindingFindings

    let coveredPairs = if pairIsCovered then 1 else 0

    let pairFindings =
        if pairIsCovered then
            []
        else
            [ finding
                  "bdd-uncovered-owner-adapter"
                  document
                  (sprintf "%s@%s" document.Owner (adapterName document.Adapter))
                  coveredPairs
                  1
                  ""
                  (if Option.isNone document.Driver then
                       "declare-driver"
                   else
                       "bind-corpus") ]

    let covered =
        { Files = coveredFiles
          Examples = coveredExamples
          Scenarios = coveredScenarios
          Steps = coveredSteps
          Pairs = coveredPairs }

    let total =
        { Files = totalFiles
          Examples = totalExamples
          Scenarios = totalScenarios
          Steps = totalSteps
          Pairs = 1 }

    let findings =
        keywordFindings
        @ bindingFindings
        @ unusedFindings
        @ exampleFindings
        @ scenarioFindings
        @ featureFindings
        @ pairFindings

    if List.isEmpty findings then
        Ok
            { Project = document.Project
              Owner = document.Owner
              Adapter = document.Adapter
              Disposition = document.Disposition
              Reason = document.Reason
              Covered = covered
              Total = total }
    else
        let summary =
            sprintf
                "behavior-coverage-failed project=%s owner=%s adapter=%s disposition=%s %s"
                document.Project
                document.Owner
                (adapterName document.Adapter)
                (dispositionName document.Disposition)
                (renderCounts covered total)

        Error(TestContract.ContractFailure(String.Join("\n", findings @ [ summary ])))

/// Enumerates the corpus, resolves every step instance against the adapter's
/// bindings, and requires integer equality in all five categories. An
/// `inapplicable` adapter builds no denominator: the registry disposition is
/// the evidence, so the validator returns a structured not-applicable report
/// rather than an ungoverned echo.
let validateDocument (document: BddDocument) : Result<BddReport, TestContract.Failure> =
    match document.Disposition with
    | BddInapplicable ->
        let empty =
            { Files = 0
              Examples = 0
              Scenarios = 0
              Steps = 0
              Pairs = 0 }

        Ok
            { Project = document.Project
              Owner = document.Owner
              Adapter = document.Adapter
              Disposition = document.Disposition
              Reason = document.Reason
              Covered = empty
              Total = empty }
    | _ -> validateApplicable document

/// Renders the success line for a valid adapter report.
let formatReport (report: BddReport) : string =
    match report.Disposition with
    | BddInapplicable ->
        sprintf
            "behavior-coverage-not-applicable project=%s owner=%s adapter=%s reason=%s"
            report.Project
            report.Owner
            (adapterName report.Adapter)
            (defaultArg report.Reason "")
    | _ ->
        sprintf
            "behavior-coverage-valid project=%s owner=%s adapter=%s disposition=%s %s"
            report.Project
            report.Owner
            (adapterName report.Adapter)
            (dispositionName report.Disposition)
            (renderCounts report.Covered report.Total)
