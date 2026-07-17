"""Example 29: Extract a Pure Core from a Mutating Routine."""

report_log: list[str] = []  # => the ORIGINAL routine's hidden side effect target


def process_orders_impure(
    orders: list[int],
) -> int:  # => mixes computation AND I/O together
    total = 0  # => the running sum, mutated below
    for amount in orders:  # => a loop mutating both total and the module-level log
        total += amount  # => mutates total AND appends below -- two side effects per iteration
        report_log.append(
            f"processed {amount}"
        )  # => side effect buried inside the loop
    return total  # => the caller cannot test this without also inspecting report_log


def sum_orders_pure(
    orders: list[int],
) -> int:  # => the EXTRACTED core -- no I/O, no logging
    return sum(orders)  # => a pure fold, trivially testable with no mocking


def make_log_lines(
    orders: list[int],
) -> list[str]:  # => the logging, extracted as its OWN pure function
    return [
        f"processed {amount}" for amount in orders
    ]  # => still pure: builds and returns, doesn't print


orders = [10, 20, 30]  # => shared input for both the impure routine and the pure core

impure_total = process_orders_impure(
    orders
)  # => also mutates report_log as a side effect
pure_total = sum_orders_pure(
    orders
)  # => computes the SAME total with zero side effects

# => this is the co-28 functional-core/imperative-shell split in miniature
print(
    impure_total == pure_total
)  # => Output: True -- same answer, radically different testability
print(
    make_log_lines(orders) == report_log
)  # => Output: True -- logging extracted without losing it
