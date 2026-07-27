"""Example 57: Dictionary Encoding."""
# Dictionary encoding (co-28) replaces repeated string values with small integer codes.


def dictionary_encode(
    column: list[str],
) -> tuple[list[int], dict[int, str]]:  # => co-28: encode + dictionary
    unique_values = sorted(
        set(column)
    )  # => the distinct values, in a stable, deterministic order
    code_of: dict[str, int] = {
        value: i for i, value in enumerate(unique_values)
    }  # => value -> its code
    dictionary: dict[int, str] = {
        i: value for value, i in code_of.items()
    }  # => code -> its value, for decode
    codes = [
        code_of[value] for value in column
    ]  # => the column, rewritten as small integers
    return (
        codes,
        dictionary,
    )  # => the encoded codes plus the lookup table needed to decode them


def dictionary_decode(
    codes: list[int], dictionary: dict[int, str]
) -> list[str]:  # => the inverse operation
    return [
        dictionary[code] for code in codes
    ]  # => look each code back up in the dictionary


column = [
    "red",
    "blue",
    "red",
    "red",
    "blue",
    "green",
    "red",
]  # => a low-cardinality column: 3 distinct values
codes, dictionary = dictionary_encode(
    column
)  # => run the encoder over the fixture column
decoded = dictionary_decode(codes, dictionary)  # => and immediately decode it back
print(codes)  # => Output: [2, 0, 2, 2, 0, 1, 2]
print(dictionary)  # => Output: {0: 'blue', 1: 'green', 2: 'red'}
print(decoded)  # => Output: ['red', 'blue', 'red', 'red', 'blue', 'green', 'red']

raw_size = sum(
    len(v) for v in column
)  # => bytes if every value were stored as its own string
encoded_size = len(codes) + sum(
    len(v) for v in dictionary.values()
)  # => codes (1 byte each) + dictionary once
print(raw_size)  # => Output: 25
print(encoded_size)  # => Output: 19

assert decoded == column  # => dictionary encoding round-trips exactly
assert encoded_size < raw_size  # => encoding is smaller precisely because values repeat
print("ex-57 OK")  # => Output: ex-57 OK
