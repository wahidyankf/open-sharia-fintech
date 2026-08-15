// ex-67 · fsharp-example-67
type Expr = Number of int | Add of Expr * Expr
let rec evaluate expr = match expr with | Number n -> n | Add (l, r) -> evaluate l + evaluate r
printfn "%d" (evaluate (Add (Number 1, Number 2)))
