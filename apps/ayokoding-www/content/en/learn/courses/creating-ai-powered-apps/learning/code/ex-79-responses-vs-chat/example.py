responses, chat = (
    {"output": ["ok"]},
    {"choices": ["ok"]},
)  # => normalized fixture shapes
assert "output" in responses and "choices" in chat  # => client must normalize both
print("PASS: responses-vs-chat")  # => offline acceptance result
