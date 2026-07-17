"""Kata 5 (after): calling .result() RE-RAISES the worker's stored exception -- nothing is lost."""

from concurrent.futures import ThreadPoolExecutor


def parse_amount(raw: str) -> float:
    return float(raw)  # still raises ValueError on "n/a" -- that part of the bug is unrelated to the fix


with ThreadPoolExecutor(max_workers=2) as pool:
    future = pool.submit(parse_amount, "n/a")
    print("submitted the parse job")
    try:
        future.result()  # FIX: .result() re-raises whatever the worker itself raised
    except ValueError as exc:
        print(f"caught: {exc}")  # => Output: caught: could not convert string to float: 'n/a'
    else:
        raise AssertionError("expected future.result() to re-raise ValueError")
print("kata OK (fix verified: the ValueError was caught exactly where the caller expects it)")
