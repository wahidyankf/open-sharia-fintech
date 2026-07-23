"""Example 70: pytest verification for a Three-Stage Read-Transform-Write Pipeline."""

import queue
import threading

from example import read_stage, transform_stage, write_stage


def test_pipeline_preserves_order_and_transforms_every_item() -> None:
    raw_queue: "queue.Queue[int | None]" = queue.Queue()
    transformed_queue: "queue.Queue[int | None]" = queue.Queue()
    written: list[int] = []

    reader = threading.Thread(target=read_stage, args=(raw_queue,))
    transformer = threading.Thread(target=transform_stage, args=(raw_queue, transformed_queue))
    writer = threading.Thread(target=write_stage, args=(transformed_queue, written))
    for stage in (reader, transformer, writer):
        stage.start()
    for stage in (reader, transformer, writer):
        stage.join()

    assert written == [i * i for i in range(15)]  # => every item passed through all three stages, in order


# => Run: pytest -- Output: 1 passed
