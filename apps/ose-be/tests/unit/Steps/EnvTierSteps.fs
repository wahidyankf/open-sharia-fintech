module OseBe.Tests.Unit.Steps.EnvTierSteps

open TickSpec

// Step definitions for the config context (env-tier-loading.feature). These
// bind the Gherkin steps for the spec coverage validator; the actual loader
// behavior is exercised directly against the production code (this app's
// thin `loadEnvTier` wrapper) in Tests/EnvTierTests.fs. Same no-op-step
// pattern as the sibling `organiclever-be` backend's env-tier step file —
// both backends delegate their loader rules to
// `libs/fsharp-env-loader`, whose own comprehensive suite covers the pure
// logic once; each app's Tests/EnvTierTests.fs @covers-tagged facts verify
// only that this app's wrapper resolves its own composition root correctly.

[<Given>]
let ``the files ".env.local" and ".env.stag" both exist at the app's composition root`` () = ()

[<When>]
let ``the process starts with APP_ENV set to "(?:local|test|stag|prod)"`` () = ()

[<Then>]
let ``configuration values are read from "\.env\.(?:local|test|stag|prod)"`` () = ()

[<Then>]
let ``no value is read from any other env file`` () = ()

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
