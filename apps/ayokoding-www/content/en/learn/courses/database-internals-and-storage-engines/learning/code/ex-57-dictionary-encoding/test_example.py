"""Example 57: pytest verification for Dictionary Encoding."""

from example import dictionary_decode, dictionary_encode


def test_dictionary_encoding_round_trips() -> None:
    column = ["x", "y", "x", "x"]
    codes, dictionary = dictionary_encode(column)
    assert dictionary_decode(codes, dictionary) == column


def test_encoded_form_is_smaller_for_a_repetitive_column() -> None:
    column = ["aaaaaaaaaa"] * 10
    codes, dictionary = dictionary_encode(column)
    encoded_size = len(codes) + sum(len(v) for v in dictionary.values())
    raw_size = sum(len(v) for v in column)
    assert encoded_size < raw_size


# => Run: pytest -- Output: 2 passed
