# Resource URIs identify independently readable context.
resources = {"note://one": "first", "note://two": "second"}
# Listing returns identities without transferring every payload.
uris = tuple(resources)
# Reading happens explicitly for each selected URI.
contents = {uri: resources[uri] for uri in uris}
# Both local texts are available through their own reads.
assert contents == {"note://one": "first", "note://two": "second"}
# Print the discovered resource content.
print(contents)
