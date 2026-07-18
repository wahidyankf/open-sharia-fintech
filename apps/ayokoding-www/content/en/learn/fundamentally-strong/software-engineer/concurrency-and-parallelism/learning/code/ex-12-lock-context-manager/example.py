"""Example 12: `with lock:` vs Manual acquire()/release()."""  # => co-11: same guarantee, two syntaxes

import threading  # => threading.Lock supports BOTH the context-manager and manual styles


def manual_style(lock: threading.Lock, log: list[str]) -> None:  # => the verbose, error-prone style
    lock.acquire()  # => step 1: acquire -- MUST be paired with a release, by hand
    try:  # => without this try/finally, an exception would leave the lock held forever
        log.append("manual-inside")  # => the critical section's actual work
    finally:  # => runs no matter what happened inside the try
        lock.release()  # => step 2: release -- easy to forget without the try/finally boilerplate


def context_manager_style(lock: threading.Lock, log: list[str]) -> None:  # => the idiomatic style
    with lock:  # => `with` calls acquire() on entry and release() on exit, EVEN if an exception occurs
        log.append("with-inside")  # => the identical critical-section work, far less boilerplate


def context_manager_releases_on_exception(lock: threading.Lock) -> bool:  # => proves the safety claim
    try:  # => wraps the `with` block so this function can observe the exception afterward
        with lock:  # => acquires the lock
            raise ValueError("boom")  # => an exception INSIDE the critical section
    except ValueError:  # => catches it here, one frame up
        pass  # => intentionally swallowed -- this function only cares whether the lock got released
    return lock.locked()  # => False means `with` released it despite the exception; True would be a bug


if __name__ == "__main__":  # => module entry point
    events: list[str] = []  # => shared log both styles append into, to compare their effect
    manual_style(threading.Lock(), events)  # => runs the manual acquire/release style once
    context_manager_style(threading.Lock(), events)  # => runs the `with lock:` style once
    print(events)  # => Output: ['manual-inside', 'with-inside']

    still_locked = context_manager_releases_on_exception(threading.Lock())  # => tests exception safety
    print(f"still_locked_after_exception={still_locked}")  # => Output: still_locked_after_exception=False

    # => prefer `with lock:` in real code -- it's equally correct AND immune to a forgotten `finally`.
    assert events == ["manual-inside", "with-inside"]  # => confirms BOTH styles ran their critical section
    assert still_locked is False  # => confirms `with lock:` released even though the body raised
    print("ex-12 OK")  # => Output: ex-12 OK
