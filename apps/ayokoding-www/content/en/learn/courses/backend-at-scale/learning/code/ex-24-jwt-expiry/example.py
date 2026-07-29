# pyright: strict
"""Example 24: JWT -- an expired token is rejected. (co-14)

A JWT carries an `exp` (expiry) claim: the receiver rejects any token whose
exp is in the past. This is how short-lived tokens limit the blast radius of a
stolen token. Source: RFC 7519 Sec 4.1.4 (`exp`).
"""

import base64  # => stdlib: base64url segment encoding
import hashlib  # => stdlib: SHA-256 for the HMAC
import hmac  # => stdlib: HMAC-SHA256 signing
import json  # => stdlib: serialize header and claims


SECRET = b"super-secret-key"  # => the HMAC shared secret


def b64url(raw: bytes) -> str:  # => base64url without padding
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")  # => JWT segment format


def sign(message: bytes) -> str:  # => HMAC-SHA256 -> base64url
    return b64url(hmac.new(SECRET, message, hashlib.sha256).digest())  # => keyed hash


def encode(claims: dict[str, object]) -> str:  # => build a signed compact JWT
    header = b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())  # => header segment
    payload = b64url(json.dumps(claims, separators=(",", ":")).encode())  # => claims segment
    return f"{header}.{payload}.{sign(f'{header}.{payload}'.encode())}"  # => compact JWT


def verify(token: str, now: int) -> dict[str, object] | None:  # => co-14: signature + expiry check
    header_b64, payload_b64, signature = token.split(".")  # => the three segments
    if not hmac.compare_digest(sign(f"{header_b64}.{payload_b64}".encode()), signature):  # => signature mismatch
        return None  # => reject
    claims: dict[str, object] = json.loads(base64.urlsafe_b64decode(payload_b64 + "=="))  # => decode claims
    exp = claims.get("exp")  # => co-14: the expiry timestamp
    if isinstance(exp, int) and now >= exp:  # => co-14: `now` is AT/AFTER exp -> token expired
        return None  # => reject -- the token's lifetime is over
    return claims  # => fresh enough -> valid


fresh = encode({"sub": "user-1", "exp": 2000})  # => a token expiring at t=2000
expired = encode({"sub": "user-1", "exp": 1000})  # => a token that already expired at t=1000

print(f"fresh at now=1500:   {verify(fresh, now=1500)}")  # => Output: claims -- now < exp
print(f"expired at now=1500: {verify(expired, now=1500)}")  # => Output: None -- now >= exp

assert verify(fresh, now=1500) is not None  # => co-14: a not-yet-expired token passes
assert verify(expired, now=1500) is None  # => co-14: an expired token is rejected
