# A server can publish one parameterized prompt.
template = "Summarize {topic} in one sentence."
# Different task values reuse the identical contract.
first = template.format(topic="tools")
# A second rendering confirms no copied prompt text is needed.
second = template.format(topic="resources")
# Both outputs preserve the server-owned framing.
assert first.startswith("Summarize") and second.endswith("sentence.")
# Print the reusable prompt instances.
print(first, second)
