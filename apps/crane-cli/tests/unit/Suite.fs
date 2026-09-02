module CraneCli.Tests.Unit.Suite

open System.IO
open System.Reflection
open TickSpec
open Xunit

let private assembly = Assembly.GetExecutingAssembly()

let private gherkinRoot =
    match System.Environment.GetEnvironmentVariable("GHERKIN_ROOT") with
    | null -> Path.Combine(__SOURCE_DIRECTORY__, "../../../../specs/apps/crane/cli/behaviors")
    | root -> root

/// Every scenario in the owner corpus, one xUnit row each.
///
/// This function raises rather than degrading. A corpus that cannot be read is
/// indistinguishable at the exit code from a corpus that passes, so an earlier
/// version returned a single no-op row "so [Theory] does not fail with No data
/// found" — which is exactly what let a retired `gherkinRoot` path hide 36
/// scenarios behind a green target. A missing directory, an unreadable feature
/// file, and an empty corpus are all failures here.
let private buildScenarioData () : seq<obj[]> =
    if not (Directory.Exists gherkinRoot) then
        failwithf "the Gherkin corpus directory does not exist: %s" gherkinRoot

    let files =
        Directory.GetFiles(gherkinRoot, "*.feature", SearchOption.AllDirectories)

    if Array.isEmpty files then
        failwithf "no .feature file was found under %s" gherkinRoot

    let defs = StepDefinitions(assembly)

    let loaded =
        files
        |> Seq.collect (fun path ->
            let feature = defs.GenerateFeature(path)
            feature.Scenarios |> Seq.map (fun scenario -> [| scenario :> obj |]))
        |> Seq.toList

    if List.isEmpty loaded then
        failwithf "the %d feature file(s) under %s expanded to no scenarios" files.Length gherkinRoot

    loaded :> seq<_>

type CraneCliUnitSuite() =
    static member Scenarios() : seq<obj[]> =
        buildScenarioData () |> Seq.toList :> seq<_>

    [<Theory>]
    [<MemberData("Scenarios")>]
    member _.``Crane unit scenarios``(item: obj) =
        match item with
        | :? Scenario as scenario -> scenario.Action.Invoke()
        | other -> failwithf "expected a TickSpec Scenario row, got %O" (other.GetType())
