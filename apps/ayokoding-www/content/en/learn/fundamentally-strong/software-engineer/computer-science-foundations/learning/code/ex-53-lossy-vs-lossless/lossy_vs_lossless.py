# learning/code/ex-53-lossy-vs-lossless/lossy_vs_lossless.py
"""Example 53: Quantization (Lossy) vs. zlib (Lossless) -- Only One Path Reconstructs Exactly."""  # => co-27: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import struct  # => co-27: packs the original float samples into bytes for zlib to compress
import zlib  # => co-27: stdlib DEFLATE -- a genuinely LOSSLESS general-purpose compressor


def quantize(samples: list[float], levels: int = 16) -> list[float]:  # => co-27: LOSSY -- rounds to a coarse grid
    """Lossy compression: snap each sample to the nearest of `levels` evenly-spaced values in [0, 1]."""  # => co-27: documents quantize's contract -- no runtime output, just sets its __doc__
    step = 1.0 / (levels - 1)  # => co-27: the spacing between adjacent quantization levels
    return [round(round(s / step) * step, 10) for s in samples]  # => co-27: DISCARDS the exact original value, by design


if __name__ == "__main__":  # => co-27: entry point -- this block runs only when the file executes directly, not on import
    samples = [0.0, 0.123456, 0.5, 0.6789, 0.987654, 1.0]  # => co-27: original data with fine-grained precision
    quantized = quantize(samples)  # => co-27: the LOSSY path -- coarser, smaller, but NOT exactly reversible
    print(f"original:  {samples}")  # => co-27: full-precision input
    print(f"quantized: {quantized}")  # => co-27: snapped to a coarse 16-level grid -- visibly different values
    lossy_reconstructs_exactly = quantized == samples  # => co-27: expected to be False -- precision was discarded
    print(f"quantization reconstructs original exactly: {lossy_reconstructs_exactly}")  # => co-27: expect False
    assert not lossy_reconstructs_exactly, "quantization must NOT reconstruct the exact original values"  # => co-27

    packed = struct.pack(f"{len(samples)}d", *samples)  # => co-27: raw bytes -- the exact bit pattern of every float
    compressed = zlib.compress(packed)  # => co-27: the LOSSLESS path -- DEFLATE finds redundancy, discards nothing
    decompressed = zlib.decompress(compressed)  # => co-27: DEFLATE's decompression is the exact inverse of compress()
    reconstructed = list(struct.unpack(f"{len(samples)}d", decompressed))  # => co-27: back to a list of floats
    print(f"zlib round-trip: {reconstructed}")  # => co-27: should be BIT-IDENTICAL to the original
    lossless_reconstructs_exactly = reconstructed == samples  # => co-27: expected to be True -- nothing was discarded
    print(f"zlib reconstructs original exactly: {lossless_reconstructs_exactly}")  # => co-27: expect True
    assert lossless_reconstructs_exactly, "zlib round-trip must reconstruct the exact original values"  # => co-27
    print(f"Only the lossless (zlib) path reconstructs the input exactly: True")  # => co-27: both asserts above passed
    # => co-27: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
