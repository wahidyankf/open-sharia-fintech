"""Kata 5 (before): a worker's exception is silently swallowed because .result() is never called."""

from concurrent.futures import ThreadPoolExecutor


def parse_amount(raw: str) -> float:
    return float(raw)  # BUG-ADJACENT: raises ValueError on "n/a" -- nothing here catches it


with ThreadPoolExecutor(max_workers=2) as pool:
    future = pool.submit(parse_amount, "n/a")  # SMELL: the future is submitted but never inspected
    print("submitted the parse job")
    # BUG: the function body never calls future.result(), so the ValueError raised inside
    # parse_amount() is stored on the Future object and silently DISCARDED when the pool shuts down.
print("pool closed -- did anything go wrong? no exception was ever raised here")
print("kata OK (bug reproduced: the ValueError never surfaced anywhere)")
