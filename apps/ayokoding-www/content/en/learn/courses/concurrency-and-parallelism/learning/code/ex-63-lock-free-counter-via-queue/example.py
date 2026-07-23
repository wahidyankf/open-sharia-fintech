"""Example 63: A "Lock-Free" Counter -- via a Single-Owner Queue, Not a Lock."""

import queue  # => co-20, co-21: the queue itself is the ONLY synchronization primitive used here
import threading  # => multiple client threads REQUEST increments; one owner thread APPLIES them

REQUESTS_PER_CLIENT = 500  # => how many increment requests each client thread sends
CLIENT_COUNT = 4  # => how many independent client threads send requests concurrently


def client(requests: "queue.Queue[int]", count: int) -> None:
    for _ in range(count):  # => sends `count` increment requests, one at a time
        requests.put(1)  # => "please add 1" -- the QUEUE, not a lock, serializes concurrent access to it


def owner(requests: "queue.Queue[int | None]", total: list[int]) -> None:
    while True:  # => the counter's ONE AND ONLY owner -- no other thread ever touches `total` directly
        item = requests.get()  # => blocks until a request (or the sentinel) arrives
        if item is None:  # => None: the shutdown sentinel, sent once all clients have finished
            break  # => stops the owner loop
        total[0] += item  # => SAFE without a lock: this is the ONLY thread that ever reads or writes `total`


if __name__ == "__main__":  # => module entry point
    requests: "queue.Queue[int | None]" = queue.Queue()  # => the single channel every client sends requests through
    total = [0]  # => total[0]: the counter, touched EXCLUSIVELY by the owner thread below

    owner_thread = threading.Thread(target=owner, args=(requests, total))
    owner_thread.start()  # => starts the SOLE thread that will ever mutate `total`

    clients = [threading.Thread(target=client, args=(requests, REQUESTS_PER_CLIENT)) for _ in range(CLIENT_COUNT)]
    for c in clients:  # => starts every client thread
        c.start()  # => each begins sending REQUESTS_PER_CLIENT increment requests into the SAME queue
    for c in clients:  # => waits for every client to finish sending
        c.join()  # => join() blocks until that client's loop has enqueued all its requests

    requests.put(None)  # => tells the owner "no more requests are coming" -- AFTER every client has finished
    owner_thread.join()  # => waits for the owner to drain the queue and process every request

    expected = CLIENT_COUNT * REQUESTS_PER_CLIENT  # => expected: the mathematically correct total
    print(f"expected={expected} actual={total[0]}")  # => Output: expected=2000 actual=2000

    # => This "counter" has NO lock protecting it anywhere -- it doesn't need one, because exactly ONE
    # => thread (the "owner") ever reads or writes it (co-20). Instead of many threads racing to mutate
    # => shared state directly (needing a lock, ex-08/ex-11), every OTHER thread sends a REQUEST through
    # => a thread-safe queue (co-21), and the owner applies requests one at a time, in isolation. This
    # => single-owner pattern is the core idea behind actor-style concurrency: communicate by sending
    # => messages, rather than by sharing memory and coordinating access to it with locks.
    assert total[0] == expected  # => confirms every single increment request was applied, exactly once
    print("ex-63 OK")  # => Output: ex-63 OK
