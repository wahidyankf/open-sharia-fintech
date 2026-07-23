# learning/code/ex-30-dummy-object-unused/test_example.py
"""Example 30: A Dummy Object, Never Called."""


# ex-30: a DUMMY only fills a required parameter slot -- it is never actually invoked (co-11)
def process_value(value: int, logger: object) -> int:  # => logger's TYPE doesn't matter here  # fmt: skip
    if value < 0:  # => the ONLY branch that would ever touch logger
        logger.log(f"received negative value: {value}")  # => never reached in THIS test  # fmt: skip
        return abs(value)  # => also never reached in this test
    return value  # => the positive-value path -- logger is completely irrelevant here


def test_dummy_logger_is_never_invoked() -> None:
    dummy_logger = object()  # => a DUMMY: a plain object with NO methods at all (co-11)
    # => object() has no .log() method whatsoever -- if process_value's negative branch
    # => were ever reached with this dummy, Python would raise AttributeError immediately
    result = process_value(5, dummy_logger)  # => act: value=5 is positive, so the branch above never fires  # fmt: skip
    assert result == 5  # => confirms the positive path -- dummy_logger's absence of methods never mattered  # fmt: skip
    # => this is EXACTLY what makes it a dummy rather than a stub: a stub's canned RETURN
    # => value matters to the test (ex-29); a dummy's only job is filling the parameter slot
