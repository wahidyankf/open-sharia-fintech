# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 3: keep calculation and delivery responsibilities separate."""


# => This keeps the modeled rule explicit so its trade-off can be inspected.
def subtotal(lines: list[int]) -> int:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    return sum(lines)


# => This keeps the modeled rule explicit so its trade-off can be inspected.
def send_receipt(address: str, total: int) -> str:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    return f"sent {total} to {address}"


# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(send_receipt("reader@example.test", subtotal([3, 4])))
