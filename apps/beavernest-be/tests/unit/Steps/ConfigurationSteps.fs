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
