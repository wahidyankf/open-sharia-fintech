"""Example 70: A Three-Stage Pipeline -- Read -> Transform -> Write, via Two Queues."""

import queue  # => co-22, co-21: each STAGE is a thread; each QUEUE is the hand-off between two stages
import threading  # => one dedicated thread per stage -- read, transform, write

ITEM_COUNT = 15  # => how many items flow all the way through the pipeline


def read_stage(raw_out: "queue.Queue[int | None]") -> None:
    # => stage 1 of 3 -- the ONLY producer for raw_queue
    for i in range(ITEM_COUNT):  # => "reads" ITEM_COUNT items -- simulated here as just their own index
        raw_out.put(i)  # => hands each raw item off to the transform stage via the first queue
    raw_out.put(None)  # => sentinel: tells the transform stage there's nothing more to read


def transform_stage(raw_in: "queue.Queue[int | None]", transformed_out: "queue.Queue[int | None]") -> None:
    # => stage 2 of 3 -- the ONLY consumer of raw_queue AND the ONLY producer for transformed_queue
    while True:  # => keeps pulling raw items until its OWN sentinel arrives
        item = raw_in.get()  # => blocks until the read stage has something ready
        if item is None:  # => the read stage's sentinel -- no more raw items are coming
            transformed_out.put(None)  # => propagates a sentinel of its OWN to the write stage
            break  # => stops the transform stage
        transformed_out.put(item * item)  # => the actual "transform": squaring, handed to the write stage


def write_stage(transformed_in: "queue.Queue[int | None]", written: list[int]) -> None:
    # => stage 3 of 3 -- the ONLY consumer of transformed_queue
    while True:  # => keeps pulling transformed items until the sentinel arrives
        item = transformed_in.get()  # => blocks until the transform stage has something ready
        if item is None:  # => the transform stage's sentinel -- nothing more is coming
            break  # => stops the write stage
        written.append(item)  # => "writes" the item -- here, just records it for verification


if __name__ == "__main__":  # => module entry point
    raw_queue: "queue.Queue[int | None]" = queue.Queue()  # => raw_queue: hand-off between read and transform
    transformed_queue: "queue.Queue[int | None]" = queue.Queue()  # => transformed_queue: hand-off between transform and write
    written: list[int] = []  # => written: filled in by the write stage, in the FINAL pipeline order

    reader = threading.Thread(target=read_stage, args=(raw_queue,))
    transformer = threading.Thread(target=transform_stage, args=(raw_queue, transformed_queue))
    writer = threading.Thread(target=write_stage, args=(transformed_queue, written))
    for stage in (reader, transformer, writer):  # => starts all three stages together
        stage.start()  # => each stage begins running concurrently, connected only by the two queues
    for stage in (reader, transformer, writer):  # => waits for every stage to fully drain and exit
        stage.join()  # => join() blocks until that stage's loop has completed

    expected = [i * i for i in range(ITEM_COUNT)]  # => expected: what the WHOLE pipeline should have produced
    print(f"written={written}")  # => Output: written=[0, 1, 4, 9, 16, ..., 196]

    # => Each stage is its OWN thread, and each `queue.Queue` between two stages is thread-safe by
    # => construction (co-21) -- no explicit lock is needed anywhere in this pipeline. Because EACH
    # => queue has exactly ONE producer thread and ONE consumer thread here, FIFO ordering (co-22) is
    # => preserved end-to-end: item `i` is read, transformed, and written in that SAME relative order it
    # => started in, even though all three stages are running concurrently with each other the whole time.
    assert written == expected  # => confirms every item passed through all three stages, correctly, in order
    print("ex-70 OK")  # => Output: ex-70 OK
