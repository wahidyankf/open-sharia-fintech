"""Example 1: Allocate a Fixed-Size Page -- the unit of I/O every storage engine reads and writes in."""

# A database never reads or writes a single row directly -- it reads and
# writes whole PAGES (co-01). Postgres/SQL Server default to 8 KB pages;
# InnoDB defaults to 16 KB -- the exact size is engine-specific, so this
# constant is named, not a hardcoded literal sprinkled through the file.
PAGE_SIZE: int = 4096  # => 4 KB, a convenient small-scale page size for this course


def new_page() -> bytearray:  # => allocates one zero-filled page buffer
    return bytearray(PAGE_SIZE)  # => bytearray(n) is mutable AND zero-initialized


page: bytearray = new_page()  # => a single fresh page
print(len(page))  # => Output: 4096
print(page[:8])  # => Output: bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00')

assert (
    len(page) == PAGE_SIZE
)  # => the page's byte length always equals the page-size constant
assert all(
    byte == 0 for byte in page
)  # => a brand-new page is entirely zero-filled before any write
print("ex-01 OK")  # => Output: ex-01 OK
