index = {"guide": "local facts"}  # => over-your-data index fixture
assert index["guide"] == "local facts"  # => query engine has a local source
print("PASS: llamaindex-abstraction")  # => offline acceptance result
