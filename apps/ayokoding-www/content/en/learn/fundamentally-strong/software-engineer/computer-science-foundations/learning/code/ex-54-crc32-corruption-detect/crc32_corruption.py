# learning/code/ex-54-crc32-corruption-detect/crc32_corruption.py
"""Example 54: CRC32 -- Flip One Bit, Watch the Checksum Mismatch Flag It."""  # => co-28: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import zlib  # => co-28: zlib.crc32 -- the stdlib's fast, non-cryptographic checksum for ACCIDENTAL corruption


def flip_one_bit(data: bytes, byte_index: int, bit_index: int) -> bytes:  # => co-28: simulates a single bit-flip
    """Return a copy of data with exactly one bit flipped, simulating accidental corruption."""  # => co-28: documents flip_one_bit's contract -- no runtime output, just sets its __doc__
    mutable = bytearray(data)  # => co-28: bytes are immutable -- bytearray gives us a mutable copy to flip a bit in
    mutable[byte_index] ^= 1 << bit_index  # => co-28: XOR with a single set bit flips EXACTLY that one bit, nothing else
    return bytes(mutable)  # => co-28: back to an immutable bytes object, matching the original's type


if __name__ == "__main__":  # => co-28: entry point -- this block runs only when the file executes directly, not on import
    original = b"this message must arrive completely intact"  # => co-28: the data a checksum will protect
    original_checksum = zlib.crc32(original)  # => co-28: a 32-bit fingerprint of the ORIGINAL, uncorrupted bytes
    print(f"original: {original!r}")  # => co-28: the data under test
    print(f"original CRC32: {original_checksum:#010x}")  # => co-28: printed as an 8-hex-digit value
    corrupted = flip_one_bit(original, byte_index=5, bit_index=2)  # => co-28: exactly ONE bit changed, everything else identical
    corrupted_checksum = zlib.crc32(corrupted)  # => co-28: recomputed over the (now corrupted) bytes
    print(f"corrupted: {corrupted!r}")  # => co-28: visibly different from `original` by exactly one character
    print(f"corrupted CRC32: {corrupted_checksum:#010x}")  # => co-28: expected to differ from the original checksum
    checksums_match = original_checksum == corrupted_checksum  # => co-28: the actual detection test
    print(f"checksums match: {checksums_match}")  # => co-28: expect False -- corruption IS detected
    assert original != corrupted, "the corrupted bytes must genuinely differ from the original"  # => co-28: sanity check
    assert not checksums_match, "a single bit-flip must change the CRC32 checksum"  # => co-28: the detection itself
    print(f"Checksum mismatch flags the corruption: True")  # => co-28: reached only if both asserts above passed
    # => co-28: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
