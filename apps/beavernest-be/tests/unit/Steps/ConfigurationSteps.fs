module BeaverNestBe.Tests.Unit.Steps.ConfigurationSteps

open TickSpec

[<Given>]
let ``the files ".env.local" and ".env.stag" both exist at the app's composition root`` () = ()

[<When>]
let ``the process starts with APP_ENV set to "([^"]*)"`` (_tier: string) = ()

[<Then>]
let ``configuration values are read from "([^"]*)"`` (_path: string) = ()

[<Then>]
let ``no value is read from any other env file`` () = ()

// Raw no-op step bindings for the two scenarios below — same pattern as above and as
// organiclever-be's Steps/EnvTierSteps.fs: these satisfy the spec coverage validator's
// step-text matcher, while the actual rule 3 / rule 4 behavior is exercised in
// Tests/EnvTierLoaderTests.fs's ``loadEnvTierFrom never overrides a variable already set in
// the process environment`` and ``loadEnvTierFrom does nothing when the tier file is absent``
// (both @covers-tagged to these two scenarios).

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
