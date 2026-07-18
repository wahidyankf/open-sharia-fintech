"""Example 72: pytest verification for `multiprocessing.shared_memory`."""

import struct
from multiprocessing import Process, shared_memory

from example import ITEM_SIZE, double_values_in_place


def test_child_process_mutates_the_shared_block_in_place() -> None:
    length = 100
    shm = shared_memory.SharedMemory(create=True, size=length * ITEM_SIZE)
    buf = shm.buf
    assert buf is not None
    try:
        for i in range(length):
            struct.pack_into("q", buf, i * ITEM_SIZE, i)

        child = Process(target=double_values_in_place, args=(shm.name, length))
        child.start()
        child.join()

        results = [struct.unpack_from("q", buf, i * ITEM_SIZE)[0] for i in range(length)]
        assert results == [i * 2 for i in range(length)]  # => the child's writes are visible without copying
    finally:
        shm.close()
        shm.unlink()


# => Run: pytest -- Output: 1 passed
