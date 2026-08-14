# A broad verb conceals unrelated authorities.
before = ("manage_everything",)
# Focused names expose their intended use cases.
after = ("read_note", "write_note")
# The revised API separates read from write authority.
assert len(after) == 2 and "read_note" in after
# Print the review comparison.
print(before, after)
