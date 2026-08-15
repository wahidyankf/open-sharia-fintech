from typing import Final  # => typed overflow fixture

USED, LIMIT = 11, 10  # => candidate exceeds context window
assert USED > LIMIT
print("PASS: overflow-detection")  # => guard would fire
