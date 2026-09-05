/// Resource-free decision core for the public Harness command family.
///
/// `HarnessRuntime.fs` preserves the existing public module/API and owns
/// repository, filesystem, and process composition. This module holds the
/// cross-boundary decisions that remain directly measurable by Unit tests,
/// independently of any checkout.
module RhinoCli.Application.HarnessPolicy

type ChangeAttribution =
    | NeitherChanged
    | MirrorChanged
    | CanonicalChanged
    | BothChanged

let attributeChanges (mirrorEdited: bool) (canonicalEdited: bool) : ChangeAttribution =
    match mirrorEdited, canonicalEdited with
    | false, false -> NeitherChanged
    | true, false -> MirrorChanged
    | false, true -> CanonicalChanged
    | true, true -> BothChanged

let validateRequestedHarness (accepted: string list) (requested: string) : Result<unit, string> =
    if List.contains requested accepted then
        Ok()
    else
        let choices = accepted |> List.map (sprintf "'%s'") |> String.concat ", "
        Error(sprintf "unknown harness name '%s'; expected one of %s" requested choices)

let classifyCatalogPresence (directory: string) (exists: bool) (catalogText: Result<string, string>) : bool * string =
    match exists, catalogText with
    | false, _ -> true, sprintf "%s absent on disk; no catalog row required" directory
    | true, Error error -> false, error
    | true, Ok catalog when catalog.Contains(directory) -> true, sprintf "%s is referenced by the catalog" directory
    | true, Ok _ -> false, sprintf "%s exists but is not referenced by the platform-bindings catalog" directory

let classifyBindingContent
    (relativePath: string)
    (expected: string)
    (actual: Result<string option, string>)
    : bool * string =
    match actual with
    | Error error -> false, error
    | Ok None -> false, sprintf "%s is missing" relativePath
    | Ok(Some content) when content = expected -> true, sprintf "%s matches generated content" relativePath
    | Ok(Some _) -> false, sprintf "%s drifted from generated content" relativePath

let triggerMatches (paths: string list) (triggers: string list) : bool =
    let matches (trigger: string) (path: string) =
        let normalized = trigger.TrimEnd('/')

        path = normalized
        || path.StartsWith(normalized + "/", System.StringComparison.Ordinal)

    paths
    |> List.exists (fun path -> triggers |> List.exists (fun trigger -> matches trigger path))

type WordBudgetGateDecision =
    | NotApplicable
    | Passed
    | Failed of int

let decideWordBudgetGate (changedPaths: string list) (triggers: string list) (exitCode: int) : WordBudgetGateDecision =
    if not (triggerMatches changedPaths triggers) then
        NotApplicable
    elif exitCode = 0 then
        Passed
    else
        Failed exitCode

let classifyTrackedPath (declarations: (string * 'ownership) list) (path: string) : 'ownership option =
    declarations
    |> List.filter (fun (declared, _) ->
        let normalized = declared.TrimEnd('/')

        path = normalized
        || path.StartsWith(normalized + "/", System.StringComparison.Ordinal))
    |> List.sortByDescending (fun (declared, _) -> declared.Length)
    |> List.tryHead
    |> Option.map snd
