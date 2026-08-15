"""Example 56: enforce count and byte budgets for fixture screenshots."""

# => The budget bounds both retained artifacts and their total byte cost.
max_count, max_bytes = 2, 16
# => Two tiny fixture captures fit within the stated limits.
captures = [b"PNG-a", b"PNG-b"]
# => Enforce both policies before artifact retention succeeds.
assert len(captures) <= max_count and sum(map(len, captures)) <= max_bytes
# => Output reports the bounded artifact count.
print(f"retained screenshots: {len(captures)}")
