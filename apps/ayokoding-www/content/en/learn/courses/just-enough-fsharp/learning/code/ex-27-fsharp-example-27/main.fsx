// ex-27 · fsharp-example-27
let values = [1; 2; 3]
values |> List.map (fun value -> value + 1) |> printfn "%A"
