"""Kata 9 (after): state-fault-line fix -- each thread owns a private slot; combine with a pure fold at the end."""

import threading

results: list[int] = [0, 0]  # each thread writes to its OWN index -- never the same memory location


def record_view(index: int) -> None:
    results[index] = 1  # a single write to a private slot -- nothing else can read or write it mid-flight


thread_a = threading.Thread(target=record_view, args=(0,))
thread_b = threading.Thread(target=record_view, args=(1,))
thread_a.start()
thread_b.start()
thread_a.join()
thread_b.join()

total_views = sum(results)  # combine ONLY after both threads finished -- no concurrent write to `total_views`
print(total_views)  # both views correctly counted, every single run
