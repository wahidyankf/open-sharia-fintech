small, large = 100, 1000  # => precision-versus-context alternatives
assert (
    small < large
)  # => smaller chunks target finer details than larger context windows
print("PASS: chunk-size-tradeoff")  # => offline acceptance result
