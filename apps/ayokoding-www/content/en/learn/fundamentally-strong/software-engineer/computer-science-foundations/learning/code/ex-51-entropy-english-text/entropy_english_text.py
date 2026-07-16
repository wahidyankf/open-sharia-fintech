# learning/code/ex-51-entropy-english-text/entropy_english_text.py
"""Example 51: Estimating the Per-Character Entropy of Sample English Text."""  # => co-26: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import math  # => co-26: log2 -- the same Shannon-entropy formula Example 50 applied to a coin, now to letters
from collections import Counter  # => co-26: tallies each character's observed frequency across the sample

SAMPLE_TEXT = (  # => co-26: ordinary English prose -- lowercase letters and spaces, no punctuation, for a clean count
    "the quick brown fox jumps over the lazy dog while the sun sets slowly behind "  # => co-26: one chunk of the multi-line literal, concatenated with its neighbors
    "the distant hills and the wind carries the scent of rain across the open field "  # => co-26: one chunk of the multi-line literal, concatenated with its neighbors
    "every programmer eventually learns that information has a cost measured in bits "  # => co-26: one chunk of the multi-line literal, concatenated with its neighbors
    "and that natural language is far from random since common letters like e and t "  # => co-26: one chunk of the multi-line literal, concatenated with its neighbors
    "appear much more often than rare letters like q and z in ordinary written text"  # => co-26: one chunk of the multi-line literal, concatenated with its neighbors
)  # => co-26: closes the multi-line construct opened above


def zero_order_entropy(text: str) -> float:  # => co-26: "zero-order" -- treats each character as independent
    """Estimate per-character Shannon entropy from the sample's own character-frequency distribution."""  # => co-26: documents zero_order_entropy's contract -- no runtime output, just sets its __doc__
    counts = Counter(text)  # => co-26: how many times each distinct character appears
    n = len(text)  # => co-26: total character count -- the denominator for every probability estimate
    probabilities = (count / n for count in counts.values())  # => co-26: empirical P(char) for every distinct symbol
    return -sum(p * math.log2(p) for p in probabilities)  # => co-26: Shannon's formula, summed over the alphabet


if __name__ == "__main__":  # => co-26: entry point -- this block runs only when the file executes directly, not on import
    entropy = zero_order_entropy(SAMPLE_TEXT)  # => co-26: this sample's estimated per-character entropy
    distinct_chars = len(set(SAMPLE_TEXT))  # => co-26: alphabet size actually observed in this sample
    uniform_entropy = math.log2(distinct_chars)  # => co-26: the MAXIMUM possible entropy for this alphabet size
    print(f"sample length: {len(SAMPLE_TEXT)} characters, {distinct_chars} distinct symbols")  # => co-26
    print(f"estimated entropy: {entropy:.4f} bits/char")  # => co-26: the headline measurement
    print(f"uniform-distribution ceiling: log2({distinct_chars}) = {uniform_entropy:.4f} bits/char")  # => co-26
    assert entropy < uniform_entropy, "real text must have LESS entropy than a uniform distribution over the same alphabet"  # => co-26
    assert 3.5 < entropy < 4.5, "ordinary English text's zero-order entropy lands near 4 bits/char"  # => co-26: syllabus's claim
    print(f"Entropy lands near 4 bits/char: True")  # => co-26: reached only if both asserts above passed
    # => co-26: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
