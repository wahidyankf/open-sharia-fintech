/// Plain xunit tests for `RhinoCli.Domain.Finding` — no dedicated Gherkin
/// scenario covers this module directly (it is a cross-cutting helper folded
/// out of `Md.fs`'s own private `hasBlockingFinding` copy, Wave D PR11, for
/// the git pre-commit hook shim's integration tests to reuse), mirroring the
/// rationale `DoctorUnitTests.fs`'s module doc comment states for its own
/// split from `DoctorSteps.fs`. `hasBlocking` is exercised indirectly by
/// every `Md.fs` audit-scenario unit test via `findingsOutcome`; these tests
/// pin its direct contract plus `formatText`'s rendering, which has no other
/// caller in the unit-tier suite.
module RhinoCli.Tests.Unit.Steps.FindingUnitTests

open Xunit
open RhinoCli.Domain.Types
open RhinoCli.Domain.Finding

let private blocking (path: string) (message: string) : Finding =
    { Severity = Severity.Blocking
      Message = message
      Path = Some path }

let private advisory (message: string) : Finding =
    { Severity = Severity.Advisory
      Message = message
      Path = None }

// ---- hasBlocking ----

[<Fact>]
let ``hasBlocking is false for an empty list`` () = Assert.False(hasBlocking [])

[<Fact>]
let ``hasBlocking is false when every finding is Advisory`` () =
    Assert.False(hasBlocking [ advisory "warn one"; advisory "warn two" ])

[<Fact>]
let ``hasBlocking is true when at least one finding is Blocking`` () =
    Assert.True(hasBlocking [ advisory "warn"; blocking "a.md" "fail" ])

// ---- formatText ----

[<Fact>]
let ``formatText renders an empty list as an empty string`` () = Assert.Equal("", formatText [])

[<Fact>]
let ``formatText renders a path-scoped finding as path colon message`` () =
    Assert.Equal("a.md: broken link", formatText [ blocking "a.md" "broken link" ])

[<Fact>]
let ``formatText renders a pathless finding as the message alone`` () =
    Assert.Equal("no path here", formatText [ advisory "no path here" ])

[<Fact>]
let ``formatText joins multiple findings with newlines, preserving order`` () =
    let findings =
        [ blocking "a.md" "first"; advisory "second"; blocking "b.md" "third" ]

    Assert.Equal("a.md: first\nsecond\nb.md: third", formatText findings)
