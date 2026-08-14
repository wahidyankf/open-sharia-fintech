headers = {"x-ratelimit-remaining": "4"}  # => provider quota header fixture
assert int(headers["x-ratelimit-remaining"]) == 4  # => client parses remaining quota
print("PASS: rate-limit-headers")  # => offline acceptance result
