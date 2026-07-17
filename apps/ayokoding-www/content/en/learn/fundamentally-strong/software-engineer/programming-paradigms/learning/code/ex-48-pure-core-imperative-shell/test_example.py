"""Example 48: pytest verification for Pure Core, Imperative Shell."""

from example import compute_invoice_total


def test_core_is_tested_with_zero_io_and_zero_mocks() -> None:
    # => this test never touches print(), a file, or a network call -- proves the core needs no I/O
    assert compute_invoice_total(1000, 3, 10) == 2700  # => 3000 - 300


def test_core_is_deterministic_across_repeated_calls() -> None:
    first = compute_invoice_total(500, 2, 20)  # => call #1
    second = compute_invoice_total(500, 2, 20)  # => call #2, identical arguments
    assert first == second == 800  # => 1000 - 200, same both times -- no hidden state anywhere


# => Run: pytest -- Output: 2 passed
