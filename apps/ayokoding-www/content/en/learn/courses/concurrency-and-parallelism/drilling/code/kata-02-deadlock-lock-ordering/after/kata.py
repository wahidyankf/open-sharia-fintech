"""Kata 2 (after): a single GLOBAL lock-acquisition order breaks the circular wait -- no deadlock."""

import threading

# => Fix: BOTH workers now agree to always acquire `printer` before `scanner`, regardless of which
# => task they are performing -- this ONE global order makes a circular wait structurally impossible.
# => (No Barrier is needed here, unlike the before/ version: with a shared first lock, at most ONE
# => worker can ever be mid-acquisition at a time, so there is no "both hold their first lock
# => simultaneously" state left to force -- the fix removes the deadlock at the STRUCTURAL level,
# => not merely by winning a timing race.)


def worker_prints_then_scans(printer: threading.Lock, scanner: threading.Lock) -> None:
    with printer:  # => grabs printer FIRST, same as before
        with scanner:  # => grabs scanner second -- always reachable, printer is never held by scanner-first code
            pass


def worker_scans_then_prints(printer: threading.Lock, scanner: threading.Lock) -> None:
    with printer:  # => FIX: also grabs printer first -- the SAME global order as worker_prints_then_scans
        with scanner:  # => grabs scanner second, matching the agreed-upon order
            pass


def run_without_deadlock() -> tuple[bool, bool]:  # => returns (worker_a_still_hung, worker_b_still_hung)
    printer = threading.Lock()
    scanner = threading.Lock()
    w_a = threading.Thread(target=worker_prints_then_scans, args=(printer, scanner), daemon=True)
    w_b = threading.Thread(target=worker_scans_then_prints, args=(printer, scanner), daemon=True)
    w_a.start()
    w_b.start()
    w_a.join(timeout=0.5)  # => with the fix, both workers finish well inside this bound
    w_b.join(timeout=0.5)
    return w_a.is_alive(), w_b.is_alive()  # => False, False means both finished -- no deadlock


if __name__ == "__main__":
    a_hung, b_hung = run_without_deadlock()
    print(f"a_hung={a_hung} b_hung={b_hung}")
    # => Whichever worker grabs `printer` first simply runs to completion (grabs scanner, releases
    # => both) before the other worker's own `printer` acquisition can even succeed -- the circular
    # => wait Coffman condition can never arise once every path agrees on ONE lock-acquisition order.
    assert a_hung is False  # => confirms worker_a finished and released both locks
    assert b_hung is False  # => confirms worker_b finished and released both locks
    print("kata OK (fix verified)")
