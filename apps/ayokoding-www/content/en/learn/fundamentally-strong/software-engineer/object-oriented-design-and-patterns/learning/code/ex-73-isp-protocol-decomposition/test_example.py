"""Example 73: pytest verification that minimal implementations satisfy only the narrow protocols they need."""

from example import BasicPrinter, FaxMachine, MultiFunctionDevice, Printer, Scanner, run_print_job


def test_minimal_implementation_satisfies_only_the_printer_protocol() -> None:
    basic = BasicPrinter()
    assert isinstance(basic, Printer)  # => structurally satisfies the narrow Printer protocol
    assert not isinstance(basic, Scanner)  # => correctly excluded -- never implemented scan_document
    assert not isinstance(basic, FaxMachine)  # => correctly excluded -- never implemented send_fax


def test_multi_function_device_satisfies_all_three_narrow_protocols() -> None:
    mfd = MultiFunctionDevice()
    assert isinstance(mfd, Printer)
    assert isinstance(mfd, Scanner)
    assert isinstance(mfd, FaxMachine)  # => a richer device can still satisfy every narrow protocol at once


def test_a_function_depending_on_the_narrow_protocol_accepts_the_minimal_implementation() -> None:
    result = run_print_job(BasicPrinter(), "invoice.pdf")  # => run_print_job only ever needs Printer
    assert result == "printed: invoice.pdf"


def test_a_function_depending_on_the_narrow_protocol_also_accepts_the_richer_implementation() -> None:
    result = run_print_job(MultiFunctionDevice(), "invoice.pdf")  # => ISP: the richer device fits the narrow need too
    assert result == "printed: invoice.pdf"


# => Run: pytest -q -- Output: 4 passed
