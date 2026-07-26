"""Example 59: Delta Encoding for Monotonic Timestamps."""
# Delta encoding (co-28) stores the first value plus small differences instead of full values.


def delta_encode(
    timestamps: list[int],
) -> tuple[int, list[int]]:  # => co-28: first value + deltas
    if not timestamps:  # => nothing to encode
        return 0, []  # => no base value, no deltas
    base = timestamps[0]  # => the FULL first value -- everything else is relative to it
    deltas: list[
        int
    ] = []  # => the difference from each value to the one right before it
    for i in range(1, len(timestamps)):  # => walk every consecutive pair
        deltas.append(
            timestamps[i] - timestamps[i - 1]
        )  # => a SMALL number, if the series is monotonic-ish
    return (
        base,
        deltas,
    )  # => the base value plus the list of deltas needed to reconstruct the rest


def delta_decode(base: int, deltas: list[int]) -> list[int]:  # => the inverse operation
    result = [base]  # => the first value is exactly the stored base
    for delta in deltas:  # => walk deltas in order, accumulating back up to full values
        result.append(
            result[-1] + delta
        )  # => each value is the previous one plus its delta
    return result  # => the fully reconstructed timestamp column


timestamps = [
    1700000000,
    1700000001,
    1700000003,
    1700000004,
    1700000010,
]  # => monotonic seconds
base, deltas = delta_encode(timestamps)  # => run the encoder over the fixture column
decoded = delta_decode(base, deltas)  # => and immediately decode it back
print(base)  # => Output: 1700000000
print(deltas)  # => Output: [1, 2, 1, 6]
print(
    decoded
)  # => Output: [1700000000, 1700000001, 1700000003, 1700000004, 1700000010]

assert decoded == timestamps  # => delta encoding round-trips exactly
assert all(
    delta < 100 for delta in deltas
)  # => every delta is a small integer, unlike the full timestamps
print("ex-59 OK")  # => Output: ex-59 OK
