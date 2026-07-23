"""Example 41: pytest verification for a Hand-Built Condition-Based Bounded Buffer."""

import threading

from example import BoundedBuffer, consumer, producer


def test_fifo_order_preserved_through_a_bounded_buffer() -> None:
    buffer = BoundedBuffer(capacity=2)
    produced = list(range(10))
    collected: list[int] = []

    p = threading.Thread(target=producer, args=(buffer, produced))
    c = threading.Thread(target=consumer, args=(buffer, len(produced), collected))
    p.start()
    c.start()
    p.join(timeout=2)
    c.join(timeout=2)

    assert collected == produced  # => strict FIFO -- capacity constraint never lost or reordered an item


def test_put_blocks_once_the_buffer_is_at_capacity() -> None:
    buffer = BoundedBuffer(capacity=1)
    buffer.put(1)  # => fills the only slot -- the buffer is now at capacity

    finished = [False]

    def second_put() -> None:
        buffer.put(2)  # => must BLOCK, since the buffer has no room until something is get()'d
        finished[0] = True

    t = threading.Thread(target=second_put)
    t.start()
    t.join(timeout=0.2)
    assert finished[0] is False  # => confirms put() is genuinely blocked at capacity, not silently overflowing

    first = buffer.get()  # => frees the only slot
    t.join(timeout=1)
    assert first == 1  # => the FIRST item put is the FIRST item retrieved (FIFO)
    assert finished[0] is True  # => the blocked put() unblocked once room was made


# => Run: pytest -- Output: 2 passed
