direct, indirect = (
    "user prompt",
    "retrieved file",
)  # => OWASP direct and indirect sources
assert direct != indirect  # => distinct attack vectors need separate controls
print("PASS: owasp-llm01")  # => offline acceptance result
