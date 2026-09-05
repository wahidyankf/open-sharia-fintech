module RhinoCli.Tests.Unit.Steps.ContractsSteps

open TickSpec
open Xunit
open RhinoCli.Application.Contracts

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/contracts/contracts-dart-scaffold.feature" ]

type ContractsSteps() =
    let mutable models: string list = []
    let mutable oldScaffold = false
    let mutable plan: DartScaffoldPlan option = None

    let result () =
        plan |> Option.defaultWith (fun () -> failwith "scaffold was not planned")

    [<Given>]
    member _.``a generated-contracts directory with model Dart files``() =
        models <- [ "user.dart"; "account.dart" ]

    [<Given>]
    member _.``a generated-contracts directory with no model files``() = models <- []

    [<Given>]
    member _.``an existing generated-contracts directory with old scaffold files``() = oldScaffold <- true

    [<When>]
    member _.``the developer runs specs scaffold dart on the directory``() = plan <- Some(planDartScaffold models)

    [<Then>]
    member _.``the command exits successfully``() =
        Assert.True((result ()).Result.PubspecCreated && (result ()).Result.BarrelCreated)

    [<Then>]
    member _.``pubspec.yaml is created with correct content``() =
        Assert.Equal(PubspecContent, (result ()).Pubspec)

    [<Then>]
    member _.``pubspec.yaml is created``() =
        Assert.Equal(PubspecContent, (result ()).Pubspec)

    [<Then>]
    member _.``the barrel library is created with part directives for each model``() =
        Assert.Equal<string list>([ "account.dart"; "user.dart" ], (result ()).Result.ModelFiles)
        Assert.Contains("part 'model/account.dart';", (result ()).Barrel)
        Assert.Contains("part 'model/user.dart';", (result ()).Barrel)

    [<Then>]
    member _.``the barrel library is created without part directives``() =
        Assert.DoesNotContain("part 'model/", (result ()).Barrel)

    [<Then>]
    member _.``the existing files are overwritten with fresh scaffold``() =
        Assert.True(oldScaffold)
        Assert.Equal(PubspecContent, (result ()).Pubspec)
        Assert.Equal(BarrelHeader + BarrelUtils, (result ()).Barrel)

[<Fact>]
let ``Normal scaffold with model files`` () =
    let w = ContractsSteps() in
    w.``a generated-contracts directory with model Dart files`` ()
    w.``the developer runs specs scaffold dart on the directory`` ()
    w.``the command exits successfully`` ()
    w.``pubspec.yaml is created with correct content`` ()
    w.``the barrel library is created with part directives for each model`` ()

[<Fact>]
let ``Scaffold with no model files`` () =
    let w = ContractsSteps() in
    w.``a generated-contracts directory with no model files`` ()
    w.``the developer runs specs scaffold dart on the directory`` ()
    w.``the command exits successfully`` ()
    w.``pubspec.yaml is created`` ()
    w.``the barrel library is created without part directives`` ()

[<Fact>]
let ``Scaffold overwrites existing files`` () =
    let w = ContractsSteps() in
    w.``an existing generated-contracts directory with old scaffold files`` ()
    w.``the developer runs specs scaffold dart on the directory`` ()
    w.``the command exits successfully`` ()
    w.``the existing files are overwritten with fresh scaffold`` ()
