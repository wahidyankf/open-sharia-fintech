"""Kata 8 (before): a plain module-level counter, "mutated" in a child PROCESS, never changes for the parent."""

from __future__ import annotations

import multiprocessing as mp

counter = 0  # SMELL: an ordinary module-level int -- NOT a multiprocessing-aware shared value


def bump_in_child() -> None:
    global counter
    counter += 1  # BUG: mutates the CHILD process's own PRIVATE copy of `counter`, not the parent's
    print(f"inside child: counter={counter}")  # => Output (from the child): inside child: counter=1


if __name__ == "__main__":
    print(f"before: counter={counter}")  # => Output: before: counter=0
    p = mp.Process(target=bump_in_child)
    p.start()  # => forks/spawns a whole SEPARATE process, with its OWN copy of every global variable
    p.join()  # => waits for the child process to fully exit
    print(f"after: counter={counter}")  # BUG: still counter=0 in the PARENT -- the child's write never crossed over
    # => Each process has its own address space -- there is no shared memory here at all, so a plain
    # => module-level int can only ever be "mutated" inside whichever process runs that line.
    assert counter == 0  # => confirms the parent's own copy of `counter` was never touched
    print("kata OK (bug reproduced)")
