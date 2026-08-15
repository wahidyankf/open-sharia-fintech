# An ad hoc answer can vary across runs.
adhoc = ("inspect", "maybe-summarize")
# A skill gives the task a fixed procedure.
skill = ("inspect", "summarize")
# Repeatability is visible in the declared sequence.
assert skill != adhoc
# Print the comparison.
print({"adhoc": adhoc, "skill": skill})
