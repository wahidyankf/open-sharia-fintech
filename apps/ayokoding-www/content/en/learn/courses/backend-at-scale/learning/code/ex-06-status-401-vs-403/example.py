# pyright: strict
"""Example 6: 401 Unauthorized vs 403 Forbidden. (co-02)

401 = authentication required and has failed or not been provided; 403 = the
server refuses to authorize a VALID identity that lacks permission. The two
are distinct: 401 is "who are you?", 403 is "I know who you are, but no."
Source: RFC 9110 Sec 15.5.1 (401) and Sec 15.5.4 (403).
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-02: status plus an error message
class Response:
    status: int  # => the HTTP status code
    body: dict[str, str]  # => a short error explanation


# A toy token store: token -> (user, role). "admin" can delete; "viewer" cannot.
TOKENS: dict[str, tuple[str, str]] = {"tok-admin": ("ada", "admin"), "tok-viewer": ("grace", "viewer")}
REQUIRED_ROLE = "admin"  # => the role this protected operation demands


def delete_task(token: str | None, task_id: int) -> Response:  # => DELETE /tasks/{id}, auth-gated
    if token is None or token not in TOKENS:  # => co-02: no identity provided OR identity not recognized -> 401
        return Response(401, {"error": "authentication required"})  # => 401: "who are you?"
    _user, role = TOKENS[token]  # => identity is valid -- now check authorization
    if role != REQUIRED_ROLE:  # => co-02: valid identity, but lacks the required role -> 403
        return Response(403, {"error": "insufficient role"})  # => 403: "I know you, but no."
    return Response(204, {"deleted": str(task_id)})  # => authenticated AND authorized -> 204


no_token = delete_task(token=None, task_id=1)  # => no Authorization header at all
print(f"no token:     status={no_token.status}, body={no_token.body}")  # => Output: 401

bad_token = delete_task(token="tok-bogus", task_id=1)  # => a token the server does not recognize
print(f"bad token:    status={bad_token.status}, body={bad_token.body}")  # => Output: 401

wrong_role = delete_task(token="tok-viewer", task_id=1)  # => valid identity, but role "viewer" cannot delete
print(f"wrong role:   status={wrong_role.status}, body={wrong_role.body}")  # => Output: 403

ok = delete_task(token="tok-admin", task_id=1)  # => valid identity, correct role
print(f"admin:        status={ok.status}, body={ok.body}")  # => Output: 204

assert no_token.status == 401 and bad_token.status == 401  # => co-02: auth-missing is 401
assert wrong_role.status == 403  # => co-02: valid-auth-but-forbidden is 403
assert ok.status == 204  # => authorized
