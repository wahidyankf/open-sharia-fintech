"""Worked Example 3: keep calculation and delivery responsibilities separate."""


def subtotal(lines: list[int]) -> int:
    return sum(lines)


def send_receipt(address: str, total: int) -> str:
    return f"sent {total} to {address}"


print(send_receipt("reader@example.test", subtotal([3, 4])))
