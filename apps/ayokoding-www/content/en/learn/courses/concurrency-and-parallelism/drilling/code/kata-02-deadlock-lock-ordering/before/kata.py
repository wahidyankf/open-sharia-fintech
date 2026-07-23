"""Kata 2 (before): two office workers grab a printer and a scanner lock in OPPOSITE order -- deadlock."""

import threading


def worker_prints_then_scans(printer: threading.Lock, scanner: threading.Lock, both_ready: threading.Barrier) -> None:
    with printer:  # => grabs printer FIRST
        both_ready.wait()  # => rendezvous: waits until the other worker ALSO holds its first lock
        with scanner:  # => wants scanner -- but the other worker already holds it (deadlock)
            pass  # => never reached if the deadlock occurs


def worker_scans_then_prints(printer: threading.Lock, scanner: threading.Lock, both_ready: threading.Barrier) -> None:
    with scanner:  # => grabs scanner FIRST -- the OPPOSITE order from worker_prints_then_scans
        both_ready.wait()  # => rendezvous: waits until the other worker ALSO holds its first lock
        with printer:  # => wants printer -- but the other worker already holds it (deadlock)
            pass  # => never reached if the deadlock occurs


def reproduce_deadlock() -> tuple[bool, bool]:  # => returns (worker_a_still_hung, worker_b_still_hung)
    printer = threading.Lock()  # => shared resource A
    scanner = threading.Lock()  # => shared resource B
    rendezvous = threading.Barrier(2)  # => forces BOTH workers to hold their first lock before either tries the second
    w_a = threading.Thread(target=worker_prints_then_scans, args=(printer, scanner, rendezvous), daemon=True)
    w_b = threading.Thread(target=worker_scans_then_prints, args=(printer, scanner, rendezvous), daemon=True)
    # => daemon=True: these threads may hang FOREVER -- daemon prevents them blocking process exit
    w_a.start()
    w_b.start()
    w_a.join(timeout=0.5)  # => bounded wait -- a genuine deadlock means this NEVER returns early
    w_b.join(timeout=0.5)  # => bounded wait -- same for worker_b
    return w_a.is_alive(), w_b.is_alive()  # => True, True means both are still stuck -- deadlocked


if __name__ == "__main__":
    a_hung, b_hung = reproduce_deadlock()
    print(f"a_hung={a_hung} b_hung={b_hung}")
    # => Each worker holds ONE lock the other needs, and neither can proceed until it gets the
    # => other's lock -- a textbook circular wait. The Barrier guarantees BOTH workers hold their
    # => first lock before either attempts the second, making the deadlock deterministic every run.
    assert a_hung is True  # => confirms worker_a never got past its second `with scanner:`
    assert b_hung is True  # => confirms worker_b never got past its second `with printer:`
    print("kata OK (bug reproduced)")
