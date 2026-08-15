# Fixture file names stand in for bounded per-file tasks.
files = ("a.py", "b.py")
# Map produces one summary per input file.
mapped = {name: "checked" for name in files}
# Reduce combines the source-labelled summaries.
summary = ",".join(mapped)
# Every file survives the map-reduce flow.
assert summary == "a.py,b.py"
# Print the reduction.
print(summary)
