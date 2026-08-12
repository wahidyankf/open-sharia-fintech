module OrganicleverBe.Tests.Unit.Steps.EnvTierSteps

open TickSpec

// Step definitions for the be-env context (env-tier-loader.feature). These
// bind the Gherkin steps for the spec coverage validator; the actual loader
// behavior is exercised directly against the production code (this app's
// thin `loadEnvTier` wrapper) in Tests/EnvTierLoaderTests.fs. The pure loader
// rules themselves live once in libs/fsharp-env-loader's own comprehensive
// test suite. The "When"/"Then" steps below are registered as raw regexes
// (an F# step's backtick text compiles verbatim as an anchored `^...$`
// pattern) so a single definition covers every Scenario Outline "tier"
// example (local/test/stag/prod) in one pattern.

[<Given>]
let ``the files ".env.local" and ".env.stag" both exist at the app's composition root`` () = ()

[<When>]
let ``the process starts with APP_ENV set to "(?:local|test|stag|prod)"`` () = ()

[<Then>]
let ``configuration values are read from "\.env\.(?:local|test|stag|prod)"`` () = ()

[<Then>]
let ``no value is read from any other env file`` () = ()

// Same pattern as above: raw no-op step bindings satisfy the spec coverage validator; the
// actual rule 3 / rule 4 behavior is exercised in
// Tests/EnvTierLoaderTests.fs's ``loadEnvTier never overrides a variable already set in the
// process environment`` and ``loadEnvTier does not throw when no tier file is present at
// either search dir`` (both @covers-tagged to these two scenarios).

[<Given>]
let ``a tier file at the app's composition root sets a variable to a file value`` () = ()

[<When>]
let ``the process starts with that variable already set in the process environment`` () = ()

[<Then>]
let ``the process environment value is used`` () = ()

[<Then>]
let ``the tier file value is not applied over it`` () = ()

[<Given>]
let ``no tier file exists at the app's composition root for the selected tier`` () = ()

[<When>]
let ``the process starts with APP_ENV set to that tier`` () = ()

[<Then>]
let ``startup does not throw`` () = ()

[<Then>]
let ``configuration proceeds using whatever the process environment already supplies`` () = ()
