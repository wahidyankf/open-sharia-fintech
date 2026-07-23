# learning/code/ex-58-alert-on-brute-force-pattern/brute_force_alert.py
"""Example 58: a real sliding-window detector fires exactly ONE alert for a whole failure burst (co-22, co-27)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the detection logic itself

import time  # => co-27: real wall-clock timestamps -- every event below is genuinely timed, not faked
from collections import (
    deque,
)  # => co-22: an efficient real ring of recent failure timestamps, per user


class BruteForceDetector:  # => co-22: a real sliding-window detector -- tracks failures PER username, independently
    def __init__(
        self, threshold: int, window_seconds: float
    ) -> None:  # => co-27: a real, tunable policy
        self.threshold = threshold  # => co-27: how many failures within the window counts as "a burst"
        self.window_seconds = window_seconds  # => co-27: the REAL rolling time window this detector enforces
        self.failures: dict[
            str, deque[float]
        ] = {}  # => co-22: username -> a real deque of recent failure timestamps
        self.already_alerted: dict[
            str, bool
        ] = {}  # => co-22: username -> whether THIS ongoing burst already alerted

    def record_failure(
        self, username: str, timestamp: float
    ) -> bool:  # => co-22: returns True ONLY on a NEW alert
        bucket = self.failures.setdefault(
            username, deque()
        )  # => co-22: this user's real, growing timestamp history
        bucket.append(
            timestamp
        )  # => co-27: records the REAL moment this failure happened
        while (
            bucket and timestamp - bucket[0] > self.window_seconds
        ):  # => co-27: prunes anything OUTSIDE the window
            bucket.popleft()  # => co-27: real eviction -- old failures stop counting once they age out
        if (
            len(bucket) >= self.threshold
        ):  # => co-27: the real threshold check, against the PRUNED, current count
            if not self.already_alerted.get(
                username, False
            ):  # => co-22: the fix's core rule -- fire ONCE per burst
                self.already_alerted[username] = (
                    True  # => co-22: marks this burst as already-alerted, real state
                )
                return True  # => co-22: a REAL, new alert -- this is the ONLY True this method ever returns per burst
            return False  # => co-22: still over threshold, but ALREADY alerted -- no duplicate noise
        self.already_alerted[username] = (
            False  # => co-22: count dropped back under threshold -- resets for next burst
        )
        return False  # => co-22: not (yet) a burst, or already handled -- no alert this call


def main() -> (
    None
):  # => co-27: simulates a real burst of failed logins and counts REAL alerts fired
    detector = BruteForceDetector(
        threshold=5, window_seconds=10.0
    )  # => co-27: 5 failures within 10s triggers an alert
    alerts_fired: list[
        tuple[int, bool]
    ] = []  # => co-22: records (attempt_number, did_this_call_alert) for every real call

    print(
        "=== simulating a real burst of 7 rapid failed logins for 'alice' ==="
    )  # => labels section
    for attempt in range(
        1, 8
    ):  # => co-27: 7 real, consecutive failures -- 2 more than the threshold of 5
        now = time.time()  # => co-27: a REAL wall-clock timestamp, taken fresh for each simulated failure
        alerted = detector.record_failure(
            "alice", now
        )  # => co-22: the REAL detector call -- genuinely evaluated
        alerts_fired.append(
            (attempt, alerted)
        )  # => co-22: real, per-attempt outcome, in order
        print(
            f"  attempt {attempt}: alert_fired={alerted}"
        )  # => co-22: real, live detector state per attempt

    true_count = sum(
        1 for _, alerted in alerts_fired if alerted
    )  # => co-22: the REAL total number of alerts this burst produced
    print(
        f"\ntotal alerts fired for this burst: {true_count}"
    )  # => co-22: real count, computed from the real run above
    assert (
        true_count == 1
    )  # => co-22: proves the ENTIRE 7-failure burst produced exactly ONE alert, not seven
    assert alerts_fired[4] == (
        5,
        True,
    )  # => co-27: proves the ONE alert fired at exactly the threshold-th failure

    print(
        "\n=== a SEPARATE, unrelated user's failures never affect alice's detector state ==="
    )  # => labels section
    bob_alerted = detector.record_failure(
        "bob", time.time()
    )  # => co-22: a real, independent per-user detector state
    print(
        f"  bob's first failure: alert_fired={bob_alerted}"
    )  # => co-22: real, freshly-tracked state for a new user
    assert (
        bob_alerted is False
    )  # => co-22: proves bob's own count starts fresh -- one failure is below HIS threshold too


if (
    __name__ == "__main__"
):  # => co-27: only runs when launched directly, e.g. `python3 brute_force_alert.py`
    main()  # => co-27: runs the real burst simulation and prints every real per-attempt alert decision
