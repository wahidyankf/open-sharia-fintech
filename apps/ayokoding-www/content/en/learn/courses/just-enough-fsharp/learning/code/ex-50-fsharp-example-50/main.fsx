// ex-50 · fsharp-example-50
let values = [1; 2; 3]
values |> List.map (fun value -> value + 1) |> printfn "%A"
