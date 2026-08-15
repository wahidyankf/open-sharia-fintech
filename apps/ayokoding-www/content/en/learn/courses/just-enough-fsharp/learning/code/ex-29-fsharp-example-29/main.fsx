// ex-29 · fsharp-example-29
let values = [1; 2; 3]
values |> List.map (fun value -> value + 1) |> printfn "%A"
