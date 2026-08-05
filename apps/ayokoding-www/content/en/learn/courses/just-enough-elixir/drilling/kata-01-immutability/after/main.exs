original = [1, 2]
changed = original ++ [3]
IO.inspect({original, changed}, label: "preserve both values")
