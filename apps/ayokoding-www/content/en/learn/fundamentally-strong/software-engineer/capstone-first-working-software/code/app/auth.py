"""Pass-1 capstone: Habit Tracker -- argon2id password hashing + a signed, expiring bearer
token (topic 17 security hardening). This module reuses the exact pattern topic 17's own
Security Essentials capstone already built and verified (`security-essentials/learning/capstone/code/app/auth.py`):
argon2id via `argon2-cffi`, a timing-safe HMAC-SHA256 signature check, and a bounded token
lifetime -- proven correct there, reused here rather than re-derived from scratch.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time

from argon2 import PasswordHasher  # => argon2-cffi's high-level hasher (topic 17 co-09)
from argon2.exceptions import (
    VerifyMismatchError,
)  # => the specific "wrong password" exception

# OWASP's current minimum-tier argon2id parameters -- 19 MiB memory, 2 iterations, 1 degree of
# parallelism -- deliberately slow AND memory-hard against offline cracking (topic 17 co-09).
_HASHER = PasswordHasher(memory_cost=19456, time_cost=2, parallelism=1)

TOKEN_TTL_SECONDS = (
    3600  # => a bounded lifetime -- a leaked token stops working on its own
)


def hash_password(
    password: str,
) -> str:  # => the ONLY function allowed to touch a raw password
    """Hash a password with argon2id. The DB stores ONLY this value, never the raw password."""
    return _HASHER.hash(
        password
    )  # => argon2id generates its own random salt internally, every call


def verify_password(stored_hash: str, candidate: str) -> bool:
    """Verify a candidate password against a stored argon2id hash."""
    try:
        return _HASHER.verify(
            stored_hash, candidate
        )  # => True only if candidate re-hashes to stored_hash
    except (
        VerifyMismatchError
    ):  # => argon2-cffi's specific exception for "wrong password"
        return False  # => normalizes the exception into a plain boolean for callers


def _sign(
    payload_b64: str, secret: str
) -> str:  # => `secret` is ALWAYS a caller-supplied env value --
    digest = hmac.new(
        secret.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256
    )  # never hardcoded here
    return digest.hexdigest()


def issue_token(user_id: int, secret: str) -> str:
    """Mint a signed, expiring bearer token. The signing algorithm is FIXED at HMAC-SHA256 --
    never read from the token itself, so an attacker cannot downgrade or confuse it."""
    payload = {
        "sub": user_id,
        "exp": int(time.time()) + TOKEN_TTL_SECONDS,
    }  # => a bounded-lifetime claim
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode(
        "ascii"
    )
    signature = _sign(payload_b64, secret)
    return f"{payload_b64}.{signature}"  # => opaque to the client -- carries no readable secret itself


def resolve_token(token: str, secret: str) -> int | None:
    """Verify a bearer token's signature and expiry, returning the user id if valid."""
    try:
        payload_b64, signature = token.split(".", 1)
    except (
        ValueError
    ):  # => malformed input fails closed -- no crash, just "not authenticated"
        return None
    expected_signature = _sign(payload_b64, secret)
    if not hmac.compare_digest(
        signature, expected_signature
    ):  # => TIMING-SAFE compare --
        return None  # => a plain `==` here would leak how many leading bytes of the signature matched
    try:
        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode("ascii")))
    except (ValueError, UnicodeDecodeError):
        return None
    if int(payload.get("exp", 0)) < int(
        time.time()
    ):  # => expired tokens are rejected, not just old ones
        return None
    return int(payload["sub"])
