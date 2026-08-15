// ex-10 · fsharp-example-10
let values = [1; 2; 3]
values |> List.map (fun value -> value + 1) |> printfn "%A"
