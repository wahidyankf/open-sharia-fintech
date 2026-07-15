# learning/code/ex-14-md5-password-store-is-broken/md5_crack.py
"""Example 14: MD5 Password Store Is Broken."""  # => co-09/co-10: module docstring

from __future__ import (
    annotations,
)  # => co-09: DD-39 hygiene, unrelated to the crack itself

import hashlib  # => co-09: hashlib.md5 -- fast, unsalted, and exactly what makes this crack cheap
import time  # => co-09: times the dictionary attack to show HOW cheap "cheap" really is


def md5_hash(
    password: str,
) -> str:  # => co-09: the vulnerable storage function -- NO salt, NO slowness
    """Hash a password with unsalted MD5 -- VULNERABLE, do not copy."""  # => co-09: doc
    return hashlib.md5(
        password.encode()
    ).hexdigest()  # => co-09: same input ALWAYS produces the same output


def seed_database() -> dict[
    str, str
]:  # => co-09/co-10: three accounts, each password hashed the SAME broken way
    """Store three accounts as unsalted MD5 hashes -- what a leaked DB dump would contain."""  # => co-09: doc
    return {  # => co-09: username -> MD5 hash, exactly what an attacker would see in a breach
        "alice": md5_hash(
            "password123"
        ),  # => co-09: a common, dictionary-guessable password
        "bob": md5_hash("qwerty"),  # => co-09: another extremely common password
        "carol": md5_hash(
            "Xk9#mQ2vL7pR"
        ),  # => co-10: a genuinely RANDOM password -- the dictionary WON'T find this
    }  # => co-09: end of the leaked-hash dict


COMMON_PASSWORD_DICTIONARY: list[
    str
] = [  # => co-09: a tiny dictionary -- real attacker lists have MILLIONS of entries
    "123456",
    "password",
    "password123",
    "qwerty",
    "letmein",
    "admin",
    "welcome",  # => co-09: 7 common guesses
]  # => co-09: end of the dictionary


def crack_via_dictionary(
    leaked_hashes: dict[str, str], dictionary: list[str]
) -> dict[str, str]:  # => co-09: the attack
    """Recover plaintext passwords by hashing every dictionary word and comparing to leaked hashes."""  # => co-09: doc
    recovered: dict[
        str, str
    ] = {}  # => co-09: username -> recovered plaintext, filled in as matches are found
    for (
        username,
        leaked_hash,
    ) in (
        leaked_hashes.items()
    ):  # => co-09: one leaked hash per account, checked independently
        for guess in (
            dictionary
        ):  # => co-09: hash EVERY guess -- MD5 is fast enough that this is nearly free
            if (
                md5_hash(guess) == leaked_hash
            ):  # => co-09: an unsalted hash means the SAME guess ALWAYS matches
                recovered[username] = (
                    guess  # => co-09: cracked -- the leaked hash maps back to a known password
                )
                break  # => co-09: no need to keep guessing once this account's password is found
    return recovered  # => co-09: everything the dictionary attack managed to recover


if (
    __name__ == "__main__"
):  # => co-09: entry point -- seed, time the crack, then report what was recovered
    leaked = (
        seed_database()
    )  # => co-09: three MD5 hashes, as an attacker would find them in a breach
    print(
        "Leaked hashes:"
    )  # => co-09: what the attacker actually starts with -- opaque-LOOKING hex strings
    for (
        username,
        h,
    ) in leaked.items():  # => co-09: prints each account's leaked hash for reference
        print(f"  {username:<6} {h}")  # => co-09: one leaked hash per line

    start = (
        time.perf_counter()
    )  # => co-09: starts the clock right before the dictionary attack begins
    recovered = crack_via_dictionary(
        leaked, COMMON_PASSWORD_DICTIONARY
    )  # => co-09: the crack itself
    elapsed = (
        time.perf_counter() - start
    )  # => co-09: total wall-clock time for all three accounts, all seven guesses

    print(
        f"\nRecovered in {elapsed * 1000:.3f} ms:"
    )  # => co-09: sub-millisecond -- this IS "seconds" territory
    for (
        username,
        password,
    ) in (
        recovered.items()
    ):  # => co-09: one recovered plaintext per successfully cracked account
        print(
            f"  {username:<6} -> {password!r}"
        )  # => co-09: the ACTUAL plaintext, recovered with zero salting cost
    print(
        f"\naccounts cracked: {len(recovered)} of {len(leaked)}"
    )  # => co-10: carol's random password survives
