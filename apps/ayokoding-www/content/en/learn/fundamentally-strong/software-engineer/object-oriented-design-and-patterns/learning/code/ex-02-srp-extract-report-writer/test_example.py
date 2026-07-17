"""Example 2: pytest verification for Extract the Report Writer from the Calculator."""

import inspect

from example import SalesCalculator, SalesReportWriter


def test_calculator_source_contains_no_io_keywords() -> None:
    source: str = inspect.getsource(SalesCalculator)  # => reads the calculator's own source text
    # => "print(", "open(", and ".append(" to a sink are all IO-flavored calls
    assert "print(" not in source
    assert "open(" not in source
    assert "sink" not in source  # => the calculator never even names a sink parameter


def test_calculation_and_write_stay_correct_when_separated() -> None:
    calculator: SalesCalculator = SalesCalculator()
    total: float = calculator.total([100.0, 200.0, 300.0])
    average: float = calculator.average([100.0, 200.0, 300.0])
    sink: list[str] = []
    line: str = SalesReportWriter().write(total, average, sink)
    assert line == "total=600.00 average=200.00"  # => writer formats correctly
    assert sink == [line]  # => exactly one write recorded, by the writer alone


# => Run: pytest -- Output: 2 passed
