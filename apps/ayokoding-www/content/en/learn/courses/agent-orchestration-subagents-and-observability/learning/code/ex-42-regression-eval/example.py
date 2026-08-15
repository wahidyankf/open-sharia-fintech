# The former expected behavior is recorded in the fixture.
expected = "ok"
# A changed agent result intentionally violates it.
actual = "error"
# The eval detects the regression.
assert actual != expected
# Print the detected failure state.
print("regression")
