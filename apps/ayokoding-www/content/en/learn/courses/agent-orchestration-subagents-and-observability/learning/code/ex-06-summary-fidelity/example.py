# The parent declares the decision it needs next.
required = "approve"
# The child summary preserves that decision.
summary = "evidence checked; approve"
# Fidelity means required information survives compression.
assert required in summary
# Print the usable summary.
print(summary)
