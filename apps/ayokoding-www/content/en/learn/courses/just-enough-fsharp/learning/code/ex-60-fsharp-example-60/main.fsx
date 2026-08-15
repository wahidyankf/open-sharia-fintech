// ex-60 · fsharp-example-60
type Expr = Number of int | Add of Expr * Expr
let rec evaluate expr = match expr with | Number n -> n | Add (l, r) -> evaluate l + evaluate r
printfn "%d" (evaluate (Add (Number 1, Number 2)))
