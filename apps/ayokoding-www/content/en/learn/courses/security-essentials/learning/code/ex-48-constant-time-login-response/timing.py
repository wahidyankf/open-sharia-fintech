"""Example 48: naive short-circuit login leaks WHICH usernames exist via timing; hashing a dummy narrows it (co-11, co-27)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the timing measurement itself

import hashlib  # => co-11: real PBKDF2 hashing -- the SAME expensive work both paths must (or must not) pay
import hmac  # => co-11: hmac.compare_digest -- constant-time comparison, not a plain "=="
import time  # => co-27: real wall-clock timestamps -- every measurement below is genuinely timed

SALT = b"ex48-fixed-demo-salt"  # => co-11: a real salt -- fixed here only so both paths hash identical work
DUMMY_HASH = hashlib.pbkdf2_hmac(
    "sha256", b"dummy-password", SALT, 100_000
)  # => co-11: precomputed ONCE, reused
USERS = {
    "alice": hashlib.pbkdf2_hmac("sha256", b"correct-horse", SALT, 100_000)
}  # => co-11: one REAL known user


def naive_login(
    username: str, password: str
) -> bool:  # => co-27: VULNERABLE -- short-circuits for unknown users
    if (
        username not in USERS
    ):  # seeded bug: returns immediately, WITHOUT ever hashing anything
        return False  # => co-27: this branch is dramatically cheaper than the one below -- a real timing signal
    candidate = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), SALT, 100_000
    )  # => co-11: real, expensive hashing
    return hmac.compare_digest(
        candidate, USERS[username]
    )  # => co-11: constant-time compare -- but only reached here


def constant_time_login(
    username: str, password: str
) -> bool:  # => co-11: FIXED -- always pays the same real cost
    stored_hash = USERS.get(
        username, DUMMY_HASH
    )  # => co-11: a REAL user's hash, or the precomputed dummy -- same size
    candidate = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), SALT, 100_000
    )  # => co-11: hashed EVERY time, no exception
    is_match = hmac.compare_digest(
        candidate, stored_hash
    )  # => co-11: constant-time compare, always executed
    return (
        is_match and username in USERS
    )  # => co-11: the ACTUAL correctness check, after the timing-safe work is done


def average_time(
    login_fn, username: str, password: str, iterations: int
) -> float:  # => co-27: real timing harness
    start = time.perf_counter()  # => co-27: a real, high-resolution wall-clock start
    for _ in range(
        iterations
    ):  # => co-27: repeats the SAME call many times to average out real system noise
        login_fn(
            username, password
        )  # => co-27: the actual call under measurement -- return value unused here
    return (
        time.perf_counter() - start
    ) / iterations  # => co-27: real average seconds per call


def main() -> (
    None
):  # => co-27: measures known-vs-unknown-username timing for BOTH the naive and fixed functions
    iterations = 2000  # => co-27: enough repeats for the real timing gap to become measurable, not just noise

    print("=== naive_login: known user vs. unknown user ===")  # => labels section
    naive_known = average_time(
        naive_login, "alice", "wrong-password", iterations
    )  # => co-27: real average, known user
    naive_unknown = average_time(
        naive_login, "not-a-real-user", "wrong-password", iterations
    )  # => co-27: unknown user
    naive_gap = abs(
        naive_known - naive_unknown
    )  # => co-27: the real, measured timing DIFFERENCE
    print(
        f"known={naive_known * 1e6:.1f}us unknown={naive_unknown * 1e6:.1f}us gap={naive_gap * 1e6:.1f}us"
    )

    print("\n=== constant_time_login: SAME two cases ===")  # => labels section
    fixed_known = average_time(
        constant_time_login, "alice", "wrong-password", iterations
    )  # => co-11: real average
    fixed_unknown = average_time(
        constant_time_login, "not-a-real-user", "wrong-password", iterations
    )  # => co-11
    fixed_gap = abs(
        fixed_known - fixed_unknown
    )  # => co-11: the real, measured timing difference -- should be SMALLER
    print(
        f"known={fixed_known * 1e6:.1f}us unknown={fixed_unknown * 1e6:.1f}us gap={fixed_gap * 1e6:.1f}us"
    )

    print(
        f"\nnaive_gap / fixed_gap = {naive_gap / max(fixed_gap, 1e-9):.1f}x"
    )  # => co-11: real, relative narrowing
    assert (
        fixed_gap < naive_gap
    )  # => co-11: proves hashing a dummy for unknown users really narrows the real gap


if (
    __name__ == "__main__"
):  # => co-27: only runs when launched directly, e.g. `python3 timing.py`
    main()  # => co-27: runs all four real timing measurements and prints the real comparison
