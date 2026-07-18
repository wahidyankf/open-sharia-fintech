"""Example 26: `add_done_callback` Fires on Completion."""

import threading  # => guards the shared log the callback appends to (co-11)
from collections.abc import Callable  # => precisely types the closure add_done_callback expects
from concurrent.futures import Future, ThreadPoolExecutor  # => co-25: Futures and their callbacks


def slow_double(x: int) -> int:  # => the work a pool thread runs
    return x * 2  # => the eventual result the Future will hold


def make_callback(log: list[str], lock: threading.Lock) -> Callable[["Future[int]"], None]:
    # => returns a closure so the callback can safely append to `log` without a race (co-11)
    def on_done(fut: "Future[int]") -> None:  # => the EXACT signature add_done_callback requires
        with lock:  # => protects `log` -- callbacks can run on a DIFFERENT thread than the caller
            log.append(f"done:{fut.result()}")  # => fut.result() never blocks here -- it's already done

    return on_done  # => the callable to register


if __name__ == "__main__":  # => module entry point
    events: list[str] = []  # => shared log the callback writes into
    guard = threading.Lock()  # => protects `events` from concurrent callback invocations
    with ThreadPoolExecutor(max_workers=1) as pool:  # => a single worker thread
        future: "Future[int]" = pool.submit(slow_double, 21)  # => schedules the work, returns a Future
        future.add_done_callback(make_callback(events, guard))  # => registers the typed callback above
        result = future.result()  # => blocks until slow_double() finishes AND the callback has run

    print(f"result={result}")  # => Output: result=42
    print(events)  # => Output: ['done:42']

    # => `add_done_callback` fires automatically the moment the Future transitions to "done" --
    # => no polling required. If the Future was ALREADY done when registered, the callback fires
    # => immediately, on whatever thread called add_done_callback (not necessarily the worker).
    assert result == 42  # => confirms the underlying computation's result is correct
    assert events == ["done:42"]  # => confirms the callback actually ran, with the correct result
    print("ex-26 OK")  # => Output: ex-26 OK
