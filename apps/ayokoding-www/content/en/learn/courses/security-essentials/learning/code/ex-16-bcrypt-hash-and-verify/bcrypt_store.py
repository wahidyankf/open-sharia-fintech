# learning/code/ex-16-bcrypt-hash-and-verify/bcrypt_store.py
"""Example 16: bcrypt Hash and Verify."""  # => co-09: module docstring

from __future__ import (
    annotations,
)  # => co-09: DD-39 hygiene, unrelated to hashing itself

import bcrypt  # => co-09: bcrypt 5.0.0 -- the OTHER OWASP-approved slow hash, alongside argon2id (Ex 15)

WORK_FACTOR = 12  # => co-09: the bcrypt "cost" -- each +1 DOUBLES the hashing time, 12 is a solid floor


def store_password(
    password: str,
) -> bytes:  # => co-09: the fixed storage function -- work-factor baked into the hash
    """Hash a password with bcrypt at work-factor 12 -- FIXED, an alternative to argon2id."""  # => co-09: doc
    salt = bcrypt.gensalt(
        rounds=WORK_FACTOR
    )  # => co-10: gensalt() draws a FRESH random salt every single call
    return bcrypt.hashpw(
        password.encode(), salt
    )  # => co-09: the salt AND cost are embedded in the returned hash


def check_password(
    stored_hash: bytes, candidate: str
) -> bool:  # => co-09: the verify half of the same fix
    """Verify a candidate password against a stored bcrypt hash."""  # => co-09: doc
    return bcrypt.checkpw(
        candidate.encode(), stored_hash
    )  # => co-09: re-derives the hash using the EMBEDDED salt/cost


if (
    __name__ == "__main__"
):  # => co-09: entry point -- hash/verify, then the 72-byte truncation demo
    stored = store_password(
        "Summer2026!"
    )  # => co-09: this is what the DATABASE now holds -- never the raw string
    print(
        f"Stored hash: {stored.decode()}"
    )  # => co-09: embeds the algorithm id AND cost factor in its own text

    embeds_cost = stored.decode().startswith(
        "$2b$12$"
    )  # => co-09: '2b' = bcrypt variant, '12' = the work factor
    print(
        f"hash embeds algorithm '2b' and cost '12': {embeds_cost}"
    )  # => co-09: True -- visible without decoding

    print(
        f"\nverify('Summer2026!'): {check_password(stored, 'Summer2026!')}"
    )  # => co-09: True -- correct password
    print(
        f"verify('wrong-password'): {check_password(stored, 'wrong-password')}"
    )  # => co-09: False -- rejected cleanly

    print(
        "\n=== bcrypt's hard 72-byte input limit ==="
    )  # => co-09: the caveat this example also proves
    long_a = ("A" * 72) + "-tail-one"  # => co-09: 72 'A' bytes, THEN a unique suffix
    long_b = (
        ("A" * 72) + "-tail-TWO-totally-different"
    )  # => co-09: the SAME first 72 bytes, a DIFFERENT suffix
    truncated_a = long_a.encode()[
        :72
    ]  # => co-09: bcrypt itself refuses inputs over 72 bytes -- truncate manually first
    truncated_b = long_b.encode()[
        :72
    ]  # => co-09: manual truncation, mirroring what bcrypt enforces internally
    print(
        f"first 72 bytes identical: {truncated_a == truncated_b}"
    )  # => co-09: True -- both truncate to the SAME bytes
    shared_salt = bcrypt.gensalt(
        rounds=WORK_FACTOR
    )  # => co-09: SAME salt for both, isolating the truncation effect
    hash_a = bcrypt.hashpw(
        truncated_a, shared_salt
    )  # => co-09: hashes password A's truncated 72 bytes
    hash_b = bcrypt.hashpw(
        truncated_b, shared_salt
    )  # => co-09: hashes password B's truncated 72 bytes
    print(
        f"hash of password A: {hash_a.decode()}"
    )  # => co-09: the resulting bcrypt hash for long_a
    print(
        f"hash of password B: {hash_b.decode()}"
    )  # => co-09: the resulting bcrypt hash for long_b
    print(
        f"hashes are IDENTICAL despite different passwords: {hash_a == hash_b}"
    )  # => co-09: True -- the 72-byte cap in action
