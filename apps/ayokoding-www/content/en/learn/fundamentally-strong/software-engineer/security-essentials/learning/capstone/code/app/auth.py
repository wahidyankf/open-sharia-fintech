"""Capstone: hardened task API -- argon2id password hashing + signed bearer tokens.

NEW module (co-09, co-10, co-11, co-12, co-17) -- Backend-Essentials had no login system at
all, only a single hardcoded token compared with `!=`. This module replaces that with real
password-hash-backed auth and a signed, expiring token whose signing key lives in an env var.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time

from argon2 import PasswordHasher  # => co-09: argon2-cffi's high-level hasher
from argon2.exceptions import (
    VerifyMismatchError,
)  # => co-09: the specific "wrong password" exception

# co-09: OWASP's current minimum-tier argon2id parameters -- 19 MiB memory, 2 iterations,
# 1 degree of parallelism -- deliberately slow AND memory-hard against offline cracking.
_HASHER = PasswordHasher(memory_cost=19456, time_cost=2, parallelism=1)

TOKEN_TTL_SECONDS = (
    3600  # => co-12: a bounded lifetime -- a leaked token stops working on its own
)


def hash_password(
    password: str,
) -> str:  # => co-09: the ONLY function allowed to touch a raw password
    """Hash a password with argon2id. The DB stores ONLY this value, never the raw password."""
    return _HASHER.hash(
        password
    )  # => co-10: argon2id generates its own random salt internally, every call


def verify_password(
    stored_hash: str, candidate: str
) -> bool:  # => co-09: the verify half of the same fix
    """Verify a candidate password against a stored argon2id hash."""
    try:
        return _HASHER.verify(
            stored_hash, candidate
        )  # => co-09: True only if candidate re-hashes to stored_hash
    except (
        VerifyMismatchError
    ):  # => co-09: argon2-cffi's specific exception for "wrong password"
        return (
            False  # => co-09: normalizes the exception into a plain boolean for callers
        )


def _sign(
    payload_b64: str, secret: str
) -> str:  # => co-17: `secret` is ALWAYS a caller-supplied env value --
    digest = hmac.new(
        secret.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256
    )  # => never hardcoded here
    return digest.hexdigest()


def issue_token(user_id: int, secret: str) -> str:
    """Mint a signed, expiring bearer token.

    The signing algorithm is FIXED at HMAC-SHA256 -- never read from the token itself, so an
    attacker cannot downgrade or confuse it (co-14's `alg` confusion lesson, applied here).
    """
    payload = {
        "sub": user_id,
        "exp": int(time.time()) + TOKEN_TTL_SECONDS,
    }  # => co-12: a bounded-lifetime claim
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode(
        "ascii"
    )
    signature = _sign(payload_b64, secret)
    return f"{payload_b64}.{signature}"  # => co-12: opaque to the client -- carries no readable secret itself


def resolve_token(token: str, secret: str) -> int | None:
    """Verify a bearer token's signature and expiry, returning the user id if valid."""
    try:
        payload_b64, signature = token.split(".", 1)
    except (
        ValueError
    ):  # => co-23: malformed input fails closed -- no crash, just "not authenticated"
        return None
    expected_signature = _sign(payload_b64, secret)
    if not hmac.compare_digest(
        signature, expected_signature
    ):  # => co-11: TIMING-SAFE compare --
        return None  # => a plain `==` here would leak how many leading bytes of the signature matched
    try:
        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode("ascii")))
    except (ValueError, UnicodeDecodeError):
        return None
    if int(payload.get("exp", 0)) < int(
        time.time()
    ):  # => co-12: expired tokens are rejected, not just old ones
        return None
    return int(payload["sub"])
