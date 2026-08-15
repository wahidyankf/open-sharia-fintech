type Email = Email of string
type Verification = Unverified of Email | Verified of Email

let parse (raw: string) =
    if raw.Contains "@" then Ok (Email raw) else Error "email must contain @"

let verify email = Verified email

let send verification =
    match verification with
    | Verified (Email value) -> "sent to " + value
    | Unverified _ -> "not verified"

parse "reader@example.test" |> Result.map verify |> Result.map send |> printfn "%A"
