# pyright: strict
"""Example 25: RBAC -- a role-restricted route. (co-17)

Role-Based Access Control (RBAC) maps users -> roles -> privileges (the NIST
model, Ferraiolo & Kuhn 1992, INCITS 359). A route demands a role; a user
with the right role is allowed (200), a user with the wrong role is denied
(403). Source: NIST CSRC RBAC.
"""

from dataclasses import dataclass  # => a small typed response record


@dataclass  # => co-17: status plus a short message
class Response:
    status: int  # => 200 allowed, 403 forbidden
    body: dict[str, str]  # => a short message


# users -> role; the role -> the set of privileges it grants.
USERS: dict[str, str] = {"ada": "admin", "grace": "viewer"}  # => the user -> role mapping
ROLE_PRIVILEGES: dict[str, set[str]] = {"admin": {"billing:read", "billing:write"}, "viewer": {"billing:read"}}  # => role -> privileges


def view_billing(username: str) -> Response:  # => GET /billing -- requires billing:read
    role = USERS.get(username)  # => the user's role (None if unknown)
    privileges = ROLE_PRIVILEGES.get(role or "", set())  # => the privileges that role grants
    if "billing:read" not in privileges:  # => co-17: the role lacks the required privilege
        return Response(403, {"error": f"role {role!r} cannot read billing"})  # => 403
    return Response(200, {"billing": "ok", "viewed_by": username})  # => 200, allowed


admin = view_billing("ada")  # => role "admin" has billing:read
print(f"admin views billing:  status={admin.status}, body={admin.body}")  # => Output: 200

viewer = view_billing("grace")  # => role "viewer" ALSO has billing:read
print(f"viewer views billing: status={viewer.status}, body={viewer.body}")  # => Output: 200


# A write attempt needs billing:write, which "viewer" lacks -- the RBAC gate denies it.
def write_billing(username: str) -> Response:  # => POST /billing -- requires billing:write
    role = USERS.get(username)  # => the user's role
    privileges = ROLE_PRIVILEGES.get(role or "", set())  # => that role's privileges
    if "billing:write" not in privileges:  # => co-17: lacks the write privilege
        return Response(403, {"error": f"role {role!r} cannot write billing"})  # => 403
    return Response(200, {"written_by": username})  # => 200


viewer_write = write_billing("grace")  # => "viewer" lacks billing:write -> 403
print(f"viewer writes billing: status={viewer_write.status}, body={viewer_write.body}")  # => Output: 403

assert admin.status == 200 and viewer.status == 200  # => co-17: read allowed for both roles
assert write_billing("ada").status == 200 and viewer_write.status == 403  # => co-17: write gated by role
