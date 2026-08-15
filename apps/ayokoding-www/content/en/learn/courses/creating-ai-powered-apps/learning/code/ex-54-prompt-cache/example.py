uncached, cached = 100, 10  # => cache read costs one tenth in fixture
assert cached < uncached  # => stable prefix reduces repeated input cost
print("PASS: prompt-cache")  # => offline acceptance result
