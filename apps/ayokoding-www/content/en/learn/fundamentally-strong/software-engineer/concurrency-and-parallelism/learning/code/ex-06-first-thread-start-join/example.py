"""Example 6: Your First Thread -- start() and join()."""  # => co-06: the two calls every thread lifecycle needs

import threading  # => the stdlib module for OS-backed threads (co-06)

ran: list[str] = []  # => a shared list the worker appends to, proving it actually executed


def worker() -> None:  # => the function the new thread will run
    ran.append("worker-ran")  # => appends a marker -- visible from the main thread after join()


if __name__ == "__main__":  # => module entry point
    thread = threading.Thread(target=worker)  # => builds a Thread object -- NOT yet running
    print(f"is_alive_before_start={thread.is_alive()}")  # => Output: is_alive_before_start=False
    thread.start()  # => start() launches the OS thread; worker() begins running concurrently
    thread.join()  # => join() blocks the main thread until worker() has fully returned
    print(f"is_alive_after_join={thread.is_alive()}")  # => Output: is_alive_after_join=False

    # => start() returns immediately -- the calling thread does NOT wait for worker() to begin or finish.
    # => join() is the only way to know, for certain, that the spawned thread has fully completed.
    assert ran == ["worker-ran"]  # => confirms worker() actually ran (join() guarantees this)
    assert thread.is_alive() is False  # => confirms the thread has fully finished, not just started
    print("ex-06 OK")  # => Output: ex-06 OK
