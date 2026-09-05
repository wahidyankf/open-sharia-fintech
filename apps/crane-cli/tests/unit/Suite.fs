module CraneCli.Tests.Unit.Suite

open System
open System.IO
open System.Reflection
open TickSpec
open Xunit

let private assembly = Assembly.GetExecutingAssembly()

/// Every scenario in the owner corpus, one xUnit row each.
///
/// Feature text is embedded at build time so Unit setup remains in-process and
/// never discovers or reads the real filesystem at runtime.
let private buildScenarioData () : seq<obj[]> =
    let resources =
        assembly.GetManifestResourceNames()
        |> Array.filter (fun name -> name.EndsWith(".feature", StringComparison.Ordinal))

    if Array.isEmpty resources then
        failwith "no embedded .feature resource was found for the Crane Unit corpus"

    let defs = StepDefinitions(assembly)

    let loaded =
        resources
        |> Seq.collect (fun resourceName ->
            use stream = assembly.GetManifestResourceStream(resourceName)

            if isNull stream then
                failwithf "embedded Gherkin resource cannot be opened: %s" resourceName

            use reader = new StreamReader(stream)

            let lines =
                reader.ReadToEnd().Replace("\r\n", "\n", StringComparison.Ordinal).Split('\n')

            let feature = defs.GenerateFeature(resourceName, lines)
            feature.Scenarios |> Seq.map (fun scenario -> [| scenario :> obj |]))
        |> Seq.toList

    if List.isEmpty loaded then
        failwithf "the %d embedded feature resource(s) expanded to no scenarios" resources.Length

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
