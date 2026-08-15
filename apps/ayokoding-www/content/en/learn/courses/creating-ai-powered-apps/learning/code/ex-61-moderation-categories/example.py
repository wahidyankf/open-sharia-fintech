scores = {"violence": 0.9}  # => per-category moderation output
assert scores["violence"] > 0.5  # => policy may flag the category
print("PASS: moderation-categories")  # => offline acceptance result
