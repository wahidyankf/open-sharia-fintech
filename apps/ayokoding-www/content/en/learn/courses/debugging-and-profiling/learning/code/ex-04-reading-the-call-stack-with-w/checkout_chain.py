"""A three-level call chain used by this cluster of pdb navigation examples."""

from __future__ import annotations


def to_cents(amount: float) -> int:
    """The deepest frame -- three calls down from handle_request()."""
    breakpoint()
    return round(amount * 100)


def parse_amount(amount: str) -> int:
    """Middle frame -- parses the RAW string into a float, shadowing the name 'amount'."""
    amount = float(
        amount
    )  # => same NAME as the caller's, but now a float, not a string
    return to_cents(amount)


def handle_request(amount: str) -> int:
    """Outer frame -- 'amount' here is still the RAW, unparsed string from the request."""
    return parse_amount(amount)


if __name__ == "__main__":
    print(handle_request("19.99"))
