"""Example 74: State Fault-Line Case Study (Shared-Mutable vs Immutable, Under Threads)."""

import threading  # => the fault line only shows up under real concurrent execution, so both PARTS use it


class SharedMutableCounter:  # => BEFORE: one shared mutable int, both threads read-then-write it
    def __init__(self) -> None:  # => constructor seeds the single shared box
        self.value = 0  # => a single shared box -- the fault line this example is built around


def racy_increment(counter: SharedMutableCounter, read_done: threading.Event, may_write: threading.Event) -> None:  # => forces a deterministic race
    current = counter.value  # => STEP 1: read the shared value
    read_done.set()  # => signal "I have read" -- used to force a specific, deterministic interleaving
    may_write.wait()  # => STEP 2: wait until told it's safe to write (forces the race window open)
    counter.value = current + 1  # => STEP 3: write back based on the STALE value read in step 1


shared = SharedMutableCounter()  # => starts at 0
event_a_read = threading.Event()  # => "thread A has read" signal
event_b_read = threading.Event()  # => "thread B has read" signal
thread_a = threading.Thread(target=racy_increment, args=(shared, event_a_read, event_b_read))  # => thread A waits on B's read
thread_b = threading.Thread(target=racy_increment, args=(shared, event_b_read, event_a_read))  # => thread B waits on A's read
# => each thread waits on the OTHER thread's "read done" signal before it's allowed to write --
# => this deterministically forces BOTH threads to read 0 before EITHER of them writes 1, every run
thread_a.start()  # => launch thread A
thread_b.start()  # => launch thread B
thread_a.join()  # => wait for thread A to finish before reading the result
thread_b.join()  # => wait for thread B to finish before reading the result

print(shared.value)  # => THE RACE: two increments happened, but only one survived -- a LOST UPDATE
# => Output: 1


def partial_sum(nums: tuple[int, ...]) -> int:  # => AFTER: a pure function, no shared mutable target at all
    total = 0  # => local to THIS call only -- never shared across threads
    for n in nums:  # => a plain fold over this call's own private slice of numbers
        total += n  # => mutates only the LOCAL total -- no other thread can ever see or touch it
    return total  # => returned, never written into a shared box


results: list[int] = [0, 0]  # => each thread writes to its OWN index -- never the SAME memory location


def run_partial(index: int, nums: tuple[int, ...]) -> None:  # => each thread owns a disjoint slice of work
    results[index] = partial_sum(nums)  # => writes to a location no other thread ever touches


thread_c = threading.Thread(target=run_partial, args=(0, (1, 2, 3, 4, 5)))  # => thread C sums its own half
thread_d = threading.Thread(target=run_partial, args=(1, (6, 7, 8, 9, 10)))  # => thread D sums its own half
thread_c.start()  # => launch thread C
thread_d.start()  # => launch thread D
thread_c.join()  # => wait for thread C -- no shared box to race on, so join order doesn't matter
thread_d.join()  # => wait for thread D

combined = sum(results)  # => combine ONLY after both threads finished -- no concurrent write to `combined`
print(combined)  # => 1+2+..+10 = 55, correct every single run -- no shared mutable target to race on
# => Output: 55
