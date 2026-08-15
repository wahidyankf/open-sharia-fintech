window, prompt_tokens, reserved = 100, 60, 30  # => input and output budget
assert prompt_tokens + reserved <= window  # => request fits the context window
print("PASS: context-window-check")  # => offline acceptance result
