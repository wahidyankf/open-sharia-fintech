# learning/code/ex-64-password-upgrade-on-login/upgrade_on_login.py
"""Example 64: a real legacy bcrypt hash transparently upgrades to argon2id on the FIRST successful login (co-09, co-10)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the upgrade logic itself

import bcrypt  # => co-09: bcrypt 5.0.0 pinned -- the REAL legacy hasher this user's stored hash starts as
from argon2 import (
    PasswordHasher,
)  # => co-09: argon2-cffi 25.1.0 pinned -- the REAL target hasher this example upgrades to
from argon2.exceptions import (
    VerifyMismatchError,
)  # => co-09: the REAL exception argon2's verify() raises on a bad password

argon2_hasher = (
    PasswordHasher()
)  # => co-09: one real, shared argon2id hasher -- default (OWASP min-tier) parameters
USERS: dict[str, str] = {
    "alice": bcrypt.hashpw(b"correct-horse", bcrypt.gensalt()).decode()
}  # => co-09: a REAL bcrypt hash


def login(
    username: str, password: str
) -> bool:  # => co-09: the ONE real login function -- verify, then maybe upgrade
    stored_hash = USERS.get(
        username
    )  # => co-09: the REAL, current on-file hash for this user -- bcrypt OR argon2id
    if stored_hash is None:  # => co-09: a real guard -- no such user at all
        return False  # => co-09: a real, unambiguous failure for an unknown username

    if stored_hash.startswith("$2b$") or stored_hash.startswith(
        "$2a$"
    ):  # => co-09: the REAL bcrypt PHC-string prefix
        is_valid = bcrypt.checkpw(
            password.encode(), stored_hash.encode()
        )  # => co-09: a real bcrypt verification
        if (
            is_valid
        ):  # => co-09: ONLY on a real, successful login does the upgrade ever happen
            # => co-09: the fix -- transparently rehash with argon2id and REPLACE the stored value,
            # => using the password the user JUST proved they know, right here, while it's in memory
            USERS[username] = argon2_hasher.hash(
                password
            )  # => co-09: a REAL argon2id hash now REPLACES the bcrypt one
        return is_valid  # => co-09: the real login outcome -- unaffected by whether an upgrade happened

    # => co-09: stored_hash is ALREADY argon2id -- the normal, no-upgrade-needed path
    try:  # => co-09: argon2's verify() raises on a mismatch rather than returning False
        argon2_hasher.verify(
            stored_hash, password
        )  # => co-09: a real argon2id verification
        return True  # => co-09: a real, successful login -- no upgrade needed, already on the target hasher
    except (
        VerifyMismatchError
    ):  # => co-09: the REAL exception type argon2-cffi raises for a wrong password
        return False  # => co-09: a real, failed login


def main() -> (
    None
):  # => co-09: proves the hash is bcrypt-shaped BEFORE login, argon2id-shaped immediately AFTER
    print(
        f"stored hash BEFORE login: {USERS['alice'][:12]}..."
    )  # => co-09: real, truncated -- starts with $2b$
    assert USERS["alice"].startswith(
        "$2b$"
    )  # => co-09: proves alice's stored hash really is legacy bcrypt right now

    print("\n=== a real login with the CORRECT password ===")  # => labels section
    ok = login(
        "alice", "correct-horse"
    )  # => co-09: a REAL login call -- the SAME password bcrypt.hashpw used above
    print(f"login result: {ok}")  # => co-09: real, computed outcome
    assert (
        ok is True
    )  # => co-09: proves the login itself really succeeded, via the bcrypt verification path

    print(
        f"\nstored hash AFTER login: {USERS['alice'][:20]}..."
    )  # => co-09: real, truncated -- now starts with $argon2id$
    assert USERS["alice"].startswith(
        "$argon2id$"
    )  # => co-09: proves the transparent upgrade REALLY happened, in-place

    print(
        "\n=== a SECOND real login -- now verified via argon2id, no further upgrade needed ==="
    )  # => labels section
    ok2 = login(
        "alice", "correct-horse"
    )  # => co-09: a REAL second login -- this time against the NEW argon2id hash
    print(f"login result: {ok2}")  # => co-09: real, computed outcome
    assert (
        ok2 is True
    )  # => co-09: proves the upgraded hash itself really authenticates the same real password
    assert USERS["alice"].startswith(
        "$argon2id$"
    )  # => co-09: proves it stays argon2id -- no re-upgrade, no re-hash churn

    print(
        "\n=== a real login with the WRONG password never upgrades anything ==="
    )  # => labels section
    wrong_hash_before = USERS[
        "alice"
    ]  # => co-09: a real snapshot of the current stored hash, before the bad attempt
    ok3 = login(
        "alice", "totally-wrong-password"
    )  # => co-09: a REAL, deliberately wrong login attempt
    print(f"login result: {ok3}")  # => co-09: real, computed outcome -- False
    assert (
        ok3 is False and USERS["alice"] == wrong_hash_before
    )  # => co-09: proves a failed login NEVER mutates the hash


if (
    __name__ == "__main__"
):  # => co-09: only runs when launched directly, e.g. `python3 upgrade_on_login.py`
    main()  # => co-09: runs all three real login scenarios and verifies the real bcrypt -> argon2id transition
