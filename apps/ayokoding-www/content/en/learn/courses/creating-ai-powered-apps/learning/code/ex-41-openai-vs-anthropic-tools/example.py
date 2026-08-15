openai_arguments, anthropic_input = (
    '{"city":"Jakarta"}',
    {"city": "Jakarta"},
)  # => string versus object
assert isinstance(openai_arguments, str) and isinstance(
    anthropic_input, dict
)  # => shapes differ
print("PASS: openai-vs-anthropic-tools")  # => offline acceptance result
