# learning/code/ex-44-property-roundtrip/test_example.py
"""Example 44: Property -- Round-Trip."""

from hypothesis import given  # => same property-test decorator as ex-43 (co-18)
from hypothesis import strategies as st  # => st.text() generates arbitrary Unicode strings, not just ASCII (co-20)  # fmt: skip


def encode(text: str) -> bytes:  # => the unit under test, half A: text -> bytes
    return text.encode(
        "utf-8"
    )  # => a real, standard encoding -- not a toy transformation


def decode(data: bytes) -> str:  # => the unit under test, half B: bytes -> text
    return data.decode("utf-8")  # => the INVERSE operation of encode above


@given(st.text())  # => co-18/co-20: generates strings including empty, emoji, surrogate-adjacent chars  # fmt: skip
def test_decode_of_encode_is_the_identity(original: str) -> None:
    # => ROUND-TRIP: applying encode THEN decode should always recover the ORIGINAL value --
    # => this is a much stronger check than any single hand-picked example could offer (co-18)  # fmt: skip
    round_tripped = decode(encode(original))  # => act: encode then immediately decode  # fmt: skip
    assert round_tripped == original  # => the invariant: nothing was lost or corrupted in the round trip  # fmt: skip
