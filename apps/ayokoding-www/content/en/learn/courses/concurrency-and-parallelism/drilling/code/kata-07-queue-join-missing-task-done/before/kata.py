"""Kata 7 (before): draining a Queue without calling task_done() makes Queue.join() hang FOREVER."""

import queue
import threading


def drain_without_marking_done(q: "queue.Queue[int]") -> None:
    while True:
        try:
            q.get_nowait()  # => pulls each item out of the queue...
            # BUG: ...but never calls q.task_done() -- the queue's internal "unfinished tasks"
            # counter is never decremented, even though every item has genuinely been consumed.
        except queue.Empty:
            break


def demonstrate_hang() -> bool:  # => returns True if Queue.join() is STILL blocked after a bounded wait
    q: "queue.Queue[int]" = queue.Queue()
    for i in range(5):
        q.put(i)  # => unfinished_tasks: 0 -> 5
    drain_without_marking_done(q)  # => all 5 items are physically gone, but unfinished_tasks is STILL 5
    joiner = threading.Thread(target=q.join, daemon=True)  # => queue.Queue.join() has NO timeout parameter --
    joiner.start()  # => run it on a daemon thread so a genuine hang can't block this script forever
    joiner.join(timeout=0.5)  # => bounded wait ON the wrapper thread, not on q.join() itself
    return joiner.is_alive()  # => True means q.join() never returned -- still hung


if __name__ == "__main__":
    hung = demonstrate_hang()
    print(f"hung={hung}")
    # => q.join() blocks until unfinished_tasks reaches 0, which only happens via task_done() calls
    # => matching every put() -- draining items with get_nowait() alone never touches that counter.
    assert hung is True  # => confirms q.join() is still blocked, even though the queue is empty
    print("kata OK (bug reproduced)")
