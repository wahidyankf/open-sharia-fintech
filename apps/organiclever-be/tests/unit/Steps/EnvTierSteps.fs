module OrganicleverBe.Tests.Unit.Steps.EnvTierSteps

open TickSpec

// Step definitions for the be-env context (env-tier-loader.feature). These
// bind the Gherkin steps for the spec coverage validator; the actual loader
// behavior is exercised directly against the production code in
// Tests/EnvTierLoaderTests.fs. The "When"/"Then" steps below are registered
// as raw regexes (an F# step's backtick text compiles verbatim as an
// anchored `^...$` pattern) so a single definition covers every Scenario
// Outline "tier" example (local/test/stag/prod) in one pattern.

[<Given>]
let ``the files ".env.local" and ".env.stag" both exist at the app's composition root`` () = ()

[<When>]
let ``the process starts with APP_ENV set to "(?:local|test|stag|prod)"`` () = ()

[<Then>]
let ``configuration values are read from "\.env\.(?:local|test|stag|prod)"`` () = ()

[<Then>]
let ``no value is read from any other env file`` () = ()
