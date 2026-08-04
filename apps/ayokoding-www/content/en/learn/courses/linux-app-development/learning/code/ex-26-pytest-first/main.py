"""A first pytest test for Linux application core logic."""


def status_line(count: int) -> str:
    return f"pending={count}"


def test_status_line():
    assert status_line(2) == "pending=2"
