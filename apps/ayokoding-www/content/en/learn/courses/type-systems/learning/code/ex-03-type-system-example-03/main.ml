(* ex-03 · type-system-example-03 *)
type value = Number of int | Missing
let render = function Number n -> string_of_int n | Missing -> "missing"
let () = print_endline (render (Number 1))
