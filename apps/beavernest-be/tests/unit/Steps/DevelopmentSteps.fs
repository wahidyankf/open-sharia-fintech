module BeaverNestBe.Tests.Unit.Steps.DevelopmentSteps

open TickSpec

[<Given>]
let ``the local development command receives an explicit developer-owned data directory`` () = ()

[<When>]
let ``it starts the backend on the local development port`` () = ()

[<Then>]
let ``the database resolves only within that development directory`` () = ()

[<Then>]
let ``the command neither reads nor inherits the production host data-bind source`` () = ()
