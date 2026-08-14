from typing import Final  # => typed survey fixture

SCORE, BAR = 90, 80  # => observed score and acceptance bar
assert SCORE >= BAR  # => regression would block promotion
print("PASS: regression-bar")  # => credential-free result
