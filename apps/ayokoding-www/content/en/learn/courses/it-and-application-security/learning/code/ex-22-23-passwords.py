"""Examples 22–23: Argon2id password hashing and verification."""

from __future__ import (
    annotations,
)  # => Modern type syntax without runtime compatibility surprises.

from argon2 import (
    PasswordHasher,
)  # => Maintained Argon2id implementation, not a fast general hash.
from argon2.exceptions import (
    VerifyMismatchError,
)  # => Wrong-password result is expected control flow.

HASHER = PasswordHasher(
    memory_cost=19_456, time_cost=2, parallelism=1
)  # => OWASP minimum-tier Argon2id settings.


def verify(
    candidate: str,
) -> bool:  # => Candidate represents one login attempt, never stored plaintext.
    stored = HASHER.hash(
        "correct horse battery staple"
    )  # => Generates a fresh salt inside the encoded hash.
    try:  # => Verification can reject ordinary wrong credentials without revealing why.
        return HASHER.verify(
            stored, candidate
        )  # => True only when candidate matches the Argon2id hash.
    except VerifyMismatchError:  # => Mismatch is deliberately normalized to false.
        return False  # => Caller can emit the same generic login failure response.


if __name__ == "__main__":  # => Demonstrates both outcomes locally.
    print(verify("correct horse battery staple"))  # => Expected: True.
    print(verify("incorrect"))  # => Expected: False.
