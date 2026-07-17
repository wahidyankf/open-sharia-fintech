"""Example 22: A `None` Sentinel Cleanly Shuts Down a Consumer."""  # => co-22: a clean, explicit stop signal

import queue  # => the producer/consumer channel, now with an explicit "stop" signal
import threading  # => one producer, one consumer, coordinating shutdown through the queue itself

SENTINEL = None  # => a value that can NEVER be a real work item -- unambiguous "stop" marker


def producer(q: "queue.Queue[int | None]", items: list[int]) -> None:  # => sends work, then stops
    for item in items:  # => sends every real item first
        q.put(item)  # => a normal work item
    q.put(SENTINEL)  # => the LAST thing put -- tells the consumer "there is nothing more coming"


def consumer(q: "queue.Queue[int | None]", collected: list[int]) -> None:  # => loops until sentinel
    while True:  # => runs until the sentinel is seen -- no fixed count needed, unlike ex-21
        item = q.get()  # => blocks until either a real item or the SENTINEL arrives
        if item is None:  # => the stop signal (SENTINEL) -- checked BEFORE treating item as real work
            break  # => exits the loop cleanly -- no exception, no hang, no busy-wait
        collected.append(item)  # => a real item -- pyright narrows `item` to `int` past the check above


if __name__ == "__main__":  # => module entry point
    channel: "queue.Queue[int | None]" = queue.Queue()  # => carries both real ints AND the sentinel
    to_send = [1, 2, 3]  # => the real work items the producer will send before stopping
    collected: list[int] = []  # => every real item the consumer collected before seeing the sentinel
    t_prod = threading.Thread(target=producer, args=(channel, to_send))  # => sends items then SENTINEL
    t_cons = threading.Thread(target=consumer, args=(channel, collected))  # => stops on SENTINEL
    t_prod.start()  # => starts sending
    t_cons.start()  # => starts consuming -- loops forever until it sees None
    t_prod.join()  # => waits for the producer to finish (including the final sentinel put)
    t_cons.join()  # => waits for the consumer's loop to actually break -- proves clean termination

    print(collected)  # => Output: [1, 2, 3]
    # => with multiple consumers, put ONE sentinel per consumer -- each get() only ever removes one.
    assert collected == to_send  # => confirms every real item was collected before the stop signal
    assert not t_cons.is_alive()  # => confirms the consumer thread actually terminated, not hung
    print("ex-22 OK")  # => Output: ex-22 OK
