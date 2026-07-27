"""Example 9: Detect Page Corruption with a Checksum."""

import zlib  # => stdlib module -- CRC32 is fast and good enough for a corruption DETECTOR

PAGE_SIZE: int = 4096  # => same 4 KB page size used throughout this course

# A checksum over the whole page is a cheap corruption DETECTOR, not a fix
# (co-26) -- CRC32 is not cryptographically strong, but flipping even one bit
# anywhere it covers changes the result, which is all detection needs.


def checksum(
    page: bytes | bytearray,
) -> int:  # => a single deterministic integer summarizing every byte
    return zlib.crc32(
        bytes(page)
    )  # => same input bytes always produce the same checksum


page = bytearray(PAGE_SIZE)  # => start from a fresh, zero-filled page
page[100:110] = b"hello-row!"  # => simulate SOME real content living on the page
original = checksum(page)  # => the checksum of the page as it exists right now
print(
    hex(original)
)  # => Output: 0x9fc341db (a genuine, captured hex CRC for this exact byte layout)

corrupted = bytearray(page)  # => an independent COPY -- `page` itself stays untouched
corrupted[0] ^= 0x01  # => flip a SINGLE bit in a byte the CRC actually covers
corrupted_sum = checksum(corrupted)  # => recompute over the corrupted copy

assert (
    corrupted_sum != original
)  # => one flipped bit changes the checksum -- corruption is detectable
assert (
    checksum(bytes(page)) == original
)  # => an UNCHANGED page always reproduces the same checksum
print("ex-09 OK")  # => Output: ex-09 OK
