"""Example 58: Run-Length Encoding."""
# RLE (co-28) collapses consecutive repeated values into (value, run-length) pairs.


def rle_encode(
    column: list[str],
) -> list[tuple[str, int]]:  # => co-28: consecutive repeats collapse
    if not column:  # => an empty column has no runs at all
        return []  # => nothing to encode
    runs: list[
        tuple[str, int]
    ] = []  # => the encoded (value, count) pairs, built up in order
    current_value = column[0]  # => the value the current run is tracking
    current_count = (
        1  # => how many times current_value has repeated so far, consecutively
    )
    for value in column[1:]:  # => walk every remaining value in original order
        if value == current_value:  # => still the same run -- extend it
            current_count += 1  # => one more consecutive repeat
        else:  # => the run broke -- close it out and start a new one
            runs.append((current_value, current_count))  # => record the finished run
            current_value = value  # => start tracking a NEW run
            current_count = 1  # => the new run's first (and so-far only) occurrence
    runs.append(
        (current_value, current_count)
    )  # => the final run never got closed inside the loop
    return runs  # => the fully run-length-encoded column


def rle_decode(runs: list[tuple[str, int]]) -> list[str]:  # => the inverse operation
    decoded: list[str] = []  # => the reconstructed column, one value at a time
    for value, count in runs:  # => walk every (value, count) run in order
        decoded.extend(
            [value] * count
        )  # => expand this run back into `count` repeated values
    return decoded  # => the fully reconstructed column


column = [
    "a",
    "a",
    "a",
    "b",
    "b",
    "c",
    "c",
    "c",
    "c",
]  # => a sorted, highly repetitive column
runs = rle_encode(column)  # => run the encoder
decoded = rle_decode(runs)  # => and immediately decode it back
print(runs)  # => Output: [('a', 3), ('b', 2), ('c', 4)]
print(decoded)  # => Output: ['a', 'a', 'a', 'b', 'b', 'c', 'c', 'c', 'c']

assert decoded == column  # => RLE round-trips exactly
assert len(runs) < len(
    column
)  # => the encoded run count collapsed below the original element count
print("ex-58 OK")  # => Output: ex-58 OK
