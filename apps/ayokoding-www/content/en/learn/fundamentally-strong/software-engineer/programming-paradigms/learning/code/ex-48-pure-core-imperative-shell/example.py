"""Example 48: Pure Core, Imperative Shell."""


def compute_invoice_total(unit_price: int, quantity: int, discount_pct: int) -> int:  # => the PURE CORE
    subtotal = unit_price * quantity  # => no I/O, no globals, only its own arguments
    discount = subtotal * discount_pct // 100  # => pure arithmetic
    return subtotal - discount  # => deterministic: same inputs always produce the same output
    # => this function can be tested with zero I/O, zero mocks, zero setup -- that is the whole point


def print_invoice(unit_price: int, quantity: int, discount_pct: int) -> None:  # => the IMPERATIVE SHELL
    total = compute_invoice_total(unit_price, quantity, discount_pct)  # => delegate all logic to the core
    print(f"Total: {total}")  # => the ONLY line in this file that performs I/O -- the shell's whole job
    # => the shell contains no business logic of its own -- it just wires the pure core to the outside world


print_invoice(1000, 3, 10)  # => 1000*3=3000, 10% off = 300, total 2700
# => Output: Total: 2700
