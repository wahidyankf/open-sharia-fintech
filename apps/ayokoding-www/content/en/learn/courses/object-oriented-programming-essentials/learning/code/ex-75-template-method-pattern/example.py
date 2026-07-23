"""Example 75: The Template Method Pattern."""

import abc  # => imports the abc module


class ReportBuilder(abc.ABC):  # => ReportBuilder extends abc.ABC
    def build(self) -> str:  # => the FIXED algorithm -- never overridden by subclasses
        return f"{self.header()} | {self.body()} | {self.footer()}"  # => calls the hooks below

    def header(
        self,
    ) -> str:  # => a hook with a sensible default -- optional to override
        return "REPORT"  # => returns this value to the caller

    @abc.abstractmethod  # => marks the next method as required for every subclass
    def body(
        self,
    ) -> str: ...  # => a REQUIRED hook -- every subclass must supply its own

    def footer(self) -> str:  # => another optional hook, with its own default
        return "END"  # => returns this value to the caller


class SalesReport(ReportBuilder):  # => SalesReport extends ReportBuilder
    def body(self) -> str:  # => only overrides the ONE required hook
        return "sales figures"  # => returns this value to the caller


print(
    SalesReport().build()
)  # => the overall flow (build) is fixed; only body() varied per subclass
# => Output: REPORT | sales figures | END
# => `build()` is never overridden by any subclass
