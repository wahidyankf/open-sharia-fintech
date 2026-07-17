"""Example 29: Two Threads, Two Locks, Opposite Order -- A Reproduced Deadlock."""  # => co-16: the four Coffman conditions, live

import threading  # => co-16: a cyclic wait between two threads holding what the other needs


def thread_a(lock_a: threading.Lock, lock_b: threading.Lock, both_ready: threading.Barrier) -> None:  # => wants A then B
    with lock_a:  # => thread_a grabs lock_a FIRST -- it now holds lock_a
        both_ready.wait()  # => rendezvous: waits until thread_b ALSO holds its first lock
        with lock_b:  # => thread_a now wants lock_b -- but thread_b already holds it (deadlock)
            pass  # => never reached -- this line only runs if the deadlock somehow doesn't occur


def thread_b(lock_a: threading.Lock, lock_b: threading.Lock, both_ready: threading.Barrier) -> None:  # => wants B then A
    with lock_b:  # => thread_b grabs lock_b FIRST -- the OPPOSITE order from thread_a
        both_ready.wait()  # => rendezvous: waits until thread_a ALSO holds its first lock
        with lock_a:  # => thread_b now wants lock_a -- but thread_a already holds it (deadlock)
            pass  # => never reached -- this line only runs if the deadlock somehow doesn't occur


def reproduce_deadlock() -> tuple[bool, bool]:  # => returns (a_still_hung, b_still_hung)
    lock_a = threading.Lock()  # => resource A
    lock_b = threading.Lock()  # => resource B
    rendezvous = threading.Barrier(2)  # => forces BOTH threads to hold their first lock before either tries the second
    t_a = threading.Thread(target=thread_a, args=(lock_a, lock_b, rendezvous), daemon=True)
    t_b = threading.Thread(target=thread_b, args=(lock_a, lock_b, rendezvous), daemon=True)
    # => daemon=True: these threads will hang FOREVER -- daemon prevents them from blocking process exit
    t_a.start()  # => starts thread_a -- acquires lock_a, then waits at the rendezvous
    t_b.start()  # => starts thread_b -- acquires lock_b, then waits at the rendezvous
    t_a.join(timeout=0.5)  # => bounded wait -- a genuine deadlock means this NEVER returns True early
    t_b.join(timeout=0.5)  # => bounded wait -- same for thread_b
    return t_a.is_alive(), t_b.is_alive()  # => True, True means both are still stuck -- deadlocked


if __name__ == "__main__":  # => module entry point
    a_hung, b_hung = reproduce_deadlock()  # => a_hung/b_hung: whether each thread is STILL blocked
    print(f"a_hung={a_hung} b_hung={b_hung}")  # => Output: a_hung=True b_hung=True

    # => Each thread holds ONE lock the other needs, and neither can proceed until it gets the
    # => other's lock -- a textbook circular wait (co-16). The Barrier guarantees BOTH threads
    # => hold their first lock before either attempts the second, making the deadlock deterministic.
    assert a_hung is True  # => confirms thread_a never got past its second `with lock_b:`
    assert b_hung is True  # => confirms thread_b never got past its second `with lock_a:`
    print("ex-29 OK")  # => Output: ex-29 OK
