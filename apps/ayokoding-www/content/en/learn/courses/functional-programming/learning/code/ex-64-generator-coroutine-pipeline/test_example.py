"""Example 64: pytest verification for A Pull Pipeline of yield Stages."""

from example import read_lines, strip_blank, uppercase


def test_pipeline_streams_through_all_three_stages() -> None:
    text = "a\n\nb"
    pipeline = uppercase(strip_blank(read_lines(text)))
    assert list(pipeline) == ["A", "B"]


# => Run: pytest -- Output: 1 passed
