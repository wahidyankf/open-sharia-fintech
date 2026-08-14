import html

encoded = html.escape("<script>")  # => encode untrusted text for an HTML sink
assert encoded == "&lt;script&gt;"  # => raw markup cannot execute downstream
print("PASS: output-encoding-downstream")  # => offline acceptance result
