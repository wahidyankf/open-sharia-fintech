module OrganicleverBe.Tests.Unit.Tests.JournalDomainTests

open Xunit
open OrganicleverBe.Contexts.Journal.Domain

// ---------------------------------------------------------------------------
// Entry-name validation mirrors the PGlite client schema
// (apps/organiclever-app-web/src/contexts/journal/domain/schema.ts EntryName):
// 1..64 chars, lowercase, matching ^[a-z][a-z0-9-]*$.
// ---------------------------------------------------------------------------

[<Fact>]
let ``validateName accepts a well-known kind slug`` () =
    match validateName "workout" with
    | Ok name -> Assert.Equal("workout", name)
    | Error msg -> Assert.Fail(sprintf "expected Ok, got Error %s" msg)

[<Fact>]
let ``validateName accepts a custom-prefixed slug`` () =
    match validateName "custom-meditation" with
    | Ok name -> Assert.Equal("custom-meditation", name)
    | Error msg -> Assert.Fail(sprintf "expected Ok, got Error %s" msg)

[<Fact>]
let ``validateName rejects an empty name`` () =
    match validateName "" with
    | Ok _ -> Assert.Fail("expected Error for empty name")
    | Error _ -> ()

[<Fact>]
let ``validateName rejects an uppercase name`` () =
    match validateName "Workout" with
    | Ok _ -> Assert.Fail("expected Error for uppercase name")
    | Error _ -> ()

[<Fact>]
let ``validateName rejects a name longer than 64 characters`` () =
    let tooLong = String.replicate 65 "a"

    match validateName tooLong with
    | Ok _ -> Assert.Fail("expected Error for a name over the 64-character limit")
    | Error msg -> Assert.Contains("64", msg)

[<Fact>]
let ``validateNewEntry rejects a blank name`` () =
    let input: NewEntryInput =
        { Name = ""
          Payload = "{}"
          StartedAt = "2026-06-14T10:00:00Z"
          FinishedAt = "2026-06-14T10:30:00Z"
          Labels = [] }

    match validateNewEntry input with
    | Ok _ -> Assert.Fail("expected Error for blank name")
    | Error _ -> ()

[<Fact>]
let ``validateNewEntry accepts a valid input`` () =
    let input: NewEntryInput =
        { Name = "reading"
          Payload = "{\"title\":\"Clean Code\"}"
          StartedAt = "2026-06-14T10:00:00Z"
          FinishedAt = "2026-06-14T10:30:00Z"
          Labels = [ "books" ] }

    match validateNewEntry input with
    | Ok validated -> Assert.Equal("reading", validated.Name)
    | Error msg -> Assert.Fail(sprintf "expected Ok, got Error %s" msg)
