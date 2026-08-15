# A generator models ordered streaming chunks.
from typing import Iterator


# The provider yields compact pieces of one observation.
def stream() -> Iterator[str]:
    # Each chunk can reach the client early.
    yield from ("hel", "lo")


# The client preserves the received order.
result = "".join(stream())
# The complete result matches the streamed chunks.
assert result == "hello"
# Print the merged stream.
print(result)
