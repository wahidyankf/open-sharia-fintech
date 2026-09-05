module CraneCli.Tests.E2E.Suite

open System.IO
open System.Reflection
open TickSpec
open Xunit

let private assembly = Assembly.GetExecutingAssembly()

let private gherkinRoot =
    match System.Environment.GetEnvironmentVariable("GHERKIN_ROOT") with
    | null -> Path.Combine(__SOURCE_DIRECTORY__, "../../../../specs/apps/crane/cli/behaviours")
    | root -> root

let private buildScenarioData () : seq<obj[]> =
    if not (Directory.Exists gherkinRoot) then
        failwithf "the Gherkin corpus directory does not exist: %s" gherkinRoot

    let files =
        Directory.GetFiles(gherkinRoot, "*.feature", SearchOption.AllDirectories)

    if Array.isEmpty files then
        failwithf "no .feature file was found under %s" gherkinRoot

    let definitions = StepDefinitions(assembly)

    files
    |> Seq.collect (fun path ->
        let feature = definitions.GenerateFeature(path)
        feature.Scenarios |> Seq.map (fun scenario -> [| scenario :> obj |]))
    |> Seq.toList
    :> seq<_>

type CraneCliE2eSuite() =
    static member Scenarios() : seq<obj[]> = buildScenarioData ()

    [<Theory>]
    [<MemberData("Scenarios")>]
    member _.``Crane process-boundary scenarios``(item: obj) =
        match item with
        | :? Scenario as scenario -> scenario.Action.Invoke()
        | other -> failwithf "expected a TickSpec Scenario row, got %O" (other.GetType())
