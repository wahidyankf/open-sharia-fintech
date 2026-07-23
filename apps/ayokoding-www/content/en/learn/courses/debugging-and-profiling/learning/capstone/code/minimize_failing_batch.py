"""Capstone step 1 (continued): delta-debug the 400-order failing batch down to
a minimal reproducer, verifying the minimized case still fails with the
IDENTICAL exception.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to delta-debugging itself

import sys  # => needed only for sys.path.insert below

sys.path.insert(
    0, "."
)  # => co-11: makes local make_failing_batch.py/pipeline.py importable regardless of caller's cwd
from make_failing_batch import make_failing_batch  # noqa: E402  # => co-11: the SAME 400-order batch this whole capstone starts from
from pipeline import build_customer_report  # noqa: E402  # => co-11: the SAME pipeline function whose KeyError this example minimizes


def crash_signature(
    orders: list[dict],
) -> (
    str | None
):  # => co-11: the SAME oracle shape as ex-45/46/62 -- name+message, not the traceback
    try:  # => co-11: catches whatever build_customer_report() actually raises, to compare signatures across candidates
        build_customer_report(
            orders
        )  # => co-11: the SAME function under minimization, called with a candidate subset
    except Exception as exc:  # noqa: BLE001 -- deliberately broad: compare signatures  # => co-11: catches ANY exception type
        return f"{type(exc).__name__}: {exc}"  # => co-11: the signature ddmin_orders compares against the original
    return None  # => co-11: no exception at all -- this candidate does NOT reproduce the crash


def ddmin_orders(
    orders: list[dict], target_signature: str
) -> list[dict]:  # => co-11: the SAME n-way ddmin loop as ex-62
    n = 2  # => co-11: starts by splitting the input into 2 chunks
    current = list(
        orders
    )  # => co-11: the SMALLEST failing input found SO FAR -- shrinks across iterations
    while len(current) >= 2:  # => co-11: stops once no further splitting is possible
        chunk_size = max(
            1, len(current) // n
        )  # => co-11: at least 1 order per chunk, even as current shrinks
        chunks = [
            current[i : i + chunk_size] for i in range(0, len(current), chunk_size)
        ]  # => co-11: n roughly-equal chunks
        reduced = False  # => co-11: tracks whether THIS pass found a smaller failing candidate
        for i in range(
            len(chunks)
        ):  # => co-11: tries removing each chunk in turn, one at a time
            candidate = [
                order for j, chunk in enumerate(chunks) if j != i for order in chunk
            ]  # => co-11: all EXCEPT chunk i
            if (
                candidate and crash_signature(candidate) == target_signature
            ):  # => co-11: still fails the SAME way?
                current = candidate  # => co-11: keeps the smaller candidate -- a genuine reduction
                n = max(
                    n - 1, 2
                )  # => co-11: retries with fewer chunks next pass, per the classic ddmin algorithm
                reduced = (
                    True  # => co-11: signals the outer while loop to continue shrinking
                )
                break  # => co-11: restarts chunking from the new, smaller current
        if (
            not reduced
        ):  # => co-11: no single-chunk removal reproduced the crash this pass
            if n >= len(
                current
            ):  # => co-11: already at maximum granularity -- cannot split further
                break  # => co-11: ddmin has converged -- current is now 1-minimal
            n = min(
                n * 2, len(current)
            )  # => co-11: doubles the chunk count for a finer-grained next attempt
    return current  # => co-11: the final, minimized-but-still-crashing batch


def main() -> (
    None
):  # => co-11: builds the 400-order batch, minimizes it, and verifies the result
    original = make_failing_batch()  # => co-11: the large, realistic starting batch
    original_signature = crash_signature(
        original
    )  # => co-11: the exception ddmin must preserve exactly
    assert original_signature is not None, (
        "sanity check: the 400-order batch must fail first"
    )  # => co-11: the real check
    print(
        f"original batch: {len(original)} orders"
    )  # => co-11: confirms the starting size before minimizing
    print(
        f"original failure: {original_signature}"
    )  # => co-11: the exact signature the minimized case must match

    minimal = ddmin_orders(
        original, original_signature
    )  # => co-11: the automated reduction, start to finish
    minimal_signature = crash_signature(
        minimal
    )  # => co-11: re-derives the signature from the MINIMIZED batch
    print(
        f"minimized batch: {len(minimal)} order(s)"
    )  # => co-11: the headline result -- how far it shrank
    print(
        f"minimized order(s): {minimal!r}"
    )  # => co-11: shows the actual surviving order(s), for a human to read
    print(
        f"minimized failure: {minimal_signature}"
    )  # => co-11: proves the SAME exception, not a different one

    assert minimal_signature == original_signature, (
        "minimized batch must raise the IDENTICAL exception"
    )  # => co-11: real check
    print(
        f"confirmed: {len(original)} orders reduced to {len(minimal)}, same exception preserved exactly"
    )  # => co-11: the payoff


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that builds, minimizes, and verifies the failing batch
