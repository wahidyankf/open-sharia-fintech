"""Example 25: Template Method: One Skeleton, Many Subclasses."""


class Report:  # => the BASE -- defines the algorithm SKELETON exactly once
    def header(self) -> str:  # => a default STEP every subclass may reuse as-is
        return "=== Report ==="  # => shared across every subclass, unless overridden

    def body(self) -> str:  # => the STEP every subclass is expected to override
        raise NotImplementedError  # => the base has no sensible default body

    def footer(self) -> str:  # => a default STEP every subclass may reuse as-is
        return "--- End ---"  # => shared across every subclass, unless overridden

    def generate(self) -> str:  # => the TEMPLATE METHOD -- the shared skeleton, defined ONCE
        return "\n".join(
            [self.header(), self.body(), self.footer()]
            # => the ORDER of steps is fixed here; only the step CONTENTS vary per subclass
        )  # => the skeleton never changes, no matter which subclass calls it


class SalesReport(Report):  # => fills in ONLY the body() step
    def body(self) -> str:  # => overrides body(), inherits header()/footer()/generate()
        return "Sales: $1000"  # => a real, honest implementation


class InventoryReport(Report):  # => fills in ONLY the body() step, differently
    def body(self) -> str:  # => overrides body(), inherits header()/footer()/generate()
        return "Stock: 42 units"  # => a real, honest implementation


sales: SalesReport = SalesReport()  # => constructs sales
inventory: InventoryReport = InventoryReport()  # => constructs inventory

print(sales.generate())  # => the SAME generate() method, different body() content
print("---")  # => a visual separator between the two printed reports
print(inventory.generate())  # => the SAME generate() method, called on a DIFFERENT subclass
# => Output: === Report ===
# => Sales: $1000
# => --- End ---
# => ---
# => === Report ===
# => Stock: 42 units
# => --- End ---
# => `generate()` is defined ONCE on `Report` -- neither subclass overrides it at all
