# pyright: strict
"""Example 7: 409 Conflict -- a duplicate create. (co-02)

409 Conflict means the request collides with the resource's CURRENT state --
here, creating a username that already exists. The request itself is well-
formed, but applying it right now would duplicate a unique value. Source:
RFC 9110 Sec 15.5.10.
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-02: status plus an error or success body
class Response:
    status: int  # => the HTTP status code
    body: dict[str, str]  # => either an error message or the created resource


USERNAMES: set[str] = {"ada"}  # => the "current state" a 409 uniqueness check compares against


def create_user(username: str) -> Response:  # => POST /users -- can succeed or collide
    if username in USERNAMES:  # => co-02: collides with EXISTING state -- a conflict, not a syntax error
        return Response(409, {"error": f"username {username!r} already taken"})  # => 409, state clash
    USERNAMES.add(username)  # => no collision -- the write actually happens
    return Response(201, {"username": username})  # => success, resource created


conflict = create_user("ada")  # => "ada" already exists -> conflict
print(f"duplicate: status={conflict.status}, body={conflict.body}")  # => Output: 409

created = create_user("grace")  # => a brand-new username -> succeeds
print(f"new user:  status={created.status}, body={created.body}")  # => Output: 201

second_conflict = create_user("grace")  # => "grace" now also exists -> conflict
print(f"duplicate: status={second_conflict.status}, body={second_conflict.body}")  # => Output: 409

assert conflict.status == 409 and second_conflict.status == 409  # => co-02: both duplicates are 409
assert created.status == 201  # => the genuinely new one succeeded
