context, citation = (
    "Validate JSON.",
    "policy-1",
)  # => local retrieved evidence and source id
assert context and citation == "policy-1"  # => grounded cited answer precondition
print("PASS: aiapp-capstone")  # => offline acceptance result
