// ex-43 · fsharp-example-43
let values = [1; 2; 3]
values |> List.map (fun value -> value + 1) |> printfn "%A"
