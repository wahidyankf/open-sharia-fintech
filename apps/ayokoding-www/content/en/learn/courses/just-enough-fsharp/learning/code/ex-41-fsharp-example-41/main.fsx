// ex-41 · fsharp-example-41
let values = [1; 2; 3]
values |> List.map (fun value -> value + 1) |> printfn "%A"
