"""Example 56: pytest verification for Reactive Debounce."""

from example import DebouncedStream


def test_only_the_final_value_of_a_burst_is_delivered() -> None:
    stream = DebouncedStream()  # => fresh stream, isolated from the module-level demo
    delivered: list[int] = []  # => local recorder
    stream.subscribe(lambda v: delivered.append(v))
    for v in (10, 20, 30, 40):  # => a burst of four rapid pushes
        stream.push(v)
    assert delivered == []  # => nothing delivered mid-burst
    stream.flush()  # => the burst ends
    assert delivered == [40]  # => only the final value survives


def test_a_second_burst_after_flush_delivers_its_own_final_value() -> None:
    stream = DebouncedStream()  # => fresh stream
    delivered: list[int] = []  # => local recorder
    stream.subscribe(lambda v: delivered.append(v))
    stream.push(1)
    stream.flush()  # => first burst delivers 1
    stream.push(99)
    stream.push(100)
    stream.flush()  # => second burst delivers only its own final value
    assert delivered == [1, 100]  # => two independent flushes, each keeping only its burst's last value


# => Run: pytest -- Output: 2 passed
