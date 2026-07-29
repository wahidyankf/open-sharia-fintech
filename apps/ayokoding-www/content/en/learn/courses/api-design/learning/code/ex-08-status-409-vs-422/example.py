# pyright: strict
"""Example 8: 409 Conflict vs. 422 Unprocessable Content. (co-07)

Two failures LOOK similar (both reject a write) but mean different things:
`409 Conflict` says the request collides with the resource's CURRENT state
(a duplicate unique value); `422 Unprocessable Content` (RFC 9110 Sec.
15.5.21) says the request body is well-formed but SEMANTICALLY invalid.
"""

from dataclasses import dataclass  # => a small typed response record for this example

USERNAMES: set[str] = {"ada"}  # => the "current state" a 409 check compares against
# => USERNAMES is {'ada'} (type: set[str]) before any of the three calls below


@dataclass  # => co-07: status plus a small JSON-shaped error/success body
class Response:
    status: int  # => the HTTP status code
    body: dict[str, str]  # => either an error message or the created resource


def create_user(username: str, age: int) -> Response:  # => POST /users -- can fail two ways
    if username in USERNAMES:  # => co-07: collides with EXISTING state -- a conflict, not a syntax error
        return Response(409, {"error": f"username {username!r} already taken"})  # => 409, state clash
    if age < 0:  # => co-07: syntactically fine (a valid integer), but semantically NONSENSE
        return Response(422, {"error": "age must be non-negative"})  # => 422, semantic failure
    USERNAMES.add(username)  # => neither failure applies -- the write actually happens
    return Response(201, {"username": username})  # => success, resource created


conflict = create_user("ada", 30)  # => "ada" already exists -> conflict, not a validation error
print(f"conflict: status={conflict.status}, body={conflict.body}")  # => Output: 409

invalid = create_user("grace", -5)  # => a brand-new username, but a nonsensical age
print(f"invalid: status={invalid.status}, body={invalid.body}")  # => Output: 422

created = create_user("grace", 37)  # => neither problem applies -- succeeds
# => created is Response(status=201, body={'username': 'grace'})
print(f"created: status={created.status}, body={created.body}")  # => Output: 201
