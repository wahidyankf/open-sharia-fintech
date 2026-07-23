"""Example 72: `multiprocessing.shared_memory` -- Genuine No-Copy Cross-Process Access."""

import struct  # => packs/unpacks fixed-size integers directly into the shared memory buffer
from multiprocessing import Process, shared_memory  # => co-24, co-19: REAL shared memory, not a copy-based Queue

ARRAY_LENGTH = 2000  # => how many 8-byte integers live in the shared block
ITEM_SIZE = 8  # => bytes per integer -- struct format "q" (signed long long) is always 8 bytes


def double_values_in_place(shm_name: str, length: int) -> None:  # => runs in a SEPARATE process
    shm = shared_memory.SharedMemory(name=shm_name)  # => ATTACHES to the EXISTING block by name -- no copy made
    buf = shm.buf  # => buf: typed as `memoryview | None` by typeshed -- narrowed once, right here
    assert buf is not None  # => always non-None once a SharedMemory is genuinely attached (co-19's own invariant)
    try:
        for i in range(length):  # => mutates every value, IN PLACE, directly inside the shared buffer
            offset = i * ITEM_SIZE  # => offset: this value's exact byte position within `buf`
            (value,) = struct.unpack_from("q", buf, offset)  # => reads the CURRENT value at that offset
            struct.pack_into("q", buf, offset, value * 2)  # => writes the DOUBLED value back, same memory
    finally:
        shm.close()  # => releases THIS process's handle -- does NOT destroy the underlying shared memory itself


if __name__ == "__main__":  # => module entry point
    shm = shared_memory.SharedMemory(create=True, size=ARRAY_LENGTH * ITEM_SIZE)  # => allocates a NEW OS-level shared block
    parent_buf = shm.buf  # => parent_buf: the SAME `memoryview | None` narrowing as inside the child process
    assert parent_buf is not None  # => always non-None right after a fresh, successful `create=True` call
    try:
        for i in range(ARRAY_LENGTH):  # => initializes the block with the values 0, 1, 2, ...
            struct.pack_into("q", parent_buf, i * ITEM_SIZE, i)  # => writes value `i` at its own 8-byte slot

        child = Process(target=double_values_in_place, args=(shm.name, ARRAY_LENGTH))  # => child: attaches by NAME
        child.start()  # => the child process opens the SAME underlying memory -- no serialization of the array itself
        child.join()  # => waits for the child to finish doubling every value in place

        results = [struct.unpack_from("q", parent_buf, i * ITEM_SIZE)[0] for i in range(ARRAY_LENGTH)]
        expected = [i * 2 for i in range(ARRAY_LENGTH)]  # => expected: what doubling every original value SHOULD give
        print(f"results[:5]={results[:5]} expected[:5]={expected[:5]}")  # => Output: results[:5]=[0,2,4,6,8] expected[:5]=[0,2,4,6,8]

        # => Unlike `multiprocessing.Queue` (ex-46), which PICKLES and COPIES every item across the
        # => process boundary, `shared_memory.SharedMemory` gives BOTH processes direct access to the
        # => SAME underlying OS memory block (co-24) -- the child's writes are visible to the parent
        # => WITHOUT any explicit copy or message being sent back. This matters for large arrays, where
        # => copying would dominate the cost; only the small `shm.name` string needs to cross processes.
        # => Manual synchronization (co-19) is still the caller's responsibility -- unlike ex-47's
        # => `Value`, plain `SharedMemory` has no built-in lock of its own.
        assert results == expected  # => confirms every value was doubled correctly, IN the shared block itself
    finally:
        shm.close()  # => releases the PARENT's own handle to the shared memory
        shm.unlink()  # => releases the underlying OS resource -- only the CREATOR should ever call this
    print("ex-72 OK")  # => Output: ex-72 OK
