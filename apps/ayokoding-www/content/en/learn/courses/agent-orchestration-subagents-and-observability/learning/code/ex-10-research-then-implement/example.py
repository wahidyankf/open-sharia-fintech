# Research returns a bounded evidence summary.
summary = {"decision": "use-index"}
# Implementation consumes only the documented handoff.
implementation = f"implement:{summary['decision']}"
# The parent did not receive any child transcript.
assert implementation == "implement:use-index"
# Print the summary-driven work.
print(implementation)
