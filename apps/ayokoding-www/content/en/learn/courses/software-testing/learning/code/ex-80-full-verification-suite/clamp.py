# The GREEN implementation below -- kept byte-identical in statement count and shape so the
# coverage/mutation Output blocks in bdd.md stay accurate; only trailing comments were added here.
def clamp(value: float, lo: float, hi: float) -> float:  # => co-17: built AFTER the red tests below  # fmt: skip
    """Constrain value to the closed interval [lo, hi]."""  # => single-line docstring, no extra bare lines
    if value < lo:  # => co-17: the FIRST failing test (below zero) drove this branch into existence  # fmt: skip
        return lo  # => co-17: floors an out-of-range value at the lower bound  # fmt: skip
    if value > hi:  # => co-17: the SECOND failing test (above hi) drove THIS branch  # fmt: skip
        return hi  # => co-17: caps an out-of-range value at the upper bound  # fmt: skip
    return value  # => co-17: the THIRD test (already in range) drove this fallthrough  # fmt: skip
