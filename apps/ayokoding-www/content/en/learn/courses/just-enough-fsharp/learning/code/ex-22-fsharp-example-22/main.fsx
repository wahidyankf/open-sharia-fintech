// ex-22 · fsharp-example-22
let values = [1; 2; 3]
values |> List.map (fun value -> value + 1) |> printfn "%A"
