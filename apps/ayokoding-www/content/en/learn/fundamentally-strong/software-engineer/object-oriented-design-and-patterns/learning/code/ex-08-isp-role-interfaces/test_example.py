"""Example 8: pytest verification for Break a Fat Interface into Role Protocols."""

from example import AllInOnePrinter, Faxable, Printable, Scannable, SimplePrinter


def test_plain_printer_depends_on_exactly_one_protocol() -> None:
    printer: SimplePrinter = SimplePrinter()
    assert isinstance(printer, Printable)  # => the one role it genuinely satisfies
    assert not isinstance(printer, Scannable)  # => never forced to fake this role
    assert not isinstance(printer, Faxable)  # => never forced to fake this role either


def test_all_in_one_printer_satisfies_every_role() -> None:
    device: AllInOnePrinter = AllInOnePrinter()
    assert isinstance(device, Printable)
    assert isinstance(device, Scannable)
    assert isinstance(device, Faxable)  # => genuinely does all three jobs


# => Run: pytest -- Output: 2 passed
