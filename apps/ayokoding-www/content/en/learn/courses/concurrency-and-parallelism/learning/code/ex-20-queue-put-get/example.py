"""Example 20: `queue.Queue` -- put() and get() Between Threads."""  # => co-21: a synchronized hand-off channel

import queue  # => queue.Queue -- a thread-safe, synchronized hand-off channel (co-21)
import threading  # => the two threads that hand items off through the queue


def sender(q: "queue.Queue[int]", items: list[int]) -> None:  # => puts each item, in order
    for item in items:  # => iterates the items to send, in their original order
        q.put(item)  # => put() is thread-safe -- no external lock needed around it (co-20)


def receiver(q: "queue.Queue[int]", count: int, out: list[int]) -> None:  # => gets `count` items
    for _ in range(count):  # => pulls exactly `count` items -- one per sender item
        out.append(q.get())  # => get() BLOCKS until an item is available, then returns it


if __name__ == "__main__":  # => module entry point
    channel: "queue.Queue[int]" = queue.Queue()  # => an UNBOUNDED FIFO queue -- no maxsize set
    to_send = [10, 20, 30, 40]  # => the items the sender thread will put(), in this exact order
    received: list[int] = []  # => the receiver appends each get() result here, in arrival order
    t_send = threading.Thread(target=sender, args=(channel, to_send))  # => the producing thread
    t_recv = threading.Thread(target=receiver, args=(channel, len(to_send), received))  # => consuming
    t_recv.start()  # => starts first -- immediately blocks on q.get() since nothing is queued yet
    t_send.start()  # => starts sending -- each put() unblocks the receiver's next pending get()
    t_send.join()  # => waits for the sender to finish putting all items
    t_recv.join()  # => waits for the receiver to finish getting all items

    print(received)  # => Output: [10, 20, 30, 40]
    # => starting the receiver FIRST proves get() genuinely blocks -- it isn't a lucky race.
    assert received == to_send  # => confirms FIFO delivery: items arrive in the SAME order they were sent
    print("ex-20 OK")  # => Output: ex-20 OK
