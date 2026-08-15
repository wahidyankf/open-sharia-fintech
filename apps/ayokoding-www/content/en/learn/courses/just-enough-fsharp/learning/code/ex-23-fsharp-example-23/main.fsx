// ex-23 · fsharp-example-23
let values = [1; 2; 3]
values |> List.map (fun value -> value + 1) |> printfn "%A"
