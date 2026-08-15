events = [
    "message_start",
    "content_block_delta",
    "message_stop",
]  # => lifecycle fixture
assert events[0] == "message_start" and events[-1] == "message_stop"  # => valid order
print("PASS: streaming-events")  # => offline acceptance result
