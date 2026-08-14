# Each stage consumes the output of its predecessor.
value = "task"
# The first worker transforms the input.
value = f"plan:{value}"
# The second worker depends on that plan.
value = f"run:{value}"
# The final stage observes the ordered pipeline.
assert value == "run:plan:task"
# Print the final stage output.
print(value)
