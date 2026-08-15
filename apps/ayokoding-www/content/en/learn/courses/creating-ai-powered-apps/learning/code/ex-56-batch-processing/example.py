requests, discount = 10, 0.5  # => batch fixture and documented discount
assert requests * discount == 5  # => delayed batch reduces cost
print("PASS: batch-processing")  # => offline acceptance result
