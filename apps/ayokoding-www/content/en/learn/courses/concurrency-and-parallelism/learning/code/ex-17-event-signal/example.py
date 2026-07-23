"""Example 17: A `threading.Event` Signal."""  # => co-15: a one-shot flag one thread sets, another waits on

import threading  # => threading.Event -- a simple one-shot signal flag between threads
import time  # => proves the waiter genuinely BLOCKED, not just got lucky with timing


def waiter(event: threading.Event, log: list[str]) -> None:  # => blocks until signaled
    log.append("waiting")  # => recorded BEFORE the block, proving this thread reached wait()
    event.wait()  # => blocks THIS thread until some other thread calls event.set()
    log.append("proceeded")  # => only reached AFTER set() unblocks the wait() call above


def signaler(event: threading.Event, delay: float) -> None:  # => sets the event after a delay
    time.sleep(delay)  # => a deliberate pause -- the waiter must still be blocked when this runs
    event.set()  # => flips the internal flag to True and wakes EVERY thread blocked in wait()


if __name__ == "__main__":  # => module entry point
    signal = threading.Event()  # => starts UNSET (internal flag is False)
    events_log: list[str] = []  # => records the waiter's progress, in order
    t_wait = threading.Thread(target=waiter, args=(signal, events_log))  # => the blocked thread
    t_signal = threading.Thread(target=signaler, args=(signal, 0.1))  # => the thread that unblocks it
    t_wait.start()  # => starts waiting immediately -- signal.is_set() is still False
    time.sleep(0.02)  # => gives the waiter time to reach event.wait() before signaling
    still_unset = not signal.is_set()  # => still_unset: confirms the waiter really is blocked
    t_signal.start()  # => now starts the delayed signaler
    t_wait.join()  # => blocks the main thread until the waiter's wait() call returns
    t_signal.join()  # => blocks until the signaler's sleep+set() call returns

    print(events_log)  # => Output: ['waiting', 'proceeded']
    print(f"still_unset_before_signal={still_unset}")  # => Output: still_unset_before_signal=True

    # => unlike a Lock, an Event carries no ownership -- ANY thread can set() or wait() on it, freely.
    assert events_log == ["waiting", "proceeded"]  # => confirms the waiter blocked, THEN proceeded
    assert still_unset is True  # => confirms the event was genuinely unset while the waiter blocked
    assert signal.is_set() is True  # => confirms the final state is set
    print("ex-17 OK")  # => Output: ex-17 OK
