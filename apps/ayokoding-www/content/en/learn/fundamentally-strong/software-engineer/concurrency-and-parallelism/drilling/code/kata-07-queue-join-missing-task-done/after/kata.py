"""Kata 7 (after): calling task_done() for every item makes Queue.join() return promptly."""

import queue
import threading


def drain_and_mark_done(q: "queue.Queue[int]") -> None:
    while True:
        try:
            q.get_nowait()
            q.task_done()  # FIX: decrements unfinished_tasks -- matches this get_nowait() to its put()
        except queue.Empty:
            break


def demonstrate_no_hang() -> bool:  # => returns True if Queue.join() is STILL blocked after a bounded wait
    q: "queue.Queue[int]" = queue.Queue()
    for i in range(5):
        q.put(i)  # => unfinished_tasks: 0 -> 5
    drain_and_mark_done(q)  # => unfinished_tasks correctly reaches 0 -- 5 task_done() calls, one per put()
    joiner = threading.Thread(target=q.join, daemon=True)
    joiner.start()
    joiner.join(timeout=0.5)  # => with the fix, this returns well inside the 0.5s bound
    return joiner.is_alive()  # => False means q.join() already returned -- no hang


if __name__ == "__main__":
    hung = demonstrate_no_hang()
    print(f"hung={hung}")
    # => Every get_nowait() is now paired with a task_done(), so unfinished_tasks correctly reaches 0
    # => and the underlying `Condition` inside Queue wakes up any thread blocked in join().
    assert hung is False  # => confirms q.join() returned promptly once every item was marked done
    print("kata OK (fix verified)")
