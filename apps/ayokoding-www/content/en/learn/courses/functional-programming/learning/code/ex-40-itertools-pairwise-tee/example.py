"""Example 40: Adjacent Pairs via pairwise and tee."""

from itertools import (
    pairwise,
    tee,
)  # => pairwise: consecutive pairs; tee: split one iterator in two

readings = [10, 12, 9, 15, 15]  # => a sequence of sensor readings

deltas = [
    b - a for a, b in pairwise(readings)
]  # => consecutive differences, one per adjacent pair
# => pairwise([10, 12, 9, 15, 15]) yields (10,12), (12,9), (9,15), (15,15) -- 4 pairs from 5 readings

original_stream, backup_stream = tee(
    iter(readings)
)  # => splits ONE iterator into two INDEPENDENT ones
first_from_original = next(original_stream)  # => advances original_stream only
first_from_backup = next(
    backup_stream
)  # => backup_stream is UNAFFECTED by the pull above

print(deltas)  # => Output: [2, -3, 6, 0]
print(
    first_from_original == first_from_backup
)  # => Output: True -- both streams start from readings[0]
