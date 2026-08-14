from typing import Final  # => typed survey fixture

APPROVED: Final[bool] = False  # => consequential action pauses
assert not APPROVED  # => loop must halt for review
print("PASS: human-in-the-loop-interrupt")  # => offline result
