"""Example 61: A Hand-Built Reader-Writer Lock -- Many Readers, OR One Writer."""

import threading  # => co-13, co-11: builds a richer invariant than a plain Semaphore or Lock alone
import time  # => simulates readers/writers "doing work" while holding their respective access


class ReaderWriterLock:  # => allows ANY NUMBER of concurrent readers, but only ONE writer, never both at once
    def __init__(self) -> None:
        # => no plain Lock or Semaphore alone can express "many readers OR one writer" -- Condition can
        self._condition = threading.Condition()  # => ONE Condition coordinates both readers and writers
        self._active_readers = 0  # => _active_readers: how many readers currently hold read access
        self._writer_active = False  # => _writer_active: True while exactly one writer holds write access

    def acquire_read(self) -> None:
        with self._condition:  # => acquires the Condition's lock for this check-and-update
            while self._writer_active:  # => a WHILE loop (co-14) -- readers wait out any active writer
                self._condition.wait()  # => releases the lock and sleeps until notified
            self._active_readers += 1  # => now safe to join as ANOTHER concurrent reader

    def release_read(self) -> None:
        with self._condition:  # => acquires the lock to safely decrement and possibly wake a waiting writer
            self._active_readers -= 1  # => one fewer active reader
            if self._active_readers == 0:  # => only wake others once the LAST reader has actually left
                self._condition.notify_all()  # => a waiting writer (or new readers) can now proceed

    def acquire_write(self) -> None:
        with self._condition:  # => acquires the lock for this check-and-update
            while self._writer_active or self._active_readers > 0:  # => a writer needs EXCLUSIVE access
                self._condition.wait()  # => waits out both other writers AND any currently-active readers
            self._writer_active = True  # => now safe to become THE one active writer

    def release_write(self) -> None:
        with self._condition:  # => acquires the lock to safely clear the writer flag
            self._writer_active = False  # => releases exclusive access
            self._condition.notify_all()  # => wakes ALL waiters -- readers and writers alike, to re-check


def reader(rw_lock: ReaderWriterLock, active_readers: list[int], peak_readers: list[int], violations: list[int]) -> None:
    rw_lock.acquire_read()  # => blocks until no writer is active
    active_readers[0] += 1  # => one more concurrent reader, tracked for the invariant check below
    peak_readers[0] = max(peak_readers[0], active_readers[0])  # => peak_readers: the highest concurrency observed
    time.sleep(0.01)  # => simulates reading -- long enough for OTHER readers to overlap, if the lock is correct
    active_readers[0] -= 1  # => this reader is done
    rw_lock.release_read()  # => may wake a waiting writer if this was the LAST active reader


def writer(rw_lock: ReaderWriterLock, active_readers: list[int], violations: list[int]) -> None:
    rw_lock.acquire_write()  # => blocks until NO readers and NO other writer are active
    violations[0] += 1 if active_readers[0] > 0 else 0  # => THE invariant check: a writer must NEVER see active readers
    time.sleep(0.01)  # => simulates writing, while genuinely EXCLUDING every reader
    rw_lock.release_write()  # => wakes all waiters to re-check the (now cleared) writer flag


if __name__ == "__main__":  # => module entry point
    rw_lock = ReaderWriterLock()  # => the shared reader-writer lock under test
    active_readers = [0]  # => active_readers[0]: how many readers are CURRENTLY inside their critical section
    peak_readers = [0]  # => peak_readers[0]: the max concurrency any reader batch actually reached
    violations = [0]  # => violations[0]: incremented if a writer EVER observed an active reader (a bug)

    readers = [threading.Thread(target=reader, args=(rw_lock, active_readers, peak_readers, violations)) for _ in range(5)]
    # => readers: 5 independent reader threads, all sharing the SAME rw_lock and active_readers counter
    writers = [threading.Thread(target=writer, args=(rw_lock, active_readers, violations)) for _ in range(3)]
    # => writers: 3 independent writer threads, competing for EXCLUSIVE access against readers AND each other
    all_threads = readers + writers  # => all_threads: 5 readers and 3 writers, started together below
    for t in all_threads:  # => starts every reader and writer thread
        # => start() only SCHEDULES the OS thread -- it does not itself block or wait for anything
        t.start()  # => all 8 threads immediately race to acquire read or write access
    for t in all_threads:  # => waits for every thread to finish
        t.join()  # => join() blocks until that thread's reader()/writer() call returns

    print(f"peak_readers={peak_readers[0]} violations={violations[0]}")  # => Output: peak_readers=<2 to 5> violations=0
    # => a violations count above 0 would mean the invariant was BROKEN -- exactly what this checks

    # => A reader-writer lock enforces a RICHER invariant than a plain Lock: MULTIPLE readers may hold
    # => access simultaneously (peak_readers > 1 here, confirming genuine overlap), but a WRITER always
    # => gets EXCLUSIVE access -- no reader and no other writer may be active while it holds the lock
    # => (co-13). The `while` conditions on BOTH `acquire_read` and `acquire_write` (co-14) are what
    # => enforce this: a writer waits out ALL current readers, and readers wait out any active writer.
    assert peak_readers[0] >= 2  # => confirms readers genuinely overlapped -- this is NOT a plain mutex
    assert violations[0] == 0  # => confirms NO writer ever ran while a reader was active -- the core invariant
    print("ex-61 OK")  # => Output: ex-61 OK
