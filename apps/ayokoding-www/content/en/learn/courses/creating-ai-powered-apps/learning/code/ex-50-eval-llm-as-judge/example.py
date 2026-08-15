generator, judge = "mock-generator", "mock-judge"  # => judge is distinct from generator
assert generator != judge  # => avoid self-judging fixture
print("PASS: eval-llm-as-judge")  # => offline acceptance result
