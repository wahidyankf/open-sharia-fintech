# learning/code/ex-17-salt-makes-identical-passwords-differ/salt_demo.py
"""Example 17: Salt Makes Identical Passwords Differ."""  # => co-10: module docstring

from __future__ import (
    annotations,
)  # => co-10: DD-39 hygiene, unrelated to salting itself

from argon2 import (
    PasswordHasher,
)  # => co-10: reuses Example 15's hasher -- salting is BUILT IN, not a separate step

hasher = PasswordHasher(
    memory_cost=19456, time_cost=2, parallelism=1
)  # => co-10: same OWASP min-tier params as Ex 15


def extract_salt_segment(
    phc_hash: str,
) -> str:  # => co-10: pulls the salt field OUT of the PHC-format string
    """Return the salt segment of an argon2id PHC-format hash string."""  # => co-10: doc
    return phc_hash.split(
        "$"
    )[
        4
    ]  # => co-10: PHC layout: $argon2id$v=19$m=..,t=..,p=..$SALT$HASH -- index 4 is the salt


if (
    __name__ == "__main__"
):  # => co-10: entry point -- hash the SAME password twice, compare both outputs
    same_password = (
        "Summer2026!"  # => co-10: the IDENTICAL input string, hashed twice below
    )

    hash_one = hasher.hash(
        same_password
    )  # => co-10: first call -- generates its OWN fresh random salt internally
    hash_two = hasher.hash(
        same_password
    )  # => co-10: second call, SAME password -- a DIFFERENT fresh salt this time

    print(
        f"Hash #1: {hash_one}"
    )  # => co-10: the first stored hash -- what account A's row would hold
    print(
        f"Hash #2: {hash_two}"
    )  # => co-10: the second stored hash -- what account B's row would hold

    salt_one = extract_salt_segment(
        hash_one
    )  # => co-10: the random salt argon2id chose for hash_one
    salt_two = extract_salt_segment(
        hash_two
    )  # => co-10: the random salt argon2id chose for hash_two
    print(
        f"\nsalt #1: {salt_one}"
    )  # => co-10: base64-encoded, 16 random bytes chosen by argon2id itself
    print(
        f"salt #2: {salt_two}"
    )  # => co-10: a DIFFERENT 16 random bytes, drawn independently

    print(
        f"\nsalts are different: {salt_one != salt_two}"
    )  # => co-10: True -- proves each call salts independently
    print(
        f"full hashes are different: {hash_one != hash_two}"
    )  # => co-10: True -- SAME password, DIFFERENT ciphertext

    both_verify = hasher.verify(hash_one, same_password) and hasher.verify(
        hash_two, same_password
    )  # => co-10: sanity
    print(
        f"both hashes still verify the SAME original password: {both_verify}"
    )  # => co-10: True -- correctness intact
