"""Example 2: Page Header Pack and Unpack -- pd_lower/pd_upper via struct."""

import struct

# A page's header stores two offsets: pd_lower (end of the slot array, grows
# UP from the front) and pd_upper (start of tuple data, grows DOWN from the
# back) (co-02). "<HH" packs both as little-endian unsigned 16-bit integers --
# 4 bytes total, enough to address a page far larger than this course's 4 KB.
HEADER_FORMAT: str = "<HH"  # => two uint16 fields: pd_lower, pd_upper
HEADER_SIZE: int = struct.calcsize(HEADER_FORMAT)  # => 4 bytes


def pack_header(pd_lower: int, pd_upper: int) -> bytes:  # => serializes the header
    return struct.pack(
        HEADER_FORMAT, pd_lower, pd_upper
    )  # => exactly HEADER_SIZE bytes


def unpack_header(raw: bytes) -> tuple[int, int]:  # => deserializes the header
    lo, hi = struct.unpack(HEADER_FORMAT, raw[:HEADER_SIZE])
    return int(lo), int(hi)  # => (pd_lower, pd_upper), as plain Python ints


packed: bytes = pack_header(
    HEADER_SIZE, 4096
)  # => a fresh page: slots start right after the header
print(packed)  # => Output: b'\x04\x00\x00\x10'
pd_lower, pd_upper = unpack_header(packed)  # => round-trip back to Python ints
print((pd_lower, pd_upper))  # => Output: (4, 4096)

assert (pd_lower, pd_upper) == (
    HEADER_SIZE,
    4096,
)  # => unpack(pack(x)) == x -- the round-trip holds
print("ex-02 OK")  # => Output: ex-02 OK
