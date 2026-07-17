"""Example 2: pytest verification for Process vs. Thread Address Space."""

import multiprocessing as mp
import threading

import example


def test_thread_mutates_shared_global() -> None:
    example.counter = 0  # => reset the module global before this test's own measurement
    t = threading.Thread(target=example.bump_in_thread)
    t.start()
    t.join()
    assert example.counter == 1  # => the thread's mutation IS visible in this process


def test_process_does_not_mutate_parent_global() -> None:
    example.counter = 5  # => set a distinctive parent value the child must never see change
    q: "mp.Queue[int]" = mp.Queue()
    p = mp.Process(target=example.bump_in_process, args=(q,))
    p.start()
    p.join()
    child_value = q.get()
    assert child_value == 1  # => child's OWN copy started fresh at 0 (module reloaded), now 1
    assert example.counter == 5  # => parent's global is untouched by the child process


# => Run: pytest -- Output: 2 passed
