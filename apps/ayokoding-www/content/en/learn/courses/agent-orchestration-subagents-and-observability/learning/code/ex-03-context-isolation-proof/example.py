# The child transcript represents exploration detail.
child_detail = "x" * 100
# The parent retains only an actionable summary.
parent_summary = "done"
# Summary retention protects the parent budget.
assert len(parent_summary) < len(child_detail)
# Print the preserved parent state.
print(parent_summary)
