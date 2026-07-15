# learning/code/ex-15-parametrize-ids/test_example.py
"""Example 15: Parametrize with Readable ids."""

import pytest  # => same @pytest.mark.parametrize as ex-14, this time with explicit ids= (co-06)


def classify_sign(n: int) -> str:  # => the unit under test
    if n > 0:  # => branch 1
        return "positive"  # => label for anything above zero
    if n < 0:  # => branch 2
        return "negative"  # => label for anything below zero
    return "zero"  # => branch 3 -- exactly n == 0


@pytest.mark.parametrize(  # => same decorator as ex-14, now with an explicit ids= argument below  # fmt: skip
    "value, expected",  # => the two parameter NAMES, unchanged from ex-14's shape  # fmt: skip
    [  # => the same three rows as ex-14 in spirit, now paired with readable ids=  # fmt: skip
        (5, "positive"),  # => row 1 -- would otherwise show as an opaque "test_...[5-positive0]"  # fmt: skip
        (-3, "negative"),  # => row 2 -- same problem without a readable id
        (0, "zero"),  # => row 3 -- hardest row to recognize by VALUE alone in a report
    ],
    ids=["positive-input", "negative-input", "zero-input"],  # => one readable id per row, in order  # fmt: skip
)  # => end of parametrize's argument list -- three rows, three matching ids, queued above  # fmt: skip
def test_classify_sign_with_readable_ids(value: int, expected: str) -> None:  # => the SAME body runs once per row  # fmt: skip
    assert classify_sign(value) == expected  # => the assertion itself is identical to ex-14's shape  # fmt: skip
    # => what differs is purely REPORTING: -v output shows test_...[positive-input] instead
    # => of test_...[5-positive0], which matters once a suite has dozens of parametrized rows
