# Resources provide read-only context through a URI.
from dataclasses import dataclass


# A resource has an identity and text content.
@dataclass(frozen=True)
class Resource:
    # The URI distinguishes this resource from a tool call.
    uri: str
    # The text is context data, not executable code.
    text: str


# The server keeps resources separate from tools.
resources = {"policy://greeting": Resource("policy://greeting", "Greet by name.")}
# Reading selects data by URI without granting action authority.
resource = resources["policy://greeting"]
# The assertion proves the expected resource content is available.
assert resource.text == "Greet by name."
# Print the readable local context.
print(resource)
