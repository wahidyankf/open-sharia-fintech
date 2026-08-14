system = "Answer with JSON only"  # => durable application policy
reply = '{"answer":"ok"}'  # => deterministic mock honors the policy
assert system.endswith("only") and reply.startswith("{")  # => policy shaped format
print("PASS: system-prompt")  # => offline acceptance result
