# Each eval fixture pairs an input with expected outcome.
evals = ({"task": "greet", "expected": "hello"},)
# A grader expectation is present for every case.
assert all("expected" in case for case in evals)
# Print the local eval set.
print(evals)
