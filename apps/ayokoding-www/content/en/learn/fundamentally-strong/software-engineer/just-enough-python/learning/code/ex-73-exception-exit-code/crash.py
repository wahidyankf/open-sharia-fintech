"""Example 73: Uncaught Exception -> Non-zero Exit Code."""

data: dict[str, int] = {"a": 1}
print(data["missing"])  # => raises KeyError, uncaught -- the process exits non-zero
# => Run: python3 crash.py; echo $? -- prints a traceback, then a non-zero exit code
