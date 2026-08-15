from typing import Final  # => typed survey fixture

VOTES: Final[tuple[str, str, str]] = ("yes", "yes", "no")  # => independent results
assert VOTES.count("yes") > VOTES.count("no")  # => majority is observable
print("PASS: parallelization-voting")  # => offline result
