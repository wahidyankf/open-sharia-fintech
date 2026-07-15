# learning/code/ex-15-argon2id-hash-and-verify/argon2id_store.py
"""Example 15: argon2id Hash and Verify."""  # => co-09: module docstring

from __future__ import (
    annotations,
)  # => co-09: DD-39 hygiene, unrelated to hashing itself

from argon2 import (
    PasswordHasher,
)  # => co-09: argon2-cffi's high-level hasher -- the FIX for Examples 13-14
from argon2.exceptions import (
    VerifyMismatchError,
)  # => co-09: the specific exception a wrong password raises

# ex-15: OWASP's current minimum-tier argon2id parameters -- 19 MiB memory, 2
# iterations, 1 degree of parallelism -- deliberately slow AND memory-hard
hasher = PasswordHasher(
    memory_cost=19456, time_cost=2, parallelism=1
)  # => co-09: m=19456 KiB, t=2, p=1


def store_password(
    password: str,
) -> str:  # => co-09: the fixed storage function -- NEVER stores the raw password
    """Hash a password with argon2id -- FIXED, replaces plaintext (Ex 13) and MD5 (Ex 14)."""  # => co-09: doc
    return hasher.hash(
        password
    )  # => co-10: argon2id GENERATES its own random salt internally, every call


def check_password(
    stored_hash: str, candidate: str
) -> bool:  # => co-09: the verify half of the same fix
    """Verify a candidate password against a stored argon2id hash."""  # => co-09: doc
    try:  # => co-09: verify() raises on mismatch rather than returning False -- caught below
        return hasher.verify(
            stored_hash, candidate
        )  # => co-09: True only if candidate re-hashes to stored_hash
    except (
        VerifyMismatchError
    ):  # => co-09: argon2-cffi's specific exception for "wrong password"
        return (
            False  # => co-09: normalizes the exception into a plain boolean for callers
        )


if (
    __name__ == "__main__"
):  # => co-09: entry point -- hash once, then verify right and wrong candidates
    stored = store_password(
        "Summer2026!"
    )  # => co-09: this is what the DATABASE now holds -- never the raw string
    print(
        f"Stored hash: {stored}"
    )  # => co-09: a real $argon2id$ PHC-format string, not the original password

    is_phc_argon2id = stored.startswith(
        "$argon2id$v=19$m=19456,t=2,p=1$"
    )  # => co-09: confirms the PHC format
    print(
        f"is a valid $argon2id$ PHC string: {is_phc_argon2id}"
    )  # => co-09: True -- proves the format, not just a guess

    print(
        f"\nverify('Summer2026!'): {check_password(stored, 'Summer2026!')}"
    )  # => co-09: True -- correct password
    print(
        f"verify('wrong-password'): {check_password(stored, 'wrong-password')}"
    )  # => co-09: False -- rejected cleanly
