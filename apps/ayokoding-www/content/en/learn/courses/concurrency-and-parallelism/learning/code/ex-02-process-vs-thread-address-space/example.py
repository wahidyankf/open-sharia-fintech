"""Example 2: Process vs. Thread Address Space."""  # => co-02: threads share memory; processes each get their own

import multiprocessing as mp  # => separate address space per process (co-02)
import threading  # => shared address space per thread (co-02)

counter = 0  # => a module-level global -- lives in THIS process's address space only


def bump_in_thread() -> None:  # => runs on a new THREAD, inside the SAME process
    global counter  # => refers to the one and only `counter` this process has
    counter += 1  # => mutates the SHARED global -- visible to every thread in this process


def bump_in_process(q: "mp.Queue[int]") -> None:  # => runs in a CHILD process (own memory copy)
    global counter  # => refers to the CHILD's OWN copy of `counter`, not the parent's
    counter += 1  # => mutates only the child's private copy -- the parent never sees this
    q.put(counter)  # => the ONLY way to get a result back out is explicit IPC (a Queue, co-20)


if __name__ == "__main__":  # => required: multiprocessing re-imports this module in the child
    thread = threading.Thread(target=bump_in_thread)  # => builds a thread sharing this process
    thread.start()  # => runs bump_in_thread() concurrently
    thread.join()  # => waits for it to finish
    thread_saw = counter  # => thread_saw is 1 -- the thread DID mutate the shared global

    queue: "mp.Queue[int]" = mp.Queue()  # => an IPC channel -- processes share NOTHING else
    proc = mp.Process(target=bump_in_process, args=(queue,))  # => builds a child process
    proc.start()  # => forks/spawns a full copy of this process's memory, own `counter = 0`
    proc.join()  # => waits for the child to exit
    child_saw = queue.get()  # => child_saw is 1 -- the CHILD's own private counter incremented
    parent_after_process = counter  # => parent_after_process is STILL thread_saw (1), unchanged

    print(f"thread_saw={thread_saw} child_saw={child_saw} parent_after={parent_after_process}")  # => Output: thread_saw=1 child_saw=1 parent_after=1

    # => "isolated" is the whole point of a process boundary: no accidental sharing, ever.
    assert thread_saw == 1  # => confirms the thread mutated the PARENT's shared global
    assert child_saw == 1  # => confirms the child incremented its OWN isolated copy to 1
    assert parent_after_process == thread_saw  # => confirms the child's mutation never crossed back
    print("ex-02 OK")  # => Output: ex-02 OK
