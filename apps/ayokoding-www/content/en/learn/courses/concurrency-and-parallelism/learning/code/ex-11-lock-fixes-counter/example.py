"""Example 11: A `Lock` Fixes the Racing Counter."""  # => co-11: mutual exclusion applied to ex-08's lost updates

import threading  # => threading.Lock is the fix for ex-08 and ex-10's lost updates
import time  # => keeps the same widened race window ex-08 used, to prove the lock actually matters

ITERATIONS_PER_THREAD = 2_000  # => identical to ex-08 -- SAME bug shape, now with a fix applied


def increment_with_lock(counter: list[int], lock: threading.Lock) -> None:  # => co-11's fix in action
    for _ in range(ITERATIONS_PER_THREAD):  # => same iteration count as the buggy ex-08 version
        lock.acquire()  # => blocks until THIS thread is the only one inside the critical section
        try:  # => guarantees release even if something inside raised (co-11's safety discipline)
            value = counter[0]  # => READ -- but now no OTHER thread can interleave here
            time.sleep(0)  # => still yields -- proving the lock, not luck, prevents interleaving
            counter[0] = value + 1  # => WRITE BACK -- still inside the SAME critical section
        finally:  # => runs whether the `try` succeeded or raised
            lock.release()  # => releases the lock -- exactly one other thread may now proceed


def locked_total() -> int:  # => runs two threads incrementing the SAME counter, WITH a lock
    counter = [0]  # => same shared mutable state shape as ex-08
    lock = threading.Lock()  # => one Lock shared by both threads -- the mutual-exclusion gate
    threads = [threading.Thread(target=increment_with_lock, args=(counter, lock)) for _ in range(2)]
    # => threads: exactly 2 Thread objects, both racing on the SAME counter and the SAME lock
    for t in threads:  # => launches both threads
        t.start()  # => both now contend for the SAME lock before touching counter[0]
    for t in threads:  # => waits for both to finish
        t.join()  # => join() blocks until that thread's increment_with_lock() call returns
    return counter[0]  # => the FINAL value -- now expected to be EXACTLY correct


if __name__ == "__main__":  # => module entry point
    expected = 2 * ITERATIONS_PER_THREAD  # => expected: the correct total, no lost updates allowed
    actual = locked_total()  # => actual: the total after the SAME race pattern, now lock-protected
    print(f"expected={expected} actual={actual}")  # => Output: expected=4000 actual=4000

    # => same iteration count, same sleep(0) window as ex-08 -- ONLY the lock changed, and it's enough.
    assert actual == expected  # => confirms the lock eliminated EVERY lost update, not just some
    print("ex-11 OK")  # => Output: ex-11 OK
