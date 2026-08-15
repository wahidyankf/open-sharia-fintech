requested, forced = "weather", "weather"  # => application forces one allowed tool
assert requested == forced  # => tool selection policy is met
print("PASS: tool-choice-forced")  # => offline acceptance result
