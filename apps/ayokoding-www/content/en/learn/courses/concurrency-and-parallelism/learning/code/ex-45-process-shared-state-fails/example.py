"""Example 45: A Global Mutated in a Child Process Is Invisible to the Parent."""

import multiprocessing  # => co-02: processes have SEPARATE address spaces -- unlike threads (ex-02)

shared_looking_list: list[int] = []  # => a module-level "global" -- looks shared, but ISN'T across processes


def mutate_in_child() -> None:  # => runs inside a CHILD process, in its own COPY of this module
    shared_looking_list.append(999)  # => mutates the CHILD's own copy of shared_looking_list
    print(f"child sees: {shared_looking_list}")  # => Output (from the CHILD's stdout): child sees: [999]


if __name__ == "__main__":  # => module entry point -- required for multiprocessing's `spawn` start method
    shared_looking_list.append(1)  # => the PARENT process adds an item BEFORE spawning the child
    print(f"parent before spawn: {shared_looking_list}")  # => Output: parent before spawn: [1]

    child = multiprocessing.Process(target=mutate_in_child)  # => child: a NEW OS process, own memory, own GIL
    child.start()  # => on this platform's `spawn` start method, the child RE-IMPORTS the module fresh
    child.join()  # => waits for the child process to fully exit before checking the parent's own list

    print(f"parent after join: {shared_looking_list}")  # => Output: parent after join: [1] (999 is MISSING!)

    # => `multiprocessing.Process` does NOT share memory with the parent (co-02): under `spawn` (macOS's
    # => and Windows's default), the child re-imports this module from scratch, so `shared_looking_list`
    # => starts fresh at `[]` in the child and ends at `[999]` there; under `fork` (Linux's default), the
    # => child instead gets a COPIED snapshot of the parent's memory at fork time. Either way, any
    # => mutation the child makes to `shared_looking_list` stays entirely within the CHILD's own address
    # => space -- the parent's own list is completely unaffected. Contrast with `threading.Thread`
    # => (ex-02), where a mutation from a thread IS visible to every other thread in the same process.
    assert shared_looking_list == [1]  # => confirms the child's append(999) never reached the parent
    print("ex-45 OK")  # => Output: ex-45 OK
