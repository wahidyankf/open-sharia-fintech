"""Example 57: A CSV Analyzer Split into a Pure Core and an I/O Shell."""

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds the immutable Sale record


@dataclass(
    frozen=True
)  # => an immutable value object -- no sale record mutates after parsing
class Sale:  # => one parsed CSV row
    product: str  # => the product name column
    amount: float  # => the sale amount column


def parse_sales(
    csv_text: str,
) -> list[Sale]:  # => PURE CORE: text in, data out, zero I/O
    rows = csv_text.strip().splitlines()[
        1:
    ]  # => strips the header row, keeps only data rows
    sales: list[Sale] = []  # => the accumulator this pure function builds and returns
    for row in rows:  # => walks every data row exactly once
        product, amount = row.split(",")  # => splits "apple,10.0" into two fields
        sales.append(
            Sale(product=product, amount=float(amount))
        )  # => builds one immutable Sale
    return sales  # => a plain list -- testable with a string literal, no file needed


def total_by_product(
    sales: list[Sale],
) -> dict[str, float]:  # => PURE CORE: aggregate step
    totals: dict[
        str, float
    ] = {}  # => the running per-product total, local to this call
    for sale in sales:  # => folds every sale into the totals dict
        totals[sale.product] = (
            totals.get(sale.product, 0.0) + sale.amount
        )  # => accumulates per product
    return totals  # => a fresh dict -- the input list itself is never mutated


def format_report(
    totals: dict[str, float],
) -> str:  # => PURE CORE: data -> text, still no I/O
    lines = [
        f"{product}: {amount:.2f}" for product, amount in sorted(totals.items())
    ]  # => one line per product
    return "\n".join(lines)  # => a plain string -- the shell decides how to display it


def run_shell(
    csv_text: str,
) -> None:  # => the IMPERATIVE SHELL -- the ONLY function that prints
    sales = parse_sales(csv_text)  # => delegates to the pure core
    totals = total_by_product(sales)  # => delegates to the pure core
    report = format_report(totals)  # => delegates to the pure core
    print(report)  # => the topic's single I/O side effect, isolated to this one line


csv_text = "product,amount\napple,10.0\nbanana,5.0\napple,3.0\n"  # => stands in for a real file's contents
# => this is the functional-core/imperative-shell pattern (co-28) at real-tool scale
run_shell(csv_text)  # => Output: apple: 13.00 then banana: 5.00
