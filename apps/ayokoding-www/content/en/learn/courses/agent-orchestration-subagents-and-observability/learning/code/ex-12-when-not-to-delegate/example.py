# This task depends on detailed parent-held constraints.
task = {"summarizable": False}
# The decision keeps unsummarizable work in the coordinator.
decision = "delegate" if task["summarizable"] else "keep"
# The explicit result prevents reflexive agent proliferation.
assert decision == "keep"
# Print the local-work decision.
print(decision)
