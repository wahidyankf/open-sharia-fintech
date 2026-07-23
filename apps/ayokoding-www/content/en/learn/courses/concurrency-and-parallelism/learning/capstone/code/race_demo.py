"""Capstone: race_demo.py -- Step 4: a race condition + its lock fix, and a
deadlock + its lock-ordering fix, all in one file.

Reuses the SAME shapes ex-08/ex-11 (race+fix) and ex-29/ex-30 (deadlock+fix)
already established earlier in this topic, combined here to close out the
capstone's remaining two acceptance criteria: "a race condition + lock fix"
and "a reproduced-and-resolved deadlock".
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the demos themselves

import threading  # => co-08/co-11/co-16/co-18: every primitive this file demonstrates
import time  # => time.sleep(0) widens the race window; time.sleep(0.05) forces genuine lock contention

ITERATIONS_PER_THREAD = 2_000  # => co-08: small but reliable -- widens the race window enough to lose updates

# --- Part A: a shared-counter race, then its lock fix -----------------------


def increment_unsafe(counter: list[int]) -> None:  # => co-07/co-08: NO lock -- the shared-mutable-state hazard, live
    for _ in range(ITERATIONS_PER_THREAD):  # => runs the unsynchronized increment this many times
        value = counter[0]  # => READ counter[0] into a LOCAL variable -- step 1 of a non-atomic read-modify-write
        time.sleep(0)  # => yields RIGHT HERE -- widens the window for co-08's lost update
        counter[0] = value + 1  # => WRITE BACK the stale local `value` + 1 -- step 3, using possibly-OLD data


def increment_safe(counter: list[int], lock: threading.Lock) -> None:  # => co-11: the SAME operation, lock-protected
    for _ in range(ITERATIONS_PER_THREAD):  # => same iteration count -- SAME bug shape, now with a fix applied
        with lock:  # => co-11: mutual exclusion -- only ONE thread executes the block below at a time
            value = counter[0]  # => READ -- no OTHER thread can interleave here while the lock is held
            time.sleep(0)  # => still yields -- proving the LOCK, not luck, prevents interleaving
            counter[0] = value + 1  # => WRITE BACK -- still inside the SAME critical section


def racing_total() -> int:  # => co-08: two threads, ONE shared counter, NO synchronization
    counter = [0]  # => a one-element list stands in for a shared mutable int (Python ints are immutable)
    threads = [threading.Thread(target=increment_unsafe, args=(counter,)) for _ in range(2)]
    for t in threads:  # => launches both racing threads
        t.start()  # => both now interleave reads/writes to counter[0] with no coordination
    for t in threads:  # => waits for both to finish
        t.join()  # => blocks until that thread's increment_unsafe() call returns
    return counter[0]  # => the FINAL value -- expected to be WRONG due to lost updates


def locked_total() -> int:  # => co-11: the SAME two-thread race, NOW with a shared Lock
    counter = [0]  # => same shared mutable state shape as racing_total()
    lock = threading.Lock()  # => ONE Lock shared by both threads -- the mutual-exclusion gate
    threads = [threading.Thread(target=increment_safe, args=(counter, lock)) for _ in range(2)]
    for t in threads:  # => launches both threads
        t.start()  # => both now contend for the SAME lock before touching counter[0]
    for t in threads:  # => waits for both to finish
        t.join()  # => blocks until that thread's increment_safe() call returns
    return counter[0]  # => the FINAL value -- now expected to be EXACTLY correct


# --- Part B: a two-lock deadlock, then its lock-ordering fix -----------------


def deadlock_thread_a(lock_a: threading.Lock, lock_b: threading.Lock, both_ready: threading.Barrier) -> None:
    with lock_a:  # => grabs lock_a FIRST -- now holds lock_a
        both_ready.wait()  # => rendezvous: waits until deadlock_thread_b ALSO holds its first lock
        with lock_b:  # => now wants lock_b -- but deadlock_thread_b already holds it (deadlock)
            pass  # => never reached -- this line only runs if the deadlock somehow doesn't occur


def deadlock_thread_b(lock_a: threading.Lock, lock_b: threading.Lock, both_ready: threading.Barrier) -> None:
    with lock_b:  # => grabs lock_b FIRST -- the OPPOSITE order from deadlock_thread_a
        both_ready.wait()  # => rendezvous: waits until deadlock_thread_a ALSO holds its first lock
        with lock_a:  # => now wants lock_a -- but deadlock_thread_a already holds it (deadlock)
            pass  # => never reached -- this line only runs if the deadlock somehow doesn't occur


def reproduce_deadlock() -> tuple[bool, bool]:  # => co-16: returns (a_still_hung, b_still_hung)
    lock_a = threading.Lock()  # => resource A
    lock_b = threading.Lock()  # => resource B
    rendezvous = threading.Barrier(2)  # => forces BOTH threads to hold their first lock before either tries the second
    t_a = threading.Thread(target=deadlock_thread_a, args=(lock_a, lock_b, rendezvous), daemon=True)
    t_b = threading.Thread(target=deadlock_thread_b, args=(lock_a, lock_b, rendezvous), daemon=True)
    # => daemon=True: these threads WILL hang forever -- daemon prevents them from blocking process exit
    t_a.start()  # => starts deadlock_thread_a -- acquires lock_a, then waits at the rendezvous
    t_b.start()  # => starts deadlock_thread_b -- acquires lock_b, then waits at the rendezvous
    t_a.join(timeout=1.0)  # => bounded wait -- a genuine deadlock means this NEVER returns before the timeout
    t_b.join(timeout=1.0)  # => bounded wait -- same for deadlock_thread_b
    return t_a.is_alive(), t_b.is_alive()  # => True, True means both are STILL stuck -- deadlocked


def fixed_thread_a(lock_a: threading.Lock, lock_b: threading.Lock, holding_a: threading.Event) -> None:
    with lock_a:  # => acquires lock_a FIRST -- same order fixed_thread_b will use below
        holding_a.set()  # => signal fixed_thread_b it can now genuinely try to acquire lock_a and block on it
        time.sleep(0.05)  # => holds lock_a briefly so fixed_thread_b's attempt provably contends, not by luck
        with lock_b:  # => acquires lock_b SECOND -- no one else can hold lock_b while wanting lock_a here
            pass  # => reached every time: with a single order, no thread can form the opposite wait


def fixed_thread_b(lock_a: threading.Lock, lock_b: threading.Lock, holding_a: threading.Event) -> None:
    holding_a.wait()  # => waits until fixed_thread_a is DEFINITELY inside its `with lock_a:` block
    with lock_a:  # => acquires lock_a FIRST too -- the FIX: identical order to fixed_thread_a, not reversed
        with lock_b:  # => acquires lock_b SECOND -- same order as fixed_thread_a, so the cycle can't form
            pass  # => reached every time: this thread simply waited its turn for lock_a, then proceeded


def no_longer_deadlocks() -> tuple[bool, bool]:  # => co-18: returns (a_finished, b_finished)
    lock_a = threading.Lock()  # => resource A -- ALWAYS acquired first by both threads now
    lock_b = threading.Lock()  # => resource B -- ALWAYS acquired second by both threads now
    holding_a = threading.Event()  # => a signal, not a rendezvous -- see the Discussion in overview.md
    t_a = threading.Thread(target=fixed_thread_a, args=(lock_a, lock_b, holding_a))
    t_b = threading.Thread(target=fixed_thread_b, args=(lock_a, lock_b, holding_a))
    t_a.start()  # => starts fixed_thread_a -- acquires lock_a, signals, briefly holds it, then wants lock_b
    t_b.start()  # => starts fixed_thread_b -- waits for the signal, then genuinely blocks trying to get lock_a
    t_a.join(timeout=2.0)  # => a generous but FINITE timeout -- a real fix returns well before this
    t_b.join(timeout=2.0)  # => same bound for fixed_thread_b
    return not t_a.is_alive(), not t_b.is_alive()  # => True, True means BOTH finished -- no deadlock


if __name__ == "__main__":  # => module entry point
    expected = 2 * ITERATIONS_PER_THREAD  # => expected: the correct total if increments never raced

    unsafe_total = racing_total()  # => unsafe_total: the WRONG total from the unsynchronized race
    print(f"unsafe: expected={expected} actual={unsafe_total}")  # => Output: unsafe: expected=4000 actual=~2000-3999

    safe_total = locked_total()  # => safe_total: the CORRECT total after the lock fix
    print(f"safe:   expected={expected} actual={safe_total}")  # => Output: safe:   expected=4000 actual=4000

    a_hung, b_hung = reproduce_deadlock()  # => a_hung/b_hung: whether each thread is STILL blocked
    print(f"deadlock: a_hung={a_hung} b_hung={b_hung}")  # => Output: deadlock: a_hung=True b_hung=True

    a_done, b_done = no_longer_deadlocks()  # => a_done/b_done: did each thread actually complete?
    print(f"fixed:    a_done={a_done} b_done={b_done}")  # => Output: fixed:    a_done=True b_done=True

    # => co-08/co-11: the unsynchronized race demonstrably LOSES updates (a Lock around the SAME
    # => read-modify-write eliminates every one). co-16/co-18: acquiring locks in a single GLOBAL order
    # => breaks the circular wait that made the two-lock deadlock possible in the first place -- neither
    # => fix changes WHAT the code computes, only whether it computes it SAFELY (race) or AT ALL (deadlock).
    assert unsafe_total < expected  # => confirms the unsynchronized race lost at least one update
    assert safe_total == expected  # => confirms the lock eliminated EVERY lost update, not just some
    assert a_hung is True and b_hung is True  # => confirms the deadlock genuinely reproduced (both stuck)
    assert a_done is True and b_done is True  # => confirms the lock-ordering fix genuinely resolved it (both finished)
    print("race_demo.py OK")  # => Output: race_demo.py OK
