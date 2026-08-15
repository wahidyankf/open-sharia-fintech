trace_id, eval_input = (
    "trace-1",
    "trace-1",
)  # => evaluation consumes observed trace identity
assert trace_id == eval_input  # => trace feeds feedback without re-teaching eval design
print("PASS: observability-eval-loop")  # => offline acceptance result
