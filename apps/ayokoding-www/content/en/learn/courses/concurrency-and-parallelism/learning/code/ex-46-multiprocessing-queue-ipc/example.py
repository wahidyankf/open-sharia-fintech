"""Example 46: `multiprocessing.Queue` -- the Cross-Process Delivery Channel."""

import multiprocessing  # => co-20, co-02: processes can't share a plain list, but CAN share a Queue

ITEM_COUNT = 10  # => how many items the child process sends back to the parent


def produce_in_child(q: "multiprocessing.Queue[int]") -> None:  # => runs inside a SEPARATE OS process
    for i in range(ITEM_COUNT):  # => generates ITEM_COUNT items entirely within the child
        q.put(i * i)  # => serializes (pickles) each item and sends it across the process boundary
    q.put(-1)  # => -1: a sentinel telling the parent "no more items are coming"


if __name__ == "__main__":  # => module entry point -- required for multiprocessing's `spawn` start method
    ipc_queue: "multiprocessing.Queue[int]" = multiprocessing.Queue()  # => ipc_queue: backed by an OS pipe, unlike queue.Queue
    child = multiprocessing.Process(target=produce_in_child, args=(ipc_queue,))  # => child: will run produce_in_child
    child.start()  # => spawns the child process -- it starts pushing items into ipc_queue immediately

    received: list[int] = []  # => received: accumulates every item the PARENT process pulls back out
    while True:  # => keeps pulling until the sentinel arrives
        item = ipc_queue.get()  # => BLOCKS the parent until the child has an item ready to deliver
        if item == -1:  # => -1 is the shutdown sentinel the child sends after its last real item
            break  # => stops pulling -- every real item has now been received
        received.append(item)  # => records an item that ORIGINATED in a completely different process

    child.join()  # => waits for the child process to fully exit

    expected = [i * i for i in range(ITEM_COUNT)]  # => expected: what the child SHOULD have produced
    print(f"received={received}")  # => Output: received=[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

    # => `multiprocessing.Queue` is backed by an OS-level pipe plus a background thread that pickles
    # => and unpickles items crossing the process boundary -- unlike `queue.Queue` (co-21), which only
    # => works WITHIN one process's threads. This is how cooperating processes exchange data safely
    # => despite having entirely separate address spaces (co-02): NOT by sharing memory, but by
    # => explicitly SENDING copies of data through a channel designed for cross-process communication.
    assert received == expected  # => confirms every item genuinely crossed the process boundary, in order
    print("ex-46 OK")  # => Output: ex-46 OK
