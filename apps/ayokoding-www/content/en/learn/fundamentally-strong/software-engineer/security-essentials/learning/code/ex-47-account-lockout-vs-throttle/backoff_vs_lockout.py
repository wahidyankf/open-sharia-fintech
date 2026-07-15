"""Example 47: exponential backoff slows a real brute-force loop; hard lockout names its own DoS risk (co-27)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the backoff/lockout logic itself

import time  # => co-27: real wall-clock sleeps -- the backoff delay is genuinely measured, not simulated


class BackoffLimiter:  # => co-27: throttles WITHOUT ever permanently locking the account
    def __init__(
        self,
    ) -> None:  # => co-27: constructor -- starts with zero recorded failures
        self.failures = (
            0  # => co-27: a real, growing counter of consecutive wrong attempts
        )

    def delay_for_next_attempt(
        self,
    ) -> float:  # => co-27: the REAL sleep duration this failure count now costs
        return min(
            2.0**self.failures * 0.01, 1.0
        )  # => co-27: exponential growth, capped at 1s for this demo

    def record_failure(
        self,
    ) -> None:  # => co-27: called after each real wrong-password attempt
        self.failures += 1  # => co-27: legitimate users who mistype ONCE barely feel this -- it compounds slowly


class HardLockout:  # => co-27: locks the account OUTRIGHT after a fixed number of failures
    def __init__(
        self, max_failures: int = 3
    ) -> None:  # => co-27: a real, small threshold for this demo
        self.failures = (
            0  # => co-27: a real, growing counter, same shape as BackoffLimiter's
        )
        self.max_failures = max_failures  # => co-27: once reached, the account is DEAD until manual/timed reset
        self.locked = (
            False  # => co-27: the real, binary lockout state this class introduces
        )

    def record_failure(
        self,
    ) -> None:  # => co-27: called after each real wrong-password attempt
        self.failures += 1  # => co-27: identical bookkeeping to BackoffLimiter -- the RESPONSE differs, not the count
        if self.failures >= self.max_failures:  # => co-27: the real threshold check
            self.locked = True  # => co-27: from here on, EVEN THE REAL OWNER cannot log in -- that is the DoS risk


def time_brute_force_with_backoff(
    attempts: int,
) -> float:  # => co-27: real wall-clock time for N failed attempts
    limiter = BackoffLimiter()  # => co-27: a fresh limiter, zero recorded failures
    start = (
        time.monotonic()
    )  # => co-27: real wall-clock start -- not a fake/simulated clock
    for _ in range(
        attempts
    ):  # => co-27: simulates a real attacker trying `attempts` wrong passwords in a row
        time.sleep(
            limiter.delay_for_next_attempt()
        )  # => co-27: a REAL sleep -- the attacker actually waits this long
        limiter.record_failure()  # => co-27: each failure makes the NEXT sleep longer
    return (
        time.monotonic() - start
    )  # => co-27: the real, measured total time this brute-force attempt cost


def main() -> (
    None
):  # => co-27: measures real backoff timing, then demonstrates the lockout DoS risk directly
    print(
        "=== exponential backoff really slows a real brute-force loop ==="
    )  # => labels section
    elapsed_3 = time_brute_force_with_backoff(
        3
    )  # => co-27: real elapsed time for 3 consecutive failures
    elapsed_8 = time_brute_force_with_backoff(
        8
    )  # => co-27: real elapsed time for 8 consecutive failures
    print(
        f"3 attempts took {elapsed_3:.3f}s real wall-clock time"
    )  # => co-27: a real, measured number
    print(
        f"8 attempts took {elapsed_8:.3f}s real wall-clock time"
    )  # => co-27: a real, measured, LARGER number
    assert (
        elapsed_8 > elapsed_3
    )  # => co-27: proves the delay genuinely compounds as failures accumulate

    print(
        "\n=== hard lockout: a THIRD PARTY can lock out the real account owner ==="
    )  # => labels section
    lockout = HardLockout(
        max_failures=3
    )  # => co-27: a real lockout instance, same threshold as a real policy might use
    for attempt in range(
        1, 4
    ):  # => co-27: an ATTACKER, not the real owner, deliberately fails 3 times
        lockout.record_failure()  # => co-27: real state mutation -- this really happens to the SAME account row
        print(
            f"attacker's failed attempt {attempt}: locked={lockout.locked}"
        )  # => co-27: real, live lockout state
    assert lockout.locked  # => co-27: proves the account is now locked -- BEFORE the real owner ever tried logging in
    print(
        "the REAL owner, who never entered a wrong password, is now locked out too"
    )  # => co-27: the named DoS risk


if (
    __name__ == "__main__"
):  # => co-27: only runs when launched directly, e.g. `python3 backoff_vs_lockout.py`
    main()  # => co-27: measures real backoff timing, then demonstrates the real account-lockout DoS risk
