"""Example 61: pytest verification for a Hand-Built Reader-Writer Lock."""

import threading

from example import ReaderWriterLock, reader, writer


def test_readers_overlap_but_writers_never_see_an_active_reader() -> None:
    rw_lock = ReaderWriterLock()
    active_readers = [0]
    peak_readers = [0]
    violations = [0]

    readers = [threading.Thread(target=reader, args=(rw_lock, active_readers, peak_readers, violations)) for _ in range(4)]
    writers = [threading.Thread(target=writer, args=(rw_lock, active_readers, violations)) for _ in range(2)]
    all_threads = readers + writers
    for t in all_threads:
        t.start()
    for t in all_threads:
        t.join()

    assert peak_readers[0] >= 2  # => readers genuinely overlapped -- this is not a plain mutex
    assert violations[0] == 0  # => no writer ever ran while a reader was active


# => Run: pytest -- Output: 1 passed
