# pyright: strict
"""Capstone Step 2: OAuth2/OIDC + RBAC layered onto the service. (co-15, co-17)

Adds an OIDC identity layer on top of the Step-1 service: a bearer token is
verified as an OIDC id_token (co-15), and an RBAC role gate (co-17) restricts
POST /v1/articles to the "editor" role. A role-restricted route returns 403
for the wrong role and 200/201 for the right one.
"""

import base64  # => stdlib: base64url for the id_token segments
import hashlib  # => stdlib: SHA-256 for the HMAC
import hmac  # => stdlib: HMAC-SHA256 signing + constant-time compare
import json  # => stdlib: serialize the id_token claims
from dataclasses import dataclass, field  # => field: mutable-default-safe factories

SECRET = b"capstone-secret"  # => the HMAC shared secret for the OIDC issuer
REQUIRED_ROLE = "editor"  # => co-17: the role allowed to create articles

# token -> the decoded id_token claims (sub, role). Stands in for the IdP-issued id_token.
TOKEN_CLAIMS: dict[str, dict[str, object]] = {
    "tok-editor": {"sub": "ada", "role": "editor"},  # => co-17: the allowed role
    "tok-viewer": {
        "sub": "grace",
        "role": "viewer",
    },  # => co-17: a role that cannot create
}


def b64url(raw: bytes) -> str:  # => base64url without padding
    return (
        base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")
    )  # => JWT segment format


def sign(message: bytes) -> str:  # => HMAC-SHA256 -> base64url
    return b64url(hmac.new(SECRET, message, hashlib.sha256).digest())  # => keyed hash


def issue_id_token(
    claims: dict[str, object],
) -> str:  # => co-15: an OIDC id_token is a signed JWT
    header = b64url(
        json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode()
    )  # => header
    payload = b64url(json.dumps(claims, separators=(",", ":")).encode())  # => claims
    return f"{header}.{payload}.{sign(f'{header}.{payload}'.encode())}"  # => the signed id_token


def verify_id_token(
    token: str,
) -> dict[str, object] | None:  # => co-15: verify signature, return claims
    try:
        header_b64, payload_b64, signature = token.split(".")  # => the three segments
    except ValueError:  # => malformed
        return None  # => reject
    if not hmac.compare_digest(
        sign(f"{header_b64}.{payload_b64}".encode()), signature
    ):  # => signature mismatch
        return None  # => reject
    return json.loads(
        base64.urlsafe_b64decode(payload_b64 + "==")
    )  # => the verified identity claims


# Pre-issue id_tokens for the two subjects (stands in for the OIDC token endpoint).
ID_TOKENS: dict[str, str] = {
    sub: issue_id_token(claims) for sub, claims in TOKEN_CLAIMS.items()
}  # => co-15

STORE: dict[int, dict[str, object]] = {
    1: {"id": 1, "title": "Hello, Capstone"}
}  # => seed data
NEXT_ID = [2]  # => the next id


@dataclass  # => the response shape
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object] = field(
        default_factory=dict[str, object]
    )  # => resource or error


def create_article_v1(
    token: str, title: str
) -> Response:  # => POST /v1/articles -- OIDC + RBAC gated
    claims = verify_id_token(
        token
    )  # => co-15: verify the id_token (OIDC authentication)
    if claims is None:  # => invalid id_token -> 401
        return Response(401, {"error": "invalid id_token"})  # => 401
    if (
        claims.get("role") != REQUIRED_ROLE
    ):  # => co-17: valid identity, wrong role -> 403
        return Response(
            403, {"error": f"role {claims.get('role')!r} cannot create"}
        )  # => 403
    new_id = NEXT_ID[0]  # => authorized -> create
    article: dict[str, object] = {"id": new_id, "title": title}  # => the new resource
    STORE[new_id] = article  # => persist
    NEXT_ID[0] += 1  # => advance
    return Response(201, article)  # => 201 created


editor = create_article_v1(
    ID_TOKENS["tok-editor"], "Editor's article"
)  # => co-17: editor role -> allowed
viewer = create_article_v1(
    ID_TOKENS["tok-viewer"], "Viewer's attempt"
)  # => co-17: viewer role -> 403
bogus = create_article_v1("not-a-real-token", "X")  # => co-15: invalid id_token -> 401
print(f"editor creates: status={editor.status}, body={editor.body}")  # => Output: 201
print(f"viewer creates: status={viewer.status}, body={viewer.body}")  # => Output: 403
print(f"bogus token:    status={bogus.status}, body={bogus.body}")  # => Output: 401

assert (
    editor.status == 201 and viewer.status == 403 and bogus.status == 401
)  # => co-15/co-17: auth + RBAC gates work
