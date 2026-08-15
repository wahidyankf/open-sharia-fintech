model_id = "model-2026-08-01"  # => explicit immutable model snapshot identifier
assert model_id.count("-") >= 2  # => version is recorded rather than evergreen
print("PASS: model-id-pinned")  # => offline acceptance result
