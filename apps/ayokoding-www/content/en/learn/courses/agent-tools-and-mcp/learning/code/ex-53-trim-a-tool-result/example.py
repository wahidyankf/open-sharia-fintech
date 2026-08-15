# The full provider payload includes fields irrelevant to the next decision.
full = {"title": "Report", "url": "https://example.test", "html": "x" * 1000}
# The client contract keeps only the decision-relevant fields.
compact = {"title": full["title"], "url": full["url"]}
# The compact form materially reduces retained context data.
assert len(str(compact)) < len(str(full))
# The needed task fields remain available.
assert compact["title"] == "Report"
# Print the token-efficient result.
print(compact)
