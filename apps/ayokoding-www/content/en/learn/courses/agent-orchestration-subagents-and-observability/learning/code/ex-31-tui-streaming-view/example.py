# A local list represents incremental TUI output.
view: list[str] = []
# The first chunk reaches the operator early.
view.append("plan")
# The second chunk updates the same view.
view.append("result")
# Ordering preserves the streamed interaction.
assert view == ["plan", "result"]
# Print the terminal view.
print(view)
