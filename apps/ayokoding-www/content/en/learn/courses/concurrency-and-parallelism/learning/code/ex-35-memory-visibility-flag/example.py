"""Example 35: Memory Visibility -- Why a Busy-Wait Flag Is Fragile, Even When It "Works"."""

import threading  # => contrasts a raw busy-wait against threading.Event (co-19)
import time  # => measures how long each waiting style takes to observe the change


def busy_wait_setter(flag: list[bool], delay: float) -> None:  # => flips a PLAIN, unsynchronized flag
    time.sleep(delay)  # => a deliberate pause before the write
    flag[0] = True  # => a plain assignment -- NO lock, NO Event, no memory barrier of any kind


def busy_wait_waiter(flag: list[bool], observed: list[float]) -> None:  # => polls the plain flag
    start = time.perf_counter()  # => start: wall-clock time before polling begins
    while not flag[0]:  # => a raw busy-wait loop -- re-reads `flag[0]` as fast as the CPU allows
        pass  # => burns 100% of a core the ENTIRE time it's polling -- the real, measurable cost here
    observed.append(time.perf_counter() - start)  # => how long this thread spent spinning


def event_setter(event: threading.Event, delay: float) -> None:  # => the idiomatic co-15 signal
    time.sleep(delay)  # => the SAME delay as busy_wait_setter, for a fair comparison
    event.set()  # => the correct, portable way to signal another thread


def event_waiter(event: threading.Event, observed: list[float]) -> None:  # => blocks efficiently
    start = time.perf_counter()  # => start: wall-clock time before waiting begins
    event.wait()  # => blocks WITHOUT spinning -- the OS/interpreter wakes this thread on set()
    observed.append(time.perf_counter() - start)  # => how long this thread waited before waking


if __name__ == "__main__":  # => module entry point
    plain_flag = [False]  # => the unsynchronized flag under test
    busy_observed: list[float] = []  # => records how long the busy-wait took to notice the flip
    t1 = threading.Thread(target=busy_wait_waiter, args=(plain_flag, busy_observed))
    t2 = threading.Thread(target=busy_wait_setter, args=(plain_flag, 0.1))
    t1.start()  # => starts polling `plain_flag[0]` immediately
    t2.start()  # => flips it after a 0.1s delay
    t1.join()  # => waits for the busy-wait loop to notice and exit
    t2.join()  # => waits for the setter to finish

    signal_event = threading.Event()  # => the idiomatic alternative under test
    event_observed: list[float] = []  # => records how long Event.wait() took to notice the set()
    t3 = threading.Thread(target=event_waiter, args=(signal_event, event_observed))
    t4 = threading.Thread(target=event_setter, args=(signal_event, 0.1))
    t3.start()  # => starts blocking on event.wait() immediately
    t4.start()  # => sets it after the SAME 0.1s delay, for a fair comparison
    t3.join()  # => waits for the Event-based wait to return
    t4.join()  # => waits for the setter to finish

    print(f"busy_wait_saw_update_after={busy_observed[0]:.2f}s")  # => Output: busy_wait_saw_update_after=~0.1s
    print(f"event_wait_saw_update_after={event_observed[0]:.2f}s")  # => Output: event_wait_saw_update_after=~0.1s

    # => On THIS GIL-enabled CPython build, the raw busy-wait DOES eventually see the flip --
    # => the GIL serializes bytecode execution, so there is no per-thread register caching hiding
    # => the write. That is a CPython/GIL IMPLEMENTATION DETAIL, not a language guarantee (co-19):
    # => it burns CPU the whole time it polls, and it breaks down entirely on a free-threaded
    # => (no-GIL, `python3.14t`) build, where nothing forces the write to become visible promptly.
    # => `threading.Event` is correct and efficient on EVERY build, with or without the GIL.
    assert busy_observed[0] < 0.5  # => confirms the busy-wait DID observe the change (on this build)
    assert event_observed[0] < 0.5  # => confirms Event.wait() also observed it, without spinning
    print("ex-35 OK")  # => Output: ex-35 OK
