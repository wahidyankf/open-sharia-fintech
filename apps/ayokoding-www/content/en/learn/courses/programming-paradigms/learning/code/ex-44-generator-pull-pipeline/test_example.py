"""Example 44: pytest verification for Generator Pull Pipeline."""

from example import gen_filter, gen_map, source, take


def test_first_three_even_squares() -> None:
    pipeline = gen_filter(gen_map(source(), lambda n: n * n), lambda n: n % 2 == 0)
    assert take(pipeline, 3) == [4, 16, 36]  # => same result as example.py's own Output


def test_pipeline_only_pulls_as_many_source_values_as_strictly_needed() -> None:
    seen: list[int] = []  # => a fresh local counter, isolated from the module-level demo's `computed_log`

    def counting_source():
        n = 0
        while True:
            n += 1
            seen.append(n)
            yield n

    pipeline = gen_filter(gen_map(counting_source(), lambda n: n * n), lambda n: n % 2 == 0)
    take(pipeline, 1)  # => only ask for ONE matching item
    assert seen == [1, 2]  # => n=1 (square 1, odd, rejected), n=2 (square 4, even, accepted) -- then stop


# => Run: pytest -- Output: 2 passed
