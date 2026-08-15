// ex-39 · fsharp-example-39
let values = [1; 2; 3]
values |> List.map (fun value -> value + 1) |> printfn "%A"
