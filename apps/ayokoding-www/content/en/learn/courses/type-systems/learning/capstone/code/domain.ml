type email = Email of string
type verification = Unverified of email | Verified of email

let parse raw =
  if String.contains raw '@' then Ok (Email raw) else Error "email must contain @"

let verify = function
  | Email value -> Verified (Email value)

let send = function
  | Verified (Email value) -> "sent to " ^ value

let () =
  match parse "reader@example.test" with
  | Ok address -> print_endline (send (verify address))
  | Error message -> print_endline message
