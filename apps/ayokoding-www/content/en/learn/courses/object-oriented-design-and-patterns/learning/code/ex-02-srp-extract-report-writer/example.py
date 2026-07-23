"""Example 2: Extract the Report Writer from the Calculator."""  # => module docstring


class SalesCalculator:  # => computes numbers ONLY -- never touches a file or console
    def total(self, sales: list[float]) -> float:  # => defines the total() method
        return sum(sales)  # => pure arithmetic, no printing, no writing, no imports

    def average(
        self,  # => the SalesCalculator instance itself, spelled out by the split
        sales: list[float],  # => the same list of amounts passed to total()
        # => still a pure calculation -- no side effects live in this class at all
    ) -> float:  # => a second pure calculation, same concern
        return sum(sales) / len(sales) if sales else 0.0  # => guards empty input


class SalesReportWriter:  # => the ONLY class allowed to produce output text
    def write(
        self,  # => the SalesReportWriter instance, spelled out by the multi-line split
        total: float,  # => the already-computed total -- write() never computes it
        average: float,  # => the already-computed average -- write() never computes it
        sink: list[str],
        # => sink stands in for a real file handle, opened by the caller instead
    ) -> str:  # => sink simulates a file
        line: str = f"total={total:.2f} average={average:.2f}"  # => builds the line
        sink.append(line)  # => the sole write -- SalesCalculator never does this
        return line  # => returns the same line for the caller's convenience


calculator: SalesCalculator = SalesCalculator()  # => constructs calculator
writer: SalesReportWriter = SalesReportWriter()  # => constructs writer
# => two collaborators, built independently -- neither constructor needs the other
sales: list[float] = [100.0, 200.0, 300.0]  # => three sample sale amounts

total: float = calculator.total(sales)  # => total is 600.0, purely computed
average: float = calculator.average(sales)  # => average is 200.0, purely computed
sink: list[str] = []  # => the in-memory "file" the writer appends to
line: str = writer.write(
    total,  # => passed in already-computed, not recalculated by the writer
    average,  # => passed in already-computed, not recalculated by the writer
    sink,  # => the same in-memory "file" constructed above, appended to below
    # => passes numbers IN; the writer alone decides how to render and store them
)  # => the ONLY call in this program that produces text

print(line)  # => confirms the writer, not the calculator, produced this string
# => the printed text and the recorded sink entry are the SAME line object
# => Output: total=600.00 average=200.00
# => Moving `write` out of `SalesCalculator` means the calculator's tests never need a sink, a file, or a console at all
