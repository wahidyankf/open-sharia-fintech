"""Kata 8 (after): multiprocessing.Value is genuinely SHARED across the process boundary."""

from __future__ import annotations

import multiprocessing as mp
from multiprocessing.sharedctypes import Synchronized


def bump_in_child(shared_counter: "Synchronized[int]") -> None:
    with shared_counter.get_lock():  # FIX: the built-in lock makes the read-modify-write atomic too
        shared_counter.value += 1  # => mutates SHARED memory, backed by the OS, visible to BOTH processes
    print(f"inside child: counter={shared_counter.value}")  # => Output (from the child): inside child: counter=1


if __name__ == "__main__":
    shared_counter = mp.Value("i", 0)  # FIX: an actual shared-memory int, not a plain module global
    print(f"before: counter={shared_counter.value}")  # => Output: before: counter=0
    p = mp.Process(target=bump_in_child, args=(shared_counter,))
    p.start()
    p.join()
    print(f"after: counter={shared_counter.value}")  # => now correctly reflects the child's own update
    assert shared_counter.value == 1  # => confirms the parent NOW sees the child process's mutation
    print("kata OK (fix verified)")
