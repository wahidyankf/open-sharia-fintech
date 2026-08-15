"""Example 30: turn fixture table rows into structured data."""

# => The raw rows mimic text extracted from an authorized local DOM table.
rows = [("Ada", "editor"), ("Lin", "reader")]
# => Name fields at the extraction boundary so downstream code avoids positional tuples.
people = [{"name": name, "role": role} for name, role in rows]
# => The assertion verifies the structured shape and one meaningful value.
assert people[0] == {"name": "Ada", "role": "editor"}
# => Output is safe JSON-like data suitable for a follow-up assertion.
print(people)
