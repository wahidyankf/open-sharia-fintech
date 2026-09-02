/// Plain xunit tests for `RhinoCli.Application.TestContractJson`, the shared
/// JSON-reading rules `TestContractBdd.fs`, `TestContractCoverage.fs`,
/// `TestContractLayout.fs`, and `TestContractManifest.fs` all delegate to.
module RhinoCli.Tests.Unit.Steps.TestContractJsonUnitTests

open System.Text.Json
open Xunit
open RhinoCli.Application
open RhinoCli.Application.TestContractJson

// ---------------------------------------------------------------------------
// requiredString
// ---------------------------------------------------------------------------

[<Fact>]
let ``requiredString reports misuse when the key is absent`` () =
    use doc = JsonDocument.Parse("""{ "other": 1 }""")

    match requiredString doc.RootElement "name" with
    | Error(TestContract.Misuse message) -> Assert.Contains("\"name\" is required", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok raw -> failwith ("an absent key must fail, found: " + raw)

// ---------------------------------------------------------------------------
// nullableString
// ---------------------------------------------------------------------------

[<Fact>]
let ``nullableString reports misuse when the key is absent`` () =
    use doc = JsonDocument.Parse("""{ "other": 1 }""")

    match nullableString doc.RootElement "reason" with
    | Error(TestContract.Misuse message) -> Assert.Contains("\"reason\" is required", message)
    | other -> failwith (sprintf "an absent key must fail, found %A" other)

[<Fact>]
let ``nullableString reports misuse when the value is a blank string`` () =
    use doc = JsonDocument.Parse("""{ "reason": "" }""")

    match nullableString doc.RootElement "reason" with
    | Error(TestContract.Misuse message) -> Assert.Contains("\"reason\" must not be blank", message)
    | other -> failwith (sprintf "a blank string must fail, found %A" other)

[<Fact>]
let ``nullableString returns the string when present and non-blank`` () =
    use doc = JsonDocument.Parse("""{ "reason": "native denominator absent" }""")

    match nullableString doc.RootElement "reason" with
    | Ok(Some raw) -> Assert.Equal("native denominator absent", raw)
    | other -> failwith (sprintf "a present non-blank string must resolve to Some, found %A" other)

// ---------------------------------------------------------------------------
// optionalString
// ---------------------------------------------------------------------------

[<Fact>]
let ``optionalString resolves None when absent and Some when present`` () =
    use doc = JsonDocument.Parse("""{ "present": "value" }""")

    match optionalString doc.RootElement "absent" with
    | Ok None -> ()
    | other -> failwith (sprintf "an absent optional key must resolve to None, found %A" other)

    match optionalString doc.RootElement "present" with
    | Ok(Some raw) -> Assert.Equal("value", raw)
    | other -> failwith (sprintf "a present optional key must resolve to Some, found %A" other)

// ---------------------------------------------------------------------------
// requiredInt
// ---------------------------------------------------------------------------

[<Fact>]
let ``requiredInt reports misuse when the key is absent`` () =
    use doc = JsonDocument.Parse("""{ "other": 1 }""")

    match requiredInt doc.RootElement "value" with
    | Error(TestContract.Misuse message) -> Assert.Contains("\"value\" is required", message)
    | other -> failwith (sprintf "an absent key must fail, found %A" other)

[<Fact>]
let ``requiredInt reports misuse when the value is not a number`` () =
    use doc = JsonDocument.Parse("""{ "value": "99" }""")

    match requiredInt doc.RootElement "value" with
    | Error(TestContract.Misuse message) -> Assert.Contains("\"value\" must be an integer", message)
    | other -> failwith (sprintf "a string value must fail, found %A" other)

[<Fact>]
let ``requiredInt reports misuse when a number is not representable as an integer`` () =
    use doc = JsonDocument.Parse("""{ "value": 1.5 }""")

    match requiredInt doc.RootElement "value" with
    | Error(TestContract.Misuse message) -> Assert.Contains("\"value\" must be an integer", message)
    | other -> failwith (sprintf "a non-integral number must fail, found %A" other)

[<Fact>]
let ``requiredInt returns the parsed value when given a valid integer`` () =
    use doc = JsonDocument.Parse("""{ "value": 99 }""")

    match requiredInt doc.RootElement "value" with
    | Ok parsed -> Assert.Equal(99, parsed)
    | Error(TestContract.Misuse message) -> failwith ("unexpected misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("unexpected contract failure: " + message)

// ---------------------------------------------------------------------------
// requiredBool
// ---------------------------------------------------------------------------

[<Fact>]
let ``requiredBool reports misuse when the key is absent`` () =
    use doc = JsonDocument.Parse("""{ "other": true }""")

    match requiredBool doc.RootElement "applicable" with
    | Error(TestContract.Misuse message) -> Assert.Contains("\"applicable\" is required", message)
    | other -> failwith (sprintf "an absent key must fail, found %A" other)

[<Fact>]
let ``requiredBool reports misuse when the value is not a boolean`` () =
    use doc = JsonDocument.Parse("""{ "applicable": "yes" }""")

    match requiredBool doc.RootElement "applicable" with
    | Error(TestContract.Misuse message) -> Assert.Contains("\"applicable\" must be a boolean", message)
    | other -> failwith (sprintf "a string value must fail, found %A" other)

// ---------------------------------------------------------------------------
// requiredArray
// ---------------------------------------------------------------------------

[<Fact>]
let ``requiredArray reports misuse when the key is absent`` () =
    use doc = JsonDocument.Parse("""{ "other": [] }""")

    match requiredArray doc.RootElement "slices" with
    | Error(TestContract.Misuse message) -> Assert.Contains("\"slices\" is required", message)
    | other -> failwith (sprintf "an absent key must fail, found %A" other)

// ---------------------------------------------------------------------------
// requiredObject
// ---------------------------------------------------------------------------

[<Fact>]
let ``requiredObject reports misuse when the key is absent`` () =
    use doc = JsonDocument.Parse("""{ "other": {} }""")

    match requiredObject doc.RootElement "target" with
    | Error(TestContract.Misuse message) -> Assert.Contains("\"target\" is required", message)
    | other -> failwith (sprintf "an absent key must fail, found %A" other)

[<Fact>]
let ``requiredObject reports misuse when the value is not an object`` () =
    use doc = JsonDocument.Parse("""{ "target": "not-an-object" }""")

    match requiredObject doc.RootElement "target" with
    | Error(TestContract.Misuse message) -> Assert.Contains("\"target\" must be an object", message)
    | other -> failwith (sprintf "a string value must fail, found %A" other)

[<Fact>]
let ``requiredObject returns the element when the value is an object`` () =
    use doc = JsonDocument.Parse("""{ "target": { "name": "test:unit" } }""")

    match requiredObject doc.RootElement "target" with
    | Ok element -> Assert.Equal("test:unit", element.GetProperty("name").GetString())
    | Error(TestContract.Misuse message) -> failwith ("unexpected misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("unexpected contract failure: " + message)

// ---------------------------------------------------------------------------
// stringArray
// ---------------------------------------------------------------------------

[<Fact>]
let ``stringArray reports misuse when an entry is not a string`` () =
    use doc = JsonDocument.Parse("""{ "exclusions": [1] }""")

    match stringArray doc.RootElement "exclusions" with
    | Error(TestContract.Misuse message) -> Assert.Contains("\"exclusions\" must contain only strings", message)
    | other -> failwith (sprintf "a non-string entry must fail, found %A" other)

[<Fact>]
let ``stringArray reports misuse when an entry is blank`` () =
    use doc = JsonDocument.Parse("""{ "exclusions": [""] }""")

    match stringArray doc.RootElement "exclusions" with
    | Error(TestContract.Misuse message) -> Assert.Contains("\"exclusions\" must not contain a blank entry", message)
    | other -> failwith (sprintf "a blank entry must fail, found %A" other)
