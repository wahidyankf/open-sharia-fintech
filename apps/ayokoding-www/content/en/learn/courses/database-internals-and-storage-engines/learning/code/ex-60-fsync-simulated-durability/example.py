"""Example 60: fsync as a Durability Barrier."""
# fsync (co-26) is the barrier: only data flushed to disk BEFORE the last fsync survives a crash.


class DurabilityModel:  # => models an OS page cache (volatile) plus a disk (survives crashes)
    def __init__(self) -> None:  # => starts with nothing written and nothing durable
        self.os_cache: list[str] = []  # => written but NOT yet fsync'd -- lost on crash
        self.disk: list[
            str
        ] = []  # => made durable by the most recent fsync -- survives a crash

    def write(
        self, record: str
    ) -> None:  # => a write() call only reaches the OS cache, not disk yet
        self.os_cache.append(
            record
        )  # => sitting in volatile memory until an fsync moves it

    def fsync(
        self,
    ) -> None:  # => the durability barrier -- forces everything pending out to disk
        self.disk.extend(self.os_cache)  # => everything written so far becomes durable
        self.os_cache.clear()  # => the OS cache is now empty -- fully flushed

    def crash(
        self,
    ) -> list[str]:  # => simulates a crash -- the OS cache is lost, disk survives
        self.os_cache.clear()  # => volatile memory does not survive a crash
        return list(self.disk)  # => only what fsync had already committed remains


model = DurabilityModel()  # => a fresh model with nothing written yet
model.write("record-1")  # => before the fsync -- SHOULD survive
model.write("record-2")  # => before the fsync -- SHOULD survive
model.fsync()  # => the durability barrier -- record-1 and record-2 are now durable
model.write("record-3")  # => AFTER the fsync -- SHOULD NOT survive a crash
survivors = (
    model.crash()
)  # => simulate a crash right now, before record-3 is ever fsync'd
print(survivors)  # => Output: ['record-1', 'record-2']

assert (
    "record-1" in survivors and "record-2" in survivors
)  # => everything before the fsync survived
assert (
    "record-3" not in survivors
)  # => the write after the last fsync did NOT survive the crash
print("ex-60 OK")  # => Output: ex-60 OK
