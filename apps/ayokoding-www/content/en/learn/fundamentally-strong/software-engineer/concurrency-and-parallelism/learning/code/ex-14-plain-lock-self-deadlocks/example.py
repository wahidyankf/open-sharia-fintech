"""Example 14: A Plain `Lock` Self-Deadlocks on Re-Acquire."""

import threading  # => threading.Lock, contrasted with ex-13's RLock


def try_reacquire_same_thread(lock: threading.Lock, timeout: float) -> bool:
    # => attempts to acquire `lock` TWICE in a row, on the SAME thread, with a bounded wait
    lock.acquire()  # => FIRST acquire -- succeeds immediately, nothing else holds it yet
    got_second = lock.acquire(timeout=timeout)  # => SECOND acquire, same thread -- this is the test
    # => a plain Lock does NOT track "who" holds it, so it blocks even though ITSELF is the holder
    if got_second:  # => only True if acquire() somehow succeeded within the timeout (it will not)
        lock.release()  # => would release the second acquisition, if there had been one
    lock.release()  # => releases the FIRST acquisition -- always required to clean up
    return got_second  # => False proves the second acquire() timed out, i.e. self-deadlocked


if __name__ == "__main__":  # => module entry point
    my_lock = threading.Lock()  # => a fresh, plain (non-reentrant) Lock
    succeeded = try_reacquire_same_thread(my_lock, timeout=0.2)  # => bounded wait -- never hangs the test
    print(f"second_acquire_succeeded={succeeded}")  # => Output: second_acquire_succeeded=False

    # => Unlike ex-13's RLock, a plain Lock has no concept of "owning thread" -- to the Lock, the
    # => second acquire() call looks identical to a call from any OTHER thread: something already
    # => holds it, so it blocks. Calling it from the SAME thread without an intervening release()
    # => is therefore a guaranteed self-deadlock (co-11, co-12) -- here made SAFE with a timeout.
    assert succeeded is False  # => confirms the second acquire() blocked instead of succeeding
    assert my_lock.locked() is False  # => confirms the final release() left the lock free again
    print("ex-14 OK")  # => Output: ex-14 OK
