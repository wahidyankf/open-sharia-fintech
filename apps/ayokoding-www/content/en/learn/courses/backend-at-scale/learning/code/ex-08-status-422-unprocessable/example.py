# pyright: strict
"""Example 8: 422 Unprocessable Content -- well-formed but semantically invalid. (co-02)

RFC 9110 Sec 15.5.21 defines 422 "Unprocessable Content" (renamed from
RFC 4918's WebDAV-era "Unprocessable Entity"). The JSON parses fine, but a
field fails a BUSINESS rule -- here, a negative age. RFC 9110 does NOT
obsolete RFC 4918; they coexist. Teach "Unprocessable Content".
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-02: status plus an error or success body
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object]  # => either a field error or the created resource


def create_user(username: str, age: int) -> Response:  # => POST /users -- syntactically valid, semantically checked
    if age < 0:  # => co-02: a valid integer, but a nonsensical VALUE -- semantic, not syntactic
        return Response(422, {"error": "age must be non-negative", "field": "age"})  # => 422, semantic failure
    return Response(201, {"username": username, "age": age})  # => success, resource created


negative_age = create_user("grace", -5)  # => a well-formed body, but a semantically invalid age
print(f"negative age: status={negative_age.status}, body={negative_age.body}")  # => Output: 422

valid = create_user("grace", 37)  # => a fully valid input
print(f"valid:        status={valid.status}, body={valid.body}")  # => Output: 201

# Contrast with a 400 (Example 5): here the JSON parsed fine -- the failure is the VALUE's meaning.
assert negative_age.status == 422  # => co-02: semantic failure is 422, not 400
assert valid.status == 201  # => a valid value succeeds
