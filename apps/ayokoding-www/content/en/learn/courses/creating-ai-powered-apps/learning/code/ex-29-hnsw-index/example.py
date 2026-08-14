settings = {"m": 16, "ef_construction": 64}  # => HNSW build tradeoff parameters
assert (
    settings["ef_construction"] > settings["m"]
)  # => higher build search is deliberate
print("PASS: hnsw-index")  # => offline acceptance result
