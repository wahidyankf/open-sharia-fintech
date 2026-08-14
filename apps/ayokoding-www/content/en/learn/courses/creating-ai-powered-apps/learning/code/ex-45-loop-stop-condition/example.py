for iteration in range(3):  # => maximum iteration boundary
    if iteration == 1:
        break  # => success stop condition
assert iteration == 1  # => loop terminated predictably
print("PASS: loop-stop-condition")  # => offline acceptance result
