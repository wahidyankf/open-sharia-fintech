# pyright: strict
"""Example 30: OpenID Connect -- an id_token carries identity. (co-15)

OpenID Connect (OIDC) is an IDENTITY LAYER on top of OAuth 2.0: alongside
the access token, the token endpoint also issues an id_token -- a JWT whose
claims (sub, email) describe WHO the user is. So OAuth 2.0 = authorization,
OIDC = authentication. Source: OpenID Connect Core 1.0.
"""

import base64  # => stdlib: base64url for the JWT segments
import hashlib  # => stdlib: SHA-256 for HMAC
import hmac  # => stdlib: HMAC-SHA256 signing
import json  # => stdlib: serialize header and claims

SECRET = b"oidc-secret"  # => the HMAC shared secret


def b64url(raw: bytes) -> str:  # => base64url without padding
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")  # => JWT segment format


def sign(message: bytes) -> str:  # => HMAC-SHA256 -> base64url
    return b64url(hmac.new(SECRET, message, hashlib.sha256).digest())  # => keyed hash


def issue_id_token(subject: str, email: str) -> str:  # => co-15: the id_token is a SIGNED JWT
    header = b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())  # => header segment
    claims: dict[str, object] = {"sub": subject, "email": email, "iss": "https://idp.example.com"}  # => identity claims
    payload = b64url(json.dumps(claims, separators=(",", ":")).encode())  # => claims segment
    return f"{header}.{payload}.{sign(f'{header}.{payload}'.encode())}"  # => the signed id_token


def decode_id_token(token: str) -> dict[str, object]:  # => verify + decode the id_token's claims
    _header, payload_b64, signature = token.split(".")  # => the three segments
    assert hmac.compare_digest(sign(token.rsplit(".", 1)[0].encode()), signature)  # => signature valid
    return json.loads(base64.urlsafe_b64decode(payload_b64 + "=="))  # => the verified identity claims


# The token endpoint returns BOTH an access_token (OAuth2 -- what you may do) and an id_token (OIDC -- who you are).
access_token = "access-for-user-42"  # => co-15: OAuth2 -- authorization
id_token = issue_id_token(subject="user-42", email="ada@example.com")  # => co-15: OIDC -- authentication
print(f"token endpoint returned access_token + id_token (truncated): {access_token}, {id_token[:24]}...")

identity = decode_id_token(id_token)  # => co-15: the id_token's claims describe the user
print(f"verified identity (sub): {identity['sub']}, email: {identity['email']}")  # => Output: user-42, ada@example.com

assert identity["sub"] == "user-42" and identity["email"] == "ada@example.com"  # => co-15: OIDC carries identity
