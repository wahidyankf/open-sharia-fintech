/// The JSON reading rules every `test-contract` fixture validator shares:
/// closed-key rejection, typed field readers, order-preserving traversal, and
/// the repository's relative-path rules.
///
/// Extracted when the layout and manifest validators became the third and
/// fourth users of a block that `TestContractBdd.fs` and
/// `TestContractCoverage.fs` had each copied verbatim. One copy means a
/// diagnostic wording fix reaches every check at once.
///
/// Reader boundary: nothing here writes a tracked byte, opens a file, or knows
/// what any particular check means. Every function is total on its input and
/// returns [`TestContract.Failure`] rather than raising.
module RhinoCli.Application.TestContractJson

open System
open System.Text.Json

let isBlank (value: string) : bool = String.IsNullOrWhiteSpace value

let misuse (message: string) : Result<'a, TestContract.Failure> = Error(TestContract.Misuse message)

/// Threads `Result` through a field-by-field parse without a nested match per
/// field.
type ResultBuilder() =
    member _.Bind(value: Result<'a, 'e>, binder: 'a -> Result<'b, 'e>) = Result.bind binder value
    member _.Return(value: 'a) : Result<'a, 'e> = Ok value
    member _.ReturnFrom(value: Result<'a, 'e>) = value

let result = ResultBuilder()

let tryProperty (element: JsonElement) (name: string) : JsonElement option =
    match element.TryGetProperty name with
    | true, value -> Some value
    | _ -> None

/// Rejects any key the schema does not declare. Closed keys are what make an
/// unnoticed fixture typo a failure rather than a silent no-op.
let closedKeys (element: JsonElement) (allowed: string list) (scope: string) : Result<unit, TestContract.Failure> =
    let unknown =
        element.EnumerateObject()
        |> Seq.map (fun property -> property.Name)
        |> Seq.filter (fun name -> not (List.contains name allowed))
        |> Seq.sort
        |> List.ofSeq

    match unknown with
    | [] -> Ok()
    | names -> misuse (sprintf "%s rejects the unknown key %s" scope (String.concat ", " names))

let requiredString (element: JsonElement) (name: string) : Result<string, TestContract.Failure> =
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
let nullableString (element: JsonElement) (name: string) : Result<string option, TestContract.Failure> =
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

/// A key that may be absent entirely; present-but-blank is still a misuse.
let optionalString (element: JsonElement) (name: string) : Result<string option, TestContract.Failure> =
    match tryProperty element name with
    | None -> Ok None
    | Some _ -> requiredString element name |> Result.map Some

let requiredInt (element: JsonElement) (name: string) : Result<int, TestContract.Failure> =
    match tryProperty element name with
    | None -> misuse (sprintf "\"%s\" is required" name)
    | Some value when value.ValueKind <> JsonValueKind.Number -> misuse (sprintf "\"%s\" must be an integer" name)
    | Some value ->
        match value.TryGetInt32() with
        | true, parsed -> Ok parsed
        | _ -> misuse (sprintf "\"%s\" must be an integer" name)

let requiredBool (element: JsonElement) (name: string) : Result<bool, TestContract.Failure> =
    match tryProperty element name with
    | None -> misuse (sprintf "\"%s\" is required" name)
    | Some value when value.ValueKind = JsonValueKind.True -> Ok true
    | Some value when value.ValueKind = JsonValueKind.False -> Ok false
    | Some _ -> misuse (sprintf "\"%s\" must be a boolean" name)

let requiredArray (element: JsonElement) (name: string) : Result<JsonElement list, TestContract.Failure> =
    match tryProperty element name with
    | None -> misuse (sprintf "\"%s\" is required" name)
    | Some value when value.ValueKind <> JsonValueKind.Array -> misuse (sprintf "\"%s\" must be an array" name)
    | Some value -> Ok(value.EnumerateArray() |> List.ofSeq)

let requiredObject (element: JsonElement) (name: string) : Result<JsonElement, TestContract.Failure> =
    match tryProperty element name with
    | None -> misuse (sprintf "\"%s\" is required" name)
    | Some value when value.ValueKind <> JsonValueKind.Object -> misuse (sprintf "\"%s\" must be an object" name)
    | Some value -> Ok value

/// Folds a `Result`-returning mapper over a list, stopping at the first error
/// and preserving input order.
let traverse (mapper: 'a -> Result<'b, TestContract.Failure>) (items: 'a list) : Result<'b list, TestContract.Failure> =
    let rec loop (remaining: 'a list) (accumulated: 'b list) =
        match remaining with
        | [] -> Ok(List.rev accumulated)
        | head :: tail ->
            match mapper head with
            | Error failure -> Error failure
            | Ok mapped -> loop tail (mapped :: accumulated)

    loop items []

let stringArray (element: JsonElement) (name: string) : Result<string list, TestContract.Failure> =
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

/// Entries repeated within one array, reported in sorted order.
let duplicates (values: string list) : string list =
    values
    |> List.countBy id
    |> List.filter (fun (_, count) -> count > 1)
    |> List.map fst
    |> List.sort

// ---------------------------------------------------------------------------
// Path rules, mirrored from the registry validator
// ---------------------------------------------------------------------------

let isAbsolutePath (value: string) : bool =
    value.StartsWith("/", StringComparison.Ordinal)
    || (value.Length > 1 && value.[1] = ':')

let hasTraversal (value: string) : bool =
    value.Replace('\\', '/').Split('/')
    |> Array.exists (fun segment -> segment = "..")

let checkedRelativePath (label: string) (value: string) : Result<string, TestContract.Failure> =
    if isAbsolutePath value then
        misuse (sprintf "%s \"%s\" must not be an absolute path" label value)
    elif hasTraversal value then
        misuse (sprintf "%s \"%s\" must not contain a traversal segment" label value)
    else
        Ok value
