# learning/code/ex-59-isolate-io-boundary/test_example.py
"""Example 59: Isolating an I/O Boundary."""


# ex-59: a FAKE filesystem -- the unit test below touches NO real disk, network, or OS call (co-16, co-26)  # fmt: skip
class FakeFileStore:  # => a fake: genuinely stores/retrieves data, entirely in memory (co-16)  # fmt: skip
    def __init__(self) -> None:
        self._files: dict[str, str] = {}  # => an in-memory dict STANDS IN for a real filesystem  # fmt: skip

    def write(self, path: str, content: str) -> None:  # => mirrors a real filesystem's write() signature  # fmt: skip
        self._files[path] = content  # => a REAL write -- just not to actual disk

    def read(self, path: str) -> str | None:  # => mirrors a real filesystem's read() signature  # fmt: skip
        return self._files.get(path)  # => a REAL read -- returns None if never written, like a missing file  # fmt: skip


def save_and_reload(store, path: str, content: str) -> str | None:  # => the unit under test  # fmt: skip
    store.write(
        path, content
    )  # => act, part 1: writes through WHATEVER store it was given
    return store.read(path)  # => act, part 2: reads back through the SAME store  # fmt: skip


def test_save_and_reload_touches_no_real_disk() -> None:
    fake_store = FakeFileStore()  # => arrange: the ENTIRE test's "filesystem" lives in this one object (co-26)  # fmt: skip
    result = save_and_reload(fake_store, "/tmp/example.txt", "hello")  # => act  # fmt: skip
    assert result == "hello"  # => assert 1: the round trip worked, exactly like a real file would  # fmt: skip
    assert fake_store._files == {"/tmp/example.txt": "hello"}  # => assert 2: proves the write is IN-MEMORY, not on real disk  # fmt: skip
    # => no `open()`, no `os.write`, no real path "/tmp/example.txt" was ever touched --
    # => this test runs identically on any machine, any OS, any filesystem permissions (co-26)
