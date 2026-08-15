// ex-13 · fsharp-example-13
let values = [1; 2; 3]
values |> List.map (fun value -> value + 1) |> printfn "%A"
