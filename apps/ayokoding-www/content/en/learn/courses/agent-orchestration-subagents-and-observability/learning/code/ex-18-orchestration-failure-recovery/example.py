# One worker succeeds while another returns a typed error.
workers = {"a": "result", "b": "error"}
# The orchestrator retains both facts for a partial result.
partial = {name: value for name, value in workers.items()}
# A single failure did not remove the successful work.
assert partial["a"] == "result" and partial["b"] == "error"
# Print the recoverable partial result.
print(partial)
