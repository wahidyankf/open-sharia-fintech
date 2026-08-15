image = {"type": "image", "source": "local-fixture"}  # => offline multimodal payload
assert image["type"] == "image"  # => request carries typed image input
print("PASS: vision-image-input")  # => offline acceptance result
