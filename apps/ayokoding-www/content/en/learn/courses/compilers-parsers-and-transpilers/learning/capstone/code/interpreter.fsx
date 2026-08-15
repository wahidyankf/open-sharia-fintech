type Token = Number of int | Plus | End
type Expr = Literal of int | Add of Expr * Expr

let tokenize (source: string) =
    let chars = source.ToCharArray() |> Array.toList
    let rec loop remaining tokens =
        match remaining with
        | [] -> Ok (List.rev (End :: tokens))
        | ' ' :: rest -> loop rest tokens
        | '+' :: rest -> loop rest (Plus :: tokens)
        | digit :: rest when System.Char.IsDigit digit ->
            loop rest (Number (int (string digit)) :: tokens)
        | bad :: _ -> Error ("unexpected character: " + string bad)
    loop chars []

let parse tokens =
    match tokens with
    | Number left :: Plus :: Number right :: End :: [] -> Ok (Add (Literal left, Literal right))
    | Number value :: End :: [] -> Ok (Literal value)
    | _ -> Error "expected number or number + number"

let rec evaluate expr =
    match expr with
    | Literal value -> value
    | Add (left, right) -> evaluate left + evaluate right

let run source =
    tokenize source
    |> Result.bind parse
    |> Result.map evaluate

if run "2 + 3" <> Ok 5 then failwith "expected five"
if run "2 ?" <> Error "unexpected character: ?" then failwith "expected diagnostic"
printfn "%A" (run "2 + 3")
