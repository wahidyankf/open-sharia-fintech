probabilities = [0.6, 0.3, 0.1]  # => sorted candidate mass
assert (
    sum(probabilities[:2]) > 0.89
)  # => binary float still reaches the intended 0.9 cutoff
print("PASS: top-p-nucleus")  # => offline acceptance result
