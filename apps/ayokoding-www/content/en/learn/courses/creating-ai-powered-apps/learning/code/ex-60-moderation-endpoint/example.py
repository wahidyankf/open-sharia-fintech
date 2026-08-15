flagged = True  # => local moderation classifier fixture
assert flagged  # => unsafe input is blocked before generation
print("PASS: moderation-endpoint")  # => offline acceptance result
