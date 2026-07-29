# pyright: strict
"""Example 23: JWT -- encode, sign, and verify (HS256, hand-rolled). (co-14)

A JWT is a signed, self-contained claims token (RFC 7519): header.payload.
signature, base64url-encoded, signed with HMAC-SHA256. The receiver verifies
the signature WITHOUT a session lookup -- the token itself carries the claims.
"""

import base64  # => stdlib: base64url encoding for each JWT segment
import hashlib  # => stdlib: SHA-256 for the HMAC
import hmac  # => stdlib: HMAC-SHA256 signing + constant-time compare
import json  # => stdlib: serialize the header and claims to compact JSON

SECRET = b"super-secret-key"  # => the HMAC shared secret (in production, loaded from env, never hardcoded in source shipped to a client)


def b64url(raw: bytes) -> str:  # => base64url-encode WITHOUT "=" padding (the JWT segment format)
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")  # => strips padding per RFC 7515


def sign(message: bytes) -> str:  # => HMAC-SHA256, then base64url -- the JWT signature segment
    return b64url(hmac.new(SECRET, message, hashlib.sha256).digest())  # => keyed hash over header.payload


def encode(claims: dict[str, object]) -> str:  # => co-14: build a signed compact JWT
    header = b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())  # => segment 1: header
    payload = b64url(json.dumps(claims, separators=(",", ":")).encode())  # => segment 2: claims
    signing_input = f"{header}.{payload}".encode()  # => the bytes the signature covers
    signature = sign(signing_input)  # => segment 3: signature
    return f"{header}.{payload}.{signature}"  # => the compact serialised JWT


def verify(token: str) -> dict[str, object] | None:  # => co-14: verify signature + return claims, or None on tamper
    try:
        header_b64, payload_b64, signature = token.split(".")  # => the three segments
    except ValueError:  # => not three segments -> malformed
        return None  # => reject
    expected = sign(f"{header_b64}.{payload_b64}".encode())  # => recompute the signature over the same input
    if not hmac.compare_digest(expected, signature):  # => co-14: constant-time compare; mismatch -> tampered
        return None  # => reject
    raw = base64.urlsafe_b64decode(payload_b64 + "==")  # => re-pad before decoding the payload
    return json.loads(raw)  # => the verified claims


token = encode({"sub": "user-42", "role": "admin"})  # => co-14: issue a signed token
print(f"token: {token[:48]}...")  # => Output: a prefix of the compact JWT (truncated for display)

claims = verify(token)  # => co-14: verify + decode -- no session lookup needed
print(f"verified claims: {claims}")  # => Output: {'sub': 'user-42', 'role': 'admin'}

tampered = token[:-2] + ("AA" if not token.endswith("AA") else "BB")  # => corrupt the signature segment
print(f"tampered verifies: {verify(tampered)}")  # => Output: None -- signature mismatch rejected

assert claims == {"sub": "user-42", "role": "admin"}  # => co-14: round-trip succeeds
assert verify(tampered) is None  # => co-14: a tampered token is rejected
