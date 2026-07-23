# learning/code/ex-50-shannon-entropy-coin/entropy_coin.py
"""Example 50: Shannon Entropy of a Biased Coin."""  # => co-26: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import math  # => co-26: math.log2 -- Shannon entropy is measured in BITS, hence base-2 logarithm


def binary_entropy(p_heads: float) -> float:  # => co-26: H(X) = -sum(p * log2(p)) over the outcome distribution
    """Shannon entropy, in bits, of a coin landing heads with probability p_heads."""  # => co-26: documents binary_entropy's contract -- no runtime output, just sets its __doc__
    if p_heads in (0.0, 1.0):  # => co-26: a fully predictable coin (always heads or always tails) has ZERO entropy
        return 0.0  # => co-26: by convention, 0 * log2(0) is treated as 0 -- no surprise, no information
    p_tails = 1.0 - p_heads  # => co-26: the coin's only other outcome -- a two-outcome distribution
    return -(p_heads * math.log2(p_heads) + p_tails * math.log2(p_tails))  # => co-26: Shannon's 1948 formula, applied


if __name__ == "__main__":  # => co-26: entry point -- this block runs only when the file executes directly, not on import
    for p in (0.0, 0.1, 0.5, 0.9, 1.0):  # => co-26: a spread from certain to maximally uncertain and back
        h = binary_entropy(p)  # => co-26: this bias's entropy, in bits
        print(f"P(heads)={p:.1f}  H = {h:.4f} bits")  # => co-26: printed to 4 decimal places
    h_fair = binary_entropy(0.5)  # => co-26: the FAIR-coin case -- maximum uncertainty for a 2-outcome distribution
    h_biased = binary_entropy(0.9)  # => co-26: a HEAVILY biased coin -- mostly predictable, so much LESS entropy
    print(f"H(0.5) = {h_fair:.4f} bits, H(0.9) = {h_biased:.4f} bits")  # => co-26: side-by-side comparison
    assert abs(h_fair - 1.0) < 1e-9, "a fair coin must have EXACTLY 1 bit of entropy"  # => co-26: the textbook maximum
    assert h_biased < 0.5, "a 90%-biased coin must have LESS than 0.5 bits of entropy"  # => co-26: much more predictable
    print(f"H(0.5)=1 bit and H(0.9)<0.5 bit: True")  # => co-26: reached only if both asserts above passed
    # => co-26: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
