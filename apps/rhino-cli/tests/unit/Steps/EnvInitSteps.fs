module RhinoCli.Tests.Unit.Steps.EnvInitSteps

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/env/env-init.feature" ]

open TickSpec
open Xunit
open RhinoCli.Application.Env

type EnvInitSteps() =
    let root = "/virtual/repository"
    let mutable examples: string list = []
    let mutable existing: Set<string> = Set.empty
    let mutable force = false
    let mutable result: EnvInitResult option = None
    let mutable output = ""

    let outcome () =
        result |> Option.defaultWith (fun () -> failwith "env init did not run")

    let run () =
        let value = planEnvInit root examples (fun path -> Set.contains path existing) force
        result <- Some value
        output <- formatEnvInitText value

    [<Given>]
    member _.``.env.example files exist in infra/dev but no .env.local files``() =
        examples <- [ root + "/infra/dev/api/.env.example"; root + "/infra/dev/web/.env.example" ]

    [<Given>]
    member _.``.env.example files exist in infra/dev and some .env.local files already exist``() =
        examples <- [ root + "/infra/dev/api/.env.example"; root + "/infra/dev/web/.env.example" ]
        existing <- Set.singleton (root + "/infra/dev/api/.env.local")

    [<Given>]
    member _.``no .env.example files exist in infra/dev``() = examples <- []

    [<When>]
    member _.``the developer runs env init``() = run ()

    [<When>]
    member _.``the developer runs env init with the force flag``() =
        force <- true
        run ()

    [<Then>]
    member _.``the command exits successfully``() = Assert.True(result.IsSome)

    [<Then>]
    member _.``.env.local files are created from each .env.example``() = Assert.Equal(2, (outcome ()).Created)

    [<Then>]
    member _.``no bare .env file is created``() =
        Assert.DoesNotContain(
            (outcome ()).Files,
            fun file ->
                match file with
                | EnvInitCreated(path, _) -> path.EndsWith("/.env")
                | _ -> false
        )

    [<Then>]
    member _.``the output lists each created file``() =
        Assert.Contains("infra/dev/api/.env.local", output)
        Assert.Contains("infra/dev/web/.env.local", output)

    [<Then>]
    member _.``existing .env.local files are not overwritten``() = Assert.Equal(1, (outcome ()).Skipped)

    [<Then>]
    member _.``the output shows skipped files``() = Assert.Contains("Skipped:", output)

    [<Then>]
    member _.``all .env.local files are created or overwritten``() = Assert.Equal(2, (outcome ()).Created)

    [<Then>]
    member _.``the output reports zero files created``() =
        Assert.Equal(0, (outcome ()).Created)
        Assert.Contains("0 created", output)

[<Fact>]
let ``env init creates local tier paths only`` () =
    let steps = EnvInitSteps()
    steps.``.env.example files exist in infra/dev but no .env.local files`` ()
    steps.``the developer runs env init`` ()
    steps.``.env.local files are created from each .env.example`` ()
    steps.``no bare .env file is created`` ()
    steps.``the output lists each created file`` ()

[<Fact>]
let ``env init preserves existing files unless forced`` () =
    let steps = EnvInitSteps()
    steps.``.env.example files exist in infra/dev and some .env.local files already exist`` ()
    steps.``the developer runs env init`` ()
    steps.``existing .env.local files are not overwritten`` ()
    steps.``the output shows skipped files`` ()

[<Fact>]
let ``env init force overwrites existing local tiers`` () =
    let steps = EnvInitSteps()
    steps.``.env.example files exist in infra/dev and some .env.local files already exist`` ()
    steps.``the developer runs env init with the force flag`` ()
    steps.``all .env.local files are created or overwritten`` ()

[<Fact>]
let ``env init empty discovery succeeds with zero created`` () =
    let steps = EnvInitSteps()
    steps.``no .env.example files exist in infra/dev`` ()
    steps.``the developer runs env init`` ()
    steps.``the command exits successfully`` ()
    steps.``the output reports zero files created`` ()
