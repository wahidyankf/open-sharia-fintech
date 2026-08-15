# Workers return source-labelled summaries.
pairs = (("research", "facts"), ("tests", "green"))
# The reducer preserves each worker identity.
merged = dict(pairs)
# The coordinator has a coherent named result.
assert merged == {"research": "facts", "tests": "green"}
# Print the aggregation.
print(merged)
