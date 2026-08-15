# Qualified names retain provider identity.
tools = {"notes.search": lambda: "note-hit", "docs.search": lambda: "doc-hit"}
# The first server's search is selected explicitly.
note = tools["notes.search"]()
# The second server's matching short name is still distinct.
doc = tools["docs.search"]()
# Namespacing prevents the two contracts colliding.
assert (note, doc) == ("note-hit", "doc-hit")
# Print the unambiguous outputs.
print(note, doc)
