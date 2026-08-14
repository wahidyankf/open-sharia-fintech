providers = {
    "anthropic": None,
    "voyage": "embedding",
}  # => explicit provider capability note
assert (
    providers["anthropic"] is None and providers["voyage"] == "embedding"
)  # => selection is deliberate
print("PASS: embedding-provider-note")  # => offline acceptance result
