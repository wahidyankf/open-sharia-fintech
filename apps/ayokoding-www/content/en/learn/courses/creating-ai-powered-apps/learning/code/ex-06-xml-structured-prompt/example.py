prompt = "<context>facts</context><input>question</input>"  # => tagged data boundary
assert "<context>" in prompt and "<input>" in prompt  # => both blocks are distinct
print("PASS: xml-structured-prompt")  # => offline acceptance result
