"""Example 45: pytest verification for Inversion of Control."""

from collections.abc import Callable

from example import ReportFramework, render_report_you_call_library


def test_you_call_library_and_framework_calls_you_agree() -> None:
    rows = ["x", "y", "z"]  # => fresh sample, isolated from the module-level demo
    handler: Callable[[str], str] = lambda row: row.upper()  # noqa: E731
    direct = render_report_you_call_library(rows, handler)  # => your code drives the loop

    framework = ReportFramework()
    framework.register(handler)  # => hand the SAME handler to the framework
    inverted = framework.run(rows)  # => the framework drives the loop this time

    assert direct == inverted == ["X", "Y", "Z"]  # => identical results, different control-flow owner


def test_framework_invokes_the_registered_handler_not_a_default() -> None:
    framework = ReportFramework()  # => fresh framework instance
    calls: list[str] = []  # => records what the registered handler actually received
    framework.register(lambda row: calls.append(row) or row)  # => a handler with a visible side effect
    framework.run(["p", "q"])  # => the framework is the one that calls it, per row
    assert calls == ["p", "q"]  # => confirms the framework actually invoked OUR handler, in order


# => Run: pytest -- Output: 2 passed
