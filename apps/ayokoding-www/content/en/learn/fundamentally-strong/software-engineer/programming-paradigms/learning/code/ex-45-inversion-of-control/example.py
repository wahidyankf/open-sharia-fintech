"""Example 45: Inversion of Control."""

from collections.abc import Callable  # => types the row-transforming function used in both styles


def render_report_you_call_library(rows: list[str], formatter: Callable[[str], str]) -> list[str]:  # => plain function -- callers drive it directly
    # => YOU-CALL-LIBRARY: your code drives the loop, YOU decide when to call the library function
    return [formatter(row) for row in rows]  # => your code is in charge of the control flow


class ReportFramework:  # => FRAMEWORK-CALLS-YOU: the framework owns the loop, you just supply a hook
    def __init__(self) -> None:  # => constructor starts with no handler registered yet
        self._on_row: Callable[[str], str] | None = None  # => a slot for YOUR callback

    def register(self, handler: Callable[[str], str]) -> None:  # => you hand the framework your logic
        self._on_row = handler  # => the framework stores it, does not call it yet

    def run(self, rows: list[str]) -> list[str]:  # => the framework owns this loop entirely
        assert self._on_row is not None, "must register a handler first"  # => fail loudly if nothing was registered
        return [self._on_row(row) for row in rows]  # => the FRAMEWORK calls YOUR code, not the other way


rows = ["alice", "bob"]  # => shared sample data
shout: Callable[[str], str] = lambda row: row.upper()  # noqa: E731  # => the same transformation logic in both styles

you_call_result = render_report_you_call_library(rows, shout)  # => your code drives the call
print(you_call_result)  # => both styles must produce identical output
# => Output: ['ALICE', 'BOB']

framework = ReportFramework()  # => construct the framework
framework.register(shout)  # => hand it your handler -- inversion of control: framework decides when to call it
framework_result = framework.run(rows)  # => the framework's run() loop is what actually invokes `shout`
print(framework_result)  # => must be identical to the you-call-library result
# => Output: ['ALICE', 'BOB']
print(you_call_result == framework_result)  # => confirms both control-flow styles agree
# => Output: True
