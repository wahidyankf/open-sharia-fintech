# learning/code/ex-55-sha256-avalanche/sha256_avalanche.py
"""Example 55: SHA-256 Avalanche -- Two Near-Identical Inputs, ~50% of Digest Bits Differ."""  # => co-28: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import hashlib  # => co-28: hashlib.sha256 -- a cryptographic hash, unlike CRC32's accidental-corruption-only design


def digest_bits(data: bytes) -> str:  # => co-28: renders a SHA-256 digest as a 256-character binary string
    """SHA-256 digest of data, rendered as a 256-bit binary string."""  # => co-28: documents digest_bits's contract -- no runtime output, just sets its __doc__
    digest = hashlib.sha256(data).digest()  # => co-28: 32 raw bytes -- SHA-256's fixed-size, effectively-irreversible output
    return "".join(format(byte, "08b") for byte in digest)  # => co-28: each byte -> its 8-bit binary string, concatenated


def hamming_distance(bits_a: str, bits_b: str) -> int:  # => co-28: counts positions where two equal-length bitstrings differ
    """Count differing bit positions between two equal-length binary strings."""  # => co-28: documents hamming_distance's contract -- no runtime output, just sets its __doc__
    return sum(1 for a, b in zip(bits_a, bits_b) if a != b)  # => co-28: one comparison per bit position


if __name__ == "__main__":  # => co-28: entry point -- this block runs only when the file executes directly, not on import
    message_a = b"The quick brown fox jumps over the lazy dog"  # => co-28: the baseline message
    message_b = b"The quick brown fox jumps over the lazy dof"  # => co-28: ONE character changed (g -> f) -- nearly identical input
    bits_a = digest_bits(message_a)  # => co-28: message_a's full 256-bit digest, as a bitstring
    bits_b = digest_bits(message_b)  # => co-28: message_b's full 256-bit digest, as a bitstring
    print(f"message_a: {message_a!r}")  # => co-28: the two inputs, shown side by side for the single-character diff
    print(f"message_b: {message_b!r}")  # => co-28: differs from message_a by exactly one character
    print(f"sha256(a) = {hashlib.sha256(message_a).hexdigest()}")  # => co-28: message_a's digest, in familiar hex form
    print(f"sha256(b) = {hashlib.sha256(message_b).hexdigest()}")  # => co-28: message_b's digest -- expect NO visible similarity
    differing_bits = hamming_distance(bits_a, bits_b)  # => co-28: how many of the 256 bits actually differ
    fraction_differing = differing_bits / 256  # => co-28: expressed as a fraction of the full digest
    print(f"differing bits: {differing_bits} / 256 ({fraction_differing:.1%})")  # => co-28: the avalanche measurement itself
    assert bits_a != bits_b, "the two digests must be genuinely different"  # => co-28: sanity check
    assert 0.4 < fraction_differing < 0.6, "roughly half the digest bits must differ (the avalanche effect)"  # => co-28
    print(f"Approximately 50% of digest bits differ: True")  # => co-28: reached only if both asserts above passed
    # => co-28: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
