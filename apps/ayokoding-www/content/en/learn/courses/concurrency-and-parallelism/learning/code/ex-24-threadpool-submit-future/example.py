"""Example 24: `submit()` Returns a `Future`; `.result()` Blocks."""

from concurrent.futures import Future, ThreadPoolExecutor  # => co-23 pool + co-25 Future placeholder


def compute(x: int, y: int) -> int:  # => a plain function -- submit() runs it on a pool thread
    return x * y  # => the eventual result, wrapped in a Future until it's ready


if __name__ == "__main__":  # => module entry point
    with ThreadPoolExecutor(max_workers=2) as pool:  # => a small pool, auto-shutdown on exit
        future: Future[int] = pool.submit(compute, 6, 7)  # => submit() returns IMMEDIATELY -- non-blocking
        is_running_or_pending = not future.done()  # => likely True: the pool thread may not have finished yet
        value = future.result()  # => .result() BLOCKS until compute() finishes, then returns its value
    print(f"value={value}")  # => Output: value=42
    print(f"done_after_result={future.done()}")  # => Output: done_after_result=True

    # => `submit()` gives you a Future the instant you call it -- a PLACEHOLDER for a result that
    # => does not exist yet. `.result()` is the one call that actually waits for that placeholder
    # => to be filled in, turning "eventually" into "now, blocking this thread until it's ready".
    assert value == 42  # => confirms .result() returned the correct computed value
    assert future.done() is True  # => confirms the Future is now resolved
    print("ex-24 OK")  # => Output: ex-24 OK
