// ex-21 · fsharp-example-21
let values = [1; 2; 3]
values |> List.map (fun value -> value + 1) |> printfn "%A"
